#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 01 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import ResultSet
from bs4.element import AttributeValueList
from typing import Iterator

from sphinx.application import Sphinx


#// LOGIC
def _walk_list(root_ul: Tag, depth: int=0) -> Iterator[tuple[int, Tag, Tag|None, bool]]:
    """
    Walk a nested <ul>/<li> tree and yield per <li> metadata.

    For each <ul> level, this function:
        - checks whether any <li> at this level has a nested <ul> (i.e. whether this level is "expandable")
        - iterates over each <li> and reports:
            * current depth
            * the <li> tag itself
            * whether this <li> has a nested <ul>
            * whether any <li> at this level has a nested <ul> at all.

    Yield information about the current <li>:
        - [int]         ➜   Current nesting level
        - [Tag]         ➜   The <li> tag itself
        - [Tag | None]  ➜   The nested <ul> of the <li>
        - [bool]        ➜   Some <li> at this level has a nested <ul>
    """
    # Get all direct <li> children of the current <ul>
    items: ResultSet[Tag] = root_ul.find_all("li", recursive=False)

    # Look one step ahead for nested <ul>
    has_depth: bool = any(li.find("ul", recursive=False) for li in items)

    # Process each <li> at this level
    for li in items:
        # Only bother checking for a nested <ul> if at least one item at this level has it
        ul: Tag|None = None
        if has_depth:
            ul = li.find("ul", recursive=False)

        # Yield information about this <li>
        yield depth, li, ul, has_depth

        # If this <li> has a nested <ul>, recurse into it at the next depth
        if ul is not None:
            yield from _walk_list(ul, depth + 1)


def _previous_li_modified(li: Tag, hint: str, current_depth: int, config_depth: int) -> bool:
    """
    Determine whether the parent <li> of the current item was already modified.

    A parent <li> is considered "modified" if a class is starting with the :param:`hint` either:
        - in the <li> element itself
        - or in the first child tag (usually <input> or <label>)

    :return:    True if was "modified"
    """
    # Skip checks for the very first depth level
    if current_depth == 0 or current_depth == config_depth:
        return False

    # Find the nearest ancestor <li>
    parent_li = li.find_parent("li")

    # # If there's no parent <li>, nothing could have been modified
    if parent_li is None:
        return False

    # Check if the parent <li> itself has the hint related class
    for class_name in parent_li.get("class", []):  # type: ignore[assignment]
        if class_name.startswith(hint):
            return True

    # Check the parent's direct children (e.g. <input> or <label>)
    # These are where dropdown elements are injected
    for child in parent_li.children:
        if isinstance(child, Tag):
            for class_name in child.get("class", []):  # type: ignore[assignment]
                if class_name.startswith(hint):
                    return True

            # First real child tag found, but no hint related class (e.g. <a>) ➜ not modified
            return False

    # Fallback: no modification detected
    return False


def _html_page_context(app: Sphinx, _pn: str, _tm: str, context: dict[str, str|None], _dt: any) -> None:
    """
    Inject dropdown toggles and alignment classes into the Local ToC HTML.

    It rewrites the already rendered ToC HTML by adding:
        - toggle controls to <li> elements that contain nested <ul> lists (i.e. adding <input> and <label>)
        - alignment classes to sibling <li> elements when needed
    """
    # Feature disabled ➜ nothing to do
    if not app.config["localtoc_dropdown"]: return

    # No ToC in the context ➜ skip safely
    # noinspection PyBroadException
    try:
        toc: str|None = context["toc"]
    except BaseException: return

    # Depth offset: skip the first N levels before applying dropdown logic
    ltt_depth: int = max(app.config["localtoc_dropdown_depth"], 0)

    # Counter used to generate unique IDs for toggle inputs
    ltt_index: int = 0

    # Parse the ToC HTML into a BeautifulSoup system for easier life
    soup: BeautifulSoup = BeautifulSoup(toc, "html.parser")

    # Walk through all <li> elements in depth
    for depth, li, ul, has_depth in _walk_list(soup.find("ul")):

        # Apply dropdown logic after the configured offset
        if depth >= ltt_depth:

            # Inject alignment class on the configured offset so starting depth branch items can be customized
            if has_depth and depth == ltt_depth:
                # Find the nearest ancestor <ul> (usually the parent)
                parent_ul: Tag|None = li.find_parent("ul")

                if parent_ul is not None:
                    parent_ul_classes: AttributeValueList = parent_ul.get_attribute_list("class")

                    if "ltt-dropdown-branch" not in parent_ul_classes:
                        parent_ul_classes.append("slt-dropdown-branch")
                        parent_ul["class"] = parent_ul_classes

            # Case 1: this <li> has a nested <ul> ➜ inject dropdown toggle
            if ul is not None:
                ltt_index += 1
                ltt_id: str = f"slt-dropdown-{ltt_index}"

                # Checkbox acts as the toggle state (CSS-driven, no JS)
                tag_input = soup.new_tag(
                    "input",
                    attrs={
                        "type": "checkbox",
                        "role": "switch",
                        "id": ltt_id,
                        "class": "slt-dropdown"
                    }
                )

                # Label acts as the visible dropdown icon
                tag_label = soup.new_tag(
                    "label",
                    attrs={
                        "for": ltt_id,
                        "class": "slt-dropdown-icon"
                    }
                )

                # Insert label elements inside the first child (usually <a>) for easier CSS customizations
                li.find().insert(0, tag_label)
                # Insert input elements before the first child (usually <a>) for easier access of neste <ul> from CSS
                li.insert(0, tag_input)

                # Inject alignment class so nested depth items can be customized
                nested_ul_classes: AttributeValueList = ul.get_attribute_list("class")
                nested_ul_classes.append("slt-dropdown-depth")
                ul["class"] = nested_ul_classes

            # Case 2: this <li> do not have a nested <ul>, but at least one from the same depth level have it
            # Case 3: this is the end of this depth level, but the parent <li> was modified earlier
            # Case 2 & 3 ➜ inject alignment class so leaf items line up visually
            elif has_depth or _previous_li_modified(li, "slt-dropdown", depth, ltt_depth):
                li["class"] = li.get("class", []) + ["slt-dropdown-leaf"]  # type: ignore[assignment]
                
    # Replace the original ToC HTML with the modified version
    context["toc"] = soup.decode()


def setup_dropdown(app: Sphinx) -> None:
    """
    Register configuration values and event hooks for the Local ToC dropdown feature.

    This function is called by Sphinx during extension initialization.

    It defines the user-facing config options and attaches the HTML rewrite handler that injects dropdown toggles
    into the rendered Local ToC.

    Config values added:
        localtoc_dropdown (bool)
            Enable or disable the dropdown system in the local ToC.

        localtoc_dropdown_depth (int)
            Number of initial ToC depth levels to skip before applying dropdown logic.

    Connected events:
        html-page-context
            Used to modify context["toc"] before the page is rendered.
    """
    app.add_config_value(
        "localtoc_dropdown",
        True,
        "html"
    )
    app.add_config_value(
        "localtoc_dropdown_depth",
        1,
        "html"
    )

    app.connect("html-page-context", _html_page_context)
