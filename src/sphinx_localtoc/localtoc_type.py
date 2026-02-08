#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 30 Jan 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from bs4 import BeautifulSoup
from docutils import nodes
from pathlib import Path

from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment


#// LOGIC
def _html_page_context(app: Sphinx, _pn: str, _tm: str, context: dict[str, str|None], doctree: nodes.document) -> None:
    """
    Inject object‑type CSS markers into Local ToC hyperlinks before HTML rendering.

    This approach is domain‑agnostic and suppose to works for any Sphinx project
    because it relies on Sphinx’s own object classification.
    """
    # Feature disabled ➜ nothing to do
    if not app.config["localtoc_type"]: return

    # No ToC in the context or custom data in doctree ➜ skip safely
    # noinspection PyBroadException
    try:
        toc: str = context["toc"]
        localtoc: dict[str, str] = doctree.asi_localtoc_type
    except BaseException: return

    # Parse the ToC HTML into a BeautifulSoup system for easier life
    soup = BeautifulSoup(toc, "html.parser")

    # Process every hyperlink in the ToC
    for element in soup.find_all("a", recursive=True):
        # Extract the anchor target (strip leading # and whitespace)
        obj_id: str = element.get("href", "#").strip().lstrip("#")
        # Default: no type detected
        obj_type: str = ""

        # Match the anchor ID against our extracted <desc> metadata
        if obj_id in localtoc:
            obj_type = localtoc[obj_id]
            # Remove it to speed up future lookups
            del localtoc[obj_id]

        # If a type was found, inject a <span> decorator into the <a> tag
        if obj_type:
            tag_type = soup.new_tag(
                "span",
                attrs={
                    "class": f"slt-type slt-obj-{obj_type}"
                }
            )

            # Insert tag for the type decorator before the content (text or other tag) of the anchor (<a>)
            element.insert(0, tag_type)

    # Replace the original ToC HTML with the modified version
    context["toc"] = soup.decode()


def _collect_info(app: Sphinx, doctree: nodes.document, _dn: str) -> None:
    """
    Extract structured information from all <desc> nodes in the doctree.

    The result is a dictionary mapping object ID's to their Sphinx‑detected metadata (i.e.: "domain-type").

    This structure is optimized for fast lookup and deletion during HTML rendering, where each ID is consumed once and
    then removed to reduce iteration cost for large ToC's.
    """
    # Feature disabled ➜ nothing to do
    if not app.config["localtoc_type"]: return

    # Access the Sphinx build environment, which persists across all documents during the build.
    # This set is consumed by the assistant CSS generator to create CSS classes for every new detected object type.
    debug_time: bool = app.config["localtoc_type_debug_file"].strip() != ""
    env: BuildEnvironment = app.builder.env
    if debug_time:
        if not hasattr(env, "asi_object_types"):
            env.asi_object_types = set()

    # Dict of extracted objects data for the local ToC type
    ltt: dict[str, str] = {}

    # Iterate over all <desc> nodes (API objects)
    for desc in doctree.findall(addnodes.desc):
        # Basic metadata about the object
        obj_id: str = ""
        obj_domain: str = desc.get("domain", "")
        obj_type: str = desc.get("objtype", "")

        # Only inspect direct children of <desc> to avoid nested <desc> pollution
        for sig in desc.children:
            if isinstance(sig, addnodes.desc_signature):
                # Extract the object ID's assigned by Sphinx
                ids = sig.get("ids", [])
                if len(ids):
                    obj_id = ids[0]
                break

        # Store the extracted object metadata
        ltt[obj_id] = obj_type

        # Add the object's type to the global set of all discovered types.
        if debug_time:
            env.asi_object_types.add(f"{obj_domain}-{obj_type}")

    # Attach the extracted metadata directly to the doctree.
    # Sphinx will serialize this into the .doctree file, and it will be available later in needed methods
    # e.g.: In `html-page-context` as `doctree.asi_localtoc_type`
    doctree.asi_localtoc_type = ltt


def _debug_file(app: Sphinx, exception: Exception|None) -> None:
    """
    Generate a debug CSS file after the Sphinx build completes.

    This file is useful during development to inspect which object types were detected in the current project,
    including their originating domains.

    The output path may be relative (resolved against ``app.confdir``) or absolute, depending on the user configuration.
    """

    # Skip if the build failed
    if exception is not None: return

    # Path provided by the user (may be relative or absolute)
    debug_path: str = app.config["localtoc_type_debug_file"]
    if not debug_path: return

    # Resolve the final path
    debug_file: Path = Path(debug_path)
    if not debug_file.is_absolute():
        debug_file = Path(app.confdir) / debug_file

    # Ensure the parent directory exists
    debug_file.parent.mkdir(parents=True, exist_ok=True)

    # Access the environment where object types were collected
    env: BuildEnvironment = app.builder.env
    object_types = getattr(env, "asi_object_types", set())

    # Compute debug info's
    if len(object_types):
        align_base_css: str = "%-19.19s"
        base_css_classes: list[str] = [
            "%s | Common class for all object type items" % align_base_css % "slt-type",
            "%s | <input> items used as checkbox for dropdown system" % align_base_css % "slt-dropdown",
            "%s | <label> items used for the arrows of dropdown system" % align_base_css % "slt-dropdown-icon",
            "%s | Starting depth branch for <ul> items" % align_base_css % "slt-dropdown-branch",
            "%s | Nested depth branch for <ul> items" % align_base_css % "slt-dropdown-depth",
            "%s | Last <li> items in the depth branch" % align_base_css % "slt-dropdown-leaf",
        ]
        domain_name: dict[str, str] = {
            "py": "Python script",
            "js": "Java script",
            "c": "C language",
            "cpp": "C++ language",
            "rst": "reStructuredText",
            "std": "Standard",
            "math": "Math",
        }
        domains: set[str] = set()
        obj_types: set[str] = set()
        css_classes: set[str] = set()

        for value in sorted(object_types):
            dot: tuple[str, str] = value.split("-", 1)

            obj_types.add("%-4.4s | %s" % (dot[0], dot[1]))
            css_classes.add(f"slt-obj-{dot[1]}")

            if dot[0] in domain_name.keys():
                domains.add("%-4.4s | %s" % (dot[0], domain_name[dot[0]]))
            else:
                domains.add(dot[0])

        # Create or overwrite the debug file
        with debug_file.open("w", encoding="utf8") as file:
            decorator: dict[str, str] = {
                "line": f"#//|>{"-" * 113}<|",
                "line-short": f"#//|>{"-" * 56}<|",
                "prefix": "#//|"
            }
            debug_title: list[str] = [
                decorator["line"],
                f"{decorator["prefix"]} Debug Local ToC report for Sphinx extension",
                f"{decorator["prefix"]} Project: {getattr(app.config, "project", "<unknown project>")}",
                f"{decorator["prefix"]} Version: {getattr(app.config, "version", "<no-version>")}",
                decorator["line"]
            ]
            file.write("\n".join(debug_title))

            for category, values in {
                "CSS class|es": base_css_classes,
                "object type CSS class|es": css_classes,
                "domain|s": domains,
                "object type|s": obj_types,
            }.items():
                category_amound: int = len(values)
                category_title: str = f"One {category.split("|")[0]} used"

                if category_amound > 1:
                    category_title = f"Used {category.replace("|", "")}: {category_amound}"

                file.write("\n\n{line}\n{prefix} {title}\n{line}".format(
                    line=decorator["line-short"], prefix=decorator["prefix"], title=category_title)
                )

                for value in sorted(values):
                    file.write(f"\n\t\u2022 {value}")

                file.write("\n")


def setup_type(app: Sphinx) -> None:
    """
    Register configuration values and event hooks for the Local ToC "type decoration" feature.

    This feature allows the extension to decorate ToC entries based on their object type.

    The user can enable/disable the feature entirely, choose which types should be shown and define a fallback type
    for unknown entries.

    Config values added:
        localtoc_type (bool)
            Enable or disable object type annotations in the local ToC.

        localtoc_type_debug_file (str)
            Absolute or relative path (including filename) to a debug log file.

            The path may point inside the project's "conf" directory or anywhere else.
            If the file does not exist, it will be created. If it already exists, it will be overwritten.

    Connected events:
        doctree-resolved
            Extract object metadata from <desc> nodes and attach it to the doctree for later use.

        html-page-context
            Used to rewrite context["toc"] and inject type decorations.

        build-finished
            Run the assistant generator after all doctrees have been processed and all pages rendered.
    """
    app.add_config_value(
        "localtoc_type",
        True,
        "env"
    )
    app.add_config_value(
        "localtoc_type_debug_file",
        "",
        "env"
    )

    app.connect("doctree-resolved", _collect_info)
    app.connect("html-page-context", _html_page_context)
    app.connect("build-finished", _debug_file)
