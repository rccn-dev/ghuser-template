# my_tool

One sentence: what this tool makes, and for whom.

> Made from [ghuser-template](https://github.com/rccn-dev/ghuser-template): a pure
> Python core, tested outside Rhino, shipped as Grasshopper components in one `.yak`.
> Rename the four things below, then delete this note.

## Layout

```
my_tool/
├── pyproject.toml            name, Python, dependencies; [tool.ghuser] for the build
├── src/my_tool/              1. CORE     pure Python + COMPAS. No Rhino in here
├── tests/                    2. SPEC     pytest. What "correct" means
├── components/Mt_*/          3. ADAPTERS one folder per Grasshopper component
│   ├── code.py               │           find the core, call it, convert
│   ├── metadata.json         │           name, inputs, outputs
│   └── icon.png              │           24 x 24
├── yak.json                  the package's description in Rhino's Package Manager
├── scripts/dev.py            4. DEV      components linked into Grasshopper, core read from src/
├── scripts/ghuser.py         5. SHIP     components/ -> dist/*.yak, core inside
├── scripts/tests/            the scripts' own tests (CI runs them; you never edit them)
└── .github/workflows/        6. PIPELINE tests on every push; build, and release on a tag
```

The rule that holds it together: **`src/` never imports Rhino, and
`components/` never contains logic.**

## The samples

Six components in a "My Tool" tab, four panels. Each is the whole path for one
Grasshopper feature: a core function in `src/my_tool/`, its test in `tests/`, and the
adapter in `components/`. Keep the ones you can start from, delete the rest (all three
parts, and the export in `src/my_tool/__init__.py`).

| Panel | Component | Shows |
| --- | --- | --- |
| Structure | `Mt_ColumnGrid` | item inputs: numbers, an optional one with a default; points out |
| Structure | `Mt_GridLabels` | a true/false input, text out; a second row in the panel (`exposure: 4`) |
| Analysis | `Mt_SpanCheck` | a list in (`"scriptParamAccess": "list"`); four outputs; colours; an orange warning |
| Geometry | `Mt_ColumnAxes` | points and a vector in, lines out: Rhino geometry to plain numbers and back |
| Geometry | `Mt_FloorArea` | a curve in; the core's `ValueError` shown as the component's red error |
| Data | `Mt_AreaSchedule` | a tree in and out (`"tree"`), one branch per floor; text out |

What sets each of these, in `metadata.json`:

| Key | Sets | Values |
| --- | --- | --- |
| `category`, `subcategory` | the tab, and the panel in it | any text |
| `exposure` | the row in the panel | `2` first, `4` second, `8` third ...; `-1` hidden |
| `typeHintID` | what an input converts its data to | `int`, `float`, `bool`, `str`, `point`, `vector`, `curve`, `line`, `mesh`, `brep`, `color`, ... |
| `scriptParamAccess` | one item per run, the whole list, or the whole tree | `item`, `list`, `tree` |
| `optional` | may stay unconnected (it then arrives as `None`) | `true`, `false` |

`tests/test_components.py` checks these against what the build accepts, and that
every adapter imports `Grasshopper`, `Rhino` and `System`: Rhino writes type hints
such as `System.Collections.Generic.List[float]` into `RunScript` when you place a
component, and without those names it cannot run.

## Make it yours: rename four things

| What | Where | Example |
| --- | --- | --- |
| the Python package | the folder `src/my_tool/`, `pyproject.toml` (`name`, `packages`, `yak-include`), the imports in `tests/` and `components/*/code.py` | `canopy_kit` |
| the Rhino package | `yak-name` in `pyproject.toml`, `PACKAGE` in every `code.py` (a test checks they match) | `canopy-kit` |
| the component prefix | every folder `components/Mt_*/` and the class name inside its `code.py` (they must match) | `Ck_` |
| who and what | `yak.json`, `description` in `pyproject.toml`, `category` in each `metadata.json`, this README | |

Then check nothing was missed: `grep -rn "my_tool\|my-tool\|Mt_" .` should
print nothing.

## You need

Rhino 8, [uv](https://docs.astral.sh/uv/), git, and Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop/),
OrbStack or colima), running. The first build makes the builder image on your
machine, once: a few minutes.

## Work on it

```bash
uv sync                          # once: creates .venv with the core installed
uv run pytest                    # the spec. Run it after every change
uv run --python 3.9 pytest       # the same, on Rhino 8's Python: what CI runs
```

Add a function: write its test in `tests/` first, then the function in
`src/my_tool/`, then export it from `src/my_tool/__init__.py`.

## See it in Grasshopper

```bash
uv run scripts/dev.py            # build, link into Grasshopper, reload a running Rhino
```

The components now read the core straight from `src/`. Run `dev.py` after every
edit; what else to do depends on what you edited:

| You edit | Then |
| --- | --- |
| `src/` | nothing: the canvas recomputes with the new core |
| a `code.py` | replace that component on the canvas |
| a `metadata.json` or `icon.png`, or add a component | restart Rhino, then replace it |

A component placed on the canvas keeps the `code.py` it was placed with, and a `.gh`
file saves it that way. So a dev component checks, when it loads, that it matches the
latest `dev.py` build. If not, it stops with the reason on it (`dev: replace`,
`dev: restart, replace`) instead of quietly running old code.
`uv run scripts/dev.py status` says what Grasshopper loads and what collides.

To add a component: copy the sample closest to it (item, list or tree; numbers or
geometry) to a new folder, rename the class to match the folder, change the call and
the conversion at the bottom of `code.py`, and list the inputs and outputs in
`metadata.json`. The input names in `RunScript(self, ...)` must be the names in
`metadata.json`, and it returns one value per output; `tests/test_components.py`
checks both.

## Ship it

```bash
uv run scripts/dev.py uninstall          # the dev link and the .yak must not both load
uv run scripts/ghuser.py --version 0.1.0 # dist/my-tool-0.1.0-rh8_0-any.yak
```

The `.yak` is the whole tool: the core travels inside it (`lib/my_tool`). Drag
it onto Rhino 8, **restart Rhino**, and check the components work from the
ribbon before you share it. Components from the dev build now stop
(`dev: not deployed`): replace them with the installed ones in any `.gh` you share.
Uninstall the `.yak` in the Package Manager before going back to `dev.py`.

## Release

```bash
git tag v0.1.0 && git push --tags
```

CI builds, verifies and attaches the `.yak` to a GitHub Release. The tag is
the version: it is written into the package and into every component.

`[tool.ghuser] builder` pins the ghuser-builder release that builds it all.
Change it on purpose, like a lockfile: a newer one can write files an older
Rhino does not load.
