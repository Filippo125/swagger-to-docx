import yaml


class SwaggerParser:
	def __init__(self, filename):
		with open(filename, 'r') as f:
			self.swagger = yaml.load(f.read(), Loader=yaml.FullLoader)

	def get_info(self):
		return self.swagger["info"]

	def get_path(self):
		return self.swagger["paths"]

	def get_definitions(self):
		return self.swagger["definitions"]

	def get_ref(self, ref: str) -> dict:
		chunk = ref.split("/")[1:]  # ignore first '#'
		p = self.swagger
		for c in chunk:
			p = p[c]
		return p

	def build_example_object(self, obj: dict) -> dict:
		if obj["type"] == "object":
			props = obj["properties"]
			tmp = dict()
			for key, prop in props.items():
				if "type" in prop:
					if prop["type"] == "array":
						tmp[key] = [self.build_example_object(obj=self.get_ref(ref=prop["items"]["$ref"]))]
					else:
						tmp[key] = prop["type"]
				elif "$ref" in prop:
					tmp[key] = self.build_example_object(obj=self.get_ref(ref=prop["$ref"]))
			return tmp
		raise Exception("Cannot convert %s" % str(obj))

	@staticmethod
	def get_body_ref(apistruct: dict):
		if "parameters" not in apistruct:
			return None
		params = apistruct["parameters"]
		for param in params:
			if param["in"] == "body":
				return param["schema"]["$ref"]
		return None

	@staticmethod
	def get_permission_list(api_struct) -> list:
		perms = []
		for sec in api_struct.get("security",[]):
			for sec_type, sec_perms in sec.items():
				for p in sec_perms:
					perms.append("%s %s" % (sec_type, p))
		return perms
