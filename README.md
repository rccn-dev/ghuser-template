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
└── .github/workflows/        6. PIPELINE tests on every push; build, and release on a tag
```

The rule that holds it together: **`src/` never imports Rhino, and
`components/` never contains logic.**

## Make it yours: rename four things

| What | Where | Example |
| --- | --- | --- |
| the Python package | the folder `src/my_tool/`, `pyproject.toml` (`name`, `packages`, `yak-include`), the imports in `tests/` and `components/*/code.py` | `canopy_kit` |
| the Rhino package | `yak-name` in `pyproject.toml`, `PACKAGE` in every `code.py` (a test checks they match) | `canopy-kit` |
| the component prefix | the folder `components/Mt_ColumnGrid/` and the class name inside its `code.py` (they must match) | `Ck_` |
| who and what | `yak.json`, `description` in `pyproject.toml`, `category` in each `metadata.json`, this README | |

Then check nothing was missed: `grep -rn "my_tool\|my-tool\|Mt_" .` should
print nothing.

## You need

Rhino 8, [uv](https://docs.astral.sh/uv/), git, and Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop/),
OrbStack or colima). Keep the project under your home folder, which Docker shares by default.
The first build makes the builder image on your machine, once: a few minutes.

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

The components now read the core straight from `src/`. Edit it, run `dev.py`
again, and the canvas recomputes with the new code: nothing to reinstall. After
adding a component, run it and restart Grasshopper. `uv run scripts/dev.py status`
says what Grasshopper loads and what collides.

On a Mac this uses your Rhino and no Docker; components show the default icon on
the canvas. On Windows it builds in Docker.

To add a component: copy `components/Mt_ColumnGrid/` to a new folder, rename
the class to match the folder, change the one call and the conversion at the
bottom of `code.py`, and list the inputs and outputs in `metadata.json`. The
input names in `RunScript(self, ...)` must be the names in `metadata.json`;
`tests/test_components.py` checks it.

## Ship it

```bash
uv run scripts/dev.py uninstall          # the dev link and the .yak must not both load
uv run scripts/ghuser.py --version 0.1.0 # dist/my-tool-0.1.0-rh8_0-any.yak
```

The `.yak` is the whole tool: the core travels inside it (`lib/my_tool`). Drag
it onto Rhino 8, **restart Rhino**, and check the components work from the
ribbon before you hand it in. Uninstall it in the Package Manager before going
back to `dev.py`.

## Release

```bash
git tag v0.1.0 && git push --tags
```

CI builds, verifies and attaches the `.yak` to a GitHub Release. The tag is
the version: it is written into the package and into every component.

`[tool.ghuser] builder` pins the ghuser-builder release that builds it all.
Change it on purpose, like a lockfile: a newer one can write files an older
Rhino does not load.
