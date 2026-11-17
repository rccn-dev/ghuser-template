"""Span Check: the Grasshopper adapter for my_tool.check_spans. Thin on purpose.

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
from System.Drawing import Color  # noqa: E402
from ghpythonlib.componentbase import executingcomponent as component  # noqa: E402

from my_tool import check_spans  # noqa: E402


PASS, FAIL = Color.FromArgb(90, 140, 110), Color.FromArgb(200, 60, 50)


class Mt_SpanCheck(component):
    def RunScript(self, spans, limit):
        if not spans or not limit:
            return None, None, None, None
        # List access: spans is the whole list at once, not one item per run.
        report = check_spans([float(s) for s in spans], limit)
        if report.failures:
            # ghenv is the component itself, given by Grasshopper: an orange balloon, the run goes on.
            ghenv.Component.AddRuntimeMessage(  # noqa: F821
                Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, f"{report.failures} of {len(spans)} spans are over {limit} m")
        colours = [PASS if ok else FAIL for ok in report.ok]
        return report.ok, report.failures, report.worst, colours
