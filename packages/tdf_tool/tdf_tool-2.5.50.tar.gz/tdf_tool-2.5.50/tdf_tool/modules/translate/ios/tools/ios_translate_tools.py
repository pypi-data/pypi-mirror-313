# coding=utf-8
import json
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.file_util import FileUtil
from tdf_tool.modules.translate.ios.tools.ios_translate_pattern import (
    iOSTranslatePattern,
)
from tdf_tool.modules.translate.ios.tools.string_util import StringUtil
from tdf_tool.modules.translate.tools.translate_tool import (
    LanguageType,
    TranslateTool,
    TranslateType,
)
from io import TextIOWrapper


class iOSTranslateTools:
    def get_all_string(
        dir: str, pattern: str, auto_string_define_str: str
    ) -> list[str]:
        total_list = []
        for path in FileUtil.get_allfile(dir, iOSTranslatePattern.ios_suffix):
            # 打开一个文件
            f: TextIOWrapper = open(path)
            chinese_list = StringUtil.get_chinese_string(
                f.read(),
                pattern,
                spical_strs=iOSTranslatePattern.ios_special_str_list,
                except_list=[
                    # iOSTranslatePattern.pattern_oc__static_str,
                    # iOSTranslatePattern.pattern_oc__const_str,
                    iOSTranslatePattern.pattern_no_filter_str(auto_string_define_str),
                    iOSTranslatePattern.pattern_filter_track_str,
                    iOSTranslatePattern.pattern_filter_router_str,
                ],
            )
            f.close()
            if len(chinese_list) > 0:
                # print("文件名: "+ path)
                for item in chinese_list:
                    total_list.append(item)
        # 去重后返回
        return list(set(total_list))

    # repl 需要实现一个方法去替换 匹配的方法 返回修改的文件数组
    def change_all_string(dir: str, pattern: str, repl) -> list[str]:
        path_list = []
        for path in FileUtil.get_allfile(dir, iOSTranslatePattern.ios_suffix):
            # 打开一个文件
            f = open(path, "r")
            old_text = f.read()
            result = StringUtil.get_changed_chinese_string(
                old_text, pattern, iOSTranslatePattern.ios_special_str_list, repl
            )
            f.close()
            if old_text != result:
                path_list.append(path)
                f = open(path, "w")
                f.write(result)
                f.close()
        return path_list

    # 向strings文件加入key value  truple (path,string_type)   如果存在则不处理 入参为list  元素为key value的元组     source_path为strings源文件目录 优先从此文件翻译
    def update_iOS_string_key_Values(
        args, list: list[str, str], source_path
    ) -> dict[str, str]:
        path = args[0]
        string_type = args[1]
        dic_from_strings = iOSTranslateTools.get_dic_with_dir(source_path, string_type)
        string_no_trans_count = 0
        # 已经国际化过的数量
        string__local_trans_count = 0
        # 需要谷歌翻译的数量
        string__goole_trans_count = 0
        # 新增的翻译文案
        string__goole_trans_dict: dict[str, str] = {}
        # 翻译错误的数量
        string__trans_error_count = 0

        f = open(path)
        orig_content = f.read()
        # 判断最后一个是否是回车
        content = orig_content.strip() + "\n"
        f.close

        content_dict = {}
        for key, value in list:
            # (comma_key in content) 寻找是用带引号key去查找的，没有的话得补上
            comma_key = key
            if not key.startswith('"') and not key.endswith('"'):
                comma_key = '"' + key + '"'
            if (comma_key in content) == False:
                # 未本地化
                string_no_trans_count = string_no_trans_count + 1
                if len(value) == 0:
                    value = iOSTranslateTools.__translate_str_from_local(
                        key, dic_from_strings
                    )
                    if len(value) > 0:
                        string__local_trans_count = string__local_trans_count + 1
                    else:
                        value = iOSTranslateTools.__translate_str_from_goole(
                            key, string_type
                        )
                        if len(value) > 0:
                            string__goole_trans_count = string__goole_trans_count + 1
                            string__goole_trans_dict[key] = value
                        else:
                            string__trans_error_count = string__trans_error_count + 1
                            continue

                content_dict[key] = value

        for key in sorted(content_dict.keys()):
            content = content + '"' + key + '" = "' + content_dict[key] + '";\n'

        # 写入
        Print.title(
            string_type
            + "共"
            + str(len(list))
            + "个包含中文的字符串,"
            + str(string_no_trans_count)
            + "个未翻译,"
            + str(string__local_trans_count)
            + "个本地翻译,"
            + str(string__goole_trans_count)
            + "个谷歌翻译,"
            + str(string__trans_error_count)
            + "个翻译失败"
        )
        if orig_content != content:
            f = open(path, "w")
            f.write(content)
            f.close()

        return string__goole_trans_dict

    def __translate_str_from_local(str: str, dic_local: dict):
        result = dic_local.get(str, "")
        return result

    def __translate_str_from_goole(str: str, string_type) -> str:
        translator = TranslateTool(TranslateType.GOOGLE)
        languageType = LanguageType.init(string_type)
        return translator.translate(str, dest=languageType)

    # 获取组件中 .strings 中的所有键值对
    def get_module_dict(source_dir: str, string_type: str) -> dict:
        result = {}
        # 获取组件下所有的国际化键值对
        for path in FileUtil.get_allfile(source_dir, [".strings"]):
            if string_type + ".lproj" in path:
                result.update(iOSTranslateTools.get_dic_from_string_file(path))
        return result

    # 获取组件、全局json中的所有键值对
    def get_dic_with_dir(source_dir: str, string_type: str) -> dict:
        if len(source_dir) == 0:
            return {}
        result = {}

        app_strings_path = FileUtil.localizable_path()

        # 获取组件下所有的国际化键值对
        module_dict = iOSTranslateTools.get_module_dict(source_dir, string_type)
        result.update(module_dict)

        # 获取全部国际化键值对
        for path in FileUtil.get_allfile(app_strings_path, [".json"]):
            type_vaule = string_type.split(".lproj")[0]
            if type_vaule in path:
                result.update(iOSTranslateTools.get_dic_from_json_file(path))

        return result

    # 获取 .strings 中的国际化键值对
    def get_dic_from_string_file(file_path) -> dict:

        # TODO: 有空修复掉
        # 正则出来的 \n 会变成 \\n 带转义符的原因，导致匹配不对，不能使用这个方案
        # result = Cmd.run("plutil -convert json -o - " + file_path)
        # jsonData = json.loads(result)
        # return jsonData

        with open(file_path, "r") as load_f:
            dic = {}
            for line in load_f:
                line = line.replace(";\n", "")
                v = line.split('" = "')
                count = len(v)
                # 分割不正常
                if count != 2:
                    continue
                # [1:] 是去掉前面的引号，[:-1] 去掉后面的引号
                key: str = v[0][1:]
                value: str = v[1][:-1]

                # 去掉前后双引号
                if key.startswith('"') and key.endswith('"'):
                    key = key[1:-1]
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                dic[key] = value
            return dic

    # 获取 .json 中的国际化键值对
    def get_dic_from_json_file(file_path) -> dict:
        with open(file_path, "r", encoding="utf-8") as rf:
            jsonData = json.loads(rf.read())
            rf.close()
            return jsonData
