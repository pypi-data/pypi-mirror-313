from echobox.tool import functocli
from echobox.tool import dockerutil
from echobox.tool import template
from echobox.app.env import EnvTool

redis_image = 'redis:3.0.1'


@functocli.keep_class
class RedisCli(object):

    def __init__(self, app, redis_config, port=6379, container_name='redis', data_dir=None):
        self.app = app
        self.redis_config = redis_config
        self.port = port
        self.redis_container = container_name
        self.data_dir = data_dir

    def _image_name(self):
        return EnvTool(self.app).docker_url() + redis_image

    def start_redis(self):
        config_in_container = '/usr/local/etc/redis/redis.conf'
        ports = [
            str(self.port) + ':6379',
        ]

        volumes = {
            self.redis_config: config_in_container,
        }

        if self.data_dir:
            volumes[self.data_dir] = '/data'

        args = dockerutil.base_docker_args(container_name=self.redis_container, ports=ports, volumes=volumes)
        cmd_data = {'image': self._image_name(), 'args': args, 'redis_config': config_in_container}
        cmd = template.render_str(
            'docker run -d --restart always {{ args }} {{ image }} redis-server {{ redis_config }}', cmd_data)
        self.app.shell_run(cmd)

    def send_cmd_to_redis_container(self, cmd):
        cmd = 'docker exec %s %s bash -c \'%s\'' % (dockerutil.fg_mode(), self.redis_container, cmd)
        self.app.shell_run(cmd)

    def to_redis(self):
        cmd = 'redis-cli'
        self.send_cmd_to_redis_container(cmd)

    def to_redis_cli(self):
        cmd = 'bash'
        self.send_cmd_to_redis_container(cmd)

    def stop_redis(self):
        self.app.stop_container(self.redis_container)
        self.app.remove_container(self.redis_container)

    def restart_redis(self):
        self.stop_redis()
        self.start_redis()
