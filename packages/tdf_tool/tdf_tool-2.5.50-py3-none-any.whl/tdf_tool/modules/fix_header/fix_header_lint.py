from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.tools.print import Print
from tdf_tool.modules.fix_header.fix_header_entry import FixHeaderEntry, FixHeaderType


class FixHeaderLint:
    """
    iOS修复头文件lint相关：tl fixHeader lint -h 查看详情
    """

    def __init__(self):
        self.__fix_entry = FixHeaderEntry(FixHeaderType.LINT)

    def start(self):
        """
        tl fixHeader lint start，会以交互式进行进行头文件lint
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持iOS")
        elif projectType == ProjectType.IOS:
            self.__fix_entry.start()

    def module(self, name: str):
        """
        tl fixHeader lint module【模块名】，lint 指定模块名
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持iOS")
        elif projectType == ProjectType.IOS:
            self.__fix_entry.module(name)

    def path(self, path: str):
        """
        tl fixHeader lint path【模块路径】，指定模块路径进行lint
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持iOS")
        elif projectType == ProjectType.IOS:
            self.__fix_entry.lint_path(path)
            exit(0)
