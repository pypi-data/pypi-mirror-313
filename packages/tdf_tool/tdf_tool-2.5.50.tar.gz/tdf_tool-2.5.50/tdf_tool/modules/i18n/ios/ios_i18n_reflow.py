from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
    BatchPodModel,
)
from tdf_tool.modules.i18n.tools.ios_strings import iOSStrings
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.modules.i18n.tools.reflow_file import LanguageType, ReflowFile
from tdf_tool.tools.workspace import WorkSpaceTool, ProjectType


class iOSI18nReflow:
    """iOS服务端翻译回流脚本"""

    def start(self):
        """交互式回流国际化模块"""
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可执行国际化回流脚本：")
        Print.str(batchPodNames)
        while True:
            targetModule = input(
                "请输入需要执行国际化回流脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                ReflowFile.download_all_file()
                self.reflow_dict = ReflowFile.find_need_reflow_modules()
                for module in batchPodList:
                    self._reflow_module(module)
                exit(0)
            else:
                targetModule = list(
                    filter(lambda x: x.name == targetModule, batchPodList)
                )[0]
                ReflowFile.download_all_file()
                self.reflow_dict = ReflowFile.find_need_reflow_modules()
                self._reflow_module(targetModule)
                exit(0)

    def module(self, name: str):
        """指定 模块国际化回流

        Args:
            name (str): 开发中的模块名
        """
        if WorkSpaceTool.get_project_type() == ProjectType.FLUTTER:
            Print.error("不支持flutter")
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodList(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块国际化回流脚本开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            ReflowFile.download_all_file()
            self.reflow_dict = ReflowFile.find_need_reflow_modules()
            self._reflow_module(pod)
            Print.title(name + " 模块国际化回流执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    def _reflow_module(self, pod: BatchPodModel):
        """回流指定模块

        Args:
            pod (BatchPodModel): 指定模块
        """
        strings_path = f"{EnvTool.workspace()}/{pod.path}/{pod.name}/{pod.name}_strings"
        module_reflow_dict = self.reflow_dict.get(pod.name)
        # 服务端映射的 key
        server_json = iOSStrings.load_server_strings(pod.name, strings_path)
        # 更新各个.strings语言文件
        cn_need_reflow_dict = self._reflow_language(
            pod.name, strings_path, LanguageType.ZH, module_reflow_dict, server_json
        )
        self._reflow_language(
            pod.name,
            strings_path,
            LanguageType.TH,
            module_reflow_dict,
            server_json,
            cn_need_reflow_dict,
        )
        self._reflow_language(
            pod.name,
            strings_path,
            LanguageType.EN,
            module_reflow_dict,
            server_json,
            cn_need_reflow_dict,
        )
        self._reflow_language(
            pod.name,
            strings_path,
            LanguageType.CHT,
            module_reflow_dict,
            server_json,
            cn_need_reflow_dict,
        )
        # 更新服务端映射.strings文件
        self._reflow_tdf_language(pod.name, strings_path, cn_need_reflow_dict)
        # 更新代码
        self._relow_source_code(pod.name, strings_path, cn_need_reflow_dict)

    def _reflow_language(
        self,
        pod_name: str,
        strings_path: str,
        language: LanguageType,
        module_reflow_dict: dict,
        server_json: dict,
        cn_need_reflow_dict: dict = {},
    ) -> dict:
        need_reflow_dict = ReflowFile.lint_has_reflow_language(
            pod_name, strings_path, language, module_reflow_dict, server_json
        )
        if language == LanguageType.ZH:
            cn_need_reflow_dict = need_reflow_dict
        if len(need_reflow_dict.keys()) == 0 and len(cn_need_reflow_dict.keys()) == 0:
            return {}
        language_strings_file = (
            f"{strings_path}/{language.ios_str()}.lproj/{pod_name}.strings"
        )
        file_content = ""
        with open(language_strings_file, mode="r", encoding="utf-8") as file:
            file_content = file.read()
            file.close()
        with open(language_strings_file, mode="w", encoding="utf-8") as file:
            # 替换更新的value
            for k, v in need_reflow_dict.items():
                file_content = file_content.replace(f'"{k}"', f'"{v}"')
            # 替换更新的key
            if not cn_need_reflow_dict is None:
                for k, v in cn_need_reflow_dict.items():
                    file_content = file_content.replace(f'"{k}"', f'"{v}"')
            file.write(file_content)
            file.close()
        return need_reflow_dict

    def _reflow_tdf_language(
        self, pod_name: str, strings_path: str, need_reflow_dict: dict
    ):
        if len(need_reflow_dict.keys()) == 0:
            return
        app = WorkSpaceTool.get_project_app()
        language_strings_file = (
            f"{strings_path}/tdf_{app.decs()}.lproj/{pod_name}.strings"
        )
        file_content = ""
        with open(language_strings_file, mode="r", encoding="utf-8") as file:
            file_content = file.read()
            file.close()
        with open(language_strings_file, mode="w", encoding="utf-8") as file:
            # 替换更新的value
            for k, v in need_reflow_dict.items():
                file_content = file_content.replace(f'"{k}"', f'"{v}"')
            file.write(file_content)
            file.close()

    def _relow_source_code(
        self, pod_name: str, strings_path: str, need_reflow_dict: dict
    ):
        source_code_dir = strings_path.split(f"/{pod_name}_strings")[0]
        files = FileUtil.get_all_file(source_code_dir, [".m"])
        for file in files:
            file_content = ""
            with open(file, mode="r", encoding="utf-8") as f:
                file_content = f.read()
                f.close()
            with open(file, mode="w", encoding="utf-8") as f:
                for k, v in need_reflow_dict.items():
                    raw_str = f'{pod_name}LocalizedString(@"{k}"'
                    if raw_str in file_content:
                        replace_str = f'{pod_name}LocalizedString(@"{v}"'
                        file_content = file_content.replace(raw_str, replace_str)
                f.write(file_content)
                f.close()
