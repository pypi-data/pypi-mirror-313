import os
import json
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.translate_lint import FlutterTranslateLint
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable


class FlutterI18nLint:
    """flutter 后台下发国际化规范工具"""

    def start(self):
        """交互式 国际化"""
        businessModuleList = FlutterTranslateLint.businessModuleList()

        Print.str("检测到以下模块可执行国际化脚本：")
        Print.str(businessModuleList)
        while True:
            targetModule = input(
                "请输入需要执行国际化脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.module(module)
                exit(0)
            else:
                self.module(targetModule)
                exit(0)

    def module(self, name: str):
        """指定 模块国际化

        Args:
            name (str): 开发中的模块名
        """
        businessModuleList = FlutterTranslateLint.businessModuleList()
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self._deal_with(name)
            Print.title(name + " 模块国际化执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    def path(self, path: str):
        """指定路径国际化"""
        self._lint_path(path)

    def _deal_with(self, name: str):
        module_path = f"{EnvTool.workspace()}/../.tdf_flutter/{name}"
        self._lint_path(module_path)

    def _lint_path(self, path: str):
        """指定路径国际化

        Args:
            pod_name (str): pod的名称
            strings_path (str): pod的国际化文件存放路径
        """
        gitlab_ci_path = f"{path}/.gitlab-ci.yml"
        if not self._enable_i18n_lint(gitlab_ci_path):
            Print.warning(path + " 模块不支持国际化")
            exit(0)
        self._checkI18nCodeJson(path)

    def _enable_i18n_lint(self, gitlab_ci_path: str) -> bool:
        """判断是否开启国际化"""
        if TranslateEnable(gitlab_ci_path).no_translate:
            Print.warning("模块没有国际化，继续下一个组件")
            return False
        return True

    def _checkI18nCodeJson(self, path: str):
        """检查 i18n.json 文件是否缺少code"""
        Print.stage(f"{path}开始检查i18n.json文件是否缺少code")
        i18n_json_path = f"{path}/lib/tdf_intl/i18n.json"
        i18n_code_json_path = f"{path}/lib/tdf_intl/server_mapping_sources.json"
        if not os.path.exists(i18n_json_path):
            Print.error(i18n_json_path + " 文件不存在")
            exit(1)
        if not os.path.exists(i18n_code_json_path):
            Print.error(i18n_code_json_path + " 文件不存在")
            exit(1)
        i18n_json_dict = {}
        i18n_code_json_dict = {}
        with open(i18n_json_path, "r") as f:
            i18n_json_dict = json.load(f)
        with open(i18n_code_json_path, "r") as f:
            i18n_code_json_dict = json.load(f)

        # 获取每个字典的键集合
        i18n_json_keys = set(i18n_json_dict.keys())
        i18n_code_json_keys = set(i18n_code_json_dict.keys())

        # 找出i18n_json_keys中有而i18n_code_json_keys中没有的键
        missing_keys = i18n_json_keys - i18n_code_json_keys

        # 计算缺少的键的数量
        if len(missing_keys) > 0:
            Print.error(
                f"缺少multi_code的key(需要通过tl i18n start 生成)：{missing_keys}"
            )
