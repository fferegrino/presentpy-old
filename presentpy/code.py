import shlex
from functools import lru_cache
from typing import Any, Dict, List, Tuple

import pygments
import pygments.styles
from pptx.dml.color import RGBColor
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

from presentpy.code_cell_config import CodeCellConfig


def get_config_from_source(source: str) -> Tuple[str, CodeCellConfig]:
    source_lines = source.strip().split("\n")
    config = {}
    if source_lines[-1].startswith("#%"):
        config = {
            key: value for key, _, value in [conf.partition("=") for conf in shlex.split(source_lines[-1][2:].strip())]
        }

        source = "\n".join(source_lines[:-1])

    dataclass_atrributes = {"title": config.get("title")}

    if highlights := config.get("highlights"):
        lines_to_highlights = highlights.split(",")
        highlight_ints = []
        for l in lines_to_highlights:
            start, _, end = l.partition("-")
            if end:
                highlight_ints.append(list(range(int(start), int(end) + 1)))
            else:
                highlight_ints.append([int(start)])

        dataclass_atrributes["highlights"] = highlight_ints
    cell_config = CodeCellConfig(**dataclass_atrributes)
    return source.strip(), cell_config


def get_parsed_lines(source: str, language: str = "python") -> List[List[Tuple[Any, str]]]:
    lines = []
    line = []
    lexer = get_lexer_by_name(language)
    for token, value in lex(source, lexer):
        if token is Token.Text and value == "\n":
            lines.append(line)
            line = []
        else:
            line.append((token, value))

    lines.append(line)

    return lines


EXTRA_STYLES = {
    "light": {
        Token.Punctuation: RGBColor(102, 102, 102),
        Token.Literal.String.Single: RGBColor(64, 112, 160),
        Token.Literal.String.Doc: RGBColor(64, 112, 160),
        Token.Literal.Number.Integer: RGBColor(64, 160, 112),
        Token.Keyword.Namespace: RGBColor(0, 112, 32),
        Token.Name.Builtin.Pseudo: RGBColor(27, 82, 167),
        Token.Name.Function.Magic: RGBColor(49, 0, 250),
        Token.Comment.Single: RGBColor(65, 127, 127),
        Token.Keyword.Constant: RGBColor(0, 112, 32),
    },
    "dark": {
        Token.Literal.Number.Integer: RGBColor.from_string("F78C6C"),
        Token.Comment.Single: RGBColor.from_string("546E7A"),
    },
}


@lru_cache
def get_theme(theme: str = "light") -> Dict[Any, RGBColor]:
    style_name = "friendly" if theme == "light" else "material"

    style = pygments.styles.get_style_by_name(style_name)
    token_colors = {}
    for token, str_style in style.styles.items():
        if not str_style:
            continue
        _, _, color = str_style.partition("#")
        if not color:
            continue

        pad = 1 if len(color) == 3 else 2
        token_colors[token] = RGBColor(*[int(color[i : i + pad], 16) for i in range(0, len(color), pad)])

    token_colors.update(EXTRA_STYLES.get(theme, {}))

    return token_colors
