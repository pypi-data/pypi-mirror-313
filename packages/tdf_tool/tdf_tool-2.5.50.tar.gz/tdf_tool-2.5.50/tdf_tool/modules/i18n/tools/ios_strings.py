import json
import os
from typing import Tuple
from tdf_tool.modules.translate.tools.translate_tool import LanguageType
from tdf_tool.tools.cmd import Cmd
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.tools.workspace import WorkSpaceTool


class iOSStrings:
    def load_server_strings(pod_name: str, strings_path: str) -> dict[str:str]:
        app = WorkSpaceTool.get_project_app()
        server_file_dir = strings_path + "/tdf_{}.lproj".format(app.decs())
        server_file_path = server_file_dir + "/" + pod_name + ".strings"
        server_json = iOSStrings.load(server_file_path)
        return server_json

    def load_zh_strings_keys(
        pod_name: str,
        strings_path: str,
        language: LanguageType,
    ) -> list[str]:
        zh_file_dir = f"{strings_path}/{language.ios_str()}.lproj"
        zh_file_list = FileUtil.get_all_file(zh_file_dir, [pod_name + ".strings"])
        if len(zh_file_list) == 0:
            Print.warning("模块没有国际化，继续下一个组件")
            return
        zh_file_path = zh_file_list[0]
        # 中文的完整的key
        zh_json_keys = iOSStrings.load_all_keys_and_useless_key(zh_file_path)[0]
        return zh_json_keys

    def load_all_keys(file_path: str) -> list[str]:
        """解析 .strins 文件内容，返回所有key

        Args:
            file_path (str): 文件路径

        Returns:
            list[str]: .strings的内容的所有 key
        """
        json_dict: dict[str:str] = iOSStrings.load(file_path)
        return json_dict.keys()

    def load_all_keys_and_useless_key(file_path: str) -> Tuple[list[str], list[str]]:
        """解析 .strins 文件内容，返回所有key, useless_key

        Args:
            file_path (str): 文件路径

        Returns:
            _type_: .strings的内容的所有 key, useless_key
        """
        key_results: list[str] = []
        useless_results: list[str] = []
        all_keys = iOSStrings.load_all_keys(file_path)
        for r in all_keys:
            if "%" in r:
                useless_results.append(r)
            else:
                key_results.append(r)
        return (key_results, useless_results)

    def load(file_path: str) -> dict[str:str]:
        """解析 .strins 文件内容

        Args:
            file_path (str): 文件路径

        Returns:
            _type_: .strings的内容
        """
        if os.path.exists(file_path):
            json_str = Cmd.run("plutil -convert json -o - " + file_path)
            json_dict = json.loads(json_str)
            return json_dict
        else:
            return {}
