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


from typing import ClassVar, Optional, Tuple
from dataclasses import dataclass

from pyodide_mkdocs_theme.pyodide_macros.html_dependencies.deps_class import DepKind

from .. import html_builder as Html
from ..tools_and_constants import HtmlClass, Prefix
from ..parsing import items_comma_joiner
from ..pyodide_logger import logger
from .ide_term_ide import CommonTermIde





@dataclass
class Terminal(CommonTermIde):
    """
    Builds an isolated terminal, potentially associated with some python file(s).
    """

    MACRO_NAME: ClassVar[str] = "terminal"

    ID_PREFIX: ClassVar[str] = Prefix.term_only_

    DEPS_KIND: ClassVar[DepKind] = DepKind.term

    KW_TO_TRANSFER: ClassVar[Tuple[Tuple[str,str]]] = (
        ('TERM_H',  'term_height'),
        ('FILL',    'prefill_term'),
    )


    prefill_term: Optional[str] = None
    """
    Command to prefill the terminal on startup.
    """


    def handle_extra_args(self):

        bad_size_arg_as_first_arg = isinstance(self.py_name, int)
        bad_size_kwarg            = 'SIZE' in self.extra_kw

        if bad_size_arg_as_first_arg or bad_size_kwarg:
            val = self.extra_kw.pop('SIZE') if bad_size_kwarg else self.py_name
            self.env.warn_unmaintained(
                msg=f"Invalid macro argument in { self.env.file_location() }:\n"
                    f"`{'{{'} terminal({ 'SIZE='*bad_size_kwarg }{ val }) {'}}'}` "
                    f"must be replaced with `{'{{'} terminal(TERM_H={ val }) {'}}'}`"
            )

        if 'FILL' not in self.extra_kw:
            self.extra_kw['FILL'] = ''

        super().handle_extra_args()


    def _validate_files_config(self):

        forbidden = [*filter(bool,(
            "user code"      * self.files_data.has_code,
            "public tests"   * self.files_data.has_tests,
            "secret tests"   * self.files_data.has_secrets,
            "a correction"   * self.has_corr,
            "a REM file"     * self.has_rem,
            "a VIS_REM file" * self.has_vis_rem,
        ))]
        if forbidden:
            items = items_comma_joiner(forbidden, 'and')
            msg   = f"No data should be provided in these sections:\n        {items}"
            super()._validation_outcome(msg)


    def exported_items(self):
        yield from super().exported_items()
        yield ("prefill_term", self.prefill_term)


    def make_element(self) -> str:
        """
        Create an IDE (Editor+Terminal+buttons) within an Mkdocs document. {py_name}.py
        is loaded in the editor if present.
        """
        terminal_div = self.make_terminal(
            self.editor_name,
            kls = f'{HtmlClass.py_mk_wrapper} {HtmlClass.term_solo}',
            n_lines_h = self.term_height,
        )
        return terminal_div
