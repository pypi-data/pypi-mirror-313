from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodModel,
    BatchPodTools,
)
from tdf_tool.modules.translate.ios.tools.ios_module import IosModule
from tdf_tool.modules.translate.ios.tools.ios_translate_integrate import (
    iOSTranslateIntegrate,
)


class iOSTranslate:

    # 交互式 国际化
    def translate(self):
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
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
                for module in batchPodList:
                    self.translate_module(module.name)
                exit(0)
            else:
                self.translate_module(targetModule)
                exit(0)

    # 指定 模块国际化
    def translate_module(self, name: str):
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块国际化脚本开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            self.__generate_translate(pod)
            Print.title(name + " 模块国际化执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    # 整合各个模块翻译文件到一起
    def integrate(self):

        self.integrate: iOSTranslateIntegrate = iOSTranslateIntegrate()
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可整合翻译文件：")
        Print.str(batchPodNames)

        while True:
            targetModule = input(
                "请输入需要执行整合的模块名(input ! 退出，all 所有模块执行)："
            )
            all_dict = self.integrate.integrate_json_root()
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                all_dict = self.integrate.integrate_json_root()
                for module in batchPodList:
                    module_dict = self.__integrate_module(module.name)
                    all_dict = self.integrate.merge_dict(module_dict, all_dict)
            else:
                module_dict = self.__integrate_module(targetModule)
                all_dict = self.integrate.merge_dict(module_dict, all_dict)
            self.integrate.write_dict_to_json(all_dict)
            self.integrate.upload_json()
            exit(0)

    # 指定 模块国际化
    def __integrate_module(self, name: str) -> dict[str, dict[str, str]]:
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块整合开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            Print.title(name + " 模块整合完成")
            return self.integrate.integrate_pod(pod)
        else:
            Print.error(name + " 模块不在开发列表中")

    # 翻译入口
    def __generate_translate(self, target: BatchPodModel):
        module = IosModule(target.path)
        # 检查 podsepc，修改 podsepc
        module.checkout_change_pod_spec()
        # 创建本地化相关 oc 类文件
        module.create_update_oc_files()
        # 检查并修改oc文件中未本地化的字符串
        module.change_location_string()
        # 生成本地化文件
        new_translate_dict = module.create_update_location_files()
        # 检查生成的 strings 文件格式是否正确
        module.check_strings_file()
        # 检查是否还有未本地化的字符串
        module.check_location_string()
        # 新增翻译到中心化json中，并上传到远程
        iOSTranslateIntegrate().new_dict_and_upload(new_translate_dict)
