import os


class _Config:
    PASSWORD = os.getenv("YOUQU_PASSWORD") or "1"
    PYPI_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
    WORKDIR = os.path.abspath(".")
    SPECIAL_CLIENTS = {
        "autotest_deepin_installer": "uos@10.8.15.30",
    }


config = _Config()
