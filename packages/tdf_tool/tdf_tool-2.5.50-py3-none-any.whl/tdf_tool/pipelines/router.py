from hashlib import md5
from io import TextIOWrapper
import os
import shutil
from tdf_tool.modules.config.packages_config import PackageNode, PackagesJsonConfig
from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class RouterNode:
    def __init__(self):
        self.package = ""
        self.routerPath = ""
        self.filePath = ""
        self.note = ""
        self.pageWidget = ""
        self.isMainPage = False


class Router:
    """
    路由相关命令：tl router -h 查看详情
    """

    def __init__(self):
        self.__packagesList: list[PackageNode] = []
        # 文档数据
        self.__macDownDataList: list[RouterNode] = []
        # 业务入口页列表
        self.__mainPageData: list[RouterNode] = []

        self.__entryPagePath = "tdf-flutter://2dfire.com/business/entry"
        self.__entryPageNote = "flutter entry"
        self.__entryPageWidget = "TZRouterBusinessEntryPage"

        ShellDir.dirInvalidate()

    def integrate(self):
        """
        tl router integrate：对壳进行路由整合
        """
        ShellDir.dirInvalidate()
        self.fetch__packagesList()
        self.integrate_shell()
        Print.title("壳模块路由整合完成")
        exit(0)

    # 遍历壳应用.packages下的所有package,将所有tdf开头的模块都添加入packagesList中
    def fetch__packagesList(self):
        ShellDir.goInShellDir()
        # 遍历壳应用的所有package,将所有tdf开头的模块都添加入packagesList中
        self.__packagesList = PackagesJsonConfig(os.getcwd()).packages

    # 整合壳的路由文件
    def integrate_shell(self):
        self.fetch__packagesList()
        # 整合所有路由文件到壳里
        self.__integrate_all_routing_files()

        # 生成路由 初始化文件
        self.__generate_router_init_files()

        # 生成路由入口文件
        self.__generate_router_entry_files()

        # 生成路由文档
        self.__generate_router_doc()

        # 全部生成文件format
        self.__format__()

    # 整合所有路由文件到壳里
    def __integrate_all_routing_files(self):
        Print.title("整合所有路由文件到壳里")
        ShellDir.goInShellDir()
        os.chdir("lib")
        if os.path.exists("tz_router"):
            shutil.rmtree(r"tz_router")
        os.mkdir("tz_router")
        os.chdir("tz_router")
        os.mkdir("group")

        for packageItem in self.__packagesList:
            # 存在路由描述文件才进行遍历
            ShellDir.goInShellDir()
            if self.__hasRouterDartFile(packageItem.packagePath):
                os.chdir(ShellDir.getShellDir() + "/lib/tz_router/group/")
                os.mkdir(packageItem.packageName)
                os.chdir(packageItem.packageName)
                file_name = "router_map.dart"
                f = open(file_name, "w+")
                self.__defaultImportCreator(f, "'package:tdf_router/tdf_router.dart';")

                ShellDir.goInShellDir()
                os.chdir(packageItem.packagePath)

                nowaPath = os.popen(PlatformTools.pwd_cmd()).read().split("\n")[0]

                routerAliasFileList = []
                routerFileList = []
                for root, _, files in os.walk(nowaPath):
                    for file in files:
                        src_file = os.path.join(root, file)
                        if src_file.endswith(".tdf_router.dart"):
                            itemModuleName = packageItem.packageName
                            if PlatformTools.is_windows():
                                temp = src_file.split("\lib\\")[1]
                                itemFilePath = temp.replace("\\", "/")
                            else:
                                itemFilePath = src_file.split("/lib/")[1]
                            itemFileAlias = (
                                "tdf_router_"
                                + md5(itemFilePath.encode()).hexdigest()[8:-8]
                            )

                            self.__importDataCreator(
                                f, itemModuleName, itemFilePath, itemFileAlias
                            )
                            routerAliasFileList.append(itemFileAlias)
                            routerFileList.append(src_file)
                if len(routerAliasFileList) > 0:
                    Print.stage(
                        "模块{:>30}  检测到  {:>3}  个路由".format(
                            packageItem.packageName, len(routerAliasFileList)
                        )
                    )
                    self.__groupRouterClassCreator(
                        f, packageItem.packageName, routerAliasFileList
                    )
                    if PlatformTools.is_windows():
                        self.__addInWindowDownData(routerFileList)
                    else:
                        self.__addInMacDownData(routerFileList)

                f.close()

    # 生成路由 初始化文件
    def __generate_router_init_files(self):
        Print.title("生成路由初始化文件")
        ShellDir.goInShellDir()
        os.chdir("lib/tz_router")

        file_name = "init.dart"
        initF = open(file_name, "w+")

        # 生成初始化init文件
        if os.path.exists("group") == False:
            os.mkdir("group")
        os.chdir("group")
        nowaPath = os.popen(PlatformTools.pwd_cmd()).read().split("\n")[0]
        self.__defaultImportCreator(initF, "'package:tdf_router/tdf_router.dart';")
        # 添加flutter业务入口页面import
        self.__defaultImportCreator(initF, "'entry/tz_router_entry_page.dart';")
        mapList = []
        for root, _, files in os.walk(nowaPath):
            for file in files:
                src_file = os.path.join(root, file)
                if src_file.find(file_name) != -1:
                    continue
                if PlatformTools.is_windows():
                    tmpItemFilePath = src_file.split("tz_router")[1]
                    itemFilePath = tmpItemFilePath.replace("\\", "/")
                else:
                    itemFilePath = src_file.split("tz_router")[1]
                itemFileAlias = (
                    "router_map_" + md5(itemFilePath.encode()).hexdigest()[8:-8]
                )
                importContent = 'import ".{0}" as {1};\n'.format(
                    itemFilePath, itemFileAlias
                )
                initF.write(importContent)
                mapList.append(itemFileAlias)

        initF.write(
            """

        class TZRouterManager {{
            static combineMap() {{
                Map<String, TDFPageBuilder> map = Map();
                {0}
                return map;
            }}
        }}
        """.format(
                self.__mapListCombineCreater(mapList)
            )
        )

        initF.close()

    # 生成路由入口文件

    def __generate_router_entry_files(self):
        Print.title("生成路由入口文件")
        ShellDir.goInShellDir()
        os.chdir("lib/tz_router")
        # os.chdir(shellPath + "/lib/tz_router")
        if os.path.exists("entry") == False:
            os.mkdir("entry")

        os.chdir("entry")

        file_name = "tz_router_entry_page.dart"
        entryPageF = open(file_name, "w+", encoding="utf8")

        self.__defaultImportCreator(entryPageF, "'package:flutter/material.dart';")
        self.__defaultImportCreator(entryPageF, "'package:tdf_router/tdf_router.dart';")
        self.__defaultImportCreator(
            entryPageF, "'package:tdf_router_anno/router/router_anno.dart';"
        )
        self.__defaultImportCreator(
            entryPageF, "'package:tdf_base_utils/tdf_base_utils.dart';"
        )
        self.__defaultImportCreator(
            entryPageF, "'package:tdf_widgets/tdf_common_btn/tdf_btn.dart';"
        )
        self.__defaultImportCreator(
            entryPageF, "'package:tdf_widgets/title_bar/tdf_title_bar.dart';"
        )
        entryPageF.write(
            """

@TZRouter(path: '{0}', note: '{1}')
class {2} extends StatefulWidget {{
    final Map params;

    {2}(this.params);

    @override
    _{2}State createState() => _{2}State();
}}

class _{2}State extends State<{2}> {{
    final TextEditingController routerController = new TextEditingController();
    final TextEditingController controller = new TextEditingController();
    final Map<String, String> pageMap = {{
    {3}
    }};

    @override
    Widget build(BuildContext context) {{
        TDFScreen.init(context);
        return Scaffold(
            backgroundColor: Color(0xffffffff),
            appBar: TDFTitleBar(
                titleContent: \"{4}\",
                backType: TDFTitleBackWidgetType.DEFAULT_BACK,
                rightContent: "UI标准化",
                rightContentColor: 0xff0088ff,
                rightTextBtnClick: () {{
                TDFRouter.open("tdf-manager://2dfire.com/ticket/index", urlParams: {{
                    "app_key": "200800",
                    "h5url": "http://10.1.16.14:8111/"
                }});
                }},
            ),
            body: SingleChildScrollView(
                child: Column(
                    children: _getButtonList(),
                ),
            ),
        );
    }}

    List<Widget> _getButtonList() {{
        List<Widget> list = [];
        list.add(_routerJumpWidget());
        list.add(Padding(
        padding: EdgeInsets.only(top: 20.w),
        child: TDFButton(
            content: \"根据路由跳转\",
            bgColor: 0xff0088ff,
            contentColor: 0xffffffff,
            onClick: () {{
            FocusScope.of(context).requestFocus(FocusNode());
            TDFRouter.open(routerController.text);
            }},
        ),
        ));
        list.add(_searchWidget());

        List<Widget> wrapEntrylist = [];
        pageMap.forEach((key, value) {{
        if (key.contains(controller.text)) {{
            wrapEntrylist.add(GestureDetector(
                onTap: () {{
                FocusScope.of(context).requestFocus(FocusNode());
                TDFRouter.open(value);
                }},
                child: ClipRRect(
                borderRadius: BorderRadius.all(Radius.circular(3.w)),
                child: Container(
                    color: Colors.blue,
                    padding: EdgeInsets.only(
                        left: 7.w, right: 7.w, top: 4.w, bottom: 4.w),
                    child: Text(
                    key,
                    style: TextStyle(fontSize: 13.w),
                    ),
                ),
                )));
        }}
        }});
        list.add(SizedBox(
        height: 20.w,
        ));
        list.add(Wrap(
        spacing: 15.w,
        runSpacing: 10.w,
        children: wrapEntrylist,
        ));
        return list;
    }}

    Widget _routerJumpWidget() {{
        return TextField(
        controller: routerController,
        autofocus: false,
        decoration: InputDecoration(hintText: "输入页面路由"),
        onChanged: (value) {{
            setState(() {{}});
            }},
        );
    }}

    Widget _searchWidget() {{
        return TextField(
            controller: controller,
            autofocus: false,
            decoration: InputDecoration(hintText: "筛选"),
            onChanged: (value) {{
                setState(() {{}});
            }},
        );
    }}
    
}}
        """.format(
                self.__entryPagePath,
                self.__entryPageNote,
                self.__entryPageWidget,
                self.__mainPageDataCreator(),
                self.__entryPageNote,
            )
        )
        entryPageF.close()

    # 生成路由文档
    def __generate_router_doc(self):
        Print.title("生成路由文档")
        ShellDir.goInShellDir()
        if os.path.exists("路由文档") == True:
            shutil.rmtree(r"路由文档")
        os.mkdir("路由文档")
        os.chdir("路由文档")

        f = open("document.md", "w+")

        ShellDir.goInShellDir()
        # os.chdir(shellPath)
        curDir = ShellDir.getShellDir()
        for root, dirs, files in os.walk(curDir):
            for file in files:
                src_file = os.path.join(root, file)
                if src_file.find("pubspec.yaml") != -1:
                    if PlatformTools.is_windows():
                        with open("pubspec.yaml", "rb") as lines:
                            for line in lines:
                                if line.find(bytes("name: ", encoding="utf8")) != -1:
                                    f.write(
                                        "## Flutter壳应用（{0}）路由表\n".format(
                                            line.split(
                                                bytes("name: ", encoding="utf8")
                                            )[1].split(bytes("\n", encoding="utf8"))[0]
                                        )
                                    )
                                break
                    else:
                        with open("pubspec.yaml") as lines:
                            for line in lines:
                                if line.find("name: ") != -1:
                                    f.write(
                                        "## Flutter壳应用（{0}）路由表（共{1}个页面）\n".format(
                                            line.split("name: ")[1].split("\n")[0],
                                            len(self.__macDownDataList)
                                        )
                                    )
                                break

        f.write(
            '<table><thead><tr><th>{0}</th><th style = "min-width:150px !important">{1}</th><th>{2}</th></tr></thead>'.format(
                "组件名", "描述", "详情"
            )
        )
        f.write("<tbody>")

        for item in self.__macDownDataList:
            f.write(
                "<tr><th>{0}</th><th>{1}</th><th>{2}<br/>{3}<br/>{4}</th></tr>\n".format(
                    item.package,
                    item.note,
                    "类名:  " + item.pageWidget,
                    "路由:  " + item.routerPath,
                    "文件:  " + item.filePath,
                )
            )

        f.write("</tbody></table>")

        f.close()

    # 对所有tz_router目录下的文件执行format
    def __format__(self):
        ShellDir.goInShellLibDir()
        os.system("dart format ./tz_router")

    # 获取远程代码路径
    def __getRemoteCodePackagePath(self, line: str) -> PackageNode:
        packageName = line.split(":file://")[0]
        packagePath = line.split(":file://")[1].replace("%25", "%")
        if packageName.find("tdf") != -1:
            packageNode = PackageNode()
            packageNode.packageName = packageName
            if PlatformTools.is_windows():
                packageNode.packagePath = packagePath[1 : len(packagePath) - 5]
            else:
                packageNode.packagePath = packagePath[0 : len(packagePath) - 5]
            packageNode.isRemote = True
            return packageNode

    def __getSourceCodePackagePath(self, line: str) -> PackageNode:
        packageName = line.split(":")[0]
        packagePath = line.split(":")[1].replace("%25", "%")
        if packageName.find("tdf") != -1:
            packageNode = PackageNode()
            packageNode.packageName = packageName
            packageNode.packagePath = packagePath[0 : len(packagePath) - 5]
            packageNode.isRemote = False
            return packageNode

    # 判断指定目录下是否存在.tdf_router.dart结尾的文件
    def __hasRouterDartFile(self, dirPath):
        os.chdir(dirPath)
        nowaPath = os.popen(PlatformTools.pwd_cmd()).read().split("\n")[0]
        for root, dirs, files in os.walk(nowaPath):
            for file in files:
                src_file = os.path.join(root, file)
                if src_file.endswith(".tdf_router.dart"):
                    return True
        return False

    def __defaultImportCreator(self, mFileWriter, content):
        mFileWriter.write("import {0}\n".format(content))

    # 生成import数据
    def __importDataCreator(
        self, mFileWriter, itemModuleName, mFilePath, itemFileAlias
    ):
        mFileWriter.write(
            'import "package:{0}/{1}" as {2};\n'.format(
                itemModuleName, mFilePath, itemFileAlias
            )
        )

    # 路由map类生成器
    def __groupRouterClassCreator(self, mFileWriter: TextIOWrapper, moduleName, list):
        content = """
    routerMap() {{
        Map<String, TDFPageBuilder> map = Map();
        {1}
        return map;
    }}
    """
        mFileWriter.write(content.format(moduleName, self.__mapAddListCreator(list)))

    def __mapAddListCreator(self, list):
        content = ""
        for item in list:
            content += """map.putIfAbsent({0}.getRouterPath(), () =>  (String pageName, Map params, String _) => {1}.getPageWidget(params));
        """.format(
                item, item
            )
        return content

    def __addInWindowDownData(self, routerFileList):
        bytesTemp = bytes("\n", encoding="utf8")
        for fileItem in routerFileList:
            result = fileItem
            if len(fileItem) > 260:
                temp = "\\\\?\\"
                temp2 = fileItem
                result = temp + fileItem
            with open(result, "rb") as lines:
                node = RouterNode()
                for line in lines:
                    if line.find(bytes(" //#package#//", encoding="utf8")) != -1:
                        node.package = line.split(
                            bytes("//#package#//", encoding="utf8")
                        )[1].split(bytesTemp)[0]
                    if line.find(bytes("//#routerPath#//", encoding="utf8")) != -1:
                        node.routerPath = line.split(
                            bytes("//#routerPath#//", encoding="utf8")
                        )[1].split(bytesTemp)[0]
                    if line.find(bytes("//#filePath#//", encoding="utf8")) != -1:
                        node.filePath = line.split(
                            bytes("//#filePath#//", encoding="utf8")
                        )[1].split(bytesTemp)[0]
                    if line.find(bytes("//#note#//", encoding="utf8")) != -1:
                        node.note = str(
                            line.split(bytes("//#note#//", encoding="utf8"))[1].split(
                                bytesTemp
                            )[0],
                            encoding="utf8",
                        )
                    if line.find(bytes("//#pageWidget#//", encoding="utf8")) != -1:
                        node.pageWidget = line.split(
                            bytes("//#pageWidget#//", encoding="utf8")
                        )[1].split(bytesTemp)[0]
                    if line.find(bytes("//#isMainPage#//", encoding="utf8")) != -1:
                        node.isMainPage = (
                            line.split(bytes("//#isMainPage#//", encoding="utf8"))[
                                1
                            ].split(bytesTemp)[0]
                            == "true"
                        )
                self.__macDownDataList.append(node)
                if node.isMainPage == True:
                    self.__mainPageData.append(node)

    def __addInMacDownData(self, routerFileList):
        for fileItem in routerFileList:
            with open(fileItem) as lines:
                node = RouterNode()
                for line in lines:
                    if line.find("//#package#//") != -1:
                        node.package = line.split("//#package#//")[1].split("\n")[0]
                    if line.find("//#routerPath#//") != -1:
                        node.routerPath = line.split("//#routerPath#//")[1].split("\n")[
                            0
                        ]
                    if line.find("//#filePath#//") != -1:
                        node.filePath = line.split("//#filePath#//")[1].split("\n")[0]
                    if line.find("//#note#//") != -1:
                        node.note = line.split("//#note#//")[1].split("\n")[0]
                    if line.find("//#pageWidget#//") != -1:
                        node.pageWidget = line.split("//#pageWidget#//")[1].split("\n")[
                            0
                        ]
                    if line.find("//#isMainPage#//") != -1:
                        node.isMainPage = (
                            line.split("//#isMainPage#//")[1].split("\n")[0] == "true"
                        )
                self.__macDownDataList.append(node)
                if node.isMainPage == True:
                    self.__mainPageData.append(node)

    def __mapListCombineCreater(self, list):
        content = ""
        for item in list:
            content += "map.addAll({0}.routerMap());\n".format(item)
        content += 'map.putIfAbsent("{0}", () => (String pageName, Map params, String _) => {1}(params));'.format(
            self.__entryPagePath, self.__entryPageWidget
        )
        return content

    def __mainPageDataCreator(self):
        content = ""
        for item in self.__mainPageData:
            if item.isMainPage:
                content += '"{0}":"{1}",\n'.format(item.note, item.routerPath)
        return content
