import subprocess


def execute_command(command, to_file=None):
    if to_file is not None:
        to_file.write(command + "\n")
        return None
    else:
        print("Execute command: ", command)
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        print("Result: ", result)
        return result
