from enum import Enum
from genericpath import isdir
import os
from posixpath import join
from tdf_tool.tools.cmd import Cmd
from tdf_tool.tools.env import EnvTool
from tdf_tool.tools.workspace import ProjectType, WorkSpaceTool


class FileUtil:
    _I18N_PATH = ".tdf_i18n"

    def tdf_i18n_path() -> str:
        """tdf_i18n的本地路径

        Returns:
            str: tdf_i18n的本地路径
        """
        user_path = os.path.expanduser("~")
        tdf_tools_path = user_path + "/" + FileUtil._I18N_PATH
        if not os.path.exists(tdf_tools_path):
            Cmd.run(
                "git -C {} clone git@git.2dfire.net:app/other/serverdatamapping.git {}".format(
                    user_path, FileUtil._I18N_PATH
                )
            )
        type = WorkSpaceTool.get_project_type()
        if type == ProjectType.IOS:
            tdf_tools_path += "/ios"
        else:
            tdf_tools_path += "/flutter"
        if not os.path.exists(tdf_tools_path):
            os.makedirs(tdf_tools_path)
        return tdf_tools_path

    def get_all_file(path: str, suffix_str_list=[]) -> list[str]:
        """获取文件目录下指定后缀的文件路径

        Args:
            path (str): 目标文件路径
            suffix_str_list (list, optional): 指定的后缀数组. Defaults to [].

        Returns:
            list[str]: 获取到的文件路径数组
        """
        if isdir(path) == False:
            print("不存在路径：" + path)
            return []
        all_file = []
        for root, _, files in os.walk(path):
            for f in files:
                for suffix_str in suffix_str_list:
                    if f.endswith(suffix_str):
                        all_file.append(join(root, f))
        return all_file
