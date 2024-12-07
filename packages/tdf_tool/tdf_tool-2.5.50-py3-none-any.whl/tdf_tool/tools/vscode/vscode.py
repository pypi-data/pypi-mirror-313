import os
from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class VsCodeManager(object):
    def openFlutterProject(self):
        tdf_flutter_path = ShellDir.getInTdfFlutterDir()
        shell_path = ShellDir.getShellDir()

        os.system("code -a {0} -a {1} -n".format(tdf_flutter_path, shell_path))
