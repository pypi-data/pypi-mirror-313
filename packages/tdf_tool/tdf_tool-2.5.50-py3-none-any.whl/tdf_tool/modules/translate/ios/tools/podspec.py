import json
import re
from tdf_tool.tools.cmd import Cmd


class PodspecModel:
    def __init__(self, podspec_path: str):
        self.podspec_path = podspec_path

        podspec_json_str: str = Cmd.run("pod ipc spec " + podspec_path)
        self.podspec_json = json.loads(podspec_json_str)

        self.podspec_name = self.__get_name_content__()

        self.source_files = self.__get_source_files__()

        self.podspec_source_root_path = self.__get_source_root_path__()

        self.auto_string_class_name = self.podspec_name + "AutoLocationString"

        self.auto_string_define_str = self.podspec_name + "LocalizedString"

        if self.podspec_source_root_path == "Classes":
            self.localization_path = self.podspec_source_root_path + "/Localization"
        else:
            self.localization_path = (
                self.podspec_source_root_path + "/Classes/Localization"
            )

        # 本地化特有的 bundle name
        self.podspec_resource_bundle_name = self.__get_strings_resource_bundle_name__()
        self.podspec_resource_bundles = self.__get_resource_bundles__()
        # 自动生成的
        self.auto_string_bundle_source = self.__get_auto_creat_string_bundle_source__()

    # 更新podspec
    def update_pod_spec(self):
        # 更新 dependency 依赖
        self.__check_and_insert_dependency_files()
        # 更新 source_files
        self.__check_and_insert_source_files()
        # 更新 bundle_source
        self.__check_and_insert_auto_string_bundle_source()

    # 获取 podsepc 的text
    def __get_spec_content__(self, path: str) -> str:
        f = open(path)
        content = f.read()
        f.close()
        return content

    def __get_source_files__(self) -> list[str]:
        source_files = self.podspec_json["source_files"]
        if isinstance(source_files, str):
            return [source_files]
        else:
            return source_files

    # 获取 spec 的名字
    def __get_name_content__(self) -> str:
        return self.podspec_json["name"]

    # 获取 source_files 的第一个路径的根路径
    def __get_source_root_path__(self) -> str:
        source_files = self.podspec_json["source_files"]
        first_source_files = self.podspec_name
        if isinstance(source_files, str):
            first_source_files = source_files
        elif isinstance(source_files, list):
            first_source_files = source_files[0]
        return first_source_files.split("/")[0]

    # 本地化特有的 bundle name
    def __get_strings_resource_bundle_name__(self) -> str:
        return self.podspec_name + "Strings"

    # 整个 resource_bundles
    def __get_resource_bundles__(self) -> dict[str:object]:
        try:
            return self.podspec_json["resource_bundles"]
        except:
            return {}

    # 本地化字符串源文件的地址
    def __get_auto_creat_string_bundle_source__(self) -> str:
        return self.podspec_source_root_path + "/{0}_strings/*.lproj".format(
            self.podspec_name
        )

    # 更新 dependency 依赖
    def __check_and_insert_dependency_files(self):
        dependencys: dict = {}
        try:
            dependencys: dict = self.podspec_json["dependencies"]
        except:
            dependencys = {}

        if "TDFInternationalKit" in dependencys.keys():
            print("dependencies中有依赖TDFInternationalKit")
        else:
            insert_str = "  s.dependency 'TDFInternationalKit'"
            f = open(self.podspec_path, "r")
            content = f.read()
            f.close

            # 插入 头文件引用
            pattern = re.compile(r".*?s.dependency.*?[\"']\n")
            results: list[str] = pattern.findall(content)
            if len(results) > 0:
                result: str = results[0]
                newContent = result + insert_str + "\n"
                content = re.sub(pattern, newContent, content, 1)
            else:
                # 插入 s.dependency 到 s.source_files 后面
                pattern = re.compile(r"[\s]?[ ]*[^A-Za-z]s.source_files.*?\n")
                result: str = pattern.findall(content)[0]
                # 处理空格个数
                space_str = result.split("s.")[0]
                print(space_str)
                newContent = result + space_str + insert_str + "\n"
                content = re.sub(pattern, newContent, content, 1)
            # 写入podpspec
            f = open(self.podspec_path, "w")
            f.write(content)
            f.close()

    # 将新增代码的路径添加到 source_files 中
    def __check_and_insert_source_files(self):

        path = self.localization_path + "/**/*.{h,m}"

        # 插入s.source_files
        content = self.__get_spec_content__(self.podspec_path)
        pattern = re.compile(r"[^\n]?[ ]*[^A-Za-z]s.source_files.*?\n")
        result: str = pattern.findall(content)[0]
        result = result.rstrip()
        if path in self.source_files:
            print("s.source_files已包含：" + path)
        else:
            print("s.source_files写入：" + path)
            source_files_last_str = result.split("=")[1]
            source_files = list(map(lambda x: "'{0}'".format(x), self.source_files))
            new_source_files_value = (
                " " + ", ".join(source_files) + ", '" + path + "'\n"
            )
            newContent = result.replace(source_files_last_str, new_source_files_value)
            content = re.sub(pattern, newContent, content, 1)
            print("写入podpspec完成")
            # 写入podpspec
            f = open(self.podspec_path, "w")
            f.write(content)
            f.close()

    # 将新增的本地化资源文件路径加入 resource_bundles 中
    def __check_and_insert_auto_string_bundle_source(self):

        podspec_resource_bundles_list: list[str] = []
        for resourceKey in self.podspec_resource_bundles:
            resource = self.podspec_resource_bundles[resourceKey]
            if isinstance(resource, list):
                podspec_resource_bundles_list.extend(resource)
            elif isinstance(resource, str):
                podspec_resource_bundles_list.append(resource)

        if self.auto_string_bundle_source in podspec_resource_bundles_list:
            print(
                "podspec已经包含" + self.auto_string_bundle_source + "     不需要修改"
            )
        else:
            print("podspec不包含" + self.auto_string_bundle_source)
            print("podspec添加至resource_bundles" + self.auto_string_bundle_source)

            self.podspec_resource_bundles[self.podspec_resource_bundle_name] = [
                self.auto_string_bundle_source
            ]

            resource_bundles_str = " {\n"

            for key in self.podspec_resource_bundles:
                resource_bundles_str += "    '" + key + "' => ["
                resource_bundles_result = self.podspec_resource_bundles[key]
                resource_bundles: list[str] = []
                if isinstance(resource_bundles_result, list):
                    resource_bundles = resource_bundles_result
                elif isinstance(resource_bundles_result, str):
                    resource_bundles = [resource_bundles_result]
                resource_bundles = list(
                    map(lambda x: "'{0}'".format(x), resource_bundles)
                )
                resource_bundles_str += ", ".join(resource_bundles) + "],\n"

            resource_bundles_str += "  }"

            content = self.__get_spec_content__(self.podspec_path)
            pattern = re.compile(r"[^A-Za-z]?s.resource_bundles[^#]*?}\n")
            result = pattern.findall(content)
            if len(result) > 0:
                # 替换
                newContent = " s.resource_bundles =" + resource_bundles_str
                content = re.sub(pattern, newContent, content, 1)
            else:
                # 插入s.resource_bundles 到 s.source_files 后面
                pattern = re.compile(r"[\s]?[ ]*[^A-Za-z]s.source_files.*?\n")
                result: str = pattern.findall(content)[0]
                # 处理空格个数
                space_str = result.split("s.")[0]
                print(space_str)
                newContent = (
                    result
                    + space_str
                    + "s.resource_bundles ="
                    + resource_bundles_str
                    + "\n"
                )
                content = re.sub(pattern, newContent, content, 1)
            # print("podspec添加resource_bundles后",",".join(self.podspec_resource_bundles))
            print("写入podpspec完成")
            # 写入podpspec
            f = open(self.podspec_path, "w")
            f.write(content)
            f.close()
