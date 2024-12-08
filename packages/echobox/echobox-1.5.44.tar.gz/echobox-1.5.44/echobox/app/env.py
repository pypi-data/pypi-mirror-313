from echobox.tool import cache
from echobox.tool import utils


class EnvTool(object):

    def __init__(self, app):
        self.app = app
        fn = self.app.root_dir + '/.box-config.yml'
        self.box_config = utils.load_yaml(fn, {})

    def docker_url_by_env(self, image_name):
        group_names = self.app.get_group_names()
        if 'nexus-genesis' in group_names:
            return image_name
        if 'firelighter-server' in group_names:
            return self.docker_genesis_url(image_name)
        else:
            return self.docker_url(image_name)

    def docker_url(self, image_name=''):
        return self.box_config.get('docker_url_pre', '') + image_name

    def docker_publish_url(self, image_name=''):
        return self.box_config.get('docker_publish_url_pre', '') + image_name

    def docker_genesis_url(self, image_name=''):
        return self.box_config.get('docker_genesis_url_pre', '') + image_name

    def setup_redis_for_cache(self):
        config = self.box_config[self.app.env]
        redis = config['redis']
        redis_url = 'redis://:%s@%s:%s' % (redis['auth'], redis['host'], redis['port'])
        cache.set_redis_url(redis_url)
