"""Config reader class"""
import logging.config
import os
import json
from json.decoder import JSONDecodeError
from yaml import Loader, dump, load


LOGGER = logging.getLogger("Config")

class Config(dict):
    """
    Config reader class
    """
    def __init__(self, data=None):
        super(Config, self).__init__()
        if data:
            if isinstance(data, dict):
                self.__update(data, {})
            elif isinstance(data, str):
                filename = os.path.basename(data)
                ext = os.path.splitext(filename)[1]
                self.__path = data
                self.__ext = ext
                if ext == "json":
                    self.__update(self.load_json(data), {})
                elif ext == "yaml" or ext == "yml":
                    self.__update(self.load_yaml(data), {})
                else:
                    try:
                        self.__update(self.load_json(data), {})
                    except (JSONDecodeError,TypeError):
                        self.__update(self.load_yaml(data), {})
            else:
                raise ValueError("Unknown data format")

    @staticmethod
    def dump_yaml(data, file_name):
        '''Dump data to yaml file'''
        to_dump = data.copy()
        del to_dump['_Config__path']
        del to_dump['_Config__ext']
        with open(f"{file_name}", "w", encoding="utf-8") as f:
            dump(to_dump, f)

    @staticmethod
    def dump_json(data, file_name):
        '''Dump data to json file'''
        to_dump = data.copy()
        del to_dump['_Config__path']
        del to_dump['_Config__ext']
        with open(f"{file_name}", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(to_dump, indent=4))

    def save(self):
        '''Save config to file'''
        try:
            if self.__ext.lower() == ".json":
                self.save_to_json(self.__path)
            elif self.__ext.lower() == ".yaml" or self.__ext.lower() == ".yml":
                self.save_to_yaml(self.__path)
            else:
                LOGGER.error("Cannot save file, unknown extenstion %s", self.__ext)
        except Exception:
            LOGGER.error("Cannot save config", exc_info=True)

    def save_to_json(self, filename):
        '''Save config to json file'''
        self.dump_json(self, filename)

    def save_to_yaml(self, filename):
        '''Save config to yaml file'''
        self.dump_yaml(self, filename)

    @staticmethod
    def load_json(config):
        '''Load json file'''
        with open(config, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_yaml(config):
        '''Load yaml file'''
        with open(config, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)
        return data

    def new(self, data):
        '''Create new config from data'''
        self.__update(data, {})

    def load(self, data, did):
        """load methode"""
        self.__update(data, did)

    def __update(self, data, did):
        dataid = id(data)
        did[dataid] = self
        for k in data:
            dkid = id(data[k])
            if dkid in did.keys():
                self[k] = did[dkid]
            elif isinstance(data[k], Config):
                self[k] = data[k]
            elif isinstance(data[k], dict):
                obj = Config()
                obj.load(data[k], did)
                self[k] = obj
                obj = None
            elif isinstance(data[k], list) or isinstance(data[k], tuple):
                self[k] = self._add_list(data[k], did)
            else:
                self[k] = data[k]

    def _add_list(self, data, did):
        lst = []
        for l in data:
            if isinstance(l, dict):
                obj = Config()
                obj.load(l, did)
                lst.append(obj)
                obj = None
            elif isinstance(l, list) or isinstance(l, tuple):
                lst.append(self._add_list(l, did))
            else:
                lst.append(l)
        if isinstance(data, tuple):
            lst = tuple(lst)
        return lst

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            self[key] = Config(value)
        else:
            self[key] = value

    def has_key(self, k):
        """ returns True if key is present in the config"""
        if k in self.keys():
            return True
        else:
            return False

    def update(self, *args):
        for obj in args:
            for k in obj:
                if isinstance(obj[k], dict):
                    self[k] = Config(obj[k])
                else:
                    self[k] = obj[k]
        return self

    def merge(self, *args):
        """ merges the config with one or more configs"""
        for obj in args:
            for k in obj:
                if k in self.keys():
                    if isinstance(self[k], list) and isinstance(obj[k], list):
                        self[k] += obj[k]
                    elif isinstance(self[k], list):
                        self[k].append(obj[k])
                    elif isinstance(obj[k], list):
                        self[k] = [self[k]] + obj[k]
                    elif isinstance(self[k], Config) and isinstance(obj[k], Config):
                        self[k].merge(obj[k])
                    elif isinstance(self[k], Config) and isinstance(obj[k], dict):
                        self[k].merge(obj[k])
                    else:
                        self[k] = [self[k], obj[k]]
                else:
                    if isinstance(obj[k], dict):
                        self[k] = Config(obj[k])
                    else:
                        self[k] = obj[k]
        return self

    def replace_variables(self, variables):
        """ replaces all variables in the config with the given variables"""
        for k, obj in self.items():
            if isinstance(obj, Config):
                obj.replace_variables(variables)
            elif isinstance(obj, str):
                self[k] = obj.format(**variables)
            elif isinstance(obj, list) or isinstance(obj, tuple):
                self[k] = self.replace_in_list(obj, variables)

    def replace_in_list(self, obj, variables):
        """ replaces all variables in the list with the given variables"""
        for i, entry in enumerate(obj):
            if isinstance(entry, Config):
                entry.replace_variables(variables)
            elif isinstance(entry, str):
                obj[i] = entry.format(**variables)
            elif isinstance(obj, list) or isinstance(obj, tuple):
                self.replace_in_list(obj, variables)
        return obj

