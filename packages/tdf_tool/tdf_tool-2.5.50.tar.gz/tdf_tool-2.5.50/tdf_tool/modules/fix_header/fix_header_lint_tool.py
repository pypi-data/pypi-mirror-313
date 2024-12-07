import os
from io import TextIOWrapper
import re
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
)


class FixHeaderLintTool:
    __files = []
    __h_files = []
    __fail_logs = []
    __ex_swift = "-Swift.h"  # 不处理swift文件

    def lint(self, podspec_path: str):
        file_list: set[str] = BatchPodTools.get_source_files(podspec_path)
        self.__find_all_files(file_list)
        self.__find_wrong_import(file_list)

    # 查找文件，并归类
    def __find_all_files(self, files: set[str]):
        for f in files:
            file_name = f.split(r"/")[-1]
            if file_name.endswith(self.__ex_swift):
                continue
            if file_name.endswith(".h"):
                self.__h_files.append(file_name)
            self.__files.append(file_name)

    # 找到所有不符合规范的 import
    def __find_wrong_import(self, file_paths: set[str]):
        for f in file_paths:
            if os.access(f, os.R_OK):
                self.__lint_strings_in_file(f)
            else:
                Print.title("无可读权限文件：{0}".format(f))
        if self.__fail_logs:
            for str in self.__fail_logs:
                Print.warning(str)
            Print.error("以上文件有头文件引用错误，请修改")

    # 扫描某个文件的字符串，找到不符合规范的 import
    def __lint_strings_in_file(self, filename):
        if os.path.isdir(filename):
            Print.error("asdadsa")
        Print.title("开始 lint 文件：{}\n".format(filename))
        fin: TextIOWrapper = open(filename, "r")
        code = fin.read()
        fin.close()
        matchs: list[str] = re.findall(r'\n#import.*"(?:\\.|[^"\n])*"', code)
        for import_str in matchs:
            h_name = import_str.replace(" ", "").split('#import"')[1].split('"')[0]
            if self.__ex_swift not in h_name:
                if h_name not in self.__h_files:
                    self.__fail_logs.append(
                        "{}===需要修改{}的引用".format(filename, h_name)
                    )
