from genericpath import isdir
import os
from posixpath import join
from tdf_tool.tools.cmd import Cmd


class FileUtil:

    LOCALOZABLE_PATH = "/.tdf_tool/localizable"
    TOOLS_PATH = "/.tdf_tool/tools"
    LOCAL_STRING_TYPES = [
        "en",
        "zh-Hans",
        "zh-Hant",
        "th",
    ]

    def localizable_path() -> str:
        tdf_tool_path = os.path.expanduser("~") + "/.tdf_tool"
        localizable_path = os.path.expanduser("~") + FileUtil.LOCALOZABLE_PATH
        if not os.path.exists(tdf_tool_path):
            os.mkdir(tdf_tool_path)
        if os.path.exists(localizable_path):
            Cmd.run("git -C {} pull".format(localizable_path))
        else:
            Cmd.run(
                "git -C {} clone git@git.2dfire.net:app/other/localizable.git".format(
                    tdf_tool_path
                )
            )
        return localizable_path

    # 创建并返回 get_files.rb 文件
    def generate_get_files_rb() -> str:
        path = os.path.expanduser("~") + FileUtil.TOOLS_PATH
        if not os.path.exists(path):
            os.makedirs(path)

        ruby_code = r"""
        for path in ARGV
            paths = Dir::glob(path)
            puts paths
        end"""
        get_files = path + "/get_files.rb"
        file = open(get_files, "w")
        file.write(ruby_code)
        file.close()
        return get_files

    def get_allfile(path, suffix_str_list=[]) -> list[str]:
        if isdir(path) == False:
            print("不存在路径：" + path)
            return []
        all_file = []
        for (root, dirs, files) in os.walk(path):
            for f in files:
                for suffix_str in suffix_str_list:
                    if f.endswith(suffix_str):
                        all_file.append(join(root, f))
        return all_file

    def findAllFile(path):
        for root, ds, fs in os.walk(path):
            for f in fs:
                fullname = os.path.join(root, f)
                yield fullname
