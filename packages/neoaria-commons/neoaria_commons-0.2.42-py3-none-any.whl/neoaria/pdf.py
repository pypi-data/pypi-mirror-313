from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import tt2ps
from reportlab.lib import fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# PDF 파일 생성
pdf_file = "sample_korean.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)

# TTF 폰트 등록 (예: NotoSansKR-Regular 폰트)
pdfmetrics.registerFont(TTFont('NotoSans', 'NotoSansKR-Regular.ttf'))

# 폰트 설정
c.setFont("NotoSans", 12)

# PDF에 텍스트 추가
c.drawString(10 * mm, 280 * mm, "안녕하세요, 여기는 Python에서 생성된 PDF입니다.")

# PDF 저장
c.showPage()
c.save()