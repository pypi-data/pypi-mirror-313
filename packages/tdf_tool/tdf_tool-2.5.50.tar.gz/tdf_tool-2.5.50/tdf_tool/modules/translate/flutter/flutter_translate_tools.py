import json
import os
from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.config.module_json_config import ModuleJsonConfig, ModuleItemType
from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.tools.print import Print
from tdf_tool.tools.regular_tool import RegularTool
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.modules.translate.flutter.flutter_translate_lint import (
    FlutterTranslateLint,
    TranslateLintResult,
)
from tdf_tool.modules.translate.flutter.tools.flutter_translate_integrate import (
    FlutterTranslateIntegrate,
)
import hashlib
from tdf_tool.modules.translate.tools.translate_tool import (
    LanguageType,
    TranslateTool,
    TranslateType,
)
import shutil


class FlutterTranslateTools:
    def __init__(self):
        self.__translator = TranslateTool(type=TranslateType.GOOGLE)
        self.__i18nList = [
            LanguageType.ZH,
            LanguageType.EN,
            LanguageType.TH,
            LanguageType.CHT,
            LanguageType.ES,
        ]

    # 交互式 国际化
    def translate(self, all_module=False, always_yes=False):
        businessModuleList = self.__businessModuleList()

        Print.str("检测到以下模块可执行国际化脚本：")
        Print.str(businessModuleList)
        while True:
            targetModule = "!"
            if all_module:
                targetModule = "all"
            else:
                targetModule = input(
                    "请输入需要执行国际化脚本的模块名(input ! 退出，all 所有模块执行)："
                )

            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.translate_module(module, always_yes)
                exit(0)
            else:
                self.translate_module(targetModule, always_yes)
                exit(0)

    # 指定 模块国际化
    def translate_module(self, name, always_yes=False):
        businessModuleList = self.__businessModuleList()
        self.__always_yes = always_yes
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self.__generateTranslate(name)
            Print.title(name + " 模块国际化执行完成，生成 tdf_intl 相关文件")
        else:
            Print.error(name + " 模块不在开发列表中")

    # 可以进行国际化的列表
    def __businessModuleList(self) -> list:
        return FlutterTranslateLint.businessModuleList()

    # 入口
    def __generateTranslate(self, targetModule):
        ShellDir.goInShellLibDir()
        if not os.path.exists("tdf_intl"):
            os.mkdir("tdf_intl")

        # 进入tdf_intl目录
        # tdf_intl文件夹下包含i18n文件夹，其中存放4个dart文件，分别对应四种语言
        # tdf_intl文件夹下还包含一个origin.txt文件，用于存放需要转化的文案，每个文案为一行
        ShellDir.goInModuleLibDir(targetModule)
        if not os.path.exists("tdf_intl"):
            os.mkdir("tdf_intl")
        os.chdir("tdf_intl")
        tdfIntlDir = PlatformTools.curPath()

        # 如果没有i18n文件夹则生成
        self.__generate_i18n_files(tdfIntlDir, targetModule)

        # 检查是否有单引号字符串
        self.__check_apostrophe_strs(targetModule)

        # 检查是否有const的中文字符串
        self.__check_const_chinese_strs(targetModule)

        # 检查是否有未使用 intl 的中文字符串
        self.__check_un_intl_strs(targetModule)

        # 检查是否有 import 错误的文件
        self.__check_err_intl_import(targetModule)

        # 是否更新 i18n.json 文件
        self.__check_need_update_json(tdfIntlDir, targetModule)

        # 删除 json 中未用到的国际化字符串
        self.__check_delete_un_use_json(tdfIntlDir, targetModule)

        # 通过 i18n.json 生成各个翻译后的 dart 文件
        self.__generate_translate_dart_file(tdfIntlDir, targetModule)

    def __check_delete_un_use_json(self, tdfIntlDir, targetModule):
        Print.title("开始检查 i18n.json 中是否有多余的键值对")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        # 枚举中的中文字符串，在lint中要去掉这些
        unused_intl_json = [
            i for i in result.unused_json if i not in result.enum_chinese
        ]
        if len(unused_intl_json) <= 0:
            return

        Print.warning("i18n.json 中有以下字符串没有使用到：")
        Print.str(unused_intl_json)

        input_str = "N"
        if self.__always_yes:
            input_str = "Y"
        else:
            input_str = input("是否删除 i18n.json 中多余的键值对？(y/n)：")
        if input_str != "Y" and input_str != "y":
            return

        intl_json_path = tdfIntlDir + "/i18n.json"
        if not os.path.exists(intl_json_path):
            return

        read_file = open(intl_json_path, "r", encoding="utf-8")
        json_str: str = read_file.read()
        json_data: dict = json.loads(json_str)
        read_file.close()

        # 删除多余的key
        for key in unused_intl_json:
            if key in json_data:
                Print.str("删除 i18n.json 中 " + key + " 键值对")
                del json_data[key]

        # 写入json数据
        initF = open(intl_json_path, "w+", encoding="utf-8")
        initF.write(json.dumps(json_data, indent=4, ensure_ascii=False, sort_keys=True))
        initF.close()

    # 生成 i18n 相关的文件
    def __generate_i18n_files(self, tdfIntlDir, targetModule):
        Print.title("开始生成 i18n 相关的文件")
        if not os.path.exists("i18n"):
            os.mkdir("i18n")

        if not os.path.exists("i18n.json"):
            Print.str("生成" + "i18n.json 文件")
            initF = open(tdfIntlDir + "/i18n.json", "w+", encoding="utf-8")
            initF.write("{}")
            initF.close()

            for value in self.__i18nList:
                i18nType: LanguageType = value
                os.chdir(tdfIntlDir + "/i18n")
                targetFileName = targetModule + "_" + i18nType.str() + ".dart"

                if not os.path.exists(targetFileName):
                    Print.str("生成" + targetFileName + " 文件")
                    newI18nFile = open(targetFileName, "w+")
                    newI18nFile.write(
                        "Map<String, String> " + i18nType.str() + "Map = {\n};"
                    )
                    newI18nFile.close()

    def __check_const_chinese_strs(self, targetModule):
        Print.title("检查是否使用const修饰的中文字符串")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        if len(result.const_chinese) > 0:
            const_chinese_strs = []
            for i in result.const_chinese:
                const_chinese_strs += i.const_chinese_strs
            Print.line()
            Print.str(const_chinese_strs)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上中文有使用到const修饰，是否删除const修饰符 ？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
                for i in result.const_chinese:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()

                    new_file_content = RegularTool.delete_const(
                        new_file_content, const_chinese_strs
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有单引号字符串
    def __check_apostrophe_strs(self, targetModule):
        Print.title("检查是否使用单引号的字符串")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        if len(result.apostrophes) > 0:
            apostrophe_strs = []
            for i in result.apostrophes:
                apostrophe_strs += i.apostrophe_strs
            Print.line()
            Print.str(apostrophe_strs)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上有使用到单引号，是否自动替换为双引号 ？(Y 为确认)："
                )

            if input_str == "Y" or input_str == "y":
                for i in result.apostrophes:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()

                    new_file_content = RegularTool.replace_apostrophe_strs(
                        new_file_content, apostrophe_strs
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有错误导入的 import
    def __check_err_intl_import(self, targetModule):
        Print.title("检查是否有错误导入的 import")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        right_import = FlutterTranslateLint.get_module_import_str(targetModule)
        if len(result.imports) > 0:
            err_imports = []
            for i in result.imports:
                err_imports += i.import_strs
            Print.line()
            Print.str(err_imports)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上 import 错误，是否自动替换 ？(Y 为确认)："
                )

            if input_str == "Y" or input_str == "y":
                for i in result.imports:
                    Print.title("开始替换 import 的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    file_content = read_file.read()
                    for str in i.import_strs:
                        Print.str(
                            "文件：" + i.file_path.split("/")[-1] + "开始替换 import"
                        )
                        file_content = RegularTool.replace_intl_imports(
                            file_content, right_import
                        )
                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有未使用 intl 的中文字符串
    def __check_un_intl_strs(self, targetModule):
        right_import = FlutterTranslateLint.get_module_import_str(targetModule)
        Print.title("检查是否有未使用 intl 的中文字符串")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        if len(result.un_intl_list) > 0:
            un_intl_list = []
            for i in result.un_intl_list:
                un_intl_list += i.un_intl_strs
            Print.line()
            Print.str(un_intl_list)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上中文字符串没使用 intl，是否自动加上 .intl？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
                # 将中文枚举转换成map[file_path:str]，给后面使用，防止在枚举中加上.intl
                chinese_enum_map = {
                    i.file_path: i.enum_strs for i in result.chinese_enums
                }

                for i in result.un_intl_list:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()
                    lint_file_content = RegularTool.delete_remark(
                        new_file_content
                    ).lstrip()
                    # 添加 import
                    if not new_file_content.__contains__(
                        right_import
                    ) and not lint_file_content.startswith("part of"):
                        new_file_content = right_import + "\n" + new_file_content

                    # 替换 intl
                    for str in i.un_intl_strs:
                        Print.str(
                            "文件："
                            + i.file_path.split("/")[-1]
                            + " "
                            + str
                            + " 添加 intl 后缀"
                        )
                    # 先将枚举替换成md5，防止被加上.intl
                    enum_strs = chinese_enum_map.get(i.file_path, [])
                    md5_enum_strs_map: dict[str:str] = {}
                    for enum_str in enum_strs:
                        md5_str = f"【【{hashlib.md5(enum_str.encode('utf-8')).hexdigest()}】】"
                        new_file_content = new_file_content.replace(enum_str, md5_str)
                        md5_enum_strs_map[md5_str] = enum_str

                    # 替换字符，加上 .intl
                    new_file_content = RegularTool.replace_chinese_strs(
                        new_file_content, i.un_intl_strs
                    )

                    # 将md5的枚举恢复
                    for enum_str_md5 in md5_enum_strs_map.keys():
                        new_file_content = new_file_content.replace(
                            enum_str_md5, md5_enum_strs_map[enum_str_md5]
                        )

                    # 删除多个 .intl 结尾
                    new_file_content = RegularTool.replace_multi_intl(new_file_content)

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否更新 i18n.json 文件
    def __check_need_update_json(self, tdfIntlDir, targetModule):
        Print.title("检查是否更新 i18n.json 文件")
        result: TranslateLintResult = FlutterTranslateLint.get_lint_module_result(
            targetModule
        )
        if (
            len(result.new_intl_strs) > 0
            or len(result.un_intl_list) > 0
            or len(result.enum_chinese) > 0
        ):
            un_intl_list = result.new_intl_strs
            un_intl_list += result.enum_chinese
            for i in result.un_intl_list:
                un_intl_list += i.un_intl_strs
            # 没有添加到json中的国际化字段
            new_un_intl_list = list(set(un_intl_list) - set(result.unused_json))
            add_input_str = "N"
            if len(new_un_intl_list) > 0:
                Print.warning("发现以下未添加到intl.dart中的国际化字段:")
                Print.line()
                Print.str(new_un_intl_list)
                Print.line()
                add_input_str = "N"
                if self.__always_yes:
                    add_input_str = "Y"
                else:
                    add_input_str = input(
                        "检查到有以上国际化字符串没加入到 i18n.json，是否自动加入？(Y 为确认)："
                    )

            if add_input_str == "Y" or add_input_str == "y":
                read_file = open(tdfIntlDir + "/i18n.json", "r", encoding="utf-8")
                json_str: str = read_file.read()
                json_data: dict = json.loads(json_str)
                read_file.close()
                with open(tdfIntlDir + "/i18n.json", "w+", encoding="utf-8") as originF:
                    # 添加
                    if add_input_str == "Y" or add_input_str == "y":
                        for i in new_un_intl_list:
                            # 因为正则出来的带转义符，必须去掉转义符后对比
                            i = RegularTool.decode_escapes(i)
                            if not i in json_data.keys():
                                json_data[i] = i
                    json_str = json.dumps(
                        json_data, ensure_ascii=False, indent=4, sort_keys=True
                    )
                    originF.write(json_str)
                    originF.close()
                Print.title("i18n.json 更新成功")

    # 通过 i18n.json 生成各个翻译后的 dart 文件
    def __generate_translate_dart_file(self, tdfIntlDir: str, targetModule: str):
        Print.title("开始通过 i18n.json 生成各个翻译后的 dart 文件")
        with open(tdfIntlDir + "/i18n.json", "r", encoding="utf-8") as originF:
            json_str = originF.read()
            json_data = json.loads(json_str)

            # 遍历i18n目录下的四个存放语言的dart文件
            for value in self.__i18nList:
                i18nType: LanguageType = value
                os.chdir(tdfIntlDir + "/i18n")
                Print.line()
                targetFileName = targetModule + "_" + i18nType.str() + ".dart"

                paramsJson = self.__getTargetFileParamsJson(
                    targetFileName,
                    i18nType.str() + "Map",
                )

                os.chdir(tdfIntlDir + "/i18n")

                for item in json_data:
                    if len(paramsJson) > 0 and item in paramsJson:
                        continue
                    if i18nType.name == LanguageType.ZH.name:
                        paramsJson[r"{0}".format(item)] = r"{0}".format(json_data[item])
                    elif (
                        i18nType.name == LanguageType.EN.name
                        or i18nType.name == LanguageType.TH.name
                        or i18nType.name == LanguageType.CHT.name
                        or i18nType.name == LanguageType.ES.name
                    ):
                        anotherStr = self.__tdf_translate(json_data[item], i18nType)
                        print("翻译：" + json_data[item] + ":" + anotherStr)
                        paramsJson[r"{0}".format(item)] = r"{0}".format(anotherStr)

                # 去除所有翻译失败，value为空的key
                if isinstance(paramsJson, dict):
                    keyList = list(paramsJson.keys())
                    for k in keyList:
                        if not paramsJson[k]:
                            del paramsJson[k]

                with open(targetFileName, "a", encoding="utf-8") as targetFile:
                    targetFile.seek(0)  # 定位
                    targetFile.truncate()  # 清空文件
                    targetFile.write(
                        r"Map<String, String> {0}Map = {1};".format(
                            i18nType.str(),
                            json.dumps(paramsJson, ensure_ascii=False, sort_keys=True),
                        )
                    )
                os.system("dart format {0}".format(targetFileName))

            originF.close()
            self.__generateManagerClass(targetModule)

    def __generateManagerClass(self, moduleName):
        Print.str("生成" + moduleName + "_i18n.dart" + " 文件")
        # 生成manager类
        ShellDir.goInModuleIntlDir(moduleName)

        with open(moduleName + "_i18n.dart", "w+", encoding="utf-8") as managerF:
            managerF.truncate()
            managerF.write(
                """
import 'package:{0}/tdf_intl/i18n/{0}_{TH}.dart';
import 'package:{0}/tdf_intl/i18n/{0}_{EN}.dart';
import 'package:{0}/tdf_intl/i18n/{0}_{ZH}.dart';
import 'package:{0}/tdf_intl/i18n/{0}_{CHT}.dart';
import 'package:{0}/tdf_intl/i18n/{0}_{ES}.dart';
// ignore: implementation_imports
import 'package:tdf_language/tdf_language.dart';

class {1}I18n {{

  static Map<String, Map<String, String>>? i18nMap;
  static Map<String, Map<String, String>> getInstance() {{
      if (i18nMap == null) {{
          i18nMap = Map();
          i18nMap!["{ZH}"] = {ZH}Map;
          i18nMap!["{CHT}"] = {CHT}Map;
          i18nMap!["{EN}"] = {EN}Map;
          i18nMap!["{TH}"] = {TH}Map;
          i18nMap!["{ES}"] = {ES}Map;
      }}
      return i18nMap!;
  }}
}}

extension {1}IntlStringExtension on String {{
  String get intl {{
    return TDFLanguage.intl(
      input: this,
      i18nMap: {1}I18n.getInstance(),
    );
  }}
}}

    """.format(
                    moduleName,
                    self.__getManagerClassName(moduleName),
                    ZH=LanguageType.ZH.str(),
                    CHT=LanguageType.CHT.str(),
                    EN=LanguageType.EN.str(),
                    ES=LanguageType.ES.str(),
                    TH=LanguageType.TH.str(),
                )
            )

    def __getManagerClassName(self, moduleName):
        strList = moduleName.split("_")
        result = ""
        for item in strList:
            result = result + item.capitalize()
        return result

    def __getTargetFileParamsJson(self, targetFileName, mapName):
        with open(targetFileName, "r", encoding="utf-8") as readF:
            try:
                Print.str("解析{0}文件内json数据".format(targetFileName))
                fileData = readF.read()
                fileJsonData = self.correctJsonData(fileData, mapName)
                jsonData = json.loads(fileJsonData, strict=False)
                readF.close()
                return jsonData
            except Exception as e:
                readF.close()
                Print.str(e)
                exit(-1)

    def correctJsonData(self, content, mapName):
        return (
            str(content.replace("Map<String, String> {0} =".format(mapName), ""))
            .replace("\n", "")
            .strip(",};")
            .__add__("}")
        )

    def __tdf_translate(self, content: str, dest_lan: LanguageType):
        try:
            text = self.__translator.translate(
                content, src=LanguageType.ZH, dest=dest_lan
            )
            return text
        except Exception as e:
            Print.str("{0} 翻译失败：{1}".format(content, e))
            return ""

    # 整合各个模块翻译文件到一起
    def integrate(self):
        self.integrate: FlutterTranslateIntegrate = FlutterTranslateIntegrate()
        ShellDir.goInShellDir()
        businessModuleList = self.__businessModuleList()

        Print.str("检测到以下模块可整合翻译文件：")
        Print.str(businessModuleList)

        while True:
            targetModule = input(
                "请输入需要执行整合的模块名(input ! 退出，all 所有模块执行)："
            )
            all_dict = self.integrate.integrate_json_root()
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                all_dict = self.integrate.integrate_json_root()
                for module in businessModuleList:
                    module_dict = self.__integrate_module(module)
                    ####
                    all_dict = self.integrate.merge_dict(module_dict, all_dict)
            else:
                module_dict = self.__integrate_module(targetModule)
                all_dict = self.integrate.merge_dict(module_dict, all_dict)
            self.integrate.write_dict_to_json(all_dict)
            self.integrate.upload_json()
            exit(0)

    # 指定 模块国际化
    def __integrate_module(self, name: str) -> dict[str, dict[str, str]]:
        ShellDir.goInShellDir()
        businessModuleList = self.__businessModuleList()
        if name in businessModuleList:
            Print.title(name + " 模块整合开始执行")
            # pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            Print.title(name + " 模块整合完成")
            return self.integrate.integrate_module(name)
        else:
            Print.error(name + " 模块不在开发列表中")

    def clear_i18n_files(self):
        ShellDir.goInShellDir()
        businessModuleList = self.__businessModuleList()

        Print.str("检测到以下模块可清除翻译文件夹：")
        Print.str(businessModuleList)

        while True:
            targetModule = input(
                "请输入需要执行整合的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.__clear_i18n_module(module)
            else:
                self.__clear_i18n_module(targetModule)
            exit(0)

    def __clear_i18n_module(self, targetModule):
        ShellDir.goInModuleLibDir(targetModule)
        Print.title("开始删除 i18n 相关的文件")
        if os.path.exists("tdf_intl"):
            shutil.rmtree("tdf_intl")
            Print.str("删除 tdf_intl 文件夹完成")
