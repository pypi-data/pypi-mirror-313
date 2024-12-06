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

# pylint: disable=invalid-name, missing-module-docstring


from functools import wraps
from typing import Any, Optional, Type

from pyodide_mkdocs_theme.pyodide_macros.macros.ide_run_macro import AutoRun
from pyodide_mkdocs_theme.pyodide_macros.macros.ide_tester import IdeTester



from ..tools_and_constants import MACROS_WITH_INDENTS, ScriptSection
from ..parsing import build_code_fence
from ..plugin.maestro_macros import MaestroMacros
from .ide_files_data import IdeFilesExtractor
from .ide_manager import IdeManager
from .ide_ide import Ide, IdeV
from .ide_terminal import Terminal
from .ide_py_btn import PyBtn





def _element_maker(env:MaestroMacros, kls:Type[IdeManager]):

    @wraps(_element_maker)
    def wrapped(
        py_name:   str = "",
        *,
        # REMINDER: _NOTHING_ should ever be left to None at runtime (MaestroMeta),
        #           except for the ID argument.
        ID:        Optional[int] = None,
        SANS:      str = None,
        WHITE:     str = None,
        REC_LIMIT: int = None,
        MERMAID:   bool = None,
        AUTO_RUN:       bool = None,
        **kw
    ) -> str:
        return kls(
            env, py_name, ID, SANS, WHITE, REC_LIMIT, MERMAID, AUTO_RUN,
            extra_kw=kw     # Arguments sink... (see IdeManager contract)
        ).make_element()

    wrapped.__name__ = wrapped.__qualname__ = kls.MACRO_NAME
    return wrapped




def IDE(env:MaestroMacros):
    """ To build editor+terminal on 2 rows """
    MACROS_WITH_INDENTS.add('IDEv?')
    return _element_maker(env, Ide)


def IDEv(env:MaestroMacros):
    """ To build editor+terminal on 2 columns """
    return _element_maker(env, IdeV)


def IDE_tester(env:MaestroMacros):
    """ To build editor+terminal on 2 columns """
    MACROS_WITH_INDENTS.add(IdeTester.MACRO_NAME)
    return _element_maker(env, IdeTester)


def terminal(env:MaestroMacros):
    """ To build an isolated terminal """
    return _element_maker(env, Terminal)


def py_btn(env:MaestroMacros):
    """ To build an isolated button, to run python `env` sections """
    return _element_maker(env, PyBtn)


def run(env:MaestroMacros):
    """ To build an isolated button, to run python `env` sections """
    return _element_maker(env, AutoRun)





def section(env:MaestroMacros):
    """
    Insert the given section from the python file.
    Note: To use only on python scripts holding all the sections for the IDE macros. For regular
          files, use the `py` macro or regular code fences with file inclusions (for performances
          reasons).
    """
    MACROS_WITH_INDENTS.add('section')

    @wraps(section)
    def _section(
        py_name:str,
        section_name:ScriptSection,
        ID: Any=None # sink (deprecated)             # pylint: disable=unused-argument
    ):
        file_data = IdeFilesExtractor(env, py_name)
        content   = file_data.get_section(section_name)
        indent    = env.get_macro_indent()
        out       = build_code_fence(content, indent, lang='python')
        return out

    return _section
