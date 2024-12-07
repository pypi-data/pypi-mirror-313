import os
import platform
import shutil
import stat
from tdf_tool.tools.print import Print


class FlutterScript(object):

    def __init__(self):
        self.isWindow = platform.system().lower() == "windows"
        self.osTargetCommand = ""
        if self.isWindow:
            self.osTargetCommand = "cd"
        else:
            self.osTargetCommand = "pwd"

    def readonly_handler(func, path, execinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def exec(self, interpreter: str, script_name: str, args: list[str]):
        os.system("git clone git@git.2dfire.net:app/flutter/tools/flutter-script.git")
        Print.stage(f"执行脚本: {interpreter} {script_name} {args}")
        args_str = " ".join(args)
        os.system(f"{interpreter} flutter-script/{script_name} {args_str}")
        if self.isWindow:
            path = os.popen(self.osTargetCommand).read().split("\n")[0]
            path = path + "\\flutter-script"
            shutil.rmtree(path, ignore_errors=False, onerror=self.readonly_handler)
        else:
            shutil.rmtree(r"flutter-script")
