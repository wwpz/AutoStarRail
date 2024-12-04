from config.config import Config
# from pylnk3 import Lnk


VERSION_PATH = "./res/config/version.txt"
EXAMPLE_PATH = "./res/config/config.example.yaml"
CONFIG_PATH = "./config.yaml"

cfg = Config(VERSION_PATH, EXAMPLE_PATH, CONFIG_PATH)

# cfg.env = os.environ.copy()
# cfg.env['PATH'] = os.path.dirname(cfg.python_exe_path) + ';' + cfg.env['PATH']
# cfg.useragent = {"User-Agent": f"March7thAssistant/{cfg.version}"}

# if cfg.auto_set_game_path_enable:
#     detect_game_path()