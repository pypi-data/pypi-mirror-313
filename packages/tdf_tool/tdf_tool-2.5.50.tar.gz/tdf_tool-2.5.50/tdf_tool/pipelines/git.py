from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.tools.cmd import Cmd
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ProjectType, ShellDir


class Git:
    """
    tl git【git 命令】：批量操作 git 命令, 例如 tl git push
    """

    def __init__(self, arg: list):
        self.__gitArg = ["git"] + arg
        self.__arg = arg

    def run(self):
        ShellDir.goInShellDir()
        self.__batch_run_git()

    def __batch_run_git(self):
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.title("开始操作壳：" + " ".join(self.__gitArg))
            Cmd.runAndPrint(self.__gitArg, shell=False)

            for module in InitialJsonConfig().moduleNameList:
                ShellDir.goInModuleDir(module)
                Print.title("开始操作" + module + "模块：" + " ".join(self.__gitArg))
                Cmd.runAndPrint(self.__gitArg, shell=False)
        elif projectType == ProjectType.IOS:
            ios_arg = ["bundle", "exec", "pod", "bin", "batch"] + self.__arg
            Cmd.runAndPrint(ios_arg, shell=False)
