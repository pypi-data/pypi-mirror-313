import argparse
import os

from .util import execute_command


def init_vscode():
    to_install = [
        "github.copilot",
        "github.copilot-chat",
        "ms-python.debugpy",
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",
        "ms-toolsai.vscode-jupyter-cell-tags",
        "ms-toolsai.vscode-jupyter-slideshow",
    ]
    for ext in to_install:
        execute_command(f"code --install-extension {ext}")


def add_alias():
    # add to ~/.bashrc

    home_dir = os.path.expanduser("~")
    bashrc_path = os.path.join(home_dir, ".bashrc")

    # check if already added
    with open(bashrc_path) as f:
        for line in f:
            if line.startswith("# Addf's alias"):
                print("Already added")
                return

    to_add = [
        "alias pull='git pull origin'",
        "alias dupwd='du -h --max-depth=1 ./'",
    ]

    with open(bashrc_path, "a") as f:
        f.write("\n")
        f.write("# Addf's alias\n")
        for line in to_add:
            f.write(line + "\n")


def main():
    parser = argparse.ArgumentParser(description="Addf's tool")

    parser.add_argument('--init', default="", type=str, help="init")

    args = parser.parse_args()

    if args.init:
        to_do = args.init.strip()
        if to_do == 'vscode':
            init_vscode()
        elif to_do == 'git':
            execute_command('git config --global user.name "addf400"')
            execute_command('git config --global user.email "addf400@foxmail.com"')
        elif to_do == 'alias':
            add_alias()
        elif to_do == 'all':
            init_vscode()
            execute_command('git config --global user.name "addf400"')
            execute_command('git config --global user.email "addf400@foxmail.com"')
            add_alias()
        else:
            print("No such init option")


def pull():
    execute_command("git pull origin")


if __name__ == "__main__":
    main()
