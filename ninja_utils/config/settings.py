import os
from multiprocessing import cpu_count

import yaml
from ..path import verify_make_dir


class Settings:
    def __init__(self, submodule: str, default_settings_factory, config_dir=os.path.join(os.path.expanduser('~'), '.ninja')):
        verify_make_dir(config_dir)

        default_settings_dict = default_settings_factory()
        yaml_dict = {}

        if os.path.exists(os.path.join(config_dir, 'SETTINGS.yaml')):
            with open(os.path.join(config_dir, 'SETTINGS.yaml')) as inf_handle:
                yaml_dict = yaml.load(inf_handle)
                if yaml_dict and submodule in yaml_dict:
                    sm_dict = yaml_dict[submodule]

                    if 'default_dir' in sm_dict:
                        self.default_dir = sm_dict['default_dir']
                    else:
                        self.default_dir = os.path.join(config_dir, submodule)

                    for key in sm_dict:
                        if key in default_settings_dict:
                            if 'dir' in key:
                                verify_make_dir(sm_dict[key])
                            default_settings_dict[key] = sm_dict[key]
                else:
                    self.default_dir = os.path.join(config_dir, submodule)

            # sometimes a path will still be in list form from default dir
            # make the paths that are
            for name in default_settings_dict:
                if 'dir' in name:
                    value = default_settings_dict[name]
                    if isinstance(value, list):
                        path = os.path.abspath(os.path.join(*[self.default_dir] + value))
                        verify_make_dir(path)
                        default_settings_dict[name] = path
        else:
            self.default_dir = os.path.join(config_dir, submodule)

            for name in default_settings_dict:
                if 'dir' in name:
                    path = os.path.abspath(os.path.join(*[self.default_dir] + default_settings_dict[name]))
                    verify_make_dir(path)
                    default_settings_dict[name] = path

        if 'N_jobs' not in default_settings_dict:
            default_settings_dict['N_jobs'] = cpu_count()

        self.N_jobs = default_settings_dict['N_jobs']

        if 'log' not in default_settings_dict:
            default_settings_dict['log'] = os.path.join(self.default_dir, submodule + '_log.txt')

        if 'log_persists' not in default_settings_dict:
            default_settings_dict['log_persists'] = False

        yaml_dict[submodule] = default_settings_dict

        with open(os.path.join(config_dir, 'SETTINGS.yaml'), 'w') as outf_handle:
            yaml.dump(yaml_dict, outf_handle)

        self.settings = default_settings_dict

    def get_path(self, name):
        return os.path.abspath(self.settings[name])
