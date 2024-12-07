from tdf_tool.modules.i18n.flutter.flutter_i18n import FlutterI18n
from tdf_tool.modules.i18n.ios.ios_i18n_integrate import iOSI18nIntegrate
from tdf_tool.modules.i18n.ios.ios_i18n import iOSI18n
from tdf_tool.modules.i18n.i18n_lint import i18nLint
from tdf_tool.tools.workspace import WorkSpaceTool, ProjectType


class I18n:
    """后台下发国际化规范工具"""

    def __init__(self):
        self.integrate = iOSI18nIntegrate()
        self.lint = i18nLint()
        # TODO: 回流没有数据，后面有数据了再测
        # self.reflow = iOSI18nReflow()

    def start(self):
        """交互式 国际化"""
        type = WorkSpaceTool.get_project_type()
        if type == ProjectType.IOS:
            iOSI18n().start()
        else:
            FlutterI18n().start()

    def module(self, name: str):
        """指定 模块国际化

        Args:
            name (str): 开发中的模块名
        """
        type = WorkSpaceTool.get_project_type()
        if type == ProjectType.IOS:
            iOSI18n().module(name)
        else:
            FlutterI18n().module(name)
