"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""



import re
from textwrap import dedent
from argparse import Namespace
from typing import Any, Callable, ClassVar, Iterable

from mkdocs.config import config_options as C
from mkdocs.config.base import BaseConfigOption




PARAGRAPHS_SEP  = r"\n\n\s*"
BULLET_OR_TABLE = r"\n\s*(?:[|*+-]|\d[.] )"
MD_IN_HTML      = r"\n\s*\{(?![%{])"

INLINE_MD_SPLITTER: re.Pattern = re.compile( '(' + '|'.join(
    [PARAGRAPHS_SEP, BULLET_OR_TABLE, MD_IN_HTML]
) + ')')
"""
Pattern extracting blocks of markdown content from dedented strings, keeping their
individual indentation. Beginning of blocks considered:
    * Paragraphs: \\n\\n\\s*
    * Bullet points: \\n\\s*+*-   or \\n\\s*+*-
    * Table rows: \\n\\s*|
    * paragraphs attributes but not macros or jinja: \\n\\s*{(?![%{])

DOESN'T WORK WITH CODE BLOCKS OR INDENTED CONTENT (=implicit code block).
"""


def inline_md(msg:str) -> str:
    """
    Most/some docs strings will be used inside cells of tables, so the md cannot be "multiline"
    in the source content. But because it's boring AF to write those and still have something
    readable in the declaration code, the following logic is always applied:

    1. Consider the declaration is done with multiline strings.
    2. `dedent` the content.
    3. Strip the message from leading and trailing new lines
    4. Inline every "paragraph" by removing all "\\n\\s*" except when they are preceded by
        another "\\n" (which means it's the beginning of a new §, potentially with indentation).
    """
    clean = dedent(msg).strip('\r\n')

    if "```" in clean:
        raise ValueError(
            f"`inline_md` logic is not ready for code blocks (see doc or yaml_desc:\n{ clean })."
        )

    chunks_with_seps_on_odds = INLINE_MD_SPLITTER.split(clean)
    inlines = [
        chunk if i&1 else re.sub(r'\n\s*',' ',chunk)
            for i,chunk in enumerate(chunks_with_seps_on_odds)
    ]
    return f"{ ''.join(inlines).lstrip() }"
           # never add leading/trailing new lines here: inlined single § should _ACTUALLY_ be on one single line








class DeprecationTemplate(Namespace):
    """ Messages template for all DeprecationStatus """

    moved = "The option {src} is deprecated. It's equivalent is now: {moved_to}."

    removed = "The option {src} is deprecated: it will be removed in near future."

    unsupported = (
        "Macros using {src} may not work anymore and will be removed in the future. Please contact "
        "the author of the theme if you need this macro/tool."
    )








def __unicode_converter() -> Callable[[str], str] :
    replacements = {
        "\\u00e9": "é",
    }
    pattern = re.compile('|'.join(replacements).replace('\\','\\\\'))   #... x/

    def replacer(s:str):
        # print(s)          # To spot missing conversions (german!!)
        return re.sub(pattern, lambda m: replacements[m[0]], s)
    return replacer

unicode_to_nicer = __unicode_converter()










class ConfigOptionCode:
    """
    Convert a live BaseConfigOption instance to the equivalent string/code declaration.

    Note: not all the classe are implemented. See here to find how to add more:
        https://github.com/mkdocs/mkdocs/blob/master/mkdocs/config/config_options.py
    """

    DEPRECATION_TEMPLATE: ClassVar[str] = (
      "The configuration option '{}' has been deprecated and will be removed in a future release."
    )

    @classmethod
    def extract(cls, opt:BaseConfigOption):
        """
        Convert a live BaseConfigOption instance to the equivalent string/code declaration.
        Note: not all the classe are implemented.
        """
        name    = opt.__class__.__name__
        prop    = f"_{ name.lower() }"
        inner   = getattr(cls, prop)(opt)
        default = "" if opt.default is None else f', default={ opt.default !r}'
        return f'C.{ name }({ inner }{ default })'


    @classmethod
    def _optional(cls, opt:C.Optional):
        return cls.extract(opt.option)
    Deprecated = _optional

    @classmethod
    def _choice(cls, opt:C.Choice):
        return repr(opt.choices)

    @classmethod
    def _type(cls, opt:C.Type):
        return get_python_type_as_code(opt._type)       # pylint: disable=protected-access

    @classmethod
    def _dictofitems(cls, opt:C.DictOfItems):
        return cls.extract(opt.option_type)

    _listofitems = _dictofitems

    @classmethod
    def _deprecated(cls, opt:C.Deprecated):          # pylint: disable=E0102
        args = []
        for prop in 'moved_to removed option_type'.split():
            val = cls.extract(opt.option) if prop=='option_type' else getattr(opt,prop)
            if val and val != cls.DEPRECATION_TEMPLATE:
                args.append(f"{prop}={val}")
        return ', '.join(args)






def get_python_type_as_code(typ:Any):
    """
    Transform self.py_type in it's string code declaration, taking various type declarations
    in consideration:

    - basics:   int, str, ...
    - typing:   Set[str], ...
    - 3.9+:     set[str], ...
    """
    is_from_typing = hasattr(typ,'_name')
    is_simple_type = not is_from_typing and (typ is str or not issubclass(typ, Iterable))
                     # issubclass raises with typing types...

    if is_simple_type:
        py_type = typ.__name__
    elif is_from_typing:
        py_type = str(typ).replace('typing.','')
    else:
        py_type = str(typ)

    return py_type


















if __name__ == '__main__':

    print('\nTest inline_md:\n')

    TESTS = [
        (
            "Simplest case",
            """
            abc
            def

            ijklmnop
            qrs
            """,
            "abc def\n\nijklmnop qrs",
        ),
        (
            "Inner indentation",
            """
            abc

                indented + junked end.
        """,
            "abc\n\n    indented + junked end.",
        ),
        (
            "Inline inner content of bullet points",
            """
            * ab c def
            fgh ij
                - kl
                mn pq
            + MEH
            ...duh?
            """,
            "* ab c def fgh ij\n    - kl mn pq\n+ MEH ...duh?"
        ),
        (
            "Tables + stripping",
            """

            blabla

            | a |
            |:-|
            | meh |

            """,
            "blabla\n\n| a |\n|:-|\n| meh |"
        )
    ]
    for title, md, exp in TESTS:
        actual = inline_md(md)
        print(title)
        if actual != exp:
            print('"""')
            print(dedent(md), '\n"""\n\n--------------\n\nActual:\n"""')
            print(actual, '\n"""\n\n--------------\n\nEXP:\n"""')
            print(exp, '\n"""')
            assert False, "(see above)"
    print()

    print('\nTest ConfigOptionCode.extract:\n')
    TESTS = [
        (C.DictOfItems(C.Type(str)), 'C.DictOfItems(C.Type(str))'),
        (C.ListOfItems(C.Type(str)), 'C.ListOfItems(C.Type(str))'),
        (C.ListOfItems(C.Type(str), default=[]), 'C.ListOfItems(C.Type(str), default=[])'),
        (C.Optional(C.Type(bool) ), 'C.Optional(C.Type(bool))'),
        (
            C.Deprecated(option_type=C.Optional(C.Type(bool))),
           'C.Deprecated(option_type=C.Optional(C.Type(bool)))'
        ),
    ]
    for src,exp in TESTS:
        print(exp)
        actual = ConfigOptionCode.extract(src)
        assert actual == exp, f'{actual} should be {exp}'
