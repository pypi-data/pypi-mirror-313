import json
import os
from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.config.module_json_config import ModuleItemType, ModuleJsonConfig
from tdf_tool.tools.regular_tool import RegularTool
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable
from tdf_tool.tools.workspace import WorkSpaceTool
from tdf_tool.tools.env import EnvTool


class TranslateLintIntl:
    def __init__(self, file_path: str, un_intl_strs: list[str]):
        # 未国际化文件路径
        self.file_path = file_path
        # 文件中没有国际化的字符串
        self.un_intl_strs = un_intl_strs


class TranslateLintApostrophe:
    def __init__(self, file_path: str, apostrophe_strs: list[str]):
        # 单引号文件路径
        self.file_path = file_path
        # 单引号的字符串
        self.apostrophe_strs = apostrophe_strs


class TranslateLintChineseEnum:
    def __init__(self, file_path: str, enum_strs: list[str]):
        # 枚举中有中文的文件路径
        self.file_path = file_path
        # 枚举中有中文的字符串
        self.enum_strs = enum_strs
        # 枚举中的中文
        self.chinese_strs = [RegularTool.find_chinese_str(i) for i in enum_strs]
        # 枚举的名称
        self.enum_names = [RegularTool.find_enum_name(i) for i in enum_strs]


class TranslateLintConstChinese:
    def __init__(self, file_path: str, const_chinese_strs: list[str]):
        # 枚举中有中文的文件路径
        self.file_path = file_path
        # 枚举中有中文的字符串
        self.const_chinese_strs = const_chinese_strs


class TranslateLintImport:
    def __init__(self, file_path: str, import_strs: list[str]):
        # import 错误的文件路径
        self.file_path = file_path
        # import 错误的字符串
        self.import_strs = import_strs


class TranslateLintEnum:
    def __init__(self, file_path: str, enum_strs: list[str]):
        # enum 中带中文的文件路径
        self.file_path = file_path
        # enum 匹配到的字符串
        self.enum_strs = enum_strs


class TranslateLintConst:
    def __init__(self, file_path: str, const_strs: list[str]):
        # const 中带中文的文件路径
        self.file_path = file_path
        # const 匹配到的字符串
        self.const_strs = const_strs


class TranslateLintResult:
    def __init__(
        self,
        un_intl_list: list[TranslateLintIntl],
        new_intl_strs: list[str],
        unused_json: list[str],
        imports: list[TranslateLintImport],
        apostrophes: list[TranslateLintApostrophe],
        const_chinese: list[TranslateLintConstChinese],
        chinese_enums: list[TranslateLintChineseEnum],
        un_format_strs: list[str],
    ):
        # 没有使用 .intl 修饰的中文字符串，不包含枚举中的中文
        self.un_intl_list = un_intl_list
        # 与json文件对比后，新的使用 .intl 修饰的中文字符串
        self.new_intl_strs = list(set(new_intl_strs))
        # 不符合规范的 import
        self.imports = imports
        # 单引号字符串
        self.apostrophes = apostrophes
        # 使用const声明的中文字符串
        self.const_chinese = const_chinese
        # 使用了中文的枚举
        self.chinese_enums = chinese_enums
        # 没有使用format的中文文案
        self.un_format_strs = list(set(un_format_strs))
        # 枚举中的中文字符串，在intl_json中要，去掉这些
        enum_chinese = [
            i
            for sublist in chinese_enums
            for strs in sublist.chinese_strs
            for i in strs
        ]
        self.enum_chinese = list(set(enum_chinese))
        # i18n.json 中没用到的国际化字符串，包含枚举中的中文
        self.unused_json = list(set(unused_json))


class FlutterTranslateLint:
    """
    国际化相关：检测源码中是否还有没国际化的文案
    """

    def start(all_module=False):
        """
        以交互的方式选择需要 lint 的模块
        """
        businessModuleList = FlutterTranslateLint.businessModuleList()
        Print.str("检测到以下模块可执行国际化lint：")
        Print.str(businessModuleList)
        inputStr = "!"
        if all_module:
            inputStr = "all"
        else:
            inputStr = input("请输入需要执行 lint 的模块名(input ! 退出, all 全选)：")

        if inputStr == "!" or inputStr == "！":
            exit(0)
        elif inputStr == "all":
            FlutterTranslateLint.__lint_all()
            exit(0)
        elif inputStr in businessModuleList:
            FlutterTranslateLint.module(inputStr)
            exit(0)

    def module(name: str):
        """
        指定模块 lint
        """
        result = FlutterTranslateLint.get_lint_module_result(name)
        if FlutterTranslateLint.__lint_result(result):
            Print.stage(name + " 模块国际化 lint 通过")
        else:
            Print.error(name + " 模块国际化 lint 失败")

    def path(path: str):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        result = FlutterTranslateLint.__lint_intl_path(path)
        if FlutterTranslateLint.__lint_result(result):
            Print.title(path + " 路径国际化 lint 通过")
        else:
            Print.error(path + " 路径国际化lint 失败")

    def get_lint_module_result(module_name: str) -> TranslateLintResult:
        print("\n")
        Print.title(module_name + " 模块国际化 lint 开始执行")
        target_path = ShellDir.getModuleLibDir(module_name)
        if os.path.exists(target_path):
            return FlutterTranslateLint.__lint_intl_path(target_path)
        else:
            Print.error(target_path + "路径不存在")

    def __lint_all():
        results = []
        pass_result = True
        for module in FlutterTranslateLint.businessModuleList():
            result = FlutterTranslateLint.get_lint_module_result(module)
            results.append(result)
            if not FlutterTranslateLint.__lint_result(result):
                pass_result = False
                Print.error(module + " 模块国际化 lint 失败", shouldExit=False)
            else:
                Print.title(module + " 模块国际化 lint 成功")

        if pass_result:
            print("\n")
            Print.title("国际化 lint 通过")
        else:
            Print.error("国际化 lint 失败")

    # 指定路径 lint，path 的必须是 lib 文件
    def __lint_intl_path(path: str) -> TranslateLintResult:
        # 没有使用 .intl 修饰的中文字符串
        un_intl_list: list[TranslateLintIntl] = []
        # 使用 .intl 修饰的中文字符串
        intl_strs: list[str] = []  # type: ignore
        # 所有的 dart 文件路径
        dart_files: list[str] = []  # type: ignore
        # 使用单引号的字符串
        apostrophes: list[TranslateLintApostrophe] = []
        # 使用const声明的中文字符串
        const_chinese: list[TranslateLintConstChinese] = []
        # 声明中使用了中文的枚举
        use_chinese_enums: list[TranslateLintChineseEnum] = []
        # 没有使用format的中文文案
        un_format_strs: list[str] = []  # type: ignore
        # 不符合的 imports
        imports: list[TranslateLintImport] = []

        module_name = ShellDir.getModuleNameFromYaml(path + "/../pubspec.yaml")
        right_import = FlutterTranslateLint.get_module_import_str(module_name)

        i18n_json: dict = FlutterTranslateLint.__get_i18n_json(path)
        Print.stage("lint 路径：" + path)
        for root, __, files in os.walk(path):
            for file in files:
                # 过滤掉 tdf_intl 目录下的 dart 文件
                if (
                    file.endswith(".dart")
                    and not root.__contains__("/tdf_intl/")
                    and not file.endswith(".tdf_router.dart")
                ):
                    dart_files.append(root + "/" + file)
        for file in dart_files:
            f = open(file)
            file_content = f.read()

            # 寻找使用了中文的枚举
            use_chinese_enum_strs: list[str] = []
            all_enum_strs: list[str] = RegularTool.find_enums(file_content)
            for enum_str in all_enum_strs:
                if RegularTool.find_chinese_str(enum_str) != []:
                    use_chinese_enum_strs.append(enum_str)
                    # 将枚举从file_content中删除
                    file_content = file_content.replace(enum_str, "")

            if len(use_chinese_enum_strs) > 0:
                use_chinese_enums.append(
                    TranslateLintChineseEnum(file, use_chinese_enum_strs)
                )

            file_content = RegularTool.delete_remark(file_content)
            # 所有的 intl import
            all_imports = RegularTool.find_intl_imports(file_content)
            # 错误的 intl import
            err_imports = list(filter(lambda x: x != right_import, all_imports))
            if len(err_imports) > 0:
                un_import = TranslateLintImport(file, err_imports)
                imports.append(un_import)

            # lines = file_content.splitlines()
            # file_content = "".join(lines)
            file_content = RegularTool.delete_track(file_content)
            file_content = RegularTool.delete_router(file_content)
            file_content = RegularTool.delete_widgetsDoc(file_content)
            file_content = RegularTool.delete_noTranslDoc(file_content)
            file_content = RegularTool.delete_deprecated(file_content)

            # 寻找使用 const 声明的中文字符串
            const_chinese_strs = RegularTool.find_chinese_const_str(file_content)
            if len(const_chinese_strs) > 0:
                const_chinese.append(
                    TranslateLintConstChinese(file, const_chinese_strs)
                )

            # 寻找单引号字符串
            apostrophe_strs = RegularTool.find_apostrophe_strs(file_content)
            if len(apostrophe_strs) > 0:
                apostrophe = TranslateLintApostrophe(file, apostrophe_strs)
                apostrophes.append(apostrophe)

            # 寻找加上 .intl 的文案，并删除掉，以免影响 下面的操作
            _intl_strs = RegularTool.find_intl_str(file_content)
            intl_strs += _intl_strs
            file_content = RegularTool.delete_intl_str(file_content)

            # 寻找没有国际化的 文案
            _un_intl_strs = RegularTool.find_chinese_str(file_content)
            _un_format_strs = []
            # 寻找没有使用 format 的文案
            for str in _un_intl_strs:
                un_format_list = RegularTool.find_un_format(str)
                if len(un_format_list) > 0:
                    _un_format_strs.append(str)
            _un_intl_strs = [i for i in _un_intl_strs if i not in _un_format_strs]
            un_format_strs += _un_format_strs

            if len(_un_intl_strs) > 0:
                _un_intl_list = TranslateLintIntl(file, _un_intl_strs)
                un_intl_list.append(_un_intl_list)
            f.close()

        # intl_strs 去重
        intl_strs = list(set(intl_strs))
        new_intl_strs = []
        # 对比加上 .intl 的文案 和 i18n_json里面的差异
        unused_json = list(i18n_json.keys())
        for key in intl_strs:
            # 因为正则出来的带转义符，必须去掉转义符后对比
            key = RegularTool.decode_escapes(key)
            if key in unused_json:
                unused_json.remove(key)
            else:
                new_intl_strs.append(key)

        return TranslateLintResult(
            un_intl_list,
            new_intl_strs,
            unused_json,
            imports,
            apostrophes,
            const_chinese,
            use_chinese_enums,
            un_format_strs,
        )

    # 获取 i8n.json 的数据
    def __get_i18n_json(path: str) -> dict[str:str]:
        target_path = path + "/tdf_intl/i18n.json"
        if os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8") as json_file:
                json_str = json_file.read()
                json_dict = json.loads(json_str)
                return json_dict
        else:
            return {}

    # 校验 lint 的结果
    def __lint_result(result: TranslateLintResult) -> bool:
        if len(result.apostrophes) > 0:
            Print.warning("使用到了单引号字符串，请统一修改为双引号")
            for i in result.apostrophes:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有以下未国际化的字符串：")
                Print.str(i.apostrophe_strs)

        # 枚举中的中文字符串，在lint中要去掉这些
        unused_intl_json = [
            i for i in result.unused_json if i not in result.enum_chinese
        ]
        if len(unused_intl_json) > 0:
            Print.warning("i18n.json 中有以下字符串没有使用到：")
            Print.str(unused_intl_json)

        if len(result.un_intl_list) > 0:
            Print.warning("以下文件中有没国际化的中的字符串：")
            for i in result.un_intl_list:
                file_name = i.file_path.split(r"/")[-1]
                Print.warning(file_name + " 文件中有以下未国际化的字符串：")
                Print.str(i.un_intl_strs)

        if len(result.new_intl_strs) > 0:
            Print.warning("以下 .intl 修饰的字符串没有添加到 i18n.json 中：")
            Print.str(result.new_intl_strs)

        if len(result.imports) > 0:
            Print.warning("以下文件中有没不符合规范的 import ：")
            for i in result.imports:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有以下未国际化的字符串：")
                Print.str(i.import_strs)

        if len(result.const_chinese):
            Print.warning("以下文件中有使用 const 声明中文字符串：")
            for i in result.const_chinese:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有使用const修饰的中文字符串：")
                Print.str(i.const_chinese_strs)

        if len(result.chinese_enums) > 0:
            Print.warning("以下文件中有使用到中文枚举，请检查是否使用intl修饰：")
            for i in result.chinese_enums:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有使用到中文枚举：")
                Print.str(i.enum_names)

        if len(result.un_format_strs) > 0:
            Print.warning("以下文件中没有使用 format 修饰字符串，请修改后再执行脚本：")
            Print.str(result.un_format_strs)

        return (
            len(result.un_intl_list) == 0
            and len(unused_intl_json) == 0
            and len(result.new_intl_strs) == 0
            and len(result.imports) == 0
            and len(result.apostrophes) == 0
            and len(result.const_chinese) == 0
            and len(result.un_format_strs) == 0
        )

    # 获取模块正确的 import 语句
    def get_module_import_str(module_name: str) -> str:
        return "import 'package:{name}/tdf_intl/{name}_i18n.dart';".format(
            name=module_name
        )

    # 可以进行国际化的列表
    def businessModuleList() -> list:
        __initialConfig = InitialJsonConfig()
        __moduleConfig = ModuleJsonConfig()
        businessModuleList = []
        ShellDir.goInShellDir()
        for item in __initialConfig.moduleNameList:
            module_item = __moduleConfig.get_item(item)
            if (
                module_item.type == ModuleItemType.Module
                or module_item.type == ModuleItemType.Lib
                or module_item.type == ModuleItemType.Plugin
                or module_item.type == ModuleItemType.Api
                or module_item.type == ModuleItemType.Flutter
            ):
                gitlab_ci_path = (
                    EnvTool.workspace() + "/../.tdf_flutter/" + item + "/.gitlab-ci.yml"
                )
                if TranslateEnable(gitlab_ci_path).no_translate:
                    continue
                businessModuleList.append(item)
        return businessModuleList
