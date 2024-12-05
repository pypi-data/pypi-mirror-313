
ansi_val: type[str] = str
ansi_code: type[str] = str
ansi_val_collection: type[list[list[ansi_val]]] = list[list[ansi_val]]
ansi_field: type[list[ansi_val_collection]] = list[ansi_val_collection]

# Control Sequence Introducer
CSI = '\033['

# Select Graphic Rendition
SGR = 'm'


def compile_ansi_code(*ansi_vals: ansi_val) -> ansi_code:
    """Feed in any number of colour and style ANSI values and get a
    compiled ANSI code. Passing in no arguments yields the ANSI reset
    code which restores the default text colour and style.

    Example:

    ```python
    flashy_red = compile_ansi_code(
        Colour.RED,
        Colour.CYAN.background,
        Style.BLINK,
        Style.BOLD
    )
    reset = compile_ansi_code()
    print(F"Hello {flashy_red}WORLD{reset}!!!")
    ```"""
    ansi_vals = ansi_vals or ('0', )
    return CSI + ';'.join(ansi_vals) + SGR
