from Comm.path import ensure_path_sep
from Conf.models import Config
from Conf.yaml_control import GetYamlData

_data = GetYamlData(ensure_path_sep("/Conf/config.yaml")).get_yaml_data()
config = Config(**_data)