from echobox.tool import system
from echobox.tool import template

SYSTEMD_FOLDER = '/etc/systemd/system'


def reinstall_systemd_service(service_name, template_path, payload=None, exit_on_error=True):
    service_fpath = _build_service_fpath(service_name=service_name)

    template_payload = {'payload': payload}
    template.render_to_file(template_path, template_payload, service_fpath)

    system.shell_run(f'chmod 664 {service_fpath}')

    restart_systemd_service(service_name=service_name, exit_on_error=exit_on_error)


def restart_systemd_service(service_name, exit_on_error=True):
    cmd_list = [
        'systemctl daemon-reload',
        f'systemctl enable {service_name}',
        f'systemctl restart {service_name}',
        f'systemctl status {service_name} --no-pager'
    ]
    system.shell_run(cmd_list, exit_on_error=exit_on_error)


def remove_systemd_service(service_name):
    cmd_list = [
        f'systemctl disable {service_name}',
        f'systemctl stop {service_name}',
        f'systemctl status {service_name} --no-pager',
        f'unlink {_build_service_fpath(service_name)}',
    ]
    system.shell_run(cmd_list)


def _build_service_fpath(service_name):
    return f'{SYSTEMD_FOLDER}/{service_name}.service'
