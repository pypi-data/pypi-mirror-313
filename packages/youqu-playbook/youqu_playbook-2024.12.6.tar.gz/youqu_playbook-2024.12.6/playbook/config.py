import os


class _Config:
    PASSWORD = os.getenv("YOUQU_PASSWORD") or "1"
    PLAYBOOK_JSON_PATH = "./playbook.json"
    PYPI_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
    WORKDIR = os.path.abspath(".")


config = _Config()
