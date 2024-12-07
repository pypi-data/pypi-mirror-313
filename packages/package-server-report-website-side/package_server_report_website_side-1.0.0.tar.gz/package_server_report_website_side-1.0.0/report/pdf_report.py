from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf_report(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Website Monitoring Report")
    c.drawString(100, 730, f"Website URL: {data['url']}")

    # Performance Section
    c.drawString(100, 710,
                 f"Performance: {data['performance']['status']} | Response Time: {data['performance']['response_time']}s")

    # SEO Section
    c.drawString(100, 690, f"Title: {data['seo']['title']}")
    c.drawString(100, 670, f"Meta Description: {data['seo']['meta_description']}")
    c.drawString(100, 650, f"H1 Tag: {data['seo']['h1']}")

    # UI Section
    c.drawString(100, 630, f"Missing Alt Text: {', '.join(data['ui']['missing_alt_text'])}")

    # Security Section
    c.drawString(100, 610, f"SSL Certificate: {data['security']['ssl_certificate_status']}")

    c.save()
