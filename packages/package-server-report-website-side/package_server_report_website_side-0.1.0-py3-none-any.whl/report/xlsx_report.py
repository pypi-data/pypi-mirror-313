# import openpyxl
#
#
# def generate_xlsx_report(data, filename):
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Website Monitoring"
#
#     # Add headers
#     ws['A1'] = 'Metric'
#     ws['B1'] = 'Value'
#
#     # Performance Data
#     ws.append(['Performance',
#                f"Status: {data['performance']['status']} | Response Time: {data['performance']['response_time']}s"])
#
#     # SEO Data
#     ws.append(['Title', data['seo']['title']])
#     ws.append(['Meta Description', data['seo']['meta_description']])
#     ws.append(['H1 Tag', data['seo']['h1']])
#
#     # UI Data
#     ws.append(['Missing Alt Text', ', '.join(data['ui']['missing_alt_text'])])
#
#     # Security Data
#     ws.append(['SSL Certificate', data['security']['ssl_certificate_status']])
#
#     wb.save(filename)
