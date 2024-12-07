from youqu3 import setting


def pip_install_cmd(pkg_name: str):
    cmd = f'pip3 install -U {pkg_name} -i {setting.PYPI_MIRROR}'
    return f"{cmd} || {cmd} --break-system-packages"
