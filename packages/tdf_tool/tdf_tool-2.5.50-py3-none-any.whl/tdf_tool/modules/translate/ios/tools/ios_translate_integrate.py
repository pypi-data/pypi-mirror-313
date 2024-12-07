import json
import os
import re
from tdf_tool.tools.cmd import Cmd
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import BatchPodModel
from tdf_tool.modules.translate.file_util import FileUtil
from tdf_tool.modules.translate.ios.tools.ios_translate_tools import iOSTranslateTools


class iOSTranslateIntegrate:

    # 整合 json 文件
    def integrate_json_root(self) -> dict[str, dict[str, str]]:
        all_dict: dict[str, str] = {}
        for type in FileUtil.LOCAL_STRING_TYPES:
            path = FileUtil.localizable_path() + "/" + type + "/localizable.json"
            strings_dict = iOSTranslateTools.get_dic_from_json_file(path)
            strings_dict = self.__delete_double_quotes(strings_dict)
            all_dict[type] = strings_dict
        return all_dict

    # 整合主工程的 .strins 文件
    def integrate_strins_root(self, path) -> dict[str, dict[str, str]]:
        all_dict: dict[str, str] = {}
        for type in FileUtil.LOCAL_STRING_TYPES:
            path = path + type + ".lproj" + "/Localizable.strings"
            strings_dict = iOSTranslateTools.get_dic_from_string_file(path)
            strings_dict = self.__delete_double_quotes(strings_dict)
            all_dict[type] = strings_dict
        return all_dict

    # 整合模块
    def integrate_pod(self, pod: BatchPodModel) -> dict[str, dict[str, str]]:
        all_dict: dict[str, dict[str, str]] = {}
        for root, dirs, files in os.walk(pod.path):
            for file in files:
                if file.endswith(pod.name + ".strings"):
                    file_path = root + "/" + file
                    pattern = re.compile(r"[^/]*(?=\.lproj/)")
                    results = pattern.findall(file_path)
                    if len(results) > 0:
                        type = results[0]
                        strings_dict = iOSTranslateTools.get_dic_from_string_file(
                            file_path
                        )
                        strings_dict = self.__delete_double_quotes(strings_dict)
                        all_dict[type] = strings_dict
        return all_dict

    # 新增翻译到 中心化的json中，并上传
    def new_dict_and_upload(self, new_dict: dict[str, dict[str, str]]):
        Print.stage("新增翻译到 中心化的json中，并上传")
        # 目前的json字典
        old_json_dict = self.integrate_json_root()
        new_json_dict = self.merge_dict(new_dict, old_json_dict)
        self.write_dict_to_json(new_json_dict)
        self.upload_json()
        Print.stage("新增翻译到 中心化的json中，并上传成功")

    # 合并两个翻译文件，two会覆盖one
    def merge_dict(
        self, one: dict[str, dict[str, str]], two: dict[str, dict[str, str]]
    ) -> dict[str, dict[str, str]]:
        all_dict: dict[str, str] = {}
        for type in FileUtil.LOCAL_STRING_TYPES:
            one_type_dict = one[type]
            two_type_dict = two[type]
            one_type_dict.update(two_type_dict)
            all_dict[type] = one_type_dict
        return all_dict

    # 写入翻译内容到 json 中
    def write_dict_to_json(self, json_dict: dict[str, dict[str, str]]):
        for type in FileUtil.LOCAL_STRING_TYPES:
            json_path = FileUtil.localizable_path() + "/" + type
            json_file_path = json_path + "/localizable.json"
            if os.path.exists(json_path):
                print("已存在文件夹：" + json_path)
            else:
                print("不存在文件夹：" + json_path + "\n创建文件:" + json_path)
                os.makedirs(
                    json_path,
                )
            if os.path.exists(json_file_path):
                print("已存在文件：" + json_file_path)
            else:
                print("不存在文件：" + json_file_path + "\n创建文件:" + json_file_path)
                file = open(json_file_path, "a+")
                file.close()
            type_json_dict = json_dict[type]
            json_str = json.dumps(
                type_json_dict, sort_keys=True, ensure_ascii=False, indent=4
            )
            json_file = open(json_file_path, "w+")
            json_file.write(json_str)
            json_file.close()

    # 上传 jons 到远端
    def upload_json(self):
        localizable_path = FileUtil.localizable_path()
        Cmd.runAndPrint("git -C {0} pull origin master".format(localizable_path))
        Cmd.runAndPrint("git -C {0} add .".format(localizable_path))
        Cmd.runAndPrint("git -C {0} commit -m 'new translate'".format(localizable_path))
        Cmd.runAndPrint("git -C {0} push origin master".format(localizable_path))

    # 删除字段里面字符串前后的双引号
    def __delete_double_quotes(self, target: dict[str, str]) -> dict[str, str]:
        new_dict = {}
        for k, v in target.items():
            # 翻译前去掉 前后双引号
            if k.startswith('"') and k.endswith('"'):
                k = k[1:-1]
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            new_dict[k] = v
        return new_dict
