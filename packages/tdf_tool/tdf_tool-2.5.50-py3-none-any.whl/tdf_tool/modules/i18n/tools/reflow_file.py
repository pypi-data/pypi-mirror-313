import json
import os
import shutil
from tdf_tool.modules.i18n.tools.ios_strings import iOSStrings
from tdf_tool.modules.translate.tools.translate_tool import LanguageType
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.modules.i18n.tools.i18n_request import I18nRequest
from tdf_tool.modules.i18n.tools.serve_file import ServeFileTool
from tdf_tool.tools.workspace import WorkSpaceTool


class ReflowFile:
    _UNZIP_DIR = FileUtil.tdf_i18n_path() + "/files/"

    """回流文件相关操作的类"""

    def unzip_path(language: LanguageType) -> str:
        """国际化解压文件存放地址

        Args:
            language (LanguageType): 语言类型

        Returns:
            str: 存放地址
        """
        tdf_unzip_path = (
            ReflowFile._UNZIP_DIR
            + "/"
            + WorkSpaceTool.get_project_app().decs()
            + "/"
            + language.str()
        )

        if not os.path.exists(tdf_unzip_path):
            os.makedirs(tdf_unzip_path)
        return tdf_unzip_path

    def unzip_json_path(language: LanguageType) -> str:
        zip_path = ReflowFile.unzip_path(language)
        list = FileUtil.get_all_file(zip_path, [".json"])
        if len(list) > 0:
            return list[0]
        return None

    def download_zip_file(language: LanguageType):
        unzip_dir = ReflowFile.unzip_path(language)
        unzip_name = language.str() + ".zip"
        req = I18nRequest(
            host="https://boss-api.2dfire.com",
            file_name=unzip_name,
            unzip_dir=unzip_dir,
            lang_prefix=language,
        )
        req.start()

    def remove_all_zip_file():
        # 使用 shutil.rmtree() 删除文件夹及其所有内容
        unzip_dir = ReflowFile._UNZIP_DIR
        if os.path.exists(unzip_dir):
            shutil.rmtree(ReflowFile._UNZIP_DIR)

    def download_all_file():
        ReflowFile.remove_all_zip_file()
        ReflowFile.download_zip_file(LanguageType.EN)
        ReflowFile.download_zip_file(LanguageType.TH)
        ReflowFile.download_zip_file(LanguageType.CHT)
        ReflowFile.download_zip_file(LanguageType.ZH)

    def find_need_reflow_modules() -> dict:
        """查询需要回流的模块数据

        Returns:
            dict: 返回的数据结构 {"ModuleName": {"en_US": {}, "zh_CN": {},}
        """
        json_dict = ServeFileTool.server_key_desc_json()
        reqult_dict = {}
        reqult_dict = ReflowFile._find_need_reflow_keys(
            LanguageType.EN, json_dict, reqult_dict
        )
        reqult_dict = ReflowFile._find_need_reflow_keys(
            LanguageType.CHT, json_dict, reqult_dict
        )
        reqult_dict = ReflowFile._find_need_reflow_keys(
            LanguageType.ZH, json_dict, reqult_dict
        )
        reqult_dict = ReflowFile._find_need_reflow_keys(
            LanguageType.TH, json_dict, reqult_dict
        )
        return reqult_dict

    def _find_need_reflow_keys(
        language: LanguageType,
        serve_json_dict: dict,
        result_dict: dict,
    ) -> dict[str:str]:
        unzip_json = ReflowFile.unzip_json_path(language)
        if unzip_json == None:
            return result_dict
        json_dict = {}
        with open(unzip_json, "r") as f:
            json_data = f.read()
            json_dict: dict = json.loads(json_data)
            json_dict = json_dict[language.str()]
        for key, value in json_dict.items():
            real_key = key[-3:]
            module_name = serve_json_dict[real_key]["module_name"]
            if result_dict.get(module_name) == None:
                result_dict[module_name] = {language.str(): {}}
            if result_dict[module_name].get(language.str()) == None:
                result_dict[module_name][language.str()] = {}
            result_dict[module_name][language.str()][key] = value
        return result_dict

    def lint_has_reflow_language(
        pod_name: str,
        strings_path: str,
        language: LanguageType,
        module_reflow_dict: dict,
        server_json: dict,
    ) -> dict:
        """检查指定的.strings文件是否回流完成

        Args:
            pod_name (str): 模块名
            strings_path (str): .strngs文件路径
            language (LanguageType): 指定语言
            module_reflow_dict (dict): 模块的回流内容
            server_json (dict): 模块内服务端映射关系表

        Returns:
            dict: 需要更新的键值对
        """
        language_reflow_dcit = module_reflow_dict.get(language.str())
        if language_reflow_dcit is None:
            return {}
        language_strings_file = (
            f"{strings_path}/{language.ios_str()}.lproj/{pod_name}.strings"
        )
        strins_dict = iOSStrings.load(language_strings_file)
        result_dict = {}
        for k, v in strins_dict.items():
            server_code = server_json.get(k)
            if server_code is None:
                continue
            server_code = f"MULTI_MAI{server_code}"
            reflow_value = language_reflow_dcit.get(server_code)
            if reflow_value is None:
                continue
            if reflow_value != v:
                result_dict[v] = reflow_value
        return result_dict
