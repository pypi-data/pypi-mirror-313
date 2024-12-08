#!/usr/bin/env python

from echobox.app.env import EnvTool
from echobox.tool import functocli
from echobox.tool import template

opsbox_image = 'pipcli'


@functocli.keep_class
class PipCli(object):

    def __init__(self, app):
        self.app = app
        self.env_tool = EnvTool(app)
        self.opsbox_image = self.env_tool.docker_url(opsbox_image)
        self.opsbox_publish_image = self.env_tool.docker_publish_url(opsbox_image)

    def build_image(self):
        payload = {
            'opsbox_lib_version': self.app.get_global_params()['opsbox_lib_version'],
        }

        dst = self.app.app_runtime_storage_dir + '/opsbox-Dockerfile'
        self.app.template_to('opsbox-Dockerfile', dst, payload)

        cmd = 'cd %s; docker build -t %s -f %s .' % (self.app.app_runtime_storage_dir, self.opsbox_image, dst)
        self.app.shell_run(cmd)

    def push_image(self):
        self.shell_run('docker tag %s %s' % (self.opsbox_image, self.opsbox_publish_image))
        self.shell_run('docker push %s' % (self.opsbox_publish_image))

    def start_cli(self, args, cmd):
        cmd_data = {}
        cmd_data['image'] = self.opsbox_image
        cmd_data['args'] = args
        cmd_data['cmd'] = cmd
        cmd = template.render_str('docker run -d --restart always {{ args }} {{ image }} {{ cmd }}', cmd_data)
        self.app.shell_run(cmd)
