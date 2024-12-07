from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.modules.translate.flutter.flutter_translate_tools import (
    FlutterTranslateTools,
)
from tdf_tool.modules.translate.ios.ios_translate import iOSTranslate
from tdf_tool.modules.translate.translate_lint import TranslateLint


class Translate:
    """
    国际化相关：tl translate -h 查看详情
    """

    def __init__(self) -> None:
        self.lint = TranslateLint()

    def start(self, all_module=False, always_yes=False):
        """
        国际化相关：通过交互式的方式处理国际化
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().translate(all_module, always_yes)
        elif projectType == ProjectType.IOS:
            iOSTranslate().translate()

    def module(self, name, always_yes=False):
        """
        国际化相关：指定模块进行国际化
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().translate_module(name, always_yes)
        elif projectType == ProjectType.IOS:
            iOSTranslate().translate_module(name)
        exit(0)

    def integrate(self):
        """
        国际化相关：整合所有组件的国际化文件到一个文件中，用来维护一份国际化文件
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().integrate()
        elif projectType == ProjectType.IOS:
            iOSTranslate().integrate()
        exit(0)

    def clearI18nFiles(self):
        """
        国际化相关：删除国际化相关的文件夹
        """
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterTranslateTools().clear_i18n_files()
        elif projectType == ProjectType.IOS:
            pass
        exit(0)
