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
# pylint: disable=multiple-statements, line-too-long



import json
from textwrap import dedent
from typing import Dict, List, Set, Tuple, Type, TYPE_CHECKING
from itertools import starmap
from dataclasses import dataclass
from math import inf



from ... import html_builder as Html
from ...tools_and_constants import DebugConfig, EditorName
from ...parsing import compress_LZW
from ...html_dependencies.deps_class import DepKind


if TYPE_CHECKING:
    from ..pyodide_macros_plugin import PyodideMacrosPlugin
    from ...macros.ide_ide import Ide



@dataclass
class MacroPyConfig:
    """
    Configuration of one IDE in one page of the documentation. Convertible to JS, to define the
    global variable specific to each page.

    Always instantiated without arguments, and items are updated when needed.
    """
    # WARNING: this declaration is used to generate the getters in the PyodideSectionRunner class.

    py_name:      str = ""          # name to use for downloaded file
    env_content:  str = ""          # HDR part of "exo.py"
    env_term_content:  str = ""     # HDR part for terminal commands only
    user_content: str = ""          # Non-HDR part of "exo.py" (initial code)
    corr_content: str = ""          # not exported to JS!
    public_tests: str = ""          # test part of "exo.py" (initial code)
    secret_tests: str = ""          # Content of "exo_test.py" (validation tests)
    post_term_content: str = ""     # Content to run after for terminal commands only
    post_content: str = ""          # Content to run after executions are done

    excluded: List[str] = None      # List of forbidden instructions (functions or packages)
    excluded_methods: List[str] = None # List of forbidden methods accesses
    python_libs: List[str] = None
    rec_limit: int = None           # recursion depth to use at runtime, if defined (-1 otherwise).
    white_list: List[str] = None    # White list of packages to preload at runtime
    auto_run: bool = None           # Auto execute the python content on page load.

    profile: str = None             # IDE execution profile ("no_valid", "no_reveal" or "")
    attempts_left: int = None       # Not overwriting this means there is no counter displayed
    auto_log_assert: bool = None    # Build automatically missing assertion messages during validations
    corr_rems_mask: int = None      # Bit mask:   has_corr=corr_rems_mask&1 ; has_rem=corr_rems_mask&2
    has_check_btn: bool = None      # Store the info about the Ide having its check button visible or not
    has_corr_btn: bool = None       # Store the info about the Ide having its corr button visible or not
    has_reveal_btn: bool = None     # Store the info about the Ide having its reveal button visible or not
    has_counter: bool = None        # Store the info about the Ide having its counter of attempts visible or not
    is_encrypted: bool = None       # Tells if the sol & REMs div content is encrypted or not
    is_vert: bool = None            # IDEv if true, IDE otherwise.
    max_ide_lines: int = None       # Max number of lines for the ACE editor div
    min_ide_lines: int = None       # Min number of lines for the ACE editor div
    decrease_attempts_on_user_code_failure: str = None    # when errors before entering the actual validation
    deactivate_stdout_for_secrets: bool = None
    show_only_assertion_errors_for_secrets: bool = None
    src_hash: str = None            # Hash code of code+TestToken+tests
    two_cols: bool = None           # automatically goes int split screen mode if true
    std_key: str = None             # To allow the use of terminal_message during validations
    export: bool = None             # Global archive related

    prefill_term: str = None        # Command to insert in the terminal after it's startup.
    stdout_cut_off: int = None      # max number of lines displayed at once in a jQuery terminal
    cut_feedback: bool = None       # shorten stdout/err or not



    def dump_to_js_code(self):
        """
        Convert the current MacroPyConfig object to a valid JSON string representation.

        Properties whose the value is None are skipped!
        """
        # pylint: disable=no-member

        content = ', '.join(
            f'"{k}": { typ }'
            for k,typ in starmap(self._convert, self.__class__.__annotations__.items())
            if typ is not None
        )
        return f"{ '{' }{ content }{ '}' }"



    def _convert(self, prop:str, typ:Type):
        """
        Convert the current python value to the equivalent "code representation" for a JS file.

        @prop:      property name to convert
        @typ:       type (annotation) of the property
        @returns:   Tuple[str, None|Any]

        NOTE: Infinity is not part of JSON specs, so use "Infinity" as string instead, then
              convert back in JS.
        """
        val = getattr(self, prop)

        if   val is None:         out = None
        elif val == inf:          out = '"Infinity"'
        elif prop in MAYBE_LISTS: out = json.dumps(val or [])
        elif typ in CONVERTIBLES: out = json.dumps(val)

        else: raise NotImplementedError(
            f"In {self.__class__.__name__} ({prop=}): conversion for {typ} is not implemented"
        )
        return prop, out



MAYBE_LISTS:  Tuple[str,  ...] = ('excluded', 'excluded_methods', 'white_list', 'python_libs')
""" Properties that should be lists """


CONVERTIBLES: Tuple[Type, ...] = (bool, int, str)
""" Basic types that are convertible to JSON """












class PageConfiguration(Dict[EditorName,MacroPyConfig]):
    """
    Augmented dictionary.
    Represent the Configuration of the JS scripts that need to be inserted in each page of the
    documentation, and the logistic to create the corresponding html code.
    """


    def __init__(self, env):
        super().__init__()
        self.env: PyodideMacrosPlugin = env
        self.needs: Set[DepKind] = set()        # Transformed to frozenset after on_env


    def has_need(self, need:DepKind):
        return need in self.needs


    def build_page_script_tag_with_ides_configs_and_mermaid_status(self):

        configs_as_json = '{' + ', '.join(
            f'"{ editor_name }": { ide_conf.dump_to_js_code() }'
            for editor_name, ide_conf in self.items()
        ) + '}'

        if DebugConfig.check_global_json_dump:
            try:
                json.loads(configs_as_json)
            except json.JSONDecodeError as e:
                raise ValueError(repr(configs_as_json)) from e

        compressed   = self.env.encrypted_js_data
        encoded      = compress_LZW(configs_as_json, self.env) if compressed else configs_as_json
        need_mermaid = DepKind.mermaid in self.needs
        script_tag   = Html.script(dedent(
            f"""
            CONFIG.needMermaid = { json.dumps(need_mermaid) };
            let PAGE_IDES_CONFIG = { encoded !r}
            """
        ))
        return script_tag
