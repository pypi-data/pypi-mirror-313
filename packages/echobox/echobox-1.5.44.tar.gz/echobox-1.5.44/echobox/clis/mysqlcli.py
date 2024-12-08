from echobox.tool import functocli
from echobox.tool import file
from echobox.tool import dockerutil
from echobox.tool import template
from echobox.app.env import EnvTool

import sys

mysql_image = 'mysql:5.6'
busybox_image = 'busybox'


@functocli.keep_class
class MysqlCli(object):

    def __init__(self, app, mysql_config_dir, mysql_init_script_dir, mysql_data_dir, mysql_logs_dir, port=3306,
                 container_name='mysql', volumes=None):
        self.app = app
        self.mysql_config_dir = mysql_config_dir
        self.mysql_init_script_dir = mysql_init_script_dir
        self.mysql_data_dir = mysql_data_dir
        self.mysql_logs_dir = mysql_logs_dir
        self.port = port
        self.env_tool = EnvTool(self.app)
        self.mysql_image = self.env_tool.docker_url(mysql_image)
        self.busybox_image = self.env_tool.docker_url(busybox_image)
        self.mysql_container = container_name
        self.volumes = volumes

    def start_mysql(self):
        file.ensure_dir(self.mysql_data_dir)
        file.ensure_dir(self.mysql_logs_dir)
        ports = [
            str(self.port) + ':3306',
        ]

        volumes = {
            self.mysql_config_dir: '/etc/mysql/conf.d/',
            self.mysql_logs_dir: '/var/log/mysql',
            self.mysql_data_dir: '/var/lib/mysql',
        }
        if self.mysql_init_script_dir:
            volumes[self.mysql_init_script_dir] = '/docker-entrypoint-initdb.d'

        if self.volumes:
            volumes.update(self.volumes)

        envs = [
            'MYSQL_ROOT_PASSWORD=""',
            "MYSQL_ALLOW_EMPTY_PASSWORD=yes",
        ]

        args = dockerutil.base_docker_args(container_name=self.mysql_container, ports=ports, envs=envs, volumes=volumes)
        cmd_data = {'image': self.mysql_image, 'args': args}
        cmd = template.render_str('docker run -d --restart always {{ args }} {{ image }}', cmd_data)
        self.app.shell_run(cmd)
        self.wait_mysql()

    def wait_mysql(self):
        # cmd = 'while ! mysqladmin ping --silent; do sleep 1; done'
        cmd = 'while ! mysqladmin ping -h 127.0.0.1 --silent; do sleep 1; done'
        self.send_cmd_to_mysql_container(cmd)

    def send_cmd_to_mysql_container(self, cmd):
        cmd = 'docker exec %s %s bash -c \'%s\'' % (dockerutil.fg_mode(), self.mysql_container, cmd)
        self.app.shell_run(cmd)

    def exec_cmd_at_mysql_container(self, cmd):
        cmd = 'docker exec %s %s bash -c \'%s\'' % (dockerutil.fg_mode(), self.mysql_container, cmd)
        return self.app.run_cmd_ret(cmd)

    def to_mysql_env(self):
        cmd = 'bash'
        self.send_cmd_to_mysql_container(cmd)

    def to_mysql(self):
        cmd = 'mysql -A'
        self.send_cmd_to_mysql_container(cmd)

    def stop_mysql(self):
        self.app.stop_container(self.mysql_container)
        self.app.remove_container(self.mysql_container)

    def restart_mysql(self):
        self.stop_mysql()
        self.start_mysql()

    def rebuild_mysql(self):
        self.stop_mysql()
        cmd = 'rm -rf ' + self.mysql_data_dir
        self.sudo_for_storage(cmd)
        self.start_mysql()

    def sudo_for_storage(self, cmd):
        dir = '/opt/data'
        cmd = 'docker run --rm %s -v %s:%s %s sh -c "%s"' % (dockerutil.fg_mode(), dir, dir, busybox_image, cmd)
        self.app.shell_run(cmd)
