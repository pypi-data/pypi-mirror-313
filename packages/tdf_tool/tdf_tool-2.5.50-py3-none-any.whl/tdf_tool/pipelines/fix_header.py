from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.tools.print import Print
from tdf_tool.modules.fix_header.fix_header_lint import FixHeaderLint
from tdf_tool.modules.fix_header.fix_header_entry import FixHeaderEntry, FixHeaderType


class FixHeader:
    """
    iOS修复头文件相关：tl fixHeader -h 查看详情
    """

    def __init__(self):
        self.lint = FixHeaderLint()
        self.__fix_entry = FixHeaderEntry(FixHeaderType.REPLACE)

    def start(self):
        """
        tl fixHeader start，会以交互式进行进行头文件修复
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持iOS")
        elif projectType == ProjectType.IOS:
            self.__fix_entry.start()

    def module(self, name: str):
        """
        tl fixHeader module【模块名】，修复指定模块名
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持iOS")
        elif projectType == ProjectType.IOS:
            self.__fix_entry.module(name)
