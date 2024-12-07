from hashlib import md5
import os
import shutil
from tdf_tool.modules.config.packages_config import PackageNode, PackagesJsonConfig
from tdf_tool.tools.file_util import TLFileUtil
from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.generator import DefaultGenerator


class ImplNode:
    def __init__(self):
        self.packageName = ""
        self.packagePath = ""
        self.filePath = ""

    def impl_md5(self) -> str:
        return "api_" + md5((self.packageName + self.filePath).encode()).hexdigest()[8:-8]

    def print(self):
        Print.yellow("package:" + self.packageName + "/" + self.filePath)


class ApiNode:
    def __init__(self):
        self.packageName = ""
        self.packagePath = ""
        self.filePath = ""

    def api_md5(self) -> str:
        return "api_" + md5((self.packageName + self.filePath).encode()).hexdigest()[8:-8]

    def print(self):
        Print.yellow("package:" + self.packageName + "/" + self.filePath)


class ApiAnnotation:
    """
    模块间交互支持相关命令：tl api -h 查看详情
    """

    def __init__(self):
        self.ff = None
        self.__generator: str = "InterfaceAnnotationGenerator"  # 生成器名
        self.__implSuffix: str = ".tdf_impl.dart"  # 交互描述文件后缀
        self.__implNodeList: list[ImplNode] = []  # impl描述文件列表
        self.__apiSuffix: str = ".tdf_module_interface.dart"  # 交互api描述文件后缀
        self.__apiNodeList: list[ApiNode] = []  # api描述文件列表
        self.__interactionDir: str = "tdf_interaction"  # 交互文件目录
        self.__annotationName: str = "tdf_module_api_anno"  # 注解库名
        self.__packagesList: list[PackageNode] = []  # 壳依赖的所有库

    # 遍历壳应用.packages下的所有package,将所有tdf开头的模块都添加入packagesList中
    def fetch_packages_list(self):
        ShellDir.goInShellDir()
        # 遍历壳应用的所有package,将所有tdf开头的模块都添加入packagesList中
        self.__packagesList = PackagesJsonConfig(os.getcwd()).packages

    # 整合
    def integrate_shell(self):
        self.fetch_packages_list()
        # 生成交互文件夹
        tdf_api_dir = self.get_interaction_dir()
        auto_register_file = os.path.join(tdf_api_dir, "api_register.dart")
        self.ff = TLFileUtil(auto_register_file, self.__generator)

        # 整合所有 tdf_api.dart 文件
        self.__integrate_tdf_api_files()

        # 整合所有 tdf_impl.dart 文件
        self.__integrate_tdf_impl_files()

        # 生成注册代码
        self.__generate_register_code()

        self.ff.close()

        # 全部生成文件format
        self.__format__()

    def __generate_register_code(self):

        for _item in self.__implNodeList:
            self.____import_data_creator(
                self.ff, _item.packageName, _item.filePath, _item.impl_md5()
            )
        for _item in self.__apiNodeList:
            self.____import_data_creator(
                self.ff, _item.packageName, _item.filePath, _item.api_md5()
            )

        self.__import_data_creator_without_alias(
            self.ff, self.__annotationName, self.__annotationName + ".dart"
        )

        content = """
        
        class TDFApiImplAutoRegister {{
          static List<Type> apis = [
            {0}
          ];
          // 确保所有被引用的api库的实现类都已注册
          static void _ensureApiImplRegister() {{
            apis.forEach((element) {{
              if (!ApiRegisterCenter.keys.contains(element)) {{
                throw Exception("${{element}}的实现类未未注册！！！请删除库${{element}}的引用或者引入实现类");
              }}
            }});
          }}

          static void autoRegister() {{
              {1}
              _ensureApiImplRegister();
          }}
        }}
            """
        self.ff.write(
            content.format(self.api_list_creator(), self.__register_list_creator())
        )

    def __register_list_creator(self):
        content = ""
        for item in self.__implNodeList:
            content += """
            ApiRegisterCenter.register({0}.AutoRegister.apiType,{1}.AutoRegister.provider);
            """.format(
                item.impl_md5(), item.impl_md5()
            )
        return content

    def api_list_creator(self):
        content = ""
        for item in self.__apiNodeList:
            content += """
            {0}.TDFModuleInterfaceAutoInvalidate.apiType,
                    """.format(
                item.api_md5()
            )
        return content

    def __integrate_tdf_impl_files(self):
        Print.title("整合所有交互impl文件")
        for packageItem in self.__packagesList:
            __file_path_list = self.__get_target_file(
                packageItem.packagePath, self.__implSuffix
            )
            for __file_path in __file_path_list:
                _implNode = ImplNode()
                _implNode.packagePath = packageItem.packagePath
                _implNode.packageName = packageItem.packageName
                _implNode.filePath = __file_path
                _implNode.print()
                self.__implNodeList.append(_implNode)

    def __integrate_tdf_api_files(self):
        Print.title("整合所有交互api文件")
        for packageItem in self.__packagesList:
            __file_path_list = self.__get_target_file(
                packageItem.packagePath, self.__apiSuffix
            )
            for __file_path in __file_path_list:
                _apiNode = ApiNode()
                _apiNode.packagePath = packageItem.packagePath
                _apiNode.packageName = packageItem.packageName
                _apiNode.filePath = __file_path
                _apiNode.print()
                self.__apiNodeList.append(_apiNode)

    # 获取指定目录下的指定后缀文件
    def __get_target_file(self, file_path: str, suffix: str) -> list[str]:
        ShellDir.goInShellDir()
        os.chdir(file_path)

        count: int = 0
        __target_file_list: list[str] = []
        nowaPath = os.popen(PlatformTools.pwd_cmd()).read().split("\n")[0]
        for root, dirs, files in os.walk(nowaPath):
            for file in files:
                src_file = os.path.join(root, file)
                if src_file.endswith(suffix):
                    # count += 1
                    if PlatformTools.is_windows():
                        temp = src_file.split("\lib\\")[1]
                        __target_file_list.append(temp.replace("\\", "/"))
                        # __target_file = temp.replace("\\", "/")
                    else:
                        __target_file_list.append(src_file.split("/lib/")[1])
                        # __target_file = src_file.split("/lib/")[1]
        return __target_file_list
        # if count == 1:
        #     return __target_file
        # elif count > 1:
        #     raise Exception("模块{0}存在多个交互文件，请检查❌".format(file_path))
        #     return None
        # return None

    def get_interaction_dir(self):
        ShellDir.goInShellDir()
        os.chdir("lib")
        if os.path.exists(self.__interactionDir):
            shutil.rmtree(self.__interactionDir)
        os.mkdir(self.__interactionDir)
        return os.path.join(ShellDir.getShellDir(), "lib", self.__interactionDir)

    # 对所有self.__interactionDir目录下的文件执行format
    def __format__(self):
        ShellDir.goInShellLibDir()
        __path = os.path.join(ShellDir.getShellDir(), "lib", self.__interactionDir)
        os.system("dart format {0}".format(__path))

    # 生成import数据
    def ____import_data_creator(self, f_write, module_name, file_path, alias):
        f_write.write(
            'import "package:{0}/{1}" as {2};\n'.format(module_name, file_path, alias)
        )

    # 生成import数据(无重命名)
    def __import_data_creator_without_alias(self, f_write, module_name, file_path):
        f_write.write('import "package:{0}/{1}";\n'.format(module_name, file_path))
