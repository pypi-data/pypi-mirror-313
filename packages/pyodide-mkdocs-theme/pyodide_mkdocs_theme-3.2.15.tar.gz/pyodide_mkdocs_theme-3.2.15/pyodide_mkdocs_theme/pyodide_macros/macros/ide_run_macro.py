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

# pylint: disable=unused-argument


from typing import ClassVar, Tuple, Union
from dataclasses import dataclass

from pyodide_mkdocs_theme.pyodide_macros.html_dependencies.deps_class import DepKind


from ..tools_and_constants import Prefix
from .ide_py_btn import PyBtn





@dataclass
class AutoRun(PyBtn):
    """
    Builds a button + a terminal + the buttons and extra logistic needed for them.
    """
    MACRO_NAME: ClassVar[str] = "run"

    ID_PREFIX: ClassVar[str] = Prefix.auto_run_

    KW_TO_TRANSFER: ClassVar[Tuple[ Union[str, Tuple[str,str]]] ] = ()

    DEPS_KIND: ClassVar[DepKind] = DepKind.run_macro

    def handle_extra_args(self):
        self.auto_run = True
        super().handle_extra_args()


    def make_element(self) -> str:
        return ""
