from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
    BatchPodModel,
)
from tdf_tool.modules.translate.ios.tools.podspec import PodspecModel
from tdf_tool.modules.i18n.tools.ios_strings import iOSStrings
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.modules.i18n.tools.reflow_file import LanguageType, ReflowFile
from tdf_tool.tools.workspace import WorkSpaceTool, ProjectType
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable


class iOSI18nLint:
    """iOS国际化lint，检查出来是否有没有进行服务端国际化的key"""

    def start(self):
        """交互式lint国际化文件"""
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可执行国际化lint脚本：")
        Print.str(batchPodNames)
        while True:
            targetModule = input(
                "请输入需要执行国际化lint脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                ReflowFile.download_all_file()
                self.reflow_dict = ReflowFile.find_need_reflow_modules()
                for module in batchPodList:
                    self._lint_module(module)
                exit(0)
            else:
                targetModule = list(
                    filter(lambda x: x.name == targetModule, batchPodList)
                )[0]
                ReflowFile.download_all_file()
                self.reflow_dict = ReflowFile.find_need_reflow_modules()
                self._lint_module(targetModule)
                exit(0)

    def module(self, name: str):
        """指定 模块国际化lint

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
            ReflowFile.download_all_file()
            self.reflow_dict = ReflowFile.find_need_reflow_modules()
            Print.title(name + " 模块国际化lint开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            self._lint_module(pod)
            Print.title(name + " 模块国际化lint执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    def path(self, path: str):
        """指定 路径国际化lint

        Args:
            path (str): 指定路径
        """
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        podspec_path = FileUtil.get_all_file(path, [".podspec"])[0]
        podspec = PodspecModel(podspec_path)
        strings_path = (
            path + "/" + podspec.podspec_name + "/" + podspec.podspec_name + "_strings"
        )
        gitlab_ci_path = path + "/.gitlab-ci.yml"
        ReflowFile.download_all_file()
        self.reflow_dict = ReflowFile.find_need_reflow_modules()
        self._lint_path(podspec.podspec_name, strings_path, gitlab_ci_path)
        Print.title(path + " 路径国际化lint执行完成")

    def root(self):
        """远程源码分析，是否有组件没有回流成功"""
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        ReflowFile.download_all_file()
        self.reflow_dict = ReflowFile.find_need_reflow_modules()

    def _lint_module(self, pod: BatchPodModel):
        """指定 模块国际化lint

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
        gitlab_ci_path = EnvTool.workspace() + "/" + pod.path + "/.gitlab-ci.yml"
        self._lint_path(pod.name, strings_path, gitlab_ci_path)

    def _lint_path(self, pod_name: str, strings_path: str, gitlab_ci_path: str):
        """指定路径国际化

        Args:
            pod_name (str): pod的名称
            strings_path (str): pod的国际化文件存放路径
        """
        if TranslateEnable(gitlab_ci_path).no_translate:
            Print.warning(pod_name + " 模块没有开启国际化，继续下一个组件")
            return
        # 中文的完整的key
        zh_json_keys = iOSStrings.load_zh_strings_keys(
            pod_name, strings_path, LanguageType.ZH
        )
        # 服务端映射的 key
        server_json: dict[str:str] = iOSStrings.load_server_strings(
            pod_name, strings_path
        )
        # 检查模块是否有新的key没有生成映射关系
        self._lint_has_new_keys(zh_json_keys, server_json.keys())
        # 检查后台返回的key本地是否存在
        self._lint_has_contain_reflow_keys(
            pod_name, server_json.values(), self.reflow_dict
        )
        # 检查是否成功回流
        self._lint_has_reflow(pod_name, server_json, strings_path)
        Print.title(pod_name + "i8n lint通过")

    def _lint_has_reflow(self, pod_name: str, server_json: dict, strings_path: str):
        # 1、检查strings文件是否是最新
        module_reflow_dict = self.reflow_dict.get(pod_name)
        if module_reflow_dict is None:
            return
        self._lint_has_reflow_language(
            pod_name, strings_path, LanguageType.ZH, module_reflow_dict, server_json
        )
        self._lint_has_reflow_language(
            pod_name, strings_path, LanguageType.EN, module_reflow_dict, server_json
        )
        self._lint_has_reflow_language(
            pod_name, strings_path, LanguageType.CHT, module_reflow_dict, server_json
        )
        self._lint_has_reflow_language(
            pod_name, strings_path, LanguageType.TH, module_reflow_dict, server_json
        )

    def _lint_has_reflow_language(
        self,
        pod_name: str,
        strings_path: str,
        language: LanguageType,
        module_reflow_dict: dict,
        server_json: dict,
    ) -> dict:
        result_dict: dict = ReflowFile.lint_has_reflow_language(
            pod_name, strings_path, language, module_reflow_dict, server_json
        )
        if len(result_dict.keys()) > 0:
            result_strs = []
            for k, v in result_dict.items():
                result_strs.append(f"{k} => {v}")
            Print.warning(
                f"请执行回流脚本，ti reflow module pod_name，{pod_name}模块{language.ios_str()}.lproj 文件中以下需要更新："
            )
            Print.error("\n".join(result_strs))

    def _lint_has_contain_reflow_keys(
        self, pod_name: str, server_json: list[str], reflow_dict: dict
    ):
        module_relow_dict: dict = reflow_dict.get(pod_name)
        if module_relow_dict == None:
            return
        for _, value in module_relow_dict.items():
            for v in value:
                v = v[-3:]
                if v not in server_json:
                    Print.error(f"{v}不在{pod_name}里面")

    def _lint_has_new_keys(self, zh_json_keys: list[str], server_json_keys: list[str]):
        """检查模块是否有新的key没有生成映射关系"""
        if len(server_json_keys) <= 0:
            return
        # 找出是否有新的没有建立服务端映射关系的key
        new_keys = [i for i in zh_json_keys if i not in set(server_json_keys)]
        if len(new_keys) > 0:
            Print.error(
                "有以下字符串没有建立服务端映射关系，调用 tl i18n start 进行建立关系：{}".format(
                    new_keys
                )
            )
