import argparse
import requests
import os
import json
import yaml
from cryptography.fernet import Fernet

from .util import execute_command


def add_api(parser):
    parser.add_argument("-k", "--key", help="f key", required=True)
    parser.add_argument("-a", "--api", help="api url")
    parser.add_argument("-n", "--name", help="name")
    parser.add_argument("-c", "--container", help="container")


def get_ubuntu_version():  
    with open("/etc/os-release") as f:
        for line in f:
            if line.startswith("VERSION_ID="):
                version = line.split("=")[1].strip().strip('"')
                return version
    return "22.04"


def create_dir_for_current_user(dir_path, sudo=False):
    command = f"mkdir -p {dir_path}"
    if sudo:
        command = "sudo " + command
    execute_command(command)
    command = f"chown $USER {dir_path}"
    if sudo:
        command = "sudo " + command
    execute_command(command)


def check_package_installed(package):
    command = f"dpkg -l | grep {package}"
    result = execute_command(command)
    if result is not None and package in result:
        return True
    return False


def install_main(args):

    to_install = []
    for package in args.packages.split():
        if check_package_installed(package):
            print(f"{package} is already installed")
            continue
        to_install.append(package)
    
    if len(to_install) == 0:
        print("All packages are already installed")
        return
    else:
        args.packages = " ".join(to_install)

    # generate install script
    if args.output_script is not None:
        script_writer = open(args.output_script, "w")
    else:
        script_writer = None
    
    # get ubuntu version
    ubuntu_version = get_ubuntu_version()

    # check if has root permission
    # if has root permission, run install script
    # else, print install script

    print("Get ubuntu version: ", ubuntu_version)
    command = f"wget https://packages.microsoft.com/config/ubuntu/{ubuntu_version}/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb"
    print("Install packages-microsoft-prod.deb")
    execute_command(command, script_writer)
    command = "dpkg -i /tmp/packages-microsoft-prod.deb"
    if args.sudo:
        command = "sudo " + command
    execute_command(command, script_writer)

    command = "apt-get update"
    if args.sudo:
        command = "sudo " + command
    execute_command(command, script_writer)

    print("Install packages: ", args.packages)

    command = f"apt-get install {args.packages} -y"
    if args.sudo:
        command = "sudo " + command
    execute_command(command, script_writer)


def mount_main(args):
    sas_token = get_token(args, info=True)

    template = {
        'logging': {'type': 'syslog', 'level': 'log_debug'}, 
        'components': ['libfuse', 'file_cache', 'attr_cache', 'azstorage'], 
        'libfuse': {'attribute-expiration-sec': 120, 'entry-expiration-sec': 120, 'negative-entry-expiration-sec': 240}, 
        'file_cache': {'path': '', 'timeout-sec': 120, 'max-size-mb': 40960}, 
        'attr_cache': {'timeout-sec': 7200}, 
        'azstorage': {
            'type': 'block', 
            'endpoint': '', 
            'account-name': '', 
            'mode': 'sas', 
            'sas': '', 
            'container': ''}, 
    }
    
    if args.template is not None:
        with open(args.template, 'r') as stream:
            try:
                template = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    
    template['file_cache']['path'] = args.buffer

    template['azstorage']['sas'] = sas_token
    template['azstorage']['endpoint'] = "https://%s.blob.core.windows.net" % args.name
    template['azstorage']['account-name'] = args.name
    template['azstorage']['container'] = args.container

    create_dir_for_current_user(args.buffer, sudo=args.sudo)
    create_dir_for_current_user(args.mount, sudo=args.sudo)

    # write config file into /tmp/config.yaml

    temp_config = "/tmp/config.yaml"
    with open(temp_config, 'w') as stream:
        yaml.dump(template, stream)

    command = f"blobfuse2 mount {args.mount} --config-file={temp_config}"
    execute_command(command)


def get_token(args, info=False):
    api_url = args.api

    f = Fernet(args.key.encode())

    an = f.encrypt(args.name.encode()).decode()
    cn = f.encrypt(args.container.encode()).decode()

    if info:
        print("Get token from: ", api_url)
        print("Name: ", an)
        print("Container: ", cn)

    params = {
        "an": an,
        "cn": cn, 
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        token = f.decrypt(data["sas"].encode()).decode()
        if token.startswith('"'):
            token = token[1:]
        if token.endswith('"'):
            token = token[:-1]
        if token.startswith("?"):
            return token
        else:
            return "?" + token
    else:
        return f"Error: {response.status_code}"


def main():
    # exmaple usage: addfblob install
    # exmaple usage: addfblob mount -k <key> -a <api> -b <buffer> -m <mount_dir>
    # exmaple usage: addfblob token -k <key> -a <api>
    parser = argparse.ArgumentParser(description="Addf's tool")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    install_parser = subparsers.add_parser('install', help='Install help')
    install_parser.add_argument("-o", "--output_script", help="output script", default=None)
    install_parser.add_argument("--packages", help="packages", default="fuse3 blobfuse2 azcopy")
    install_parser.add_argument("--sudo", help="sudo", action="store_true")

    mount_parser = subparsers.add_parser('mount', help='Mount help')
    add_api(mount_parser)
    mount_parser.add_argument("-b", "--buffer", help="buffer dir", required=True)
    mount_parser.add_argument("-m", "--mount", help="mount dir", required=True)
    mount_parser.add_argument("-t", "--template", help="yaml template file", default=None)
    mount_parser.add_argument("--sudo", help="sudo", action="store_true")

    token_parser = subparsers.add_parser('token', help='Token help')
    add_api(token_parser)

    args = parser.parse_args()

    # check current user, set --sudo if current user is not root
    if os.getuid() != 0:
        args.sudo = True

    if args.command == 'install':
        install_main(args)
    elif args.command == 'mount':
        mount_main(args)
    elif args.command == 'token':
        print(get_token(args, info=False))


if __name__ == "__main__":
    main()
