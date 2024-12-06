import sys
from ..conf import PLUGINS_FOLDER
from .importer import PluginImporter


### add plugins directory to sys.path
sys.path.insert(0, str(PLUGINS_FOLDER))


### Components Loader.
components_dir = PLUGINS_FOLDER.joinpath("components")
package_name = "flowtask.plugins.components"
try:
    sys.meta_path.append(PluginImporter(package_name, str(components_dir)))
except ImportError as exc:
    print(exc)
