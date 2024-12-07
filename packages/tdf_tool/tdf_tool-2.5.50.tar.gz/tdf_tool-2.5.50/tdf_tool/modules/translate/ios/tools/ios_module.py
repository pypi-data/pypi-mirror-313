import os
from posixpath import join
import re
from tdf_tool.tools.cmd import Cmd
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.file_util import FileUtil
from tdf_tool.modules.translate.ios.tools.ios_translate_pattern import (
    iOSTranslatePattern,
)
from tdf_tool.modules.translate.ios.tools.ios_translate_tools import iOSTranslateTools
from tdf_tool.modules.translate.ios.tools.location_string_temp import (
    LocationStringTempClass,
)
from tdf_tool.modules.translate.ios.tools.podspec import PodspecModel


class IosModule:
    # path 组件路径
    def __init__(self, path: str):
        self.path = path
        self.podspecPath = self.__get_podspec_path__()
        if self.podspecPath == "":
            raise ("" + self.path + "未找到podspec文件")
        else:
            self.podspecModel = PodspecModel(self.podspecPath)
            self.auto_string_class_name = (
                self.podspecModel.podspec_name + "AutoLocationString"
            )
            self.auto_string_define_str = (
                self.podspecModel.podspec_name + "LocalizedString"
            )

    def __get_podspec_path__(self) -> str:
        if self.path:
            names = os.listdir(self.path)
            for file in names:
                if file.endswith(".podspec"):
                    return join(self.path, file)
        return ""

    # 检查是否还有未本地化的字符串
    def check_location_string(self):
        Print.stage("检查是否还有未本地化的字符串")
        # 未本地化的字符串
        un_locating_string_array = iOSTranslateTools.get_all_string(
            self.path + "/" + self.podspecModel.podspec_source_root_path,
            iOSTranslatePattern.pattern_oc__no_localized_chinese_str,
            self.auto_string_define_str,
        )
        if len(un_locating_string_array) > 0:
            for i in un_locating_string_array:
                print(i)
            Print.error(
                "有以上未本地化的字符串{}个".format(len(un_locating_string_array)),
            )
        else:
            Print.stage("未本地化的字符串 0 个")

        # 使用NSLocalizedString本地化的包含中文的字符串
        locating_string_array = iOSTranslateTools.get_all_string(
            self.path + "/" + self.podspecModel.podspec_source_root_path,
            iOSTranslatePattern.pattern_oc__nslocalized_str,
            self.auto_string_define_str,
        )
        if len(locating_string_array) > 0:
            for i in locating_string_array:
                print(i)
            Print.error(
                "有以上使用NSLocalizedString本地化的包含中文的字符串本地化的字符串{}个".format(
                    len(locating_string_array)
                )
            )
        else:
            Print.stage(
                "使用NSLocalizedString本地化的包含中文的字符串本地化的字符串 0 个"
            )

        # 使用 TDFModuleLocalizedString 本地化，但是 .strings 文件中没有翻译的文件
        module_locating_string_array = iOSTranslateTools.get_all_string(
            self.path + "/" + self.podspecModel.podspec_source_root_path,
            '(?<={}\(@")[^"]*?[\u4E00-\u9FA5][^"]*?(?=".*?\))'.format(
                self.auto_string_define_str
            ),
            self.auto_string_define_str,
        )
        module_locating_string_dic = {}
        for string in module_locating_string_array:
            module_locating_string_dic[string] = string

        for string_type in FileUtil.LOCAL_STRING_TYPES:
            dic_from_strings = iOSTranslateTools.get_module_dict(
                self.path + "/" + self.podspecModel.podspec_source_root_path,
                string_type,
            )
            for key in dic_from_strings.keys():
                try:
                    del module_locating_string_dic[key]
                except:
                    pass

            un_translate_strings = module_locating_string_dic.keys()
            if len(un_translate_strings) > 0:
                for i in un_translate_strings:
                    print(i)
                Print.error(
                    "{}.string中使用{}本地化的包含中文的字符串本地化的字符串{}个".format(
                        string_type,
                        self.auto_string_define_str,
                        len(un_translate_strings),
                    ),
                )
            else:
                Print.stage(
                    "{}.string中使用{}本地化的包含中文的字符串本地化的字符串 0 个".format(
                        string_type,
                        self.auto_string_define_str,
                    )
                )

    # 检查 .strings 文件的有效性
    def check_strings_file(self):
        Print.stage("检查 .strings 文件的有效性")
        podspec = PodspecModel(self.podspecPath)
        podspec_resource_bundle = self.path + "/" + podspec.auto_string_bundle_source
        podspec_resource_bundle = podspec_resource_bundle.replace("/*.lproj", "")
        for root, dirs, files in os.walk(podspec_resource_bundle):
            for file in files:
                if file.endswith(".strings"):
                    file_path = root + "/" + file
                    result = Cmd.system("plutil -lint " + root + "/" + file)
                    if result != 0:
                        Print.error(file_path + "文件有错误")
        Print.stage("检查 .strings 文件的有效")

    def change_location_string(self):
        print("检查并修改未本地化的字符串")

        def __replace_impl__(str):
            print(
                "替换" + str + "\n" + self.auto_string_define_str + "(" + str + ", nil)"
            )
            return self.auto_string_define_str + "(" + str + ", nil)"

        def __replace_nslocalized_impl__(str: str):
            print(
                "替换"
                + str
                + "\n"
                + str.replace("NSLocalizedString", self.auto_string_define_str)
            )
            pattern = re.compile(r"%s" % (iOSTranslatePattern.patten_localized_suffix))
            results = pattern.findall(str)
            if len(results) > 0:
                result = results[0]
                # 把 NSLocalizedString 的第二个参数，全部换成 nil
                str = str.replace(result, ", nil)")

            return str.replace("NSLocalizedString", self.auto_string_define_str)

        path_result = []

        # 替换使用 NSLocalizedString 修饰的字符串
        path = self.path + "/" + self.podspecModel.podspec_source_root_path
        path_list = iOSTranslateTools.change_all_string(
            path,
            iOSTranslatePattern.pattern_oc__nslocalized_str,
            __replace_nslocalized_impl__,
        )
        print(path_list)
        path_result.extend(path_list)

        # 未国际化的字符串
        path = self.path + "/" + self.podspecModel.podspec_source_root_path
        path_list = iOSTranslateTools.change_all_string(
            path,
            iOSTranslatePattern.pattern_oc__no_localized_chinese_str,
            __replace_impl__,
        )
        print(path_list)
        path_result.extend(path_list)

        path_result = list(set(path_result))

        # 增加头文件引用
        for path_str in path_result:
            self.remove_static_str(path_str)
            self.add_import_str(path_str)

    # oc  static 不支持本地化
    def remove_static_str(self, path: str):
        # 查询 static 的字符串声明
        f = open(path, "r")
        content = f.read()
        f.close
        old_content = content
        pattern = re.compile(
            r"static .*?" + self.auto_string_define_str + "[\s\S]*?\);\n"
        )

        def __remove_localized_str__(matched):
            result = matched.group()
            result = result.replace(self.auto_string_define_str + "(", "")
            result = result.replace(", nil)", "")
            return result

        content = re.sub(pattern, __remove_localized_str__, content)
        # 写入
        if old_content != content:
            f = open(path, "w")
            f.write(content)
            f.close()

    def add_import_str(self, path: str):
        insert_str = '#import "' + self.auto_string_class_name + '.h"'
        f = open(path, "r")
        content = f.read()
        f.close
        if self.auto_string_define_str in content == False:
            return

        if insert_str in content:
            return
        # 插入 头文件引用
        pattern = re.compile(r".*?#import.*?\n")
        result: str = pattern.findall(content)[0]
        newContent = result + insert_str + "\n"
        content = re.sub(pattern, newContent, content, 1)
        # 写入podpspec
        f = open(path, "w")
        f.write(content)
        f.close()

    # 检查 podsepc，修改 podsepc
    def checkout_change_pod_spec(self):
        print("开始检查podspec")
        print("模块podspec路径:" + self.podspecModel.podspec_path)
        print("模块名称:" + self.podspecModel.podspec_name)
        print(
            "模块resource_bundles name:"
            + self.podspecModel.podspec_resource_bundle_name
        )
        print(
            "模块当前resource_bundles path:", self.podspecModel.podspec_resource_bundles
        )
        print("模块当前source_files:", self.podspecModel.source_files)
        # 检查并更新podspec文件
        self.podspecModel.update_pod_spec()

    # 生成本地化文件
    def create_update_location_files(self) -> dict[str, dict[str, str]]:
        # 生成本地化文件
        # 支持的语言类型
        local_string_string_types = list(
            map(lambda x: x + ".lproj", FileUtil.LOCAL_STRING_TYPES)
        )
        # 生成文件夹路径
        local_string_name = self.podspecModel.podspec_name + ".strings"
        local_string_file_paths: list[(str, str)] = []
        for string_type in local_string_string_types:
            file_string_path = (
                self.path
                + "/"
                + self.podspecModel.auto_string_bundle_source.replace(
                    "*.lproj", string_type
                )
            )
            local_string_file_paths.append((file_string_path, string_type))
        # 创建文件夹和文件
        for path, string_type in local_string_file_paths:
            string_file = path + "/" + local_string_name
            if os.path.exists(path):
                print("已存在文件夹：" + path)
            else:
                print("不存在文件夹：" + path + "\n创建文件:" + path)
                os.makedirs(
                    path,
                )
            if os.path.exists(string_file):
                print("已存在文件：" + string_file)
            else:
                print("不存在文件：" + string_file + "\n创建文件:" + string_file)
                file = open(string_file, "a+")
                file.close

            # 同步组件其他文件复制到此文件
            def __strings_filter__(path: str):
                if string_type in path:
                    if string_file != path:
                        return True
                return False

        # 获取需要翻译的所有key
        pattern = (
            "(?<=" + self.auto_string_define_str + '\(@")[\s\S]*?(?="[ ]*,[ ]*nil)'
        )
        locating_string_array = iOSTranslateTools.get_all_string(
            self.path + "/" + self.podspecModel.podspec_source_root_path,
            pattern,
            self.auto_string_define_str,
        )

        print(locating_string_array)
        print("本地化的key共%d个" % (len(locating_string_array)))
        locating_truple_arrary = []
        for locating_str in locating_string_array:
            locating_truple_arrary.append((locating_str, ""))

        # 新增的翻译
        new_translate_dict: dict[str, dict[str, str]] = {}

        for path, string_type in local_string_file_paths:
            string_file = path + "/" + local_string_name
            file_type = string_type.split(".lproj")[0]
            new_dict = iOSTranslateTools.update_iOS_string_key_Values(
                (string_file, string_type),
                locating_truple_arrary,
                self.path + "/" + self.podspecModel.podspec_source_root_path,
            )
            new_translate_dict[file_type] = new_dict

        return new_translate_dict

    # 添加本地化需要的OC文件并加入podspec的 sourcefile
    def create_update_oc_files(self):
        creat_file_full_path = self.path + "/" + self.podspecModel.localization_path
        # 添加文件夹
        if os.path.exists(creat_file_full_path):
            print("已存在文件夹：" + creat_file_full_path)
        else:
            print(
                "不存在文件夹："
                + creat_file_full_path
                + "\n创建文件:"
                + creat_file_full_path
            )
            os.makedirs(creat_file_full_path)

        for file_content in [
            LocationStringTempClass.class_h,
            LocationStringTempClass.class_m,
        ]:
            string_file = creat_file_full_path + "/" + self.auto_string_class_name
            if file_content == LocationStringTempClass.class_h:
                string_file = string_file + ".h"
            else:
                string_file = string_file + ".m"

            if os.path.exists(string_file):
                print("已存在文件：" + string_file)
            else:
                print("不存在文件：" + string_file + "\n创建文件:" + string_file)
                # 替换占位符
                file = open(string_file, "a+")

                file_content = file_content.replace(
                    "TDFLocationStringTempClass", self.auto_string_class_name
                )
                file_content = file_content.replace(
                    "TDFLocationStringTempBundle",
                    self.podspecModel.podspec_resource_bundle_name,
                )
                file_content = file_content.replace(
                    "TDFLocationStringTempTable", self.podspecModel.podspec_name
                )
                file_content = file_content.replace(
                    "TDFLocationStringTempDefine", self.auto_string_define_str
                )

                file.write(file_content)
                file.close
