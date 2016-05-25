import os
from collections import defaultdict
from multiprocessing import cpu_count

import yaml
from ninja_shogun.utilities.path import verify_make_dir


class Settings:
    def __init__(self, default_settings_dict: dict, config_dir=os.path.join(os.path.expanduser('~'), '.ninja')):
        verify_make_dir(config_dir)

        if os.path.exists(os.path.join(config_dir, 'SETTINGS.yaml')):
            with open(os.path.join(config_dir, 'SETTINGS.yaml')) as inf_handle:
                j = yaml.load(inf_handle)
                for key in j.keys():
                    if key in default_settings_dict:
                        default_settings_dict[key] = j[key]
        else:
            with open(os.path.join(config_dir, 'SETTINGS.yaml'), 'w') as settings_handle:
                yaml.dump(default_settings_dict, settings_handle)

        self.config_dir = config_dir
        self.get_path = defaultdict(self.path_return)

        for outdir in [item for item in default_settings_dict.keys() if 'dir' in item]:
            verify_make_dir(default_settings_dict[outdir])
            self.get_path[outdir] = default_settings_dict[outdir]

        if 'N_jobs' not in default_settings_dict:
            default_settings_dict['N_jobs'] = cpu_count()

        self.N_jobs = default_settings_dict['N_jobs']

    def path_return(self, name: str):
        if 'dir' in name:
            name = name[name.find('_dir')]
        path = os.path.join(self.config_dir, name)
        verify_make_dir(path)
        return path
