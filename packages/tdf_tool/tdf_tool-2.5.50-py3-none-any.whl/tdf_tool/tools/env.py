from environs import Env
import importlib.metadata
import os

# 通过 .env 文件定义以下字段调试用
# TDFTOOLS_DEBUG=true
# TDFTOOLS_WORKSPACE=/Users/imwcl/Desktop/2dfire/business_card/flutter_reset_module


class EnvTool:
    def is_debug() -> bool:
        try:
            env = Env()
            env.read_env()
            _debug = env.bool("TDFTOOLS_DEBUG")
            return _debug
        except:
            return False

    def workspaceOrNone() -> str:
        try:
            env = Env()
            env.read_env()
            _workspace = env.str("TDFTOOLS_WORKSPACE")
            return _workspace
        except:
            return None

    def workspace() -> str:
        try:
            env = Env()
            env.read_env()
            _workspace = env.str("TDFTOOLS_WORKSPACE")
            return _workspace
        except:
            return os.getcwd()

    def tdfToolVersion() -> str:
        if EnvTool.is_debug():
            return "2.4.15"
        return importlib.metadata.version("tdf-tool")
