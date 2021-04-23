from pathlib import Path

import yaml


def create_default_project(path: Path):
    dot_remote: Path = path / '.remote'
    if not dot_remote.exists():
        print(f"Creating {dot_remote}")
        dot_remote.mkdir()

    configs_file = dot_remote / 'configs.yaml'
    configs = {}
    server = {}
    if not configs_file.exists():
        print("Generating configurations")
        configs['name'] = input("Project name: ").strip()
        server['hostname'] = input("Hostname or public ip of the remote computer: ").strip()
        server['username'] = input("Username of the remote computer (ubuntu): ").strip()
        if server['username'] == '':
            server['username'] = 'ubuntu'
        # server['private_key'] = input("Path to the private key file:\n"
        #                               "(leave blank if you've setup authorized keys)\n").strip()
        if server['private_key'] == '':
            del server['private_key']

        configs['servers'] = {'default': server}
        with open(str(configs_file), 'w') as file_stream:
            file_stream.write(yaml.dump(configs,
                                        default_flow_style=False))

    exclude_file = dot_remote / 'exclude.txt'
    if not exclude_file.exists():
        print("Creating boilerplate exclude file")
        with open(str(exclude_file), 'w') as file_stream:
            file_stream.write('\n'.join([
                '.remote',
                '.git',
                '__pycache__',
                '.ipynb_checkpoints',
                'logs',
                '.DS_Store',
                '.*.swp',
                '*.egg-info/',
                '.idea'
            ]))

    print("We have created a standard configurations file and exclude list specifying files and"
          " folders that shouldn't be copied to server."
          " You can edit them at .remote/configs.yaml and .remote/exclude.txt")
