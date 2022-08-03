import yaml

class ConfigData:
    CONFIG_FILE = "E:\\Users\\Brad\\Documents\\billspy.config.yaml"

    @staticmethod
    def get_config_dict():
        with open(ConfigData.CONFIG_FILE) as f:
            return yaml.safe_load(f)
