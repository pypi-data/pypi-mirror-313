from echobox.tool import datatypes


class LegacySpec(object):

    def __init__(self, def_list, config_name, kv=None):
        self.def_list = def_list
        self.config_name = config_name
        self.config_names = set([self.config_name])

        self.config_data = {}
        if def_list:
            self.config_data_raw = {}
            if config_name in self.def_list:
                self.config_data_raw = self.def_list[config_name]

            self.config_data_parent = {}
            config_data = dict(self.config_data_raw)
            if kv:
                config_data.update({item[0]: item[1] for item in (_kv.split('=') for _kv in kv.split(','))})
            self.config_data = config_data

            if 'parent_config' in config_data:
                parent_config = config_data.get('parent_config', ())
                del config_data['parent_config']
                self._process_parent_config(parent_config)

    def _process_parent_config(self, parent_config):
        config_data = {}
        for _name in parent_config:
            # overwrite config
            parent_ecs_def = self.__class__(self.def_list, _name)
            self.config_names.update(parent_ecs_def.config_names)
            config_data = datatypes.merge(config_data, parent_ecs_def.config_data, 'merge')
        self.config_data_parent = dict(config_data)

        self.config_data = datatypes.merge(config_data, self.config_data, 'merge')

    def __str__(self):
        data = self.config_data
        return str(data)

    def __repr__(self):
        return self.__str__()
