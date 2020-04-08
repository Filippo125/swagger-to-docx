from docx import Document

from docu_builder import build_title_section, build_api_section, build_model_section
from swagger_parser import SwaggerParser
import argparse




parser = argparse.ArgumentParser(description='Generate docx from swagger file')
parser.add_argument('--swagger', dest='swagger_file', type=str, required=True, help='swagger (yaml) file path ')
parser.add_argument('--out', dest='out_file', action='store', type=str, required=True, help='output docx file path')

args = parser.parse_args()

print("Swagger source file: %s" % args.swagger_file)
out_file = args.out_file
if ".docx" not in out_file:
	out_file += ".docx"
print("Output docx file: %s" % out_file)
swagger = SwaggerParser(filename=args.swagger_file)
document = Document()
build_title_section(swagger=swagger, doc=document)
document.add_page_break()
build_api_section(swagger=swagger, doc=document)
document.add_page_break()
build_model_section(swagger=swagger, doc=document)
document.save(out_file)

exit()