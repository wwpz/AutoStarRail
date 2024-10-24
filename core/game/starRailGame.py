from core.log import Log
from typing import Optional
from utils.gameUtil import GameUtil


class StarRailGame(GameUtil):
    def __init__(self, game_path: str, game_type: str, window_name: str, window_class: Optional[str],
                 log: Optional[Log] = None) -> None:
        super().__init__(game_path, game_type, window_name, window_class, log)
