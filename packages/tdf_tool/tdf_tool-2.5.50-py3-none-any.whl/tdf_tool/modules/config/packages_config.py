

# 当前项目的packages依赖关系
import json
import os

from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.tools.print import Print


class PackageNode:
    def __init__(self):
        self.packageName: str = ""
        self.packagePath: str = ""  # ，模块根目录下
        self.packageSrcPath: str = ""  # 源代码目录，一般为lib，兼容部分库自定义的源代码目录
        self.isRemote: bool = False


package_config_file_2_2_3 = '.packages'  # flutter 2.2.3版本下的配置文件
package_config_file_3_3_10 = '.dart_tool/package_config.json'  # flutter 3.3.10版本下的配置文件


class PackagesJsonConfig:
    # src_path 读取该目录下的包配置信息
    # 是否根据tdf前缀筛选，默认开启
    def __init__(self, src_path: str, filter_by_tdf: bool = True):
        self.src_path = src_path
        self.filter_by_tdf = filter_by_tdf

        packages_list: list[PackageNode] = self.__config_initial__()

        self.remote_packages = filter(lambda e: e.isRemote, packages_list)
        self.source_packages = filter(lambda e: not e.isRemote, packages_list)
        self.packages = packages_list

    def __config_initial__(self) -> list:
        try:
            if os.path.exists(os.path.join(self.src_path, package_config_file_2_2_3)):
                return self.__load_packages()
            elif os.path.exists(os.path.join(self.src_path, package_config_file_3_3_10)):
                return self.__load_packages_config_json()
            Print.error('没有找到.packages文件或.dart_tool/package_config.json文件')
            exit(1)
        except Exception as e:
            print(e)
            Print.error('配置文件读取异常')
            exit(1)

    def __load_packages_config_json(self) -> list:

        packages_list = []
        with open(os.path.join(self.src_path, package_config_file_3_3_10), "r", encoding="utf-8") as rf:
            jsonData = json.loads(rf.read())
            for item in jsonData['packages']:
                if (str(item['name']).find("tdf") != -1 and self.filter_by_tdf == True) or self.filter_by_tdf == False:
                    node: PackageNode = PackageNode()
                    node.packageName = item['name']
                    replaceStr: str = ''
                    if PlatformTools.is_windows():
                        replaceStr = 'file:///'
                    else:
                        replaceStr = 'file://'

                    if str(item['rootUri']).find(replaceStr) != -1:
                        node.packagePath = os.path.join(
                            str(item['rootUri']).replace(replaceStr, "").replace("%25", "%"))
                        node.packageSrcPath = os.path.join(
                            str(item['rootUri']).replace(replaceStr, "").replace("%25", "%"), item['packageUri'])
                        node.isRemote = True
                    else:
                        node.packagePath = os.path.join(
                            str(item['rootUri'])).replace('../../', '../')  # 存储相对于src_path目录的相对路径

                        node.packageSrcPath = os.path.join(
                            str(item['rootUri']), item['packageUri']).replace('../../', '../')  # 存储相对于src_path目录的相对路径
                        node.isRemote = False

                    packages_list.append(node)

            rf.close()

        return packages_list

    def __load_packages(self) -> list:
        packages_list = []
        with open(os.path.join(self.src_path, package_config_file_2_2_3)) as lines:
            for line in lines:
                if line.startswith("# ") is False:
                    if line.find(":file") != -1:
                        remotePackage = self.__getRemoteCodePackagePath(
                            line)
                        if remotePackage != None:
                            packages_list.append(remotePackage)
                    else:
                        sourcePackage = self.__getSourceCodePackagePath(
                            line)
                        if sourcePackage != None:
                            packages_list.append(sourcePackage)
        return packages_list

        # 获取远程代码路径
    def __getRemoteCodePackagePath(self, line: str) -> PackageNode:
        packageName = line.split(":file://")[0]
        packagePath = line.split(":file://")[1].replace("%25", "%")
        if (packageName.find("tdf") != -1 and self.filter_by_tdf) or self.filter_by_tdf == False:
            packageNode = PackageNode()
            packageNode.packageName = packageName
            if PlatformTools.is_windows():
                packageNode.packagePath = packagePath[1: len(packagePath) - 5]
            else:
                packageNode.packagePath = packagePath[0: len(packagePath) - 5]
            packageNode.packageSrcPath = os.path.join(
                packageNode.packagePath, 'lib')
            packageNode.isRemote = True
            return packageNode

    def __getSourceCodePackagePath(self, line: str) -> PackageNode:
        packageName = line.split(":")[0]
        packagePath = line.split(":")[1].replace("%25", "%")
        if packageName.find("tdf") != -1:
            packageNode = PackageNode()
            packageNode.packageName = packageName
            packageNode.packagePath = packagePath[0: len(packagePath) - 5]
            packageNode.packageSrcPath = os.path.join(
                packageNode.packagePath, 'lib')
            packageNode.isRemote = False
            return packageNode
