import frappe
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring 
import json
import requests
import base64
import qrcode
# from datetime import datetime
# from frappe.model.document import Document
# from qr_demo.qr_code import get_qr_code
# from _future_ import unicode_literals
# from base64 import b64encode
from io import BytesIO
def get_qr_code(data: str) -> str:
	qr_code_bytes = get_qr_code_bytes(data, format="PNG")
	base_64_string = bytes_to_base64_string(qr_code_bytes)
	return add_file_info(base_64_string)


def add_file_info(data: str) -> str:
	"""Add info about the file type and encoding.
	
	This is required so the browser can make sense of the data."""
	return f"data:image/png;base64, {data}"


def get_qr_code_bytes(data, format: str) -> bytes:
	"""Create a QR code and return the bytes."""
	img = qrcode.make(data)

	buffered = BytesIO()
	img.save(buffered, format=format)

	return buffered.getvalue()


def bytes_to_base64_string(data: bytes) -> str:
	"""Convert bytes to a base64 encoded string."""
	return base64.b64encode(data).decode("utf-8")

@frappe.whitelist(allow_guest=True)
def general_si(name, is_return , posting_date , is_pos):
    if (int(is_return)) == 0:
        sales = general_sales_invoice(name , is_pos)
    elif (int(is_return)) == 1:
        sales = general_sales_return_invoice(name , is_pos)
   
    ##### Create  new QR code data 
    qr_code_data = frappe.new_doc('JO Fawtara Data')  
    
    qr_code_data.sales_invoice = name
    qr_code_data.posting_date = posting_date
    qr_code_data.insert(ignore_permissions = True)
    qr_code_data.submit()
    # encrypte_sales = base64.b64encode(sales)
    # client_id = "xxxxxxx"
    # secret_key = "xxxxxxx"

    # url = "https://backend.jofotara.gov.jo/core/invoices/"

    # header = {
    #         "Client-Id": client_id,
    #         "Secret-Key": secret_key,
    #         "Content-Type": "application/json",
    #         "Cookie": "stickounet=4fdb7136e666916d0e373058e9e5c44e|7480c8b0e4ce7933ee164081a50488f1"
    #     }
    # body = {
    #         "invoice": encrypte_sales
    #     }
    
    # response = requests.post(url , headers=header , json= body )
    response = """{
        "EINV_RESULTS":{
            "status":"PASS"
            ,"INFO":[
                {
                    "type":"INFO",
                    "status":"PASS",
                    "EINV_CODE":"XSD_VALID",
                    "EINV_CATEGORY":"XSD validation",
                    "EINV_MESSAGE":"Complied with UBL 2.1 standards"
                }],
            "WARNINGS":[],
            "ERRORS":[]
            },
        "EINV_STATUS":"SUBMITTED",
        "EINV_SINGED_INVOICE":"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPEludm9pY2UgeG1sbnM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkludm9pY2UtMiIgeG1sbnM6Y2FjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpDb21tb25BZ2dyZWdhdGVDb21wb25lbnRzLTIiIHhtbG5zOmNiYz0idXJuOm9hc2lzOm5hbWVzOnNwZWNpZmljYXRpb246dWJsOnNjaGVtYTp4c2Q6Q29tbW9uQmFzaWNDb21wb25lbnRzLTIiIHhtbG5zOmV4dD0idXJuOm9hc2lzOm5hbWVzOnNwZWNpZmljYXRpb246dWJsOnNjaGVtYTp4c2Q6Q29tbW9uRXh0ZW5zaW9uQ29tcG9uZW50cy0yIj48ZXh0OlVCTEV4dGVuc2lvbnM+PGV4dDpVQkxFeHRlbnNpb24+PGV4dDpFeHRlbnNpb25VUkk+dXJuOm9hc2lzOm5hbWVzOnNwZWNpZmljYXRpb246dWJsOmRzaWc6ZW52ZWxvcGVkOnhhZGVzPC9leHQ6RXh0ZW5zaW9uVVJJPjxleHQ6RXh0ZW5zaW9uQ29udGVudD48IS0tIFBsZWFzZSBub3RlIHRoYXQgdGhlIHNpZ25hdHVyZSB2YWx1ZXMgYXJlIHNhbXBsZSB2YWx1ZXMgb25seSAtLT48c2lnOlVCTERvY3VtZW50U2lnbmF0dXJlcyB4bWxuczpzaWc9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkNvbW1vblNpZ25hdHVyZUNvbXBvbmVudHMtMiIgeG1sbnM6c2FjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpTaWduYXR1cmVBZ2dyZWdhdGVDb21wb25lbnRzLTIiIHhtbG5zOnNiYz0idXJuOm9hc2lzOm5hbWVzOnNwZWNpZmljYXRpb246dWJsOnNjaGVtYTp4c2Q6U2lnbmF0dXJlQmFzaWNDb21wb25lbnRzLTIiPjxzYWM6U2lnbmF0dXJlSW5mb3JtYXRpb24+PGNiYzpJRD51cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2lnbmF0dXJlOjE8L2NiYzpJRD48c2JjOlJlZmVyZW5jZWRTaWduYXR1cmVJRD51cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2lnbmF0dXJlOkludm9pY2U8L3NiYzpSZWZlcmVuY2VkU2lnbmF0dXJlSUQ+PGRzOlNpZ25hdHVyZSB4bWxuczpkcz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyIgSWQ9InNpZ25hdHVyZSI+PGRzOlNpZ25lZEluZm8+PGRzOkNhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDA2LzEyL3htbC1jMTRuMTEiLz48ZHM6U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxkc2lnLW1vcmUjZWNkc2Etc2hhMjU2Ii8+PGRzOlJlZmVyZW5jZSBJZD0iaW52b2ljZVNpZ25lZERhdGEiIFVSST0iIj48ZHM6VHJhbnNmb3Jtcz48ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvVFIvMTk5OS9SRUMteHBhdGgtMTk5OTExMTYiPjxkczpYUGF0aD5ub3QoLy9hbmNlc3Rvci1vci1zZWxmOjpleHQ6VUJMRXh0ZW5zaW9ucyk8L2RzOlhQYXRoPjwvZHM6VHJhbnNmb3JtPjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy9UUi8xOTk5L1JFQy14cGF0aC0xOTk5MTExNiI+PGRzOlhQYXRoPm5vdCgvL2FuY2VzdG9yLW9yLXNlbGY6OmNhYzpTaWduYXR1cmUpPC9kczpYUGF0aD48L2RzOlRyYW5zZm9ybT48ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvVFIvMTk5OS9SRUMteHBhdGgtMTk5OTExMTYiPjxkczpYUGF0aD5ub3QoLy9hbmNlc3Rvci1vci1zZWxmOjpjYWM6QWRkaXRpb25hbERvY3VtZW50UmVmZXJlbmNlW2NiYzpJRD0nUVInXSk8L2RzOlhQYXRoPjwvZHM6VHJhbnNmb3JtPjxkczpUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDA2LzEyL3htbC1jMTRuMTEiLz48L2RzOlRyYW5zZm9ybXM+PGRzOkRpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI3NoYTI1NiIvPjxkczpEaWdlc3RWYWx1ZT5nNWVpY25XVlk0NTVRNVdPZjg2Yi9DQUZGOGdZSE9YM0V4V21lWG50aElRPTwvZHM6RGlnZXN0VmFsdWU+PC9kczpSZWZlcmVuY2U+PGRzOlJlZmVyZW5jZSBUeXBlPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjU2lnbmF0dXJlUHJvcGVydGllcyIgVVJJPSIjeGFkZXNTaWduZWRQcm9wZXJ0aWVzIj48ZHM6RGlnZXN0TWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8wNC94bWxlbmMjc2hhMjU2Ii8+PGRzOkRpZ2VzdFZhbHVlPlkyTXpabUl6WW1FM05XTTBNRFk0TURrNU1URm1aV1pqWlRoa04yUTNPVGszWXpVME1ERmtPREl5WlRrNVpURm1ORGcyTm1JNU1qTmhZekppTkROallnPT08L2RzOkRpZ2VzdFZhbHVlPjwvZHM6UmVmZXJlbmNlPjwvZHM6U2lnbmVkSW5mbz48ZHM6U2lnbmF0dXJlVmFsdWU+TUVZQ0lRQ2l4MzdsNjVqK1hYUDNGdkhFUGIyODVQSGdybVZiSlBLMEZNeVZYVm5hc3dJaEFKcEpOaHpMRHJEMW9Cd1Z1cldzOWpBSkU4aW9VOU1ZbWUxdVh0NWpkeFdkPC9kczpTaWduYXR1cmVWYWx1ZT48ZHM6S2V5SW5mbz48ZHM6WDUwOURhdGE+PGRzOlg1MDlDZXJ0aWZpY2F0ZT5NSUlDYmpDQ0FoU2dBd0lCQWdJVVU4RDdGdGozVU1udmlYR2dic0ZjSUJnaFVZd3dDZ1lJS29aSXpqMEVBd0l3Z1kweEN6QUpCZ05WQkFZVEFrcFBNUTR3REFZRFZRUUlEQVZCYlcxaGJqRU9NQXdHQTFVRUJ3d0ZRVzF0WVc0eERUQUxCZ05WQkFvTUJFbFRWRVF4RFRBTEJnTlZCQXNNQkVWVVFWZ3hHVEFYQmdOVkJBTU1FR1YwWVhndWFYTjBaQzVuYjNZdWFtOHhKVEFqQmdrcWhraUc5dzBCQ1FFV0ZtRmtiV2x1UUdWMFlYZ3VhWE4wWkM1bmIzWXVhbTh3SGhjTk1qSXdPVEV6TVRJd056STRXaGNOTWpNd09URXpNVEl3TnpJNFdqQ0JqVEVMTUFrR0ExVUVCaE1DU2s4eERqQU1CZ05WQkFnTUJVRnRiV0Z1TVE0d0RBWURWUVFIREFWQmJXMWhiakVOTUFzR0ExVUVDZ3dFU1ZOVVJERU5NQXNHQTFVRUN3d0VSVlJCV0RFWk1CY0dBMVVFQXd3UVpYUmhlQzVwYzNSa0xtZHZkaTVxYnpFbE1DTUdDU3FHU0liM0RRRUpBUllXWVdSdGFXNUFaWFJoZUM1cGMzUmtMbWR2ZGk1cWJ6QldNQkFHQnlxR1NNNDlBZ0VHQlN1QkJBQUtBMElBQklLeG9LcEF4bjJkdytUcitCWTJUUy9uMWgzbHNFUDZobmhibngwd2p6M2toZkJiSFZNU0RHVksrWjNyMG9PTHZreEhDSXh5VURxVTJ2Y0EyU2RJSEgralV6QlJNQjBHQTFVZERnUVdCQlI4NFBNdVZjMWFKR3pEMHRidzJlL0wzdGZkRnpBZkJnTlZIU01FR0RBV2dCUjg0UE11VmMxYUpHekQwdGJ3MmUvTDN0ZmRGekFQQmdOVkhSTUJBZjhFQlRBREFRSC9NQW9HQ0NxR1NNNDlCQU1DQTBnQU1FVUNJUUR1QXlzU1lSZHpjb1dvMzFseXpUWUdPR0VrMGgvRWx6bEdGMnFkM001Y0hBSWdYL2F3eWNwTzJGMkdLWTVxQmNnd09sbmNPb29FTTFHaE85dGtBL0dxT0FRPTwvZHM6WDUwOUNlcnRpZmljYXRlPjwvZHM6WDUwOURhdGE+PC9kczpLZXlJbmZvPjxkczpPYmplY3Q+PHhhZGVzOlF1YWxpZnlpbmdQcm9wZXJ0aWVzIHhtbG5zOnhhZGVzPSJodHRwOi8vdXJpLmV0c2kub3JnLzAxOTAzL3YxLjMuMiMiIFRhcmdldD0ic2lnbmF0dXJlIj48eGFkZXM6U2lnbmVkUHJvcGVydGllcyBJZD0ieGFkZXNTaWduZWRQcm9wZXJ0aWVzIj48eGFkZXM6U2lnbmVkU2lnbmF0dXJlUHJvcGVydGllcz48eGFkZXM6U2lnbmluZ1RpbWU+MjAyMy0wMy0wMVQxMDo0NDozOFo8L3hhZGVzOlNpZ25pbmdUaW1lPjx4YWRlczpTaWduaW5nQ2VydGlmaWNhdGU+PHhhZGVzOkNlcnQ+PHhhZGVzOkNlcnREaWdlc3Q+PGRzOkRpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI3NoYTI1NiIvPjxkczpEaWdlc3RWYWx1ZT5Oak5qTjJGa1l6QmpZamxqT0dNNE5UVXdNR1E0WkdVd01EUTFPRFl5TkRNek1tUXlNR1l3T0RCaE5qRTBaV0ZpWkRrMlpHVTNOVEl5WVdFMVpqa3haQT09PC9kczpEaWdlc3RWYWx1ZT48L3hhZGVzOkNlcnREaWdlc3Q+PHhhZGVzOklzc3VlclNlcmlhbD48ZHM6WDUwOUlzc3Vlck5hbWU+RU1BSUxBRERSRVNTPWFkbWluQGV0YXguaXN0ZC5nb3Yuam8sIENOPWV0YXguaXN0ZC5nb3Yuam8sIE9VPUVUQVgsIE89SVNURCwgTD1BbW1hbiwgU1Q9QW1tYW4sIEM9Sk88L2RzOlg1MDlJc3N1ZXJOYW1lPjxkczpYNTA5U2VyaWFsTnVtYmVyPjQ3ODE0OTg1MDAxNDg3NDg4NzI0MjQ0MjI2MzgwMjI5MzU1MjU3NDgxMDM3ODYzNjwvZHM6WDUwOVNlcmlhbE51bWJlcj48L3hhZGVzOklzc3VlclNlcmlhbD48L3hhZGVzOkNlcnQ+PC94YWRlczpTaWduaW5nQ2VydGlmaWNhdGU+PC94YWRlczpTaWduZWRTaWduYXR1cmVQcm9wZXJ0aWVzPjwveGFkZXM6U2lnbmVkUHJvcGVydGllcz48L3hhZGVzOlF1YWxpZnlpbmdQcm9wZXJ0aWVzPjwvZHM6T2JqZWN0PjwvZHM6U2lnbmF0dXJlPjwvc2FjOlNpZ25hdHVyZUluZm9ybWF0aW9uPjwvc2lnOlVCTERvY3VtZW50U2lnbmF0dXJlcz48L2V4dDpFeHRlbnNpb25Db250ZW50PjwvZXh0OlVCTEV4dGVuc2lvbj48L2V4dDpVQkxFeHRlbnNpb25zPjxjYmM6UHJvZmlsZUlEPnJlcG9ydGluZzoxLjA8L2NiYzpQcm9maWxlSUQ+PGNiYzpJRD5FSU4tMDEwMTwvY2JjOklEPjxjYmM6VVVJRD43YTQ0NTJlYi0wYWNkLTQ5OTgzLWI2MzAtYjJiNzlkMGFjZXJ0PC9jYmM6VVVJRD48Y2JjOklzc3VlRGF0ZT4yMDIzLTAxLTMwPC9jYmM6SXNzdWVEYXRlPjxjYmM6SW52b2ljZVR5cGVDb2RlIG5hbWU9IjAxMSI+Mzg4PC9jYmM6SW52b2ljZVR5cGVDb2RlPjxjYmM6Tm90ZT7ZhdmE2KfYrdi42KfYqiAyPC9jYmM6Tm90ZT48Y2JjOkRvY3VtZW50Q3VycmVuY3lDb2RlPkpPRDwvY2JjOkRvY3VtZW50Q3VycmVuY3lDb2RlPjxjYmM6VGF4Q3VycmVuY3lDb2RlPkpPRDwvY2JjOlRheEN1cnJlbmN5Q29kZT48Y2FjOkFkZGl0aW9uYWxEb2N1bWVudFJlZmVyZW5jZT48Y2JjOklEPklDVjwvY2JjOklEPjxjYmM6VVVJRD4xMTwvY2JjOlVVSUQ+PC9jYWM6QWRkaXRpb25hbERvY3VtZW50UmVmZXJlbmNlPjxjYWM6QWRkaXRpb25hbERvY3VtZW50UmVmZXJlbmNlPjxjYmM6SUQ+UVI8L2NiYzpJRD48Y2FjOkF0dGFjaG1lbnQ+PGNiYzpFbWJlZGRlZERvY3VtZW50QmluYXJ5T2JqZWN0IG1pbWVDb2RlPSJ0ZXh0L3BsYWluIj5BU1JpT1RZd016SXhPUzB5TURBMUxUUmxZbVl0T0RNNFppMDJPVEF5TVdJeFpUTXpNRGtDQW50OUF3Vm1ZV3h6WlFRS01qQXlNeTB3TVMwek1BVUlSVWxPTFRBeE1ERUdBQWNHTVRNd0xqQXdDQWs1T1RrNU9UazVPVE1KQmtGQlFVRkJRUW9BPC9jYmM6RW1iZWRkZWREb2N1bWVudEJpbmFyeU9iamVjdD48L2NhYzpBdHRhY2htZW50PjwvY2FjOkFkZGl0aW9uYWxEb2N1bWVudFJlZmVyZW5jZT48Y2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PjxjYWM6UGFydHk+PGNhYzpQb3N0YWxBZGRyZXNzPjxjYWM6Q291bnRyeT48Y2JjOklkZW50aWZpY2F0aW9uQ29kZT5KTzwvY2JjOklkZW50aWZpY2F0aW9uQ29kZT48L2NhYzpDb3VudHJ5PjwvY2FjOlBvc3RhbEFkZHJlc3M+PGNhYzpQYXJ0eVRheFNjaGVtZT48Y2JjOkNvbXBhbnlJRD45OTk5OTk5OTM8L2NiYzpDb21wYW55SUQ+PGNhYzpUYXhTY2hlbWU+PGNiYzpJRD5WQVQ8L2NiYzpJRD48L2NhYzpUYXhTY2hlbWU+PC9jYWM6UGFydHlUYXhTY2hlbWU+PGNhYzpQYXJ0eUxlZ2FsRW50aXR5PjxjYmM6UmVnaXN0cmF0aW9uTmFtZT5BQUFBQUE8L2NiYzpSZWdpc3RyYXRpb25OYW1lPjwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+PC9jYWM6UGFydHk+PC9jYWM6QWNjb3VudGluZ1N1cHBsaWVyUGFydHk+PGNhYzpBY2NvdW50aW5nQ3VzdG9tZXJQYXJ0eT48Y2FjOlBhcnR5PjxjYWM6UGFydHlJZGVudGlmaWNhdGlvbj48Y2JjOklEIHNjaGVtZUlEPSJOSU4iPjk4MzEwNjE2MjQ8L2NiYzpJRD48L2NhYzpQYXJ0eUlkZW50aWZpY2F0aW9uPjxjYWM6UG9zdGFsQWRkcmVzcz48Y2JjOlBvc3RhbFpvbmU+MjM0MzI8L2NiYzpQb3N0YWxab25lPjxjYWM6Q291bnRyeT48Y2JjOklkZW50aWZpY2F0aW9uQ29kZT5KTzwvY2JjOklkZW50aWZpY2F0aW9uQ29kZT48L2NhYzpDb3VudHJ5PjwvY2FjOlBvc3RhbEFkZHJlc3M+PGNhYzpQYXJ0eVRheFNjaGVtZT48Y2FjOlRheFNjaGVtZT48Y2JjOklEPlZBVDwvY2JjOklEPjwvY2FjOlRheFNjaGVtZT48L2NhYzpQYXJ0eVRheFNjaGVtZT48Y2FjOlBhcnR5TGVnYWxFbnRpdHk+PGNiYzpSZWdpc3RyYXRpb25OYW1lLz48L2NhYzpQYXJ0eUxlZ2FsRW50aXR5PjwvY2FjOlBhcnR5PjxjYWM6QWNjb3VudGluZ0NvbnRhY3Q+PGNiYzpUZWxlcGhvbmU+MzI0MzIzNDM0PC9jYmM6VGVsZXBob25lPjwvY2FjOkFjY291bnRpbmdDb250YWN0PjwvY2FjOkFjY291bnRpbmdDdXN0b21lclBhcnR5PjxjYWM6U2VsbGVyU3VwcGxpZXJQYXJ0eT48Y2FjOlBhcnR5PjxjYWM6UGFydHlJZGVudGlmaWNhdGlvbj48Y2JjOklEPjE2NjgzNjk0PC9jYmM6SUQ+PC9jYWM6UGFydHlJZGVudGlmaWNhdGlvbj48L2NhYzpQYXJ0eT48L2NhYzpTZWxsZXJTdXBwbGllclBhcnR5PjxjYWM6QWxsb3dhbmNlQ2hhcmdlPjxjYmM6Q2hhcmdlSW5kaWNhdG9yPmZhbHNlPC9jYmM6Q2hhcmdlSW5kaWNhdG9yPjxjYmM6QWxsb3dhbmNlQ2hhcmdlUmVhc29uPmRpc2NvdW50PC9jYmM6QWxsb3dhbmNlQ2hhcmdlUmVhc29uPjxjYmM6QW1vdW50IGN1cnJlbmN5SUQ9IkpPIj4yLjAwPC9jYmM6QW1vdW50PjwvY2FjOkFsbG93YW5jZUNoYXJnZT48Y2FjOkxlZ2FsTW9uZXRhcnlUb3RhbD48Y2JjOlRheEV4Y2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJKTyI+MTMyLjAwPC9jYmM6VGF4RXhjbHVzaXZlQW1vdW50PjxjYmM6VGF4SW5jbHVzaXZlQW1vdW50IGN1cnJlbmN5SUQ9IkpPIj4xMzAuMDA8L2NiYzpUYXhJbmNsdXNpdmVBbW91bnQ+PGNiYzpBbGxvd2FuY2VUb3RhbEFtb3VudCBjdXJyZW5jeUlEPSJKTyI+Mi4wMDwvY2JjOkFsbG93YW5jZVRvdGFsQW1vdW50PjxjYmM6UGF5YWJsZUFtb3VudCBjdXJyZW5jeUlEPSJKTyI+MTMwLjAwPC9jYmM6UGF5YWJsZUFtb3VudD48L2NhYzpMZWdhbE1vbmV0YXJ5VG90YWw+PGNhYzpJbnZvaWNlTGluZT48Y2JjOklEPjE8L2NiYzpJRD48Y2JjOkludm9pY2VkUXVhbnRpdHkgdW5pdENvZGU9IlBDRSI+NDQuMDA8L2NiYzpJbnZvaWNlZFF1YW50aXR5PjxjYmM6TGluZUV4dGVuc2lvbkFtb3VudCBjdXJyZW5jeUlEPSJKTyI+MTMwLjAwPC9jYmM6TGluZUV4dGVuc2lvbkFtb3VudD48Y2FjOkl0ZW0+PGNiYzpOYW1lPlByb2R1Y3QtMTwvY2JjOk5hbWU+PC9jYWM6SXRlbT48Y2FjOlByaWNlPjxjYmM6UHJpY2VBbW91bnQgY3VycmVuY3lJRD0iSk8iPjMuMDA8L2NiYzpQcmljZUFtb3VudD48Y2FjOkFsbG93YW5jZUNoYXJnZT48Y2JjOkNoYXJnZUluZGljYXRvcj5mYWxzZTwvY2JjOkNoYXJnZUluZGljYXRvcj48Y2JjOkFsbG93YW5jZUNoYXJnZVJlYXNvbj5ESVNDT1VOVDwvY2JjOkFsbG93YW5jZUNoYXJnZVJlYXNvbj48Y2JjOkFtb3VudCBjdXJyZW5jeUlEPSJKTyI+Mi4wMDwvY2JjOkFtb3VudD48L2NhYzpBbGxvd2FuY2VDaGFyZ2U+PC9jYWM6UHJpY2U+PC9jYWM6SW52b2ljZUxpbmU+PC9JbnZvaWNlPg==",
        "EINV_QR":"ASRiOTYwMzIxOS0yMDA1LTRlYmYtODM4Zi02OTAyMWIxZTMzMDkCAnt9AwVmYWxzZQQKMjAyMy0wMS0zMAUIRUlOLTAxMDEGAAcGMTMwLjAwCAk5OTk5OTk5OTMJBkFBQUFBQQoA",
        "EINV_NUM":"EIN-0101",
        "EINV_INV_UUID":"7a4452eb-0acd-49983-b630-b2b79d0acert"
        }"""
    json_file = json.loads(response) 
    if json_file["EINV_STATUS"] == 'SUBMITTED':
        qr_code = json_file['EINV_QR']

        qr = get_qr_code(qr_code)
        qr_result = frappe.db.sql("""
        SELECT tjfd.name 
        FROM `tabJO Fawtara Data` tjfd 
        INNER JOIN `tabSales Invoice` tsi ON tsi.name = tjfd.sales_invoice 
        WHERE tjfd.sales_invoice = %s
        """ , (name) , as_dict = True )

        frappe.db.set_value ('Sales Invoice' , name , 'custom_qr_data' , qr)
        frappe.db.set_value ('Sales Invoice' , name , 'custom_qr_code_data' ,qr_result[0]['name'])
        insert_data(json_file , qr_result[0]['name'] , qr )
        return f" QR Code Is Created For {name}"
    else :
         return "Failed"


@frappe.whitelist(allow_guest=True)
def general_sales_invoice(name_si  ,is_pos ):
    result = frappe.db.sql("""
           SELECT tsi.name , tsi.posting_date , tsi.payment_method  ,  tsi.company_tax_id , tsi.company  ,
		tsi.customer , tsi.total_taxes_and_charges  , tsi.total  , tsi.grand_total  , tsi.net_total ,
		tsii.idx , tsii.qty ,  tsii.description , tsii.amount , tsii.is_free_item , tsii.net_amount ,
		tittd.tax_rate ,
		tc.customer_type ,tc.customer_name ,tc.tax_id 
        FROM `tabSales Invoice` tsi
        INNER JOIN `tabSales Invoice Item` tsii ON tsi.name = tsii.parent 
        INNER JOIN `tabItem Tax Template Detail` tittd ON tsii.item_tax_template = tittd.parent 
        INNER JOIN tabCustomer tc ON tc.name =  tsi.customer
        WHERE tsi.name = %s
       """ , ( name_si ) , as_dict = True)
    


    if int(is_pos)== 1:
        payment_method = '012'
    elif int(is_pos)== 0:
        payment_method = '022' 
    # if (result[0]['payment_method'] == 'Cash'):
    #     payment_method = '012'
    # elif (result[0]['payment_method'] == 'On Account'):
    #     payment_method = '022'
    # else : 
    #     payment_method = 'XXXXXXXXXXX'
    if (result[0]['customer_type']) == 'Company':
        customer_type = "TN"
    elif (result[0]['customer_type']) == 'Individual':
        customer_type = "NIN"
    else :
        customer_type ='XXXXXXXXXXXXXXXXXX'#### plese , add PN option 
    rounded = 3
    id_szo = ''
    persent_val = 0
    uuid_num = (result[0]['name']).split('-')
    note_val = 'فاتورة تجريبية '
    invoice = ET.Element("Invoice" ,
                          attrib={
                            'xmlns'    : 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2' ,##################
                            'xmlns:cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2' ,################
                            'xmlns:cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2' , ##################
                            'xmlns:ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'################
                          })
    
    profile_id = ET.SubElement(invoice , 'cbc:ProfileID')
    profile_id.text = 'reporting:1.0'
    id = ET.SubElement(invoice , 'cbc:ID')
    id.text = result[0]['name']
    uuid = ET.SubElement(invoice , 'cbc:UUID')
    uuid.text =  result[0]['name']
    issue_date = ET.SubElement(invoice ,  'cbc:IssueDate')
    issue_date.text =  str(result[0]['posting_date'])
    invoice_type_code = ET.SubElement(invoice , 'cbc:InvoiceTypeCode' , name =payment_method )########### define name######### 
    invoice_type_code.text = '388'
    note = ET.SubElement(invoice ,'cbc:Note')
    note.text = note_val
    document_currency_code = ET.SubElement(invoice , 'cbc:DocumentCurrencyCode')
    document_currency_code.text = 'JOD'
    tax_currency_code = ET.SubElement(invoice , 'cbc:TaxCurrencyCode')
    tax_currency_code.text = 'JOD'
    additional_document_reference =ET.SubElement (invoice,'cac:AdditionalDocumentReference')
    id_additional = ET.SubElement(additional_document_reference ,'cbc:ID')
    id_additional.text = 'ICV'
    uuid_additional = ET.SubElement(additional_document_reference ,'cbc:UUID')
    uuid_additional.text =str((uuid_num[-1]) )  ###### is Ture ?? 

    ################ seller data 
    accounting_supplier_party = ET.SubElement(invoice , 'cac:AccountingSupplierParty')
    party_supp = ET.SubElement(accounting_supplier_party , 'cac:Party')
    postal_address_supp = ET.SubElement(party_supp , 'cac:PostalAddress')
    country_supp = ET.SubElement(postal_address_supp , 'cac:Country')
    identification_code_supp = ET.SubElement(country_supp ,'cbc:IdentificationCode')
    identification_code_supp.text = 'JO'
    party_tax_scheme_supp = ET.SubElement(party_supp , 'cac:PartyTaxScheme')
    company_id_supp = ET.SubElement(party_tax_scheme_supp , 'cbc:CompanyID')
    company_id_supp.text =  str(result[0]['company_tax_id'])
    party_tax_scheme_supp = ET.SubElement(party_tax_scheme_supp , 'cac:TaxScheme')
    id_tax_scheme_supp = ET.SubElement(party_tax_scheme_supp , 'cbc:ID')
    id_tax_scheme_supp.text = 'VAT'
    party_legal_entity_supp = ET.SubElement(party_supp , 'cac:PartyLegalEntity')
    registration_name_supp = ET.SubElement(party_legal_entity_supp , 'cbc:RegistrationName')
    registration_name_supp.text =  result[0]['company']



    ############## buyer Data 
    accounting_customer_party = ET.SubElement(invoice , 'cac:AccountingCustomerParty')
    party_cust = ET.SubElement(accounting_customer_party , 'cac:Party')
    party_identitfication_cust = ET.SubElement(party_cust ,'cac:PartyIdentification')
    id_cust = ET.SubElement(party_identitfication_cust ,'cbc:ID', schemeID = customer_type) 
    id_cust.text = str(result[0]['tax_id'] )
    postal_address_cust = ET.SubElement(party_cust , 'cac:PostalAddress')
    postal_zone_cust = ET.SubElement(postal_address_cust , 'cbc:PostalZone')
    postal_zone_cust.text = ' XXX'##### optional
    country_subentity_code = ET.SubElement(postal_address_cust , 'cbc:CountrySubentityCode')
    country_subentity_code.text = 'XXXXXX'
    country_cust = ET.SubElement(postal_address_cust , 'cac:Country')
    identification_code_cust = ET.SubElement(country_cust , 'cbc:IdentificationCode')
    identification_code_cust.text = 'JO'
    party_tax_scheme_cust = ET.SubElement(party_cust , 'cac:PartyTaxScheme')
    
    company_id_cust = ET.SubElement(party_tax_scheme_cust , 'cbc:CompanyID')
    company_id_cust.text = '1'
    tax_scheme_cust = ET.SubElement(party_tax_scheme_cust , 'cac:TaxScheme')
    id_tax_scheme_cust = ET.SubElement(tax_scheme_cust , 'cbc:ID')
    id_tax_scheme_cust.text = 'VAT'
    party_legal_entity_cust = ET.SubElement(party_cust ,'cac:PartyLegalEntity' ) 
    registration_name_cust = ET.SubElement(party_legal_entity_cust , 'cbc:RegistrationName')
    registration_name_cust.text = result[0]['customer_name'] 
    accounting_contact_cust = ET.SubElement(accounting_customer_party , 'cac:AccountingContact')
    telephone_cust = ET.SubElement(accounting_contact_cust , 'cbc:Telephone' )
    telephone_cust.text = '07XXXXXXX'####### optional
    
    ################ For data on the vendor's income stream
    seller_supplier_party = ET.SubElement(invoice ,'cac:SellerSupplierParty' )
    party_ss = ET.SubElement(seller_supplier_party , 'cac:Party')
    party_identitfication_ss = ET.SubElement(party_ss , 'cac:PartyIdentification')
    id_ss = ET.SubElement(party_identitfication_ss , 'cbc:ID')
    id_ss.text = 'XXXXXXXXX' ########### what here ???


    ######################### Entries for total income bill
    allowance_charge = ET.SubElement(invoice , 'cac:AllowanceCharge')
    charge_indicator= ET.SubElement(allowance_charge , 'cbc:ChargeIndicator')
    charge_indicator.text = 'false'
    allowance_charge_reason = ET.SubElement(allowance_charge, 'cbc:AllowanceChargeReason')
    allowance_charge_reason.text = 'discount'
    amount = ET.SubElement(allowance_charge , 'cbc:Amount' ,currencyID = "JO")
    amount.text = str(abs(round((float(result[0]['total'])- float(result[0]['net_total'])) , rounded)))
    tax_total = ET.SubElement(invoice , 'cac:TaxTotal')
    tax_amount = ET.SubElement(tax_total , 'cbc:TaxAmount',currencyID="JO")
    tax_amount.text = str(abs(round(float(result[0]['total_taxes_and_charges'] ),rounded)))
    legal_monetary_total = ET.SubElement(invoice , 'cac:LegalMonetaryTotal')
    tax_exclusive_amount = ET.SubElement(legal_monetary_total , 'cbc:TaxExclusiveAmount' ,currencyID="JO")
    tax_exclusive_amount.text = str(abs(round(float((result[0]['total'])),rounded)))
    tax_inclusive_amount = ET.SubElement(legal_monetary_total , 'cbc:TaxInclusiveAmount' , currencyID="JO")
    tax_inclusive_amount.text = str(abs(round(float((result[0]['grand_total'])),rounded)))
    allowance_total_amount = ET.SubElement(legal_monetary_total , 'cbc:AllowanceTotalAmount' ,currencyID="JO")
    allowance_total_amount.text = str(abs(round((float(result[0]['total']) -float( result[0]['net_total'])),rounded)))
    payable_amount = ET.SubElement(legal_monetary_total , 'cbc:PayableAmount' ,currencyID="JO")
    payable_amount.text = str(abs(round(float(result[0]['grand_total']),rounded)))

    ############Inputs for general invoice item details

    for row in result :
        invoice_line = ET.SubElement(invoice , 'cac:InvoiceLine')
        id_il = ET.SubElement(invoice_line , 'cbc:ID')
        id_il.text = str((row.get('idx')))
        invoiced_quantity_il = ET.SubElement(invoice_line , 'cbc:InvoicedQuantity' ,unitCode="PCE" )
        invoiced_quantity_il.text = str(int(row.get('qty')))
        line_extension_amount = ET.SubElement(invoice_line , 'cbc:LineExtensionAmount')
        line_extension_amount.text = str(round((float(row.get('net_amount'))) , rounded))
        tax_total_il = ET.SubElement(invoice_line , 'cac:TaxTotal')
        tax_amount_il = ET.SubElement(tax_total_il , 'cbc:TaxAmount' ,currencyID="JO")
        tax_amount_val = str(round(float((row.get('net_amount')* float(row.get('tax_rate'))/100)) ,rounded ))
        tax_amount_il.text =str(tax_amount_val)
        rounding_amount_il = ET.SubElement(tax_total_il , 'cbc:RoundingAmount' ,currencyID="JO")
        rounding_amount_il.text=str(round(float(row.get('net_amount') * ( 1 + (row.get('tax_rate')/100))) , rounded ))
        tax_subtotal_il = ET.SubElement(tax_total_il , 'cac:TaxSubtotal')
        tax_amount_sub = ET.SubElement( tax_subtotal_il , 'cbc:TaxAmount', currencyID = "JO")
        tax_amount_sub.text = str(tax_amount_val)
        tax_category_sub =ET.SubElement (tax_subtotal_il , 'cac:TaxCategory')
        id_tax_category = ET.SubElement(tax_category_sub , 'cbc:ID',attrib=
                                        {
                                             'schemeAgencyID' :"6" ,
                                             'schemeID'       : "UN/ECE 5305"
                                        })
        if int(row.get('is_free_item')) == 1 :
            id_szo = 'Z'
        elif int(row.get('is_free_item')) == 0 :
            if int(row.get('tax_rate')) == 0 :
                id_szo = 'O'
            elif int(row.get('tax_rate')) > 0 :
                id_szo = 'S'
        id_tax_category.text= id_szo
        percent = ET.SubElement(tax_category_sub , 'cbc:Percent')
        if   int(row.get('is_free_item')) == 1:
            persent_val = 0
        elif int(row.get('is_free_item')) == 0:
            persent_val = row.get('tax_rate')

        percent.text = str(int(persent_val))
        tax_scheme = ET.SubElement(tax_category_sub , 'cac:TaxScheme')
        id_tax_scheme = ET.SubElement(tax_scheme , 'cbc:ID' , attrib=
                                      {
                                          'schemeAgencyID' :"6"  ,
                                          'schemeID'       : "UN/ECE 5153"
                                      })
        id_tax_scheme.text = 'VAT'
        item = ET.SubElement(invoice_line , 'cac:Item')
        name = ET.SubElement(item , 'cbc:Name')
        name.text = row.get('description')
        price = ET.SubElement(invoice_line , 'cac:Price')
        price_amount = ET.SubElement(price , 'cbc:PriceAmount' ,currencyID="JO" )
        price_amount.text = str(round(float(row.get('net_amount')),rounded))
        allowance_charge_price = ET.SubElement(price , 'cac:AllowanceCharge')
        charge_indicator = ET.SubElement(allowance_charge_price , 'cbc:ChargeIndicator')
        charge_indicator.text = 'false'
        allowance_charge_reason_price = ET.SubElement(allowance_charge_price , 'cbc:AllowanceChargeReason')
        allowance_charge_reason_price.text = 'DISCOUNT'
        amount_price =  ET.SubElement(allowance_charge_price ,'cbc:Amount', currencyID="JO")
        amount_price.text = str(round(float(row.get('amount')) - float(row.get('net_amount')),3) )
        
    xml_string = ET.tostring(invoice, encoding="utf-8").decode("utf-8")
    return  xml_string

############## mahmoud Code for General sales return invoice
@frappe.whitelist(allow_guest=True)
def general_sales_return_invoice(name_si):
    result = frappe.db.sql("""
    SELECT tsi.name , tsi.posting_date , tsi.payment_method ,tsi.return_against  , tsi.company_tax_id ,tsi.company ,
		tsi.remarks , tsi.discount_amount , tsi.total_taxes_and_charges , tsi.total , tsi.net_total , tsi.grand_total , 
		tsii.rate ,tsii.net_rate , tsii.idx , tsii.qty , tsii.description ,tsii.discount_amount AS child_discount_amount , 
        tsii.item_tax_template , tsii.amount , tsii.net_amount , 
		tittd.tax_rate 
        FROM `tabSales Invoice` tsi
        INNER JOIN `tabSales Invoice Item` tsii ON tsi.name = tsii.parent 
        INNER JOIN `tabItem Tax Template Detail` tittd ON tsii.item_tax_template = tittd.parent 
        WHERE tsi.name = %s
    """ , (name_si) , as_dict = True )
    if result:
        against = frappe.db.sql("""
        SELECT tsii.qty , tsi.grand_total
            FROM `tabSales Invoice` tsi
            INNER JOIN `tabSales Invoice Item` tsii ON tsi.name = tsii.parent 
            WHERE tsi.name = %s
        """ , result[0]['return_against'] , as_dict = True)

    uuid_num = (result[0]['name']).split('-')
    rounded = 3 
    id_szo=''
    invoice = ET.Element("Invoice" ,
                          attrib={
                            'xmlns'    : 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2' ,##################
                            'xmlns:cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2' ,################
                            'xmlns:cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2' , ##################
                            'xmlns:ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'################
                          }
                           )
    profile_id = ET.SubElement(invoice , 'cbc:ProfileID')
    profile_id.text = 'reporting:1.0'
    id = ET.SubElement(invoice , 'cbc:ID')
    id.text = result[0]['name']
    uuid = ET.SubElement(invoice , 'cbc:UUID')
    uuid.text = result[0]['name']
    issue_date = ET.SubElement(invoice ,  'cbc:IssueDate')
    issue_date.text = str(result[0]['posting_date'])
    invoice_type_code = ET.SubElement(invoice , 'cbc:InvoiceTypeCode' , name = '011')########### define name######### 
    invoice_type_code.text = '381'
    document_currency_code = ET.SubElement(invoice , 'cbc:DocumentCurrencyCode')
    document_currency_code.text = 'JOD'
    tax_currency_code = ET.SubElement(invoice , 'cbc:TaxCurrencyCode')
    tax_currency_code.text = 'JOD'
    billing_reference=ET.SubElement(invoice , 'cac:BillingReference')
    invoice_documnet_reference = ET.SubElement(billing_reference , 'cac:InvoiceDocumentReference')
    id_ref = ET.SubElement(invoice_documnet_reference , 'cbc:ID' )
    id_ref.text = result[0]['return_against']
    uuid_ref = ET.SubElement(invoice_documnet_reference ,'cbc:UUID')
    uuid_ref.text = result[0]['return_against']
    document_description = ET.SubElement(invoice_documnet_reference ,'cbc:DocumentDescription')
    document_description.text = str(against[0]['grand_total'])
    additional_document_reference = ET.SubElement(invoice , 'cac:AdditionalDocumentReference')
    id_add_ref = ET.SubElement(additional_document_reference ,'cbc:ID' )
    id_add_ref.text = 'ICV'
    uuid_add_ref = ET.SubElement(additional_document_reference , 'cbc:UUID')
    uuid_add_ref.text = str(uuid_num[-1])

    ################# Seller's data

    accounting_supplier_party = ET.SubElement(invoice , 'cac:AccountingSupplierParty')
    party_supp = ET.SubElement(accounting_supplier_party , 'cac:Party')
    postal_address_supp = ET.SubElement(party_supp , 'cac:PostalAddress')
    country_supp = ET.SubElement(postal_address_supp , 'cac:Country')
    identification_code_supp = ET.SubElement(country_supp ,'cbc:IdentificationCode')
    identification_code_supp.text = 'JO'
    party_tax_scheme_supp = ET.SubElement(party_supp , 'cac:PartyTaxScheme')
    company_id_supp = ET.SubElement(party_tax_scheme_supp , 'cbc:CompanyID')
    company_id_supp.text = result[0]['company_tax_id']
    party_tax_scheme_supp = ET.SubElement(party_tax_scheme_supp , 'cac:TaxScheme')
    id_tax_scheme_supp = ET.SubElement(party_tax_scheme_supp , 'cbc:ID')
    id_tax_scheme_supp.text = 'VAT'
    party_legal_entity_supp = ET.SubElement(party_supp , 'cac:PartyLegalEntity')
    registration_name_supp = ET.SubElement(party_legal_entity_supp , 'cbc:RegistrationName')
    registration_name_supp.text = result[0]['company']

    ################################ Buyer's data
    ############### this part is constant code 
    accounting_customer_party = ET.SubElement(invoice , 'cac:AccountingCustomerParty')
    party_cust = ET.SubElement(accounting_customer_party , 'cac:Party')
    postal_address_cust = ET.SubElement(party_cust , 'cac:PostalAddress')
    country_cust =ET.SubElement(postal_address_cust , 'cac:Country')
    identification_code_cust = ET.SubElement(country_cust , 'cbc:IdentificationCode')
    identification_code_cust.text = 'JO'
    party_tax_scheme_cust = ET.SubElement(party_cust , 'cac:PartyTaxScheme')
    tax_scheme_cust = ET.SubElement(party_tax_scheme_cust , 'cac:TaxScheme')
    id_tax_scheme_cust = ET.SubElement(tax_scheme_cust , 'cbc:ID')
    id_tax_scheme_cust.text = 'VAT'
    party_legal_entity_cust = ET.SubElement(party_cust , 'cac:PartyLegalEntity')

    ################## Data on the seller's income source sequence
    seller_supplier_party = ET.SubElement(invoice ,'cac:SellerSupplierParty' )
    party_ss = ET.SubElement(seller_supplier_party , 'cac:Party')
    party_identitfication_ss = ET.SubElement(party_ss , 'cac:PartyIdentification')
    id_ss = ET.SubElement(party_identitfication_ss , 'cbc:ID')
    id_ss.text = 'XXXXXXXXX'#################################################################

    
    #################### Reason for return
    payment_means = ET.SubElement(invoice ,'cac:PaymentMeans')
    payment_means_code = ET.SubElement(payment_means , 'cbc:PaymentMeansCod' ,listID="UN/ECE 4461" )
    payment_means_code.text = '10'
    instruction_note = ET.SubElement(payment_means , 'cbc:InstructionNote')
    instruction_note.text=result[0]['remarks']


    ####################### Total discount
    allowance_charge = ET.SubElement(invoice , 'cac:AllowanceCharge')
    charge_indicator= ET.SubElement(allowance_charge , 'cbc:ChargeIndicator')
    charge_indicator.text = 'false'
    allowance_charge_reason = ET.SubElement(allowance_charge, 'cbc:AllowanceChargeReason')
    allowance_charge_reason.text = 'discount'
    amount = ET.SubElement(allowance_charge , 'cbc:Amount' ,currencyID = "JO")
    amount.text = str(round(abs(float(result[0]['total'])) - abs(float(result[0]['net_total'])), rounded))

    ############The total value of the tax to be returned
    tax_total = ET.SubElement(invoice , 'cac:TaxTotal')
    tax_amount = ET.SubElement(tax_total ,'cbc:TaxAmount' , currencyID = "JO")
    tax_amount.text = str(abs(result[0]['total_taxes_and_charges']))
    for sub_tax in result:
        tax_subtotal = ET.SubElement( tax_total ,'cac:TaxSubtotal')
        taxable_amount =ET.SubElement(tax_subtotal , 'cbc:TaxableAmount' , currencyID = 'JO')
        taxable_amount.text = str(round(abs(float(result[0]['net_total'])), rounded))
        tax_amount_sub = ET.SubElement( tax_subtotal , 'cbc:TaxAmount' , currencyID = "JO")
        tax_amount_sub.text = str(round((abs(float(sub_tax.get('tax_rate'))/100)* abs(float(sub_tax.get('net_rate')))),rounded))
        tax_category = ET.SubElement( tax_subtotal , 'cac:TaxCategory')
        id_tax_category = ET.SubElement(tax_category , 'cbc:ID', attrib=
                                        {
                                            'schemeID' : "UN/ECE 5305" ,
                                            'schemeAgencyID' : "6"
                                        })
        id_tax_category.text = 'S'
        percent = ET.SubElement(tax_category , 'cbc:Percent')
        percent.text = str(sub_tax.get('tax_rate'))
        tax_scheme = ET.SubElement(tax_category , 'cac:TaxScheme')
        id_tax_scheme= ET.SubElement(tax_scheme , 'cbc:ID', attrib=
                                        {
                                            'schemeID' : "UN/ECE 5153" ,
                                            'schemeAgencyID' : "6"
                                        })
        id_tax_scheme.text = 'VAT'


    ################# Entries for the total return invoice
    legal_monetary_total=ET.SubElement (invoice ,'cac:LegalMonetaryTotal')
    tax_exclusive_amount =ET.SubElement (legal_monetary_total , 'cbc:TaxExclusiveAmount' , currencyID = "JO")
    tax_exclusive_amount.text = str(round(abs(float(result[0]['total'])),rounded))
    tax_inclusive_amount = ET.SubElement(legal_monetary_total , 'cbc:TaxInclusiveAmount' , currencyID = "JO")
    tax_inclusive_amount.text = str(round( abs(float(result[0]['grand_total'])) ,rounded))
    allowance_total_amount =ET.SubElement(legal_monetary_total , 'cbc:AllowanceTotalAmount' , currencyID = "JO")
    allowance_total_amount.text = str(round(abs(float(result[0]['total']))  - abs(float(result[0]['net_total'])) ,rounded))
    prepaid_amount = ET.SubElement(legal_monetary_total , 'cbc:PrepaidAmount' , currencyID = "JO")
    prepaid_amount.text = '0'
    payable_amount = ET.SubElement(legal_monetary_total , 'cbc:PayableAmount' , currencyID = "JO")
    payable_amount.text = str(round( abs(float(result[0]['grand_total'])) ,rounded))

    ########################### Inputs for general invoice item details
    
    for row in result : 
        invoice_line = ET.SubElement(invoice , 'cac:InvoiceLine')
        id = ET.SubElement(invoice_line , 'cbc:ID')
        id.text = str(row.get('idx'))
        invoiced_quantity = ET.SubElement(invoice_line , 'cbc:InvoicedQuantity' ,unitCode="PCE" )
        invoiced_quantity.text = str(abs(row.get('qty')))
        line_extension_amount = ET.SubElement(invoice_line , 'cbc:LineExtensionAmount')
        line_extension_amount.text = str(round(abs(float(row.get('net_amount'))) , rounded))
        tax_total = ET.SubElement(invoice_line , 'cac:TaxTotal')
        tax_amount= ET.SubElement(tax_total , 'cbc:TaxAmount' ,currencyID="JO")
        tax_amount.text =str(round(abs(float(row.get('net_amount')))* abs(row.get('tax_rate'))/100 , rounded))
        rounding_amount = ET.SubElement(tax_total , 'cbc:RoundingAmount' ,currencyID="JO")
        rounding_amount.text=str(round(abs(float(row.get('net_amount'))) + (abs(float(row.get('net_amount')))  *  abs(row.get('tax_rate'))/100) , rounded))
        tax_subtotal = ET.SubElement(tax_total , 'cac:TaxSubtotal')
        taxable_amount=ET.SubElement(tax_subtotal , 'cbc:TaxableAmount' , currencyID = 'JO')
        taxable_amount.text = str(round(abs(float(row.get('net_amount')))*abs(float(row.get('tax_rate')/100)) ,rounded))
        tax_amount_sub = ET.SubElement( tax_subtotal , 'cbc:TaxAmount' , currencyID = "JO")
        tax_amount_sub.text = str(round(abs(float(row.get('net_amount')))* abs(row.get('tax_rate'))/100 , rounded))
        tax_category = ET.SubElement( tax_subtotal , 'cac:TaxCategory')
        id_tax_category = ET.SubElement(tax_category , 'cbc:ID', attrib=
                                        {
                                            'schemeAgencyID' : "6",
                                            'schemeID' : "UN/ECE 5305"
                                        })
        if row.get('tax_rate') > 0 :
            id_szo = 'S'
        elif row.get('tax_rate') == 0 :
            id_szo = 'O'
        elif row.get('tax_rate') == None :
            id_szo = 'Z'
        id_tax_category.text = str(id_szo)
        percent = ET.SubElement(tax_category , 'cbc:Percent')
        if   row.get('item_tax_template')== None:
            persent_val = 0
        elif row.get('item_tax_template')!= None:
            persent_val = (abs(row.get('tax_rate')))
        percent.text = str(int(persent_val))
        tax_scheme = ET.SubElement(tax_category , 'cac:TaxScheme')
        id_tax_scheme= ET.SubElement(tax_scheme , 'cbc:ID', attrib=
                                        {
                                            'schemeAgencyID' : "6",
                                            'schemeID' :"UN/ECE5153"
                                        })
        id_tax_scheme.text = 'VAT'
        item = ET.SubElement(invoice_line , 'cac:Item')
        name = ET.SubElement(item ,'cbc:Name')
        name.text=row.get('description')
        price = ET.SubElement(invoice_line , 'cac:Price')
        price_amount = ET.SubElement(price , 'cbc:PriceAmount' ,currencyID="JO")
        price_amount.text = str(round(abs(float(row.get('amount'))) , rounded))
        base_quantity = ET.SubElement(price , 'cbc:BaseQuantity' , unitCode="C62")
        base_quantity.text ='1'
        allowance_charge = ET.SubElement(price , 'cac:AllowanceCharge')
        charge_indicator = ET.SubElement(allowance_charge ,'cbc:ChargeIndicator')
        charge_indicator.text = 'false'
        allowance_charge_reason = ET.SubElement(allowance_charge , 'cbc:AllowanceChargeReason')
        allowance_charge_reason.text = 'DISCOUNT'
        amount= ET.SubElement(price , 'cbc:Amount' , currencyID="JO")
        amount.text = str(round(abs(float(row.get('amount')))   - abs(float(row.get('net_amount'))) , rounded))

    xml_string = ET.tostring(invoice, encoding="utf-8").decode("utf-8")
    return  xml_string



def insert_data(file , einv_name  , qr_decoded):
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"einv_status"   ,file.get("EINV_RESULTS", {}).get("status")                           )
    if file.get("EINV_RESULTS", {}).get("ERRORS") == []:
         frappe.db.set_value ('JO Fawtara Data',einv_name ,"errors" , "No Errors")
    else:
         frappe.db.set_value ('JO Fawtara Data',einv_name ,"errors"   ,(file.get("EINV_RESULTS", {}).get("ERRORS"))                         )#########
    if file.get("EINV_RESULTS", {}).get("WARNINGS") == []: 
        frappe.db.set_value ('JO Fawtara Data',einv_name ,"warnings" , " No Warnings")
    else:     
        frappe.db.set_value ('JO Fawtara Data',einv_name ,"warnings"  ,(file.get("EINV_RESULTS", {}).get("WARNINGS")  )                     )#########
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"qr_code_status",file.get("EINV_STATUS")                                              )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"qr_code"       ,qr_decoded                                                           )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"singed_invoice",file.get("EINV_SINGED_INVOICE")                                      )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"number"        ,file.get("EINV_NUM")                                                 )         
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"inv_uuid"      ,file.get("EINV_INV_UUID")                                            )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"info_type"     ,file.get("EINV_RESULTS", {}).get("INFO", [])[0].get("type")          )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"info_status"   ,file.get("EINV_RESULTS", {}).get("INFO", [])[0].get("status")        )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"info_code"     ,file.get("EINV_RESULTS", {}).get("INFO", [])[0].get("EINV_CODE")     )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"info_category" ,file.get("EINV_RESULTS", {}).get("INFO", [])[0].get("EINV_CATEGORY") )
    frappe.db.set_value ('JO Fawtara Data',einv_name ,"info_message"  ,file.get("EINV_RESULTS", {}).get("INFO", [])[0].get("EINV_MESSAGE")  )
