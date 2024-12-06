import pathlib

from syntax.path import home_resolve

CONFIG_PATH = home_resolve('.databrickscfg')


def logout():
    pathlib.Path(CONFIG_PATH).unlink(True)
