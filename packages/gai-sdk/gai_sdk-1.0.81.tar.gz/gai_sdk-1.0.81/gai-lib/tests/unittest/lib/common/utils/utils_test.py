from gai.lib.common.utils import get_app_path,get_gai_config,get_rc,get_packaged_gai_config_path
import os

def test_get_app_path():
    app_path=get_app_path()
    assert app_path==os.path.expanduser("~/.gai")

def test_get_rc():
    rc=get_rc()
    assert rc["app_dir"]=="~/.gai"

def test_get_gai_config():
    here = os.path.join(os.path.dirname(__file__),"..","..","..","..","..","..","gai","gai.yml")
    config = get_gai_config(here)
    assert config["clients"]["default"]["ttt"]=="gai-ttt"

def test_get_packaged_gai_config_path():
    config_path = get_packaged_gai_config_path()
    print(config_path)

