import getpass
import os

from echobox.app.devops import DevOpsApp
from echobox.app.devops import DevOpsAppConfigProvider
from echobox.tool import file
from echobox.tool import functocli
from echobox.tool import utils


class SimpleMultiDeveloperDevOpsAppConfigProvider(DevOpsAppConfigProvider):

    def __init__(self, app, app_base_name, kwargs):
        self.app = app
        self.app_base_name = app_base_name
        self.kwargs = kwargs
        self.developer_name = self._determine_developer_name()
        app_name = self.determine_app_name()
        DevOpsAppConfigProvider.__init__(self, app_name)

    def _determine_developer_name(self):
        app_config = DevOpsAppConfigProvider.get_box_local_config(self)
        developer_name = app_config.get('developer_name', None)
        if not developer_name:
            developer_name = getpass.getuser()
        developer_name_from_cmd = self.kwargs.get('developer_name', None)
        developer_name = developer_name_from_cmd if developer_name_from_cmd else developer_name
        return developer_name

    def determine_app_name(self):
        if self.app.isolate_by_developer():
            env = self.get_env()
            app_name = '%s-%s-%s' % (env, self.developer_name, self.app_base_name)
            return app_name
        else:
            return self.app_base_name

    def get_app_root_dir(self):
        app_root_dir = self.get_roles_dir() + '/' + self.app_base_name
        return app_root_dir

    def get_env(self):
        env_from_puppy_env = DevOpsAppConfigProvider.get_env(self)
        env_from_cmd_args = self.kwargs.get('env')
        return env_from_cmd_args if env_from_cmd_args else env_from_puppy_env


class MultiDeveloperDevOpsAppConfigProvider(SimpleMultiDeveloperDevOpsAppConfigProvider):

    def __init__(self, app, app_base_name, kwargs):
        self.sandbox_code_dir = None
        SimpleMultiDeveloperDevOpsAppConfigProvider.__init__(self, app, app_base_name, kwargs)
        self._process_sandbox()

    def get_root_dir(self):
        root_dir = SimpleMultiDeveloperDevOpsAppConfigProvider.get_root_dir(self)
        if self.sandbox_code_dir is not None:
            if self._manager_is_in_devops_folder():
                return f'{self.sandbox_code_dir}/devops'
            else:
                return self.sandbox_code_dir
        else:
            return root_dir

    def get_source_code_root_dir(self):
        root_dir = SimpleMultiDeveloperDevOpsAppConfigProvider.get_root_dir(self)
        if self._manager_is_in_devops_folder():
            return os.path.dirname(root_dir)
        else:
            return root_dir

    def _manager_is_in_devops_folder(self):
        root_dir = SimpleMultiDeveloperDevOpsAppConfigProvider.get_root_dir(self)
        return root_dir.endswith('/devops')

    def _process_sandbox(self):
        if self.sandbox_version != 0:
            self.sandbox_code_dir = '%s/sandbox-code-%03d' % (self.app_persistent_storage_dir, self.sandbox_version)

    def determine_app_name(self):
        env = self.get_env()
        if env == 'test' or env == 'dev':
            self.sandbox_version = self.kwargs.get('sandbox_version', 0)
        else:
            self.sandbox_version = 0

        self.shadow_id = int(os.getenv('shadow_id', 0))

        app_name = '%s-%s-%s' % (env, self.developer_name, self.app_base_name)
        if self.sandbox_version != 0:
            app_name = '%s-%s-%s-sandbox-%03d' % (env, self.developer_name, self.app_base_name, self.sandbox_version)

        if self.shadow_id != 0:
            app_name = '%s-%s-%s-shadow-%03d' % (env, self.developer_name, self.app_base_name, self.shadow_id)
        return app_name


class SimpleMultiDeveloperDevOpsApp(DevOpsApp):

    def __init__(self, app_base_name, **kwargs):
        self.app_base_name = app_base_name
        self.kwargs = kwargs

        self.app_config_provider = SimpleMultiDeveloperDevOpsAppConfigProvider(self, self.app_base_name, self.kwargs)
        self.developer_name = self.app_config_provider.developer_name

        DevOpsApp.__init__(self, self.app_config_provider.app_name, **kwargs)

    def create_app_config_provider(self):
        return self.app_config_provider

    def isolate_by_developer(self):
        return getpass.getuser() != 'root'

    @staticmethod
    def run_app(app, log_level='info', default_method=None, common_args_option=None):
        common_args_option_basic = {
            'args': ['env', 'developer_name'],
            'default_values': {
                'env': None,
                'developer_name': None,
            }
        }
        functocli.run_app(app, log_level, default_method, common_args_option, common_args_option_basic)


class MultiDeveloperDevOpsApp(DevOpsApp):

    def __init__(self, app_base_name, **kwargs):
        self.app_base_name = app_base_name
        self.kwargs = kwargs

        self.app_config_provider = MultiDeveloperDevOpsAppConfigProvider(self, self.app_base_name, self.kwargs)
        self.developer_name = self.app_config_provider.developer_name

        DevOpsApp.__init__(self, self.app_config_provider.app_name, **kwargs)

        self.shadow_id = self.app_config_provider.shadow_id
        self.sandbox_version = self.app_config_provider.sandbox_version

        if self.is_dev_or_test_env():
            self.do_init_for_dev(False)
        else:
            self._prepare_config_for_non_dev_or_test()

    def isolate_by_developer(self):
        return getpass.getuser() != 'root'

    def create_app_config_provider(self):
        return self.app_config_provider

    def is_dev_or_test_env(self):
        env = self.app_config_provider.get_env()
        return env == 'dev' or env == 'test'

    def _prepare_config_for_non_dev_or_test(self):
        data = utils.load_yaml(self.app_config_dir + '/env-config.yml')
        self.env_config = data[self.env]
        self.app_init_config_by_developer_name()
        self.app_do_init_for_deploy()

    @functocli.keep_method
    def do_init_for_dev(self, force=True):
        if self.sandbox_version:
            self.check_out_for_sandbox()
        self.app_config_provider.ensure_dir_and_write_permission()

        self.dev_env_config_file = self.app_persistent_storage_dir + '/dev-env-config.yml'
        if not os.path.isfile(self.dev_env_config_file) or self.shadow_id or force:
            config = self.app_build_env_config()
            utils.dump_yaml(self.dev_env_config_file, config)
            self.logger.info('generate dev env config: %s', self.dev_env_config_file)
            self.env_config = config
            self.app_init_config_by_developer_name()
            self.app_do_init_for_dev()
        else:
            self.env_config = utils.load_yaml(self.dev_env_config_file)
            self.app_init_config_by_developer_name()

    def check_out_for_sandbox(self):
        provider = self.app_config_provider
        try:
            file.rmtree(provider.sandbox_code_dir)
        except:
            pass
        file.ensure_dir(provider.sandbox_code_dir)
        cmd = "rsync -xa --no-links --delete --exclude='.git' --filter='dir-merge,- .gitignore' %s/ %s" % (provider.get_source_code_root_dir(), provider.sandbox_code_dir)
        self.shell_run(cmd)

    def app_init_config_by_developer_name(self):
        raise NotImplementedError("Please implement this method")

    def app_do_init_for_deploy(self):
        raise NotImplementedError("Please implement this method")

    def app_do_init_for_dev(self):
        raise NotImplementedError("Please implement this method")

    def app_build_env_config(self):
        raise NotImplementedError("Please implement this method")

    @staticmethod
    def run_app(app, log_level='info', default_method=None, common_args_option=None):
        common_args_option_basic = {
            'args': ['env', 'sandbox_version', 'developer_name'],
            'default_values': {
                'env': None,
                'sandbox_version': 0,
                'developer_name': None,
            }
        }
        functocli.run_app(app, log_level, default_method, common_args_option, common_args_option_basic)
