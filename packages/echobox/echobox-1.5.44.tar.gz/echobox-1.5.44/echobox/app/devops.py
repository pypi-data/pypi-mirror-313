import os
import socket
import sys
from os import path

from echobox.app.appconfig import appconfig
from echobox.tool import array
from echobox.tool import file
from echobox.tool import functocli
from echobox.tool import logger
from echobox.tool import system
from echobox.tool import template
from echobox.tool import utils
from echobox.tool import spec
from echobox.tool import systemd

import __main__ as main


class DevOpsAppConfig:

    def __init__(self, app_name, provider):
        appconfig.init(app_name, provider.get_env(), provider.get_app_config())


class DevOpsAppConfigProvider:

    def __init__(self, app_name):
        self.app_name = app_name
        self.app_storage_dir = '/opt/data/' + app_name
        self.app_persistent_storage_dir = self.app_storage_dir + '/persistent'
        self.app_runtime_storage_dir = self.app_storage_dir + '/runtime'
        self.app_logs_dir = self.app_runtime_storage_dir + '/logs'

    def get_root_dir(self):
        if hasattr(main, '__file__'):
            root_dir = path.dirname(path.realpath(sys.argv[0]))
            return root_dir
        else:
            root_dir = os.getcwd()
            return root_dir

    def get_roles_dir(self):
        return self.get_root_dir() + '/roles'

    def get_app_root_dir(self):
        app_root_dir = self.get_roles_dir() + '/' + self.app_name
        return app_root_dir

    def get_env(self):
        env = os.environ['PUPPY_ENV'] if 'PUPPY_ENV' in os.environ else 'dev'
        return env

    def get_app_config(self):
        return {}

    def get_box_local_config(self):
        fn = self.get_root_dir() + '/.box-local-config.yml'
        return utils.load_yaml(fn, {})

    def ensure_dir_and_write_permission(self):
        file.ensure_dir(self.app_storage_dir)
        file.ensure_dir(self.app_persistent_storage_dir)
        file.ensure_dir(self.app_runtime_storage_dir)
        file.ensure_dir(self.app_logs_dir)
        file.ensure_dir(self.app_logs_dir + '/syslog')


class DevOpsApp(object):

    def _want_logger_ex(self, **kwargs):
        logger.make_logger_for_app(self, **kwargs)
        logger_name = kwargs.get('log_config', {}).get('name', self.app_name)
        return logger.getLogger(logger_name)

    def __init__(self, app_name, log_level='info', exit_on_error=True, **kwargs):
        self.app_name = app_name

        self._init_app_config()

        self.log_level = log_level
        self.exit_on_error = exit_on_error
        self.logger = self._want_logger_ex(**kwargs)

        self.file_lock = None
        self._hostvar = None

    def _init_app_config(self):

        provider = self.create_app_config_provider()
        provider.ensure_dir_and_write_permission()

        hostname = socket.gethostname()
        self.hostname_fqdn = hostname
        self.hostname_short = hostname.split('.', 1)[0]

        self.env = provider.get_env()
        self.root_dir = provider.get_root_dir()
        self.roles_dir = provider.get_roles_dir()

        app_root_dir = provider.get_app_root_dir()
        self.app_root_dir = app_root_dir
        self.app_config_dir = app_root_dir + '/config'
        self.app_templates_dir = app_root_dir + '/templates'
        self.app_scripts_dir = app_root_dir + '/scripts'

        self.app_storage_dir = provider.app_storage_dir
        self.app_persistent_storage_dir = provider.app_persistent_storage_dir
        self.app_runtime_storage_dir = provider.app_runtime_storage_dir
        self.app_logs_dir = provider.app_logs_dir


    def create_app_config_provider(self):
        return DevOpsAppConfigProvider(self.app_name)

    def run_cmd_ret(self, cmd, log=True):
        if log:
            self.logger.info('run_cmd_ret: %s', cmd)
        return system.run_cmd_ret(cmd)

    def run_cmd(self, cmd, log=True):
        if log:
            self.logger.info('run_cmd: %s', cmd)
        return system.run_cmd(cmd)

    def shell_run(self, cmd, keep_pipeline=True, exit_on_error=True, dry_run=False):
        self.logger.info('shell_run: %s', cmd)
        if dry_run:
            return 0
        exit_on_error = exit_on_error and self.exit_on_error
        return system.shell_run(cmd, keep_pipeline=keep_pipeline, exit_on_error=exit_on_error)

    def remove_container(self, name, force=False, dry_run=False):
        cmd = 'docker rm %s' % (name)
        if force:
            cmd = 'docker rm -f %s' % (name)
        self.shell_run(cmd, exit_on_error=False, dry_run=dry_run)

    def container_is_running(self, name):
        cmd = 'docker ps | grep %s' % (name)
        return self.run_cmd(cmd, log=False)[0] == 0

    def stop_container(self, name, timeout=300, dry_run=False):
        cmd = 'docker stop --time %d %s' % (timeout, name)
        self.shell_run(cmd, exit_on_error=False, dry_run=dry_run)

    def _check_lock(self):
        filepath = self.app_runtime_storage_dir + '/locks/' + file.compute_lock_filepath(sys.argv)
        file_lock = file.obtain_lock(filepath)
        if file_lock is None:
            pid = 0
            with open(filepath, 'r', encoding='utf-8') as f:
                pid = f.read()
            self.logger.warning('lock file exists, pid: %s => %s', pid, filepath)
            sys.exit(1)
        else:
            self.file_lock = file_lock

    def template_to(self, template_filename, dst, payload, app_name=None):
        template_payload = {'payload': payload}
        src = self.app_templates_dir_for(app_name) + '/' + template_filename
        template.render_to_file(src, template_payload, dst)
        self.logger.info('template_to: %s => %s', src, dst)

    def read_app_config(self, config_filebasename, app_name=None):
        if '.yml' not in config_filebasename:
            config_filebasename = config_filebasename + '.yml'
        data = utils.load_yaml('%s/%s' % (self.app_config_dir_for(app_name), config_filebasename), {})
        return data

    def app_templates_dir_for(self, app_name=None):
        if app_name is None:
            return self.app_templates_dir
        return '%s/%s/templates' % (self.roles_dir, app_name)

    def app_config_dir_for(self, app_name=None):
        if app_name is None:
            return self.app_config_dir
        return '%s/%s/config' % (self.roles_dir, app_name)

    def get_group_names(self):
        return self.get_host_var().get('group_names', [])

    def get_configed_ops_scripts_dir(self):
        return self.get_host_var().get('ops_scripts_dir', '')

    def _read_hosts_var(self):
        fn = self.app_config_dir + '/hosts-var.yml'
        hosts_var = utils.load_yaml(fn, {})
        hostname = self.hostname_short
        return spec.LegacySpec(hosts_var, hostname).config_data

    def get_host_var(self):
        if self._hostvar is None:
            fn = '/etc/puppy-ansible-hostvar.json'
            ansible_kv_config = utils.load_json(fn, {})

            fn = '/etc/puppy-cloud-init-raw-data.json'
            cloud_init_raw_data = utils.load_json(fn, {})
            '''
            #### Always respect global_params / app_params from ansible
            1. Create an ECS by cloud-init, global_params from ansible, app_params from cloud-init config.
               We can not read app_params from ansible when we are using cloud-init to deloy,
               so we truncate `/etc/puppy-ansible-hostvar.json` when lauch an ECS.
               The global_params and app_params will be the value we desire.
            2. If we deploy by ansible, ansible_kv_config will overwrite cloud_init_raw_data,
               so global_params and app_params both will be the latest. So they are the value we desire too.
            '''
            hostvar = array.merge(cloud_init_raw_data, ansible_kv_config)
            hostvar = array.merge(hostvar, self._read_hosts_var())
            self._hostvar = hostvar
        return self._hostvar

    def get_app_params(self, key=None, fallback=None):
        app_params = self.get_host_var().get('app_params', {})
        if key is None:
            return app_params
        return app_params.get(key, fallback)

    def get_global_params(self, key=None, fallback=None):
        global_params = self.get_host_var().get('global_params', {})
        if key is None:
            return global_params
        return global_params.get(key, fallback)

    def reinstall_systemd_service(self, service_name, template_fname=None, payload=None):
        if template_fname is None:
            template_fname = service_name
        template_path = f'{self.app_templates_dir_for()}/{template_fname}.service'
        systemd.reinstall_systemd_service(service_name=service_name, template_path=template_path, payload=payload)
        self.logger.info('reinstall_systemd_service: %s => %s', template_path, service_name)

    @functocli.keep_method
    def check_health(self):
        print('%s is good' % (sys.argv[0]))
