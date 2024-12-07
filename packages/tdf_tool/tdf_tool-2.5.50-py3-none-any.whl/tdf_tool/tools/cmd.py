import subprocess
import os
import sys
from tdf_tool.tools.print import Print


class Cmd:
    def run(args, shell=True):
        Print.title("{0}".format(args))
        subprocess_result = subprocess.Popen(
            args, shell=shell, stdout=subprocess.PIPE)
        subprocess_return = subprocess_result.stdout.read()
        result = subprocess_return.decode("utf-8")
        if subprocess_result.returncode != 0: # 如果命令执行不成功，则先输出日志，并退出
            Print.str(result)
            # sys.exit(subprocess_result.returncode)
        return result

    def runAndPrint(args, shell=True) -> str:
        result = Cmd.run(args, shell=shell)
        Print.str(result)
        return result

    def system(cmd) -> int:
        Print.step("exec：" + cmd)
        return os.system(cmd)
