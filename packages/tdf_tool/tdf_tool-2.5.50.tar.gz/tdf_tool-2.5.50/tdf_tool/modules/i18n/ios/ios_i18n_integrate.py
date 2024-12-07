import os
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
    BatchPodModel,
)
from tdf_tool.modules.i18n.tools.ios_strings import iOSStrings
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.modules.i18n.tools.serve_file import ServeFileTool, ServerKeyDecs
from tdf_tool.tools.workspace import WorkSpaceTool, ProjectType
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable


class iOSI18nIntegrate:
    """整合国际化文件, 将没有同步到远端的键值对同步到远端"""

    def start(self):
        """交互式整合国际化文件"""
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可执行国际化整合脚本：")
        Print.str(batchPodNames)
        while True:
            targetModule = input(
                "请输入需要执行国际化整合脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                ServeFileTool.pull_form_server()
                for module in batchPodList:
                    self.module(module.name)
                ServeFileTool.upload_to_server()
                exit(0)
            else:
                ServeFileTool.pull_form_server()
                self.module(targetModule)
                ServeFileTool.upload_to_server()
                exit(0)

    def module(self, name: str):
        """指定 模块国际化整合

        Args:
            name (str): 开发中的模块名
        """
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块国际化脚本开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            if self._enable_integrate(pod):
                ServeFileTool.pull_form_server()
                self._integrate_module(pod)
                ServeFileTool.upload_to_server()
                Print.title(name + " 模块国际化执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    def _enable_integrate(self, pod: BatchPodModel) -> bool:
        """判断是否开启国际化整合"""
        gitlab_ci_path = EnvTool.workspace() + "/" + pod.path + "/.gitlab-ci.yml"
        if TranslateEnable(gitlab_ci_path).no_translate:
            Print.warning("模块没有国际化，继续下一个组件")
            return False
        return True

    def _integrate_module(self, pod: BatchPodModel):
        """指定 模块国际化整合

        Args:
            pod (BatchPodModel): 指定模块
        """
        strings_path = (
            EnvTool.workspace()
            + "/"
            + pod.path
            + "/"
            + pod.name
            + "/"
            + pod.name
            + "_strings"
        )
        # 获取中文简体带转义符的 key
        file_dir = strings_path + "/zh-Hans.lproj"
        file_list = FileUtil.get_all_file(file_dir, [pod.name + ".strings"])
        if len(file_list) == 0:
            Print.warning("模块没有国际化，继续下一个组件")
            return
        file_path = file_list[0]
        all_results = iOSStrings.load_all_keys_and_useless_key(file_path)
        useless_results: list[str] = all_results[1]
        ServeFileTool.update_useless(pod.name, useless_results)
        # 获取服务端映射的 key
        app = WorkSpaceTool.get_project_app()
        file_dir = strings_path + "/tdf_{}.lproj".format(app.decs())
        file_path = file_dir + "/" + pod.name + ".strings"
        if not os.path.exists(file_path):
            return
        desc_list: list[ServerKeyDecs] = []
        json_dict: dict[str:str] = iOSStrings.load(file_path)
        for k, v in json_dict.items():
            desc = ServerKeyDecs(v, pod.name, k)
            desc_list.append(desc)
        ServeFileTool.update_decs(desc_list)
