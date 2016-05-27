import os
from multiprocessing import cpu_count

import yaml
from ninja_trebuchet.path import verify_make_dir


class Settings:
    def __init__(self, submodule: str, default_settings_factory, config_dir=os.path.join(os.path.expanduser('~'), '.ninja')):
        verify_make_dir(config_dir)

        default_settings_dict = default_settings_factory()

        if os.path.exists(os.path.join(config_dir, 'SETTINGS.yaml')):
            with open(os.path.join(config_dir, 'SETTINGS.yaml')) as inf_handle:
                loaded_dict = yaml.load(inf_handle)
                if submodule in loaded_dict:
                    sm = loaded_dict[submodule]

                    if 'default_dir' in loaded_dict[submodule]:
                        self.default_dir = loaded_dict[submodule]['default_dir']
                    else:
                        self.default_dir = os.path.join(config_dir, submodule)

                    for key in default_settings_dict.keys():
                        if key in sm:
                            default_settings_dict[key] = sm[key]
                        else:
                            if 'dir' in key:
                                default_settings_dict[key] = os.path.join(*[self.default_dir] + default_settings_dict[key])
                else:
                    loaded_dict[submodule] = default_settings_dict
                    self.default_dir = os.path.join(config_dir, submodule)

        else:
            self.default_dir = os.path.join(config_dir, submodule)
            for name in default_settings_dict:
                if 'dir' in name:
                    path = os.path.join(*[self.default_dir] + default_settings_dict[name])
                    verify_make_dir(path)
                    default_settings_dict[name] = path
            loaded_dict = {submodule: default_settings_dict}

        self.settings = loaded_dict[submodule]

        if 'N_jobs' not in default_settings_dict:
            default_settings_dict['N_jobs'] = cpu_count()

        self.N_jobs = default_settings_dict['N_jobs']

        with open(os.path.join(config_dir, 'SETTINGS.yaml'), 'w') as outf_handle:
            yaml.dump(loaded_dict, outf_handle)
