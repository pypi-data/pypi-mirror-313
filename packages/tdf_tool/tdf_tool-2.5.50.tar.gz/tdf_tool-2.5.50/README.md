## History

### 2.5.35（2024-09-03）
-  规范依赖输出，增加可读性

### 2.5.26（2024-8-13）
-  弃用 tl upgrade，改用 pip3 install tdf_tool --upgrade

### 2.5.23（2024-8-9）
-  deps 命令使用flutter pub deps --json命令获取壳模块直接依赖后，采用递归方式构建完整依赖树（原 deps 命令）

### 2.4.16（2024-4-29）
-  修复 tl module open 命令偶现复用上一个 vscode 窗口的问题；（改为每次新建一个 vscode）

### 2.4.15（2024-4-24）

- 该版本包含自身版本控制逻辑
- 若远端存在新版本，会有提示更新（1.重大更新(强制)，2.api更新(强制)，3.小功能更新，4.无功能更新，5.异常更新）
- 提供远端版本查看链接，可以自行查看版本更新文案自行选择是否更新 tl 命令

### 2.4.13（2024-4-23）

- 新增tl 版本号校验，以便及时告知开发者更新最新版本号

### 2.4.11（2024-4-20）

- 修复路由丢失问题；

### 2.4.7（2024-4-20）

- tl router start 替换为 tl annotation start
- 新增支持通过下标指定模块执行脚本
- 针对新增的 api 自动注册文件，增加 tl 版本号标注，以便出现文件生成不一致，可进行比对

### 2.1.00

- 路由功能支持flutter版本3.3.10，兼容flutter版本2.2.3；

### 2.0.61

- Flutter国际化字符串整合；

### 2.0.38

- 路由生成完后增加路由相关代码format（解决windows代码生成后顺序错乱）；

### 2.0.01

- Cli 框架升级；
- 代码重构；

### **1.1.00（2022-4-28）**

- 国际化解决输出json中包含转义字符的问题，如\n；
- 四类语言输出文件自动格式化

### **1.0.55（2022-4-28）**

- 国际化key使用中文（依照ios项目开发形式）；

### **1.0.53（2022-4-28）**

- 国际化流程中，兼容解决部分json解析失败问题，譬如字符串中包含"="符号；

> 错误日志如：Unterminated string starting at: line 1 column 5650 (char 5649)

### **1.0.50（2022-4-28）**

- 国际化增加繁体字翻译；

## 帮助文档

```shell
NAME
    tdf_tool - 二维火 Flutter 脚手架工具，包含项目构建，依赖分析，git等功能。。

SYNOPSIS
    tdf_tool GROUP | COMMAND

DESCRIPTION
    二维火 Flutter 脚手架工具，包含项目构建，依赖分析，git等功能。。

GROUPS
    GROUP is one of the following:

     module
       模块相关工具： tdf_tool module -h 查看详情

     package
       封包工具相关：tdf_tool package -h 查看详情

     translate
       国际化相关：tdf_tool translate -h 查看详情

COMMANDS
    COMMAND is one of the following:

     git
       tdf_tool git【git 命令】：批量操作 git 命令, 例如 tdf_tool git push

     router
       tdf_tool router：会以交互式进行路由操作，对指定的模块执行路由生成和路由注册逻辑

     upgrade
       tdf_tool upgrade：升级插件到最新版本
        
```

## 插件安装方式

安装python包

```
pip3 install tdf-tool --user
```

安装并更新python包

```
pip3 install --upgrade tdf-tool --user
```

安装测试环境python包

```
pip3 install -i https://test.pypi.org/simple/ tdf-tool --user
```

安装并更新测试环境python包

```
pip3 install --upgrade -i https://test.pypi.org/simple/ tdf-tool --user
```

## 工具使用流程说明

### 1.准备工作

- 确保python的bin插件目录已经被配置到环境变量中（这一步不满足的话，插件安装之后是无法识别到本插件命令的）

- 在~目录下，创建.tdf_tool_config文件并配置相关必需属性如下

```json
git_private_token=***
```

git_private_token是gitlab的token

获取途径：进入gitlab页面，点击右上角头像，选择Preferences，选择左侧列表中的AccessToken进行创建

**上述步骤如果没有做，会在使用插件时，会有提示**

### 2.初始化

#### i.进入壳目录（确保执行命令在壳目录内）

#### ii.执行tdf_tool module init

- 判断当前目录是否存在tdf_cache，若不存在，则会自动创建tdf_cache
- 自动读取当前壳模块名称，写入initial_config.json配置文件；
- 读取当前壳分支，写入initial_config.json配置文件；
- 交互式提示用户输入需要开发的模块名并写入initial_config.json配置文件的moduleNameList列表字段中
- ！退出，即输入完成
- 自动clone所有开发模块到  ```../.tdf_flutter```  隐藏目录中；
- 将所有开发模块分支切换至与壳一致；
- 自动分析依赖树，并**由下至上**对所有模块自动执行```flutter pub upgrade```;

#### iii.开发过程中

##### 1.开发模块添加

- 若是有新模块需要添加入开发模块中，可直接修改initial_config.json配置文件，修改moduleNameList字段；
- 执行tdf_tool deps更新依赖

##### 2.新开发模块添加

- 添加新模块后，会提示找不到模块，实际查找的是```tdf_cache```文件夹中的module_config.json文件；
- 如果没有找到该模块，则可以执行```tdf_tool module-update```,更新远程module_config.json文件；
- 删掉本地的module_config.json文件，重新执行命令即可，脚本会自动判断本地是否存在该配置文件，如果不存在会**下载**；

<span style="color:#ff0000">请确保gitlab仓库的新开发模块master分支是一个flutter模块，如果判定不是flutter模块，则会报错（判定条件为存在pubspec.yaml文件）</span>

### 3.版本控制

版本控制请使用tdf_tool命令，命令详情可使用  ```tdf_tool -h```  查看，现已支持大部分命令，若有特殊命令需要执行，可以使用  ```tdf_tool <git命令>``` ，如：```tdf_tool git add .```

### 4.自动打包发布

暂未接入打包工具，预计下一季度进行支持；

**<span style="color:#ff0000">FAQ</span>**

windows系统请使用bash命令；

## 额外功能说明

### 1.二维数组表达依赖树

生成一个二维数组，可根据该二维数组的数据进行**并发**打tag，每一层的模块，都可以同时进行打tag发布操作，减少发布耗时；

```json
[
 ["tdf_channel", "tdf_event", "tdf_network"], 
 ["tdf_widgets"], 
 ["tdf_smart_devices", "tdf_account_module"], 
 ["flutter_reset_module"]
]
```

如上数据，数组中每一个节点中的模块均可同时打tag，节点之间需要由上至下的顺序进行tag操作

### 2.插件更新

执行 ```tdf_tool upgrade```

### 3.远程模块配置文件更新

执行 ```tdf_tool module module_update```

## 依赖树分析原理

采用有向有/无环图进行依赖树的分析

数据结构采用如下：

```python
class DependencyNode:
    def __init__(self):
        self.nodeName = ''
        self.parent = []  # 父亲节点列表
        self.children = []  # 子孙节点列表
        self.delete = False
```

![dependency](./README_DIR/dependency.png)

如上图1：一个正常的依赖树表示；

如上图2：对图1中，依赖树所有节点去重，变换为图2有向图；

**分析流程：**

**依赖图构建**

```python
# 生成依赖图
    def _generateDependenciesMap(self):
        for package in self.__moduleDependenciesMap:
            for module in moduleNameList:
                if package == module:
                    # 到这一步表明当前这个模块属于开发模块且在当前模块的依赖模块列表中，是当前模块的子模块
                    self._mNodeDict[self.__moduleName].children.append(package)
                    self._mNodeDict[package].parent.append(self.__moduleName)
```

- 共5个节点

  - node构建：

    - ```python
      {
       "模块1":{
          "nodeNmae": "模块1",
          "parent": [],
          "children": ["模块2","模块3","模块4","模块5"],
          "delete": False
       },
       "模块2":{
          "nodeNmae": "模块2",
          "parent": ["模块1"],
          "children": ["模块4","模块5"],
          "delete": False
       }
       "模块3":{
          "nodeNmae": "模块3",
          "parent": ["模块1"],
          "children": ["模块5"],
          "delete": False
       }
       "模块4":{
          "nodeNmae": "模块4",
          "parent": ["模块1","模块2"],
          "children": [],
          "delete": False
       }
       "模块5":{
          "nodeNmae": "模块5",
          "parent": ["模块1","模块2","模块3"],
          "children": [],
          "delete": False
       }
      }
      ```

**依赖图解析伪代码（以一维数组为例）**

```python
# 返回二维数组，用于并发打tag
    def _generateDependenciesOrder(self):
        resList = []
        while 存在节点delete属性不为True:
            
            for：查找子节点为0的节点
             设置节点delete属性为True
              
            for：deleteItemList = 拿到所有delete属性为true的节点

            for：遍历所有节点，如果节点的子节点中包含deleteItemList的节点，则将其从子节点列表中删除
```

- **initial_config.json文件说明**

  ```json
  {
      "featureBranch": "feature/test_dev_1", // 开发分支
      "shellName": "flutter_reset_module",
      // 项目需要开发的模块,可自由配置
      "moduleNameList": [
          "flutter_reset_module",
          "tdf_smart_devices",
          "tdf_widgets",
          "tdf_channel"
      ]
  }
  ```

- **module_config.json文件说明**

  ```json
  {
      "flutter_globalyun_us_module": {
         "id": "11111"
          "type": "shell",
          "git": "git@git.2dfire.net:app/flutter/app/flutter_globalyun_us_module.git"
      },
      "tdf_router_anno": {
          "type": "base",
          "git": "git@git.2dfire.net:app/flutter/app/tdf_router_anno.git"
      },
  }
  //语意
  {
    "模块名":{
      "id": 项目gitlab id
      "类型": gitlab group名
      "git": gitlab地址
    }
  }
  ```

## 后续计划

<span style="color:#ff0000">**问题：**</span>由于现在flutter ci 【lint】【tag】任务脚本成功率过于低，很多时候是因为项目模块的配置问题导致的，且后续会接入一键打tag工具

方案：在执行统一push前，对所有模块的项目配置信息进行校验，确保数据规范；

## 插件打包发布命令

**插件打包命令**

```
poetry build
```

**插件发布命令**

```
poetry publish
```

## vscode 调试配置 ##

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "i18n",
            "type": "python",
            "request": "launch",
            "pythonpath": "/Users/admin/Library/Caches/pypoetry/virtualenvs/tdf-tool-_Qh8vdX_-py3.11/bin/python", // python路径
            "cwd": "${workspaceFolder}",
            "module": "poetry",
            // "justMyCode": false,
            "args": [
                "run",
                "tl",
                "i18n",
                "reflow",
                "start",
            ]
        }
    ]
}
```
