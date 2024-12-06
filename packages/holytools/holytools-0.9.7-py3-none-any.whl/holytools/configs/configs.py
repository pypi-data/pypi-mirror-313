import os.path
import subprocess
from typing import Optional

from holytools.configs.base import BaseConfigs, DictType
from holytools.logging import LogLevel

# ---------------------------------------------------------

class FileConfigs(BaseConfigs):
    def __init__(self, fpath : str = '~/.pyconfig'):
        self._config_fpath: str = self._as_abspath(path=fpath)
        config_dirpath = os.path.dirname(self._config_fpath)
        os.makedirs(config_dirpath, exist_ok=True)
        super().__init__()

    def _retrieve_map(self) -> dict:
        if not os.path.isfile(self._config_fpath):
            self.log(msg=f'File {self._config_fpath} could not be found, configs are empty', level=LogLevel.WARNING)
            return {}

        with open(self._config_fpath, 'r') as f:
            content = f.read()

        lines = content.split(f'\n')
        current_section = None
        category_dict = {current_section : {}}

        for num, line in enumerate(lines):
            parts = line.split(f' = ')

            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                category_dict[current_section] = {}
                continue
            if len(parts) == 2:
                key, value = parts
                if ' ' in key:
                    raise ValueError(f'Key must not contain whitespaces, got key \"{key}\" in line {num+1}')
                if ' ' in value:
                    raise ValueError(f'Value must not contain whitespaces, got value \"{value}\" in line {num+1}')
                category_dict[current_section][key] = value
                continue
            if not line:
                continue

            raise ValueError(f'Line {num+1} in config file is invalid: \"{line}\"')

        return category_dict

    def _update_resource(self, key : str, value: str, section : Optional[str] = None):
        _, __ , ___ = key, value, section

        general_dict = {k:v for k,v in self._map.items() if not isinstance(v, dict)}
        sub_dicts = {k:v for k,v in self._map.items() if isinstance(v, dict)}

        config_content = ''
        for k,v in general_dict.items():
            config_content += f'{k} = {v}\n'

        for k,v in sub_dicts.items():
            config_content += f'\n[{k}]\n'
            for subkey, subval in v.items():
                config_content += f'{subkey} = {subval}\n'

        with open(self._config_fpath, 'w') as f:
            f.write(config_content)


class PassConfigs(BaseConfigs):
    def __init__(self):
        pass_dirpath = os.environ['PASSWORD_STORE_DIR']
        pass_dirpath = self._as_abspath(path=pass_dirpath)
        print(f'Password store dir is : "{pass_dirpath}"')
        os.environ['PASSWORD_STORE_DIR'] = pass_dirpath
        self._pass_dirpath : str = pass_dirpath
        super().__init__()

    def _update_resource(self, key : str, value : str, section : Optional[str] = None):
        insert_command = f"echo \"{value}\" | pass insert --echo {key}"
        self.try_run_cmd(cmd=insert_command)

    def _retrieve_map(self) -> DictType:
        keys = self.get_toplevel_keys()
        config_map = {None : {}}
        for k in keys:
            config_map[None][k] = self.try_run_cmd(f'pass {k}')
        return config_map

    # ---------------------------------------------------------

    def try_run_cmd(self, cmd : str) -> Optional[str]:
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)
            return result.stdout.strip()
        except Exception as e:
            self.log(f"An error occurred during command execution, you configuration is likely not saved to pass:\n"
                     f'err = \"{e}\"\n', level=LogLevel.WARNING)
            result = None
        return result

    def get_toplevel_keys(self) -> list[str]:
        filenames = os.listdir(path=self._pass_dirpath)
        keys = [os.path.splitext(f)[0] for f in filenames if f.endswith('.gpg')]
        return keys


if __name__ == "__main__":
    configs = FileConfigs(fpath='/tmp/testconfigs.txt')
    pin_value = configs.get(key='pin')
    print(f'Pinvalue = {pin_value}')
