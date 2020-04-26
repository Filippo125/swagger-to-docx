from docx import Document
from docu_builder import build_title_section, build_api_section, build_model_section
from swagger_parser import SwaggerParser
import argparse
import requests
import traceback




parser = argparse.ArgumentParser(description='Generate docx from swagger file')
parser.add_argument('--swagger', dest='swagger_file', type=str, required=True, help='swagger (yaml) file path or http path ')
parser.add_argument('--out', dest='out_file', action='store', type=str, required=True, help='output docx file path')




def get_content_from_http(url) :
	resp = requests.get(url=url)
	return resp.content


if __name__ == "__main__":
	try:
		args = parser.parse_args()
		if args.swagger_file.startswith("http"):
			print("Swagger source from: %s" % args.swagger_file)
			content = get_content_from_http(url=args.swagger_file)
		else:
			with open(args.swagger_file, 'r') as f:
				content = f.read()
		out_file = args.out_file
		if ".docx" not in out_file:
			out_file += ".docx"
		print("Output docx file: %s" % out_file)
		swagger = SwaggerParser(content=content)
		document = Document()
		build_title_section(swagger=swagger, doc=document)
		document.add_page_break()
		build_api_section(swagger=swagger, doc=document)
		document.add_page_break()
		build_model_section(swagger=swagger, doc=document)
		document.save(out_file)
		exit(0)
	except Exception as ex:
		traceback.print_exception(type(ex), ex, ex.__traceback__)
		print("Error: ", ex)
		exit(1)