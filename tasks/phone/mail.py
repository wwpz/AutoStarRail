import time

from automation import auto
from ..template import Template


class Mail(Template):
    def run(self):
        print("Mail")
        time.sleep(3)
        print("完成")