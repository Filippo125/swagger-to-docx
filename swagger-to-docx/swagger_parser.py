import yaml


class SwaggerParser:
	def __init__(self, content):
		self.swagger = yaml.load(content, Loader=yaml.FullLoader)

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

	def _build_array_object(self,prop) -> list:
		# check if array items has reference to object
		if "$ref" in prop["items"]:
			return [self.build_example_object(obj=self.get_ref(ref=prop["items"]["$ref"]))]
		# array has basic type field
		return [prop["items"]["type"]]

	def build_example_object(self, obj: dict):
		obj_type = obj.get("type","object")

		if "allOf" in obj:
			# composite object, iter on subobject
			tmp = dict()
			for item in obj["allOf"]:
				if "$ref" in item:
					tmp.update(self.build_example_object(self.get_ref(item["$ref"])))
				else:
					tmp.update(self.build_example_object(item))
			return tmp
		elif obj_type == "object":
			props = obj["properties"]
			tmp = dict()
			for key, prop in props.items():
				if "type" in prop:
					if prop["type"] == "array":
						tmp[key] = self._build_array_object(prop)
					else:
						tmp[key] = prop["type"]
				elif "$ref" in prop:
					tmp[key] = self.build_example_object(obj=self.get_ref(ref=prop["$ref"]))
			return tmp
		elif obj_type == "array":
			return self._build_array_object(obj)
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
	def get_header_refs(apistruct: dict):
		if "parameters" not in apistruct:
			return None
		params = apistruct["parameters"]
		out = []
		for param in params:
			if param["in"] == "header":
				out.append(param)
		return out

	@staticmethod
	def get_permission_list(api_struct) -> list:
		perms = []
		for sec in api_struct.get("security",[]):
			for sec_type, sec_perms in sec.items():
				for p in sec_perms:
					perms.append("%s %s" % (sec_type, p))
		return perms

	def get_model_triplette_list(self, model_value) -> list:
		tmp = list()
		if "properties" in model_value:
			for field, prop in model_value["properties"].items():
				tp = prop.get("type", "")
				f_text = prop.get("description", "")
				if tp == "object":
					f_text += "\n See %s for detail" % (prop["$ref"].split("/")[-1])
				elif tp == "array":
					# check if array items has reference to object
					if "$ref" in prop["items"]:
						f_text += "\n See %s for detail" % (prop["items"]["$ref"].split("/")[-1])
					else:
						# array has basic type field
						f_text += "\n Array of %s" % (prop["items"]["type"])
				tmp.append({"name": field, "type": tp,"desc": f_text})
		elif "allOf" in model_value:
			for item in model_value["allOf"]:
				if "$ref" in item:
					tmp.extend(self.get_model_triplette_list(self.get_ref(item["$ref"])))
				else:
					tmp.extend(self.get_model_triplette_list(item))
		return tmp