import os
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
    BatchPodModel,
)
from tdf_tool.modules.translate.ios.tools.podspec import PodspecModel
from tdf_tool.modules.i18n.tools.ios_strings import iOSStrings
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.modules.translate.ios.tools.location_string_temp import (
    LocationStringTempClass,
)
from tdf_tool.tools.print import Print
from tdf_tool.modules.i18n.tools.serve_file import ServeFileTool, ServerKeyDecs
from tdf_tool.tools.workspace import WorkSpaceTool
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable


class iOSI18n:
    """后台下发国际化规范工具，生成服务端与原生key的映射文件"""

    def start(self):
        """交互式 国际化"""
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可执行国际化脚本：")
        Print.str(batchPodNames)
        while True:
            targetModule = input(
                "请输入需要执行国际化脚本的模块名(input ! 退出，all 所有模块执行)："
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
        """指定 模块国际化

        Args:
            name (str): 开发中的模块名
        """
        batchPodList: list[BatchPodModel] = BatchPodTools.batchPodListFrom(
            WorkSpaceTool.podfile_path()
        )
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块国际化脚本开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            if self._enable_integrate(pod):
                ServeFileTool.pull_form_server()
                self._deal_with_module(pod)
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

    def _deal_with_module(self, pod: BatchPodModel):
        """处理指定模块

        Args:
            pod (BatchPodModel): 指定模块
        """
        self._write_server_key(pod)
        self._update_autoLocation_string_file(pod)

    def _write_server_key(self, pod: BatchPodModel):
        """写入服务端的 key 与本地 key 映射起来

        Args:
            pod (BatchPodModel): 指定模块
        """
        path = (
            EnvTool.workspace()
            + "/"
            + pod.path
            + "/"
            + pod.name
            + "/"
            + pod.name
            + "_strings"
        )
        # 获取中文简体的 key
        file_dir = path + "/zh-Hans.lproj"
        file_list = FileUtil.get_all_file(file_dir, [pod.name + ".strings"])
        if len(file_list) == 0:
            Print.warning("模块没有国际化，继续下一个组件")
            return
        file_path = file_list[0]
        all_results = iOSStrings.load_all_keys_and_useless_key(file_path)
        key_results: list[str] = all_results[0]
        useless_results: list[str] = all_results[1]
        # 获取服务端映射的 key
        app = WorkSpaceTool.get_project_app()
        new_file_dir = path + "/tdf_{}.lproj".format(app.decs())
        new_file_path = new_file_dir + "/" + pod.name + ".strings"
        old_keys: list[str] = []
        if os.path.exists(new_file_path):
            # 获取文件的当前权限
            file_mode = os.stat(new_file_path).st_mode
            # 将文件权限更改为可写
            os.chmod(new_file_path, file_mode | 0o200)
            old_keys = iOSStrings.load_all_keys(new_file_path)
        elif not os.path.exists(new_file_dir):
            os.mkdir(new_file_dir)
        # 新增加的 key
        new_keys = [i for i in key_results if i not in set(old_keys)]
        Print.stage("新增以下国际化：")
        Print.str(new_keys)
        with open(new_file_path, mode="a", encoding="utf-8") as f:
            server_index = ServeFileTool.read_key()
            desc_list: list[ServerKeyDecs] = []
            for key in new_keys:
                server_key: str = ServeFileTool.convert(server_index)
                decs = ServerKeyDecs(
                    key=server_key, module_name=pod.name, origin_key=key
                )
                desc_list.append(decs)
                server_index += 1
                f.write("\n")
                # 写入文件，转义符会消失掉，给替换下，比如：\n
                key = key.replace("\n", r"\n")
                f.write(f'"{key}" = "{server_key}";')
            f.close()
            # 更新文件
            ServeFileTool.update_key(server_index)
            ServeFileTool.update_decs(desc_list)
            ServeFileTool.update_useless(pod.name, useless_results)
        # 获取文件的当前权限
        file_mode = os.stat(new_file_path).st_mode
        # 将文件权限更改为只读
        os.chmod(new_file_path, file_mode & ~0o222)

    def _update_autoLocation_string_file(self, pod: BatchPodModel):
        """更新 TDFAutoLocationString 文件

        Args:
            pod (BatchPodModel): 指定更新的模块
        """
        pod_path = EnvTool.workspace() + "/" + pod.path
        podspec_path = pod_path + "/" + pod.name + ".podspec"
        podspec = PodspecModel(podspec_path)
        localization_path = pod_path + "/" + podspec.localization_path
        # 添加文件夹
        if not os.path.exists(localization_path):
            Print.warning("不存在文件夹：" + localization_path)
            return
        auto_string_class_m = (
            localization_path + "/" + podspec.auto_string_class_name + ".m"
        )
        with open(auto_string_class_m, mode="w", encoding="utf8") as f:
            class_m_txt = LocationStringTempClass.class_m
            class_m_txt = class_m_txt.replace(
                "TDFLocationStringTempClass", podspec.auto_string_class_name
            )
            class_m_txt = class_m_txt.replace(
                "TDFLocationStringTempBundle",
                podspec.podspec_resource_bundle_name,
            )
            class_m_txt = class_m_txt.replace(
                "TDFLocationStringTempTable", podspec.podspec_name
            )
            class_m_txt = class_m_txt.replace(
                "TDFLocationStringTempDefine", podspec.auto_string_define_str
            )
            f.write(class_m_txt)
            f.close()
