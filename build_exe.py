# build_exe.py —— 几何AI教学系统 一键打包EXE
import PyInstaller.__main__
import os
import sys

def build():
    sys.argv = [
        "pyinstaller",
        "run_webui.py",
        "--name=几何AI动画教学系统",
        "--onefile",
        "--windowed",
        "--icon=app.ico",
        "--noconsole",
        "--clean",

        # 必须把项目文件夹全部打包进去
        "--add-data=app;app",
        "--add-data=prompt;prompt",
        "--add-data=.env;.",

        # 隐藏调试信息
        "--log-level=ERROR",
    ]
    PyInstaller.__main__.run()

if __name__ == "__main__":
    build()