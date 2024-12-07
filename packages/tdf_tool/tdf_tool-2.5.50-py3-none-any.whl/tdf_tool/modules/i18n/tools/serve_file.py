import json
import os
from tdf_tool.tools.cmd import Cmd
from tdf_tool.modules.i18n.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.tools.workspace import WorkSpaceTool


class ServerKeyDecs:
    def __init__(self, key, module_name, origin_key):
        self.key = key
        self.module_name = module_name
        self.origin_key = origin_key


class ServeFileTool:
    def read_key() -> int:
        path = ServeFileTool.server_key_path()
        if not os.path.exists(path):
            return 0
        else:
            with open(path, encoding="utf8") as f:
                content = f.read()
                f.close()
                return int(content)

    def update_key(value: int):
        path = ServeFileTool.server_key_path()
        with open(path, mode="w", encoding="utf8") as f:
            f.write("{}".format(value))
            f.close()

    def convert(value: int) -> str:
        """将10进制的树转换成36进制的字符串

        Args:
            value (int): 输入的十进制

        Returns:
            str: 返回的36进制字符串
        """
        if value > 46656:
            Print.error("数值不能大于 46656")
        asc_list: list[int] = []
        for i in range(3):
            if value == 0:
                # ASCII值 0-9 是 48~57
                asc_list.insert(0, 48)
                continue
            mod = value % 36
            if mod < 10:
                # ASCII值 0-9 是 48~57
                asc_list.insert(0, mod + 48)
            else:
                # ASCII值 A-Z 是 65~90，减去 0-9 的10后等于55
                asc_list.insert(0, mod + 55)
            value = value // 36
        result_str = ""
        for r in asc_list:
            result_str += chr(r)
        return result_str

    def update_decs(decs_list: list[ServerKeyDecs]):
        """更新 key 的描述json文件

        Args:
            decs_list (list[ServerKeyDecs]): 更新的列表
        """
        if len(decs_list) == 0:
            return
        json_path = ServeFileTool.server_key_desc_path()
        json_dic = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf8") as f:
                json_str = f.read()
                json_dic = json.loads(json_str)
                f.close()
        with open(json_path, mode="w", encoding="utf8") as f:
            for decs in decs_list:
                json_dic[decs.key] = {
                    "module_name": decs.module_name,
                    "origin_key": decs.origin_key,
                }
            f.write(json.dumps(json_dic, indent=2, sort_keys=True, ensure_ascii=False))
            f.close()

    def update_useless(module_name: str, str_list: list[str]):
        """上传没有使用到的国际化字符串

        Args:
            module_name (str): 组件名
            str_list (list[str]): 没使用到的字符串数组
        """
        if len(str_list) == 0:
            return
        json_path = ServeFileTool.server_key_useless_path()
        json_dic = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf8") as f:
                json_str = f.read()
                json_dic = json.loads(json_str)
                f.close()
        with open(json_path, mode="w", encoding="utf8") as f:
            json_dic[module_name] = str_list
            f.write(json.dumps(json_dic, indent=2, sort_keys=True, ensure_ascii=False))
            f.close()

    def pull_form_server():
        """拉取服务端最新文件"""
        tdf_tools_path = os.path.expanduser("~") + "/" + FileUtil._I18N_PATH
        Cmd.run("git -C {} pull".format(tdf_tools_path))

    def upload_to_server():
        """上传文件到服务端"""
        tdf_tools_path = os.path.expanduser("~") + "/" + FileUtil._I18N_PATH
        Cmd.run("git -C {} add .".format(tdf_tools_path))
        Cmd.run("git -C {} commit -m 'update i8n'".format(tdf_tools_path))
        Cmd.run("git -C {} push".format(tdf_tools_path))

    def server_key_path() -> str:
        """获取服务端最新的key的本地地址

        Returns:
            _type_: 服务端最新的key的本地地址
        """
        app = WorkSpaceTool.get_project_app()
        tool_path = FileUtil.tdf_i18n_path()
        return tool_path + "/{}_last_server_key.txt".format(app.decs())

    def server_key_desc_path() -> str:
        """获取服务端映射关系的地址

        Returns:
            _type_: 获取服务端映射关系的地址
        """
        app = WorkSpaceTool.get_project_app()
        tool_path = FileUtil.tdf_i18n_path()
        return tool_path + "/{}_server_key.json".format(app.decs())

    def server_key_desc_json() -> dict:
        json_path = ServeFileTool.server_key_desc_path()
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                json_data = f.read()
                json_dict = json.loads(json_data)
                return json_dict

    def server_key_useless_path() -> str:
        """获取服务端没用到的key的本地地址

        Returns:
            _type_: 本地没用到的key的本地地址，主要是%等转义符
        """
        app = WorkSpaceTool.get_project_app()
        tool_path = FileUtil.tdf_i18n_path()
        return tool_path + "/{}_useless_key.json".format(app.decs())
