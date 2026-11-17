"""Area Schedule: the Grasshopper adapter for my_tool.area_schedule. Thin on purpose.

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

from my_tool import area_schedule  # noqa: E402


class Mt_AreaSchedule(component):
    def RunScript(self, areas):
        if areas is None or areas.DataCount == 0:
            return None, None, None
        # Tree access: the whole tree at once. One branch per floor; the core sees lists of lists.
        paths = list(areas.Paths)
        floors = [[float(a) for a in areas.Branch(path)] for path in paths]
        totals, shares, report = area_schedule(floors)
        # A tree out, on the same paths as the tree in.
        tree = Grasshopper.DataTree[object]()
        for path, branch in zip(paths, shares):
            tree.EnsurePath(path)
            for share in branch:
                tree.Add(share, path)
        return totals, tree, report
