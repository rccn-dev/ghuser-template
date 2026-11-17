"""Grid Labels: the Grasshopper adapter for my_tool.grid_labels. Thin on purpose.

Everything above the line of dashes is the same in every component: it finds
this package's own copy of the core (shipped inside the .yak, in lib/) and
puts it on Python's path. ghuser-build fills in {{version}}. PACKAGE is
yak-name in pyproject.toml.
"""
# r: compas

import glob
import os
import sys

PACKAGE, VERSION = "my-tool", "{{version}}"


def _package_lib():
    # Rhino installs packages to <root>/packages/<rhino version>/<name>/<version>/
    roots = [
        os.path.join(os.environ.get("APPDATA", ""), "McNeel", "Rhinoceros", "packages"),
        os.path.expanduser("~/Library/Application Support/McNeel/Rhinoceros/packages"),
    ]
    for root in roots:
        for lib in sorted(glob.glob(os.path.join(root, "*", PACKAGE, VERSION, "lib")), reverse=True):
            return lib
    return None  # not installed: a dev build (scripts/dev.py) imports the core through `# env:`


_lib = _package_lib()
if _lib and _lib not in sys.path:
    sys.path.insert(0, _lib)

# ---------------------------------------------------------------------------
# Placing a component writes type hints into RunScript's signature, such as
# System.Collections.Generic.List[float], Rhino.Geometry.Curve or
# Grasshopper.DataTree[float]: these three names must exist, or it cannot run.
import Grasshopper  # noqa: E402, F401
import Rhino  # noqa: E402, F401
import System  # noqa: E402, F401
from ghpythonlib.componentbase import executingcomponent as component  # noqa: E402

from my_tool import grid_labels  # noqa: E402


class Mt_GridLabels(component):
    def RunScript(self, nx, ny, letters_along_x):
        if not nx or not ny:
            return None
        # An optional input that is not connected arrives as None: give it its default here.
        along_x = True if letters_along_x is None else letters_along_x
        return grid_labels(nx, ny, along_x)
