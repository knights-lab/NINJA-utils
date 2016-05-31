import os
import pickle

from ..logger import Logger
from ..config.settings import Settings


class Pickleable:
    def __init__(self, settings: Settings, logger: Logger):
        self.pickle_dir = settings.get_path('pickle_dir')
        self.dump = os.path.join(self.pickle_dir, "%s.pkl" % self.__class__.__name__)
        saved = os.path.isfile(self.dump)
        if not saved:
            self._parse()
            self.save()
        else:
            self.__dict__.update(self.load(settings, logger).__dict__)

    def _parse(self):
        pass

    def save(self):
        self_dump = os.path.join(self.pickle_dir, "%s.pkl" % self.__class__.__name__)
        with open(self_dump, 'wb') as handle:
            pickle.dump(self, handle)

    @classmethod
    def load(cls, settings: Settings, logger: Logger) -> object:
        pickle_dir = os.path.join(settings.get_path['pickle_dir'])
        try:
            self_dump = os.path.join(pickle_dir, "%s.pkl" % cls.__name__)
            with open(self_dump, 'rb') as handle:
                return pickle.load(handle)
        except FileNotFoundError as error:
            logger.log('Failed to open the %s.pkl' % cls.__name__)
            raise error
