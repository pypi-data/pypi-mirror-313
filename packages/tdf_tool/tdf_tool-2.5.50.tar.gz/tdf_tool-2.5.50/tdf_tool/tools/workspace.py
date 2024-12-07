from enum import Enum
from tdf_tool.tools.env import EnvTool
from tdf_tool.tools.print import Print
import os


class ProjectType(Enum):
    FLUTTER = 1
    IOS = 2


class ProjectApp(Enum):
    REST = 1
    YUNCRSH = 2
    SUPPLYCHAIN = 3

    def decs(self) -> str:
        if self.value == 2:
            return "yun"
        elif self.value == 3:
            return "chain"
        else:
            return "rest"


class WorkSpaceTool:
    def podfile_path() -> str:
        return EnvTool.workspace() + "/Podfile"

    def get_project_app() -> ProjectApp:
        """当前项目app归属

        Returns:
            ProjectApp: 项目app归属
        """
        app_name = EnvTool.workspace().split("/")[-1]
        if (
            app_name == "YunCash"
            or app_name == "flutter_yuncash_app"
            or app_name == "flutter_yuncash_module"
        ):
            return ProjectApp.YUNCRSH
        elif app_name == "TDFSupplyChainApp":
            return ProjectApp.SUPPLYCHAIN
        else:
            return ProjectApp.REST

    def get_project_type() -> ProjectType:
        """返回当前项目类型

        Returns:
            ProjectType: 项目类型
        """
        path = EnvTool.workspace()
        if os.path.exists(path + "/Podfile"):
            return ProjectType.IOS
        elif os.path.exists(path + "/pubspec.yaml"):
            return ProjectType.FLUTTER
        else:
            for name in os.listdir(path):
                if name.endswith(".podspec"):
                    return ProjectType.IOS
            return Print.error(path + "路径不是iOS、flutter工程路径")
