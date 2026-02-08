#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 08 Feb 2026. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT


#// GLOBAL VARIABLES
prefix_main: str = "slt"
prefix_class: str = f"{prefix_main}-obj"
prefix_class_color: str = f"--color-{prefix_class}"
prefix_class_name: str = f"--name-{prefix_class}"

name_class_main: str = f"{prefix_main}-type"

obj_types_unique_abbr: dict[str, str] = {}
obj_types_unique_color: dict[str, tuple[int, int, int]] = {}
obj_types: dict[str, tuple[str, tuple[int, int, int]]] = {
    # -----------------
    # Core / containers
    # -----------------
    "module": ("mod", (110, 118, 129)),
    "namespace": ("nsp", (110, 118, 129)),
    "program": ("prog", (110, 118, 129)),

    # -----------------
    # Types & structures
    # -----------------
    "class": ("cls", (124, 184, 255)),
    "exception": ("expt", (124, 184, 255)),
    "struct": ("str", (124, 184, 255)),
    "union": ("uni", (124, 184, 255)),
    "type": ("type", (124, 184, 255)),
    "concept": ("con", (124, 184, 255)),
    "template": ("tmpl", (124, 184, 255)),
    "alias": ("als", (124, 184, 255)),

    # -----------------
    # Enums
    # -----------------
    "enum": ("enum", (158, 203, 255)),
    "enumerator": ("enum", (158, 203, 255)),

    # -----------------
    # Callables
    # -----------------
    "function": ("func", (210, 168, 255)),
    "method": ("meth", (184, 160, 255)),
    "classmethod": ("meth", (184, 160, 255)),
    "staticmethod": ("meth", (184, 160, 255)),
    "operator": ("opr", (210, 168, 255)),

    # -----------------
    # Decorators
    # -----------------
    "decorator": ("dec", (184, 160, 255)),
    "decoratormethod": ("meth", (184, 160, 255)),

    # -----------------
    # Members & data
    # -----------------
    "data": ("data", (138, 191, 136)),
    "var": ("var", (138, 191, 136)),
    "variable": ("var", (138, 191, 136)),
    "member": ("mbr", (138, 191, 136)),
    "attribute": ("attr", (158, 203, 255)),
    "property": ("prop", (158, 203, 255)),

    # -----------------
    # C-specific
    # -----------------
    "macro": ("mcr", (227, 181, 119)),

    # -----------------
    # reStructuredText
    # -----------------
    "directive": ("dir", (227, 181, 119)),
    "role": ("role", (227, 181, 119)),

    # -----------------
    # Standard domain
    # -----------------
    "label": ("lbl", (227, 181, 119)),
    "term": ("term", (227, 181, 119)),
    "glossary": ("glos", (227, 181, 119)),
    "citation": ("cit", (227, 181, 119)),
    "envvar": ("env", (138, 191, 136)),
    "option": ("opt", (227, 181, 119)),
    "cmdoption": ("cmd", (227, 181, 119)),

    # -----------------
    # Math
    # -----------------
    "equation": ("eqn", (255, 202, 128)),
}


#// LOGIC
def _generate_name(name: str, value: str) -> str:
    abbr: str = ""

    for k, v in obj_types_unique_abbr.items():
        if v == value:
            abbr = f"var({prefix_class_name}-{k})"
            break

    if not abbr:
        obj_types_unique_abbr[name] = value
        abbr = f"\"{value}\""

    return f"\n\t{prefix_class_name}-{name}: {abbr};"


def _generate_color(name: str, value: tuple[int, int, int]) -> str:
    color: str = ""

    for k, v in obj_types_unique_color.items():
        if v == value:
            color = f"var({prefix_class_color}-{k})"
            break

    if not color:
        obj_types_unique_color[name] = value
        color = str(value)[1:-1]

    return f"\n\t{prefix_class_color}-{name}: {color};"


def _generate_class(name: str) -> str:
    cls_start: str = "{"
    cls_end: str = "}"
    return f"""
.{prefix_class}-{name} {cls_start}
    color: rgb(var({prefix_class_color}-{name}));
    background-color: rgba(var({prefix_class_color}-{name}), var(--alpha-{prefix_class}-bg));
{cls_end}
.{prefix_class}-{name}::before {cls_start}
    content: var({prefix_class_name}-{name});
{cls_end}"""


def _generate_template() -> str:
    template: str = """/* Default Local ToC styling */
body {
    --icon-$prefix$-chevron-down: url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10.785 18.355C11.455 19.025 12.545 19.025 13.215 18.355L23.495 8.065C24.165 7.395 24.165 6.315 23.495 5.645C22.825 4.975 21.745 4.975 21.075 5.645L12.005 14.715L2.925 5.645C2.255 4.975 1.175 4.975 0.505 5.645C-0.165 6.315 -0.165 7.405 0.505 8.075L10.785 18.355Z"/></svg>');

    $generate_names$
    
    --color-$prefix$-dropdown: 125, 133, 144;
    --color-$prefix$-dropdown--hover: 221, 229, 240;
    $generate_colors$

    --alpha-$prefix_class$-bg: 0.125;
    --alpha-$prefix$-dropdown-icon: 0.5;

    --font-size-$class_main$: 87%;
    --font-weight-$class_main$: 600;

    --size-$prefix$-dropdown: 1rem;
    --space-$prefix$-dropdown: 0.5rem;
    --space-$class_main$: 0.25rem;
    --padding-$class_main$: 0 0.25rem;

    --border-radius-$class_main$: 0.25rem;
    --transform-$prefix$-dropdown--closed: rotate(-90deg);

    --mask-$prefix$-dropdown: var(--icon-$prefix$-chevron-down) no-repeat center / 90%;
}

/* Base shape */
.$class_main$ {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    vertical-align: middle;
    white-space: nowrap;
    align-self: stretch;
    line-height: 1;
    border-radius: var(--border-radius-$class_main$);
    margin-right: var(--space-$class_main$);
    font-size: var(--font-size-$class_main$);
    font-weight: var(--font-weight-$class_main$);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    padding: var(--padding-$class_main$);
}

/* Dropdown system */
.$prefix$-dropdown {
    display: none;
}
.$prefix$-dropdown ~ ul {
    display: block;
}
.$prefix$-dropdown:checked ~ ul {
    display: none;
}
.$prefix$-dropdown:checked + a .$prefix$-dropdown-icon {
    transform: var(--transform-$prefix$-dropdown--closed);
}
.$prefix$-dropdown-icon {
    display: inline-block;
    vertical-align: middle;
    height: var(--size-$prefix$-dropdown);
    width: var(--size-$prefix$-dropdown);
    background-color: rgba(var(--color-$prefix$-dropdown), var(--alpha-$prefix$-dropdown-icon));
    cursor: pointer;
    transition: transform 0.15s;
    mask: var(--mask-$prefix$-dropdown);
    -webkit-mask: var(--mask-$prefix$-dropdown);
    margin-right: var(--space-$prefix$-dropdown);
}
.$prefix$-dropdown-icon:hover {
    background-color: rgba(var(--color-$prefix$-dropdown--hover), var(--alpha-$prefix$-dropdown-icon));
}
/*.$prefix$-dropdown-branch {}
.$prefix$-dropdown-depth {}*/
.$prefix$-dropdown-leaf {
    margin-left: calc(var(--space-$prefix$-dropdown) + var(--size-$prefix$-dropdown));
}

/* Object type */
$generate_classes$
"""
    names: str = ""
    colors: str = ""
    classes: str = ""

    for key, value in obj_types.items():
        names += _generate_name(key, value[0])
        colors += _generate_color(key, value[1])
        classes += _generate_class(key)

    computed: str = template.replace("$prefix$", prefix_main)
    computed = computed.replace("$prefix_class$", prefix_class)
    computed = computed.replace("$class_main$", name_class_main)
    computed = computed.replace("$generate_names$", names[2:])
    computed = computed.replace("$generate_colors$", colors[2:])
    computed = computed.replace("$generate_classes$", classes[2:])

    return computed


#// RUN
if __name__ == "__main__":
    import msvcrt
    import os
    import sys

    os.system("TITLE Local ToC - CSS Generator")

    msg_prefix: str = ">>"
    msg_hint: str = "Type the file path or drag and drop it here."
    msg_warn: str = "WARNING: The file will be overwrite!"
    msg_no_file: str = "The provided file do not existing..."
    file_path: str = ""

    if len(sys.argv) == 1:
        fail_amount: int = 0
        fail_last: str = ""

        while not file_path:
            print(msg_prefix, msg_hint)
            print(msg_prefix, msg_warn)
            file_path = os.path.abspath(input(f"{msg_prefix} "))

            if not os.path.isfile(file_path):
                fail_last = f"{"\n" if fail_amount == 0 else ""}{msg_prefix} {msg_no_file}\n{msg_prefix} {file_path}\n"

                if fail_amount:
                    os.system("cls" if os.name == "nt" else "clear")

                print(fail_last)

                file_path = ""
                fail_amount += 1

        with open(file=file_path, mode="w", encoding="utf-8") as file:
            file.write(_generate_template())

    print("\n" + msg_prefix, "[ DONE ] The file was modified with success.")
    print(msg_prefix, "Press any key to exit...")
    msvcrt.getch()
