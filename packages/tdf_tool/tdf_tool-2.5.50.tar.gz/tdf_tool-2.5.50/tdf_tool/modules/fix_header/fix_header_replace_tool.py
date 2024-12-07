import os
import re
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodModel,
)
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.file_util import FileUtil


class FixHeaderReplaceTool:
    def __init__(self, root_path: str, local_pods: list[BatchPodModel]):
        self.root_path = root_path
        self.pods_path = root_path + "/" + "Pods"
        self.podfile_path = root_path + "/" + "Podfile"
        self.local_module_files: set[str] = set()
        self.local_pods = local_pods
        # retote_header_map 为头文件，value为模块名
        self.remote_header_map: dict[str, str] = {}
        self.local_header_map: dict[str, str] = {}

    def start_fix(self, module_name: str):
        self.find_remote_pod_header()
        self.find_local_pod_header(module_name)
        self.replace_import(module_name)

    # 找出 pod 中远程依赖的文件夹
    def find_remote_pod_header(self):
        Print.title("开始找出 pod 中远程依赖的文件夹")
        self.__find_remote_pod_header(self.pods_path)

    # 找出 pod 中远程依赖的文件夹
    def __find_remote_pod_header(self, path: str):
        files = FileUtil.findAllFile(path)
        for file in files:
            if file.endswith(".h"):
                module_name = file.split(self.pods_path)[1]
                module_name = module_name.split("/")[1]
                if module_name != "Headers":
                    f = file.split("/")[-1]
                    self.remote_header_map[f] = module_name

    # 找出 pod 中本地依赖的文件夹
    def find_local_pod_header(self, module_name: str):
        Print.title("开始找出 pod 中本地依赖的文件夹")
        self.__init_data()
        for pod in self.local_pods:
            for file_path in pod.source_files:
                if pod.name == module_name:
                    # 是当前模块，将模块的所有文件记录下来，存入 module_files 里
                    self.local_module_files.add(file_path)
                else:
                    # 不是本模块的找出头文件对应的模块，生成 header_map
                    if file_path.endswith(".h"):
                        h = file_path.split(r"/")[-1]
                        self.local_header_map[h] = pod.name

    # 替换所有不符合规范的 import
    def replace_import(self, module_name: str):
        Print.title("开始替换所有不符合规范的 import")
        for f in self.local_module_files:
            if os.access(f, os.W_OK):
                self.__find_strings_in_file(f, module_name)
            else:
                Print.error("无可写权限文件：{}".format(f))

    # 初始化数据
    def __init_data(self):
        self.local_module_files = set()
        self.local_header_map = {}

    # 扫描某个文件的字符串
    def __find_strings_in_file(self, filename: str, module_name: str):
        Print.title("开始处理文件：{}\n".format(filename))
        fin = open(filename, "r")
        code = fin.read()
        fin.close()
        new_code = code
        matchs: list[str] = re.findall(r'#import.*"(?:\\.|[^"\n])*"', code)
        for import_str in matchs:
            nameList = re.findall(r"\"(.+?)\"", import_str)
            h_name = nameList[0]
            if "-Swift.h" not in h_name:
                # 先取远端
                f_module_name = self.remote_header_map.get(h_name)
                # 没取到，取本地
                if f_module_name is None:
                    f_module_name = self.local_header_map.get(h_name)
                if f_module_name and f_module_name != module_name:
                    new_imoport = "#import <{}/{}>".format(f_module_name, h_name)
                    new_code = new_code.replace(import_str, new_imoport)
                    Print.warning("替换 {} ==> {}\n".format(import_str, new_imoport))

        if new_code != code:
            fout = open(filename, "w")
            fout.write(new_code)
            fout.close()

        Print.line()
