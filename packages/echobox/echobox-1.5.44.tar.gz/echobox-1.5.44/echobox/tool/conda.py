from echobox.tool import system


def get_python_executable_path(conda_env='base'):
    return system.run_cmd_ret(f'conda run -n {conda_env} python -c "import sys; print(sys.executable)"').strip()
