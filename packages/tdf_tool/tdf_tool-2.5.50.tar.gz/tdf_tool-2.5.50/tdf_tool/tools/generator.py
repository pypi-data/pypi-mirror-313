
from tdf_tool.tools.env import EnvTool
class DefaultGenerator:
    def defaultTitleDesc(generator_name: str) -> str:
        return """
// GENERATED CODE - DO NOT MODIFY BY HAND
    
// tdf-tool
// version: {0}
    
// **************************************************************************
// {1}
// **************************************************************************
            """.format(EnvTool.tdfToolVersion(), generator_name)