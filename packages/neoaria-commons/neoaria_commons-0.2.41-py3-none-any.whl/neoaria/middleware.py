from fastapi.routing import APIRoute
import logging, requests, yaml, time, jwt, httpx
from typing import Union
from logging.handlers import SysLogHandler
from fastapi import FastAPI, Request, HTTPException, APIRouter, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Match
from fastapi.middleware.cors import CORSMiddleware
from jwt import PyJWTError
from confluent_kafka import Producer

from neoaria.models.rms import DefaultAccount, DefaultPermission


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):

    logger = logging.getLogger("performance_logger")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    
    async def dispatch(self, request: Request, call_next):

        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        self.logger.info(f"Request processed in {process_time:.4f} seconds")

        return response
    
class JWTMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, config: dict):
        super().__init__(app)
        self.__load_service_yaml__()
        self.application_id = self.service_yaml['id']
        self.application_name = self.service_yaml['name']

        if config['enabled'] == True:

            #TODO token manager token을 가져오도록 수정
            self.secret_key = config['secret_key']
            self.algorithm = config['algorithms']
            self.targets = config['targets']
            self.permission_service: str = config['permission_service']
            self.permission_service_url: str = f"http://{self.permission_service['host']}:{self.permission_service['port']}/{self.permission_service['endpoint']}"
            self.cache_expiry = self.permission_service['cache_expire']
            self.auth_users:dict = {}

    def __load_service_yaml__(self):
        with open('config/source.yaml', 'r') as file:
            self.service_yaml = yaml.safe_load(file)['service']

    # fetch account information
    async def fetch_account_info(self, login_id: str) -> Union[DefaultAccount, None]:
        async with httpx.AsyncClient() as client:
            try:
                from neoaria.commons import BusinessResponse
                account_response = await client.get(f"{self.permission_service_url}/{login_id}")
                account_response.raise_for_status()

                account_result = BusinessResponse(**dict(**account_response.json()))
                account = DefaultAccount(**account_result.body['result'])

                return account
            except httpx.HTTPStatusError as e:
                return None

    # cache account information
    def cache_user_info(self, login_id: str, user_info: dict):
        self.auth_users[login_id] = {
            'data': user_info,
            'timestamp': time.time()
        }

    # gettering account information
    async def get_cached_account_info(self, login_id: str):
        user_info = self.auth_users.get(login_id)
        if user_info and (time.time() - user_info['timestamp'] < self.cache_expiry):
            return user_info['data']
        else:
            account_object = await self.fetch_account_info(login_id)
            self.auth_users[login_id] = {
                 'data': account_object,
                 'timestamp': time.time()
            }
            return account_object

    def check_execution_permission(self, permission: DefaultPermission, custom_info: dict):
        if custom_info['permission'] not in permission.permissions:
            raise HTTPException(status_code=401, detail="Permission denied")

    async def dispatch(self, request: Request, call_next) -> Response:
        
        if request.url.path in self.targets:

            auth_header = request.headers.get("Authorization")
            application_id = self.application_id

            if auth_header:

                token = auth_header.split(" ")[1]
                
                try:
                    #TODO decodeing service
                    payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

                    # loginId가 payload에 존재하면 account를 생성
                    if 'id' in payload:

                        login_id = payload['id']
                        
                        account:DefaultAccount = await self.get_cached_account_info(login_id)

                        permission:DefaultPermission = account.getPermssion()

                        if permission is None:  
                            return JSONResponse( status_code=401, content={ "status": "fail", "message": f"Permission is not define :: {application_id}" })

                        if permission.applications is None:
                            return JSONResponse( status_code=404, content={ "status": "fail", "message": f"Target applications is not define" })

                        permission_dict = permission.getPermissions()

                        if application_id in permission_dict:
                            
                            #account permission
                            func_dict = permission_dict[application_id]
                            func_id = None

                            # get function id
                            for route in request.app.routes:
                                if isinstance(route, APIRoute): 
                                    match, parameters = route.matches(request.scope)

                                    if match == Match.FULL:
                                        endpoint_func = route.endpoint
                                        custom_info = getattr(endpoint_func, '__permission_id__', None)

                                        if custom_info:
                                            func_id = custom_info['id']
                                            break

                            # check account permission id with function id
                            if not func_id is None and not func_dict is None and func_dict[func_id]:
                                   request.state.account = account
                                   return  await call_next(request)
                            else:
                                return JSONResponse( status_code=401, content={ "status": "fail", "message": f"Permission is is not found :: {application_id}, {func_id}" })
                            
                        else: 
                            return JSONResponse( status_code=401, content={ "status": "fail", "message": f"Service is not define :: {application_id}" })
                    
                except PyJWTError:
                    return JSONResponse( status_code=401, content={ "status": "fail", "message": "Invalid token"})
            else:
                return JSONResponse( status_code=401, content={ "status": "fail", "message": "Authorization header missing" })
            
        else:
            return await call_next(request)

class KafkaLogHandler(logging.Handler):

    def __init__(self, producer_info: dict, request_url: str):
        super().__init__()
        self.request_url = request_url
        self.producer_info = producer_info
        self.producer = Producer(**producer_info['producer'])

    def emit(self, record):
        
        log_entry_str: str = self.format(record)
        log_entry_str = log_entry_str.replace('log_body', self.request_url)

        try:
            self.producer.produce( self.producer_info['topic'], log_entry_str.encode('utf-8'))
            self.producer.flush()
        except Exception as e:
            print(f"Failed to send log to server: {e}")


class HTTPLogHandler(logging.Handler):
    def __init__(self, log_server_url):
        super().__init__()
        self.log_server_url = log_server_url

    def emit(self, record):
        log_entry = self.format(record)
        try:
            requests.post(self.log_server_url, json={"log": log_entry})
        except Exception as e:
            print(f"Failed to send log to server: {e}")

class RequestLoggingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, log_level: int = logging.INFO, include_headers: bool = False, config: dict = None):
        
        if config is None:
            raise ValueError("Config dictionary must be provided.")
        
        super().__init__(app)

        request_url: str  = f"http://{config['servers']['http']['host']}:{config['servers']['http']['port']}/{config['servers']['http']['endpoint']}"

        if config['type'] == 'http':
            self.log_handler = HTTPLogHandler(log_server_url=request_url)
        elif config['type'] == 'syslog':
            self.log_handler = SysLogHandler(address=(config['servers']['syslog']['host'],  config['port']))
        elif config['type'] == 'kafka':
            self.log_handler = KafkaLogHandler(producer_info=config['servers']['kafka'], request_url=request_url)

        self.log_handler.setFormatter(logging.Formatter(config['format']))

        self.logger = logging.getLogger("request_logger")
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(log_level)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        log_body = f'{request.method} {request.url} {response.status_code}'
        self.logger.log(self.logger.level, 'log_body')

        return response

def setupMiddleware(fastApi: FastAPI, router: APIRouter) -> FastAPI:

    config_yaml = __load_middleware_config() 
    __setup_middleware(config_yaml, fastApi)
    fastApi.include_router(router)
    return fastApi

def __load_middleware_config() -> dict:
    with open('config/middleware.yaml', 'r') as file:
        return yaml.safe_load(file)

def __setup_middleware(config_yaml: dict, fastApi: FastAPI):
    
    if 'logging' in config_yaml:
        __setup_logging__(config_yaml, fastApi)

    if 'jwt' in config_yaml:
        __setup_jwt__(config_yaml, fastApi)

    if 'gzip-response' in config_yaml:
        __setup_gzip__(config_yaml, fastApi)
    
    if 'cors' in config_yaml:
        __setup_cors__(config_yaml, fastApi)
    
    if 'performance-monitor' in config_yaml:
        __setup_performance_monitor__(config_yaml, fastApi)

def __setup_logging__(config_yaml: dict, fastApi: FastAPI):
    logging_yaml = config_yaml['logging']

    if logging_yaml['enabled']:
        
        check_level = logging_yaml['level'].upper()

        if check_level == 'INFO':
            log_level_type = logging.INFO
        elif check_level == 'WARNING':
            log_level_type = logging.WARNING
        elif check_level == 'ERROR':
            log_level_type = logging.ERROR
        elif check_level == 'CRITICAL':
            log_level_type = logging.CRITICAL
        else:
            log_level_type = logging.DEBUG

        fastApi.add_middleware(RequestLoggingMiddleware, 
            log_level=log_level_type, 
            include_headers=logging_yaml['include_headers'], 
            config=logging_yaml)

def __setup_jwt__(config_yaml: dict, fastApi: FastAPI):
    logging_yaml = config_yaml['jwt']
    if logging_yaml['enabled']:
        fastApi.add_middleware(JWTMiddleware, 
                                    config=logging_yaml)

def __setup_gzip__(config_yaml: dict, fastApi: FastAPI):
    logging_yaml = config_yaml['gzip-response']
    if logging_yaml['enabled']:
        fastApi.add_middleware(GZipMiddleware, 
            minimum_size=logging_yaml['minimum_size'])

def __setup_cors__(config_yaml: dict, fastApi: FastAPI):

    logging_yaml = config_yaml['cors']
    if logging_yaml['enabled']:
        fastApi.add_middleware( CORSMiddleware,
            allow_origins=logging_yaml['allow_origins'],
            allow_credentials=logging_yaml['allow_credentials'],
            allow_methods=logging_yaml['allow_methods'],
            allow_headers=logging_yaml['allow_headers'])

def __setup_performance_monitor__(config_yaml: dict, fastApi: FastAPI):
    pass
