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



from typing import ClassVar, Literal, Optional, Tuple, Union
from itertools import compress
from dataclasses import dataclass
from math import inf
from hashlib import sha256

from pyodide_mkdocs_theme.pyodide_macros.html_dependencies.deps_class import DepKind


from .. import html_builder as Html
from ..tools_and_constants import IDE_MODES, HtmlClass, IdeConstants, IdeMode, Prefix
from ..messages import Tip
from ..parsing import build_code_fence, items_comma_joiner
from ..paths_utils import convert_url_to_utf8, to_uri
from ..plugin.tools.test_cases import Case
from ..plugin.tools.macros_data import IdeToTest
from ..plugin.config import PLUGIN_CONFIG_SRC

from .ide_term_ide import CommonTermIde




#---------------------------------------------------------------------------------



SVG_FULL_SCREEN  = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3,3H11V5H3V3M13,3H21V5H13V3M3,7H11V9H3V7M13,7H21V9H13V7M3,11H11V13H3V11M13,11H21V13H13V11M3,15H11V17H3V15M13,15H21V17H13V15M3,19H11V21H3V19M13,19H21V21H13V19Z" /></svg>'''
SVG_SPLIT_SCREEN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M17 4H20C21.1 4 22 4.9 22 6V8H20V6H17V4M4 8V6H7V4H4C2.9 4 2 4.9 2 6V8H4M20 16V18H17V20H20C21.1 20 22 19.1 22 18V16H20M7 18H4V16H2V18C2 19.1 2.9 20 4 20H7V18M18 8H6V16H18V8Z" /></svg>'''




@dataclass
class Ide(CommonTermIde):
    """
    Builds an editor + a terminal + the buttons and extra logistic needed for them.
    """


    KEEP_CORR_ON_EXPORT_TO_JS: ClassVar[bool] = True

    MODE: ClassVar[ Literal["","_v"] ] = ""
    """ The terminal will be below (mode="") or on the right (mode="_v") of the editor.
        (what an awful interface, yeah... x) )
    """

    NEED_INDENTS: ClassVar[bool] = True

    MACRO_NAME: ClassVar[str] = "IDE"

    ID_PREFIX: ClassVar[str] = Prefix.editor_

    DEPS_KIND: ClassVar[DepKind] = DepKind.ide

    KW_TO_TRANSFER: ClassVar[Tuple[Tuple[str,str]]] = (
        ('MAX',        'max_attempts'),
        'MAX_SIZE',
        'MIN_SIZE',
        ('LOGS',       'auto_log_assert'),
        ('TERM_H',     'term_height'),
        ('MODE',       'profile'),
        ('TEST',       'test_config'),
        'TWO_COLS',
        'STD_KEY',
        'EXPORT',
    )



    max_attempts: Optional[Union[int, Literal["+"]]] = None
    """ Maximum number of attempts before the solution admonition will become available.
        If None, use the global default value.
    """

    max_size: Optional[int] = None
    """
    Max height of the editor (in number of lines)
    """

    min_size: Optional[int] = None
    """
    Min height of the editor (in number of lines)
    """

    auto_log_assert: Optional[bool] = None
    """ If True, failing assertions without feedback during the validation tests will be
        augmented automatically with the code of the assertion itself.
    """

    profile: Optional[IdeMode] = None
    """
    Runtime profile, to modify the executions and/or the validation logic.
    """

    test_config: Optional[ Union[str,Case] ] = None
    """
    Configuration when testing this IDE. If it's a string, it will be automatically converted
    to a Case object.
    """

    two_cols: Optional[bool] = None
    """
    If True, automatically goes in split screen mode on page load.
    """

    std_key: Optional[str] = None
    """
    Key to use to allow the use of `terminal_message` in pyodide (when the stdout is deactivated).
    """

    export: Optional[bool] = None
    """
    The editor content of this IDE will be grouped in the page archive if downloaded.
    """

    #-----------------------

    max_attempts_symbol: str = ''
    """ Actual string representation to use when creating the counter under the IDE """


    @property
    def has_any_tests(self):
        """ True if a tests or secrets section exist """
        return self.has_tests or self.has_secrets

    @property
    def has_check_btn(self):
        """
        If True, the validation button has to be in the GUI. The base logic here is:

        - If a `secrets` section exists, the button should be there, whatever the corr/REMs are...
        - Unless the MODE argument is `no_valid`.
        - The special case of a `tests` section only, with corr/REMs content is not considered
          worth of having a check button, so far (if changed, the validation logic must be changed:
          see `forbid_hidden_corr_and_REMs_without_secrets`).
        """
        if self.profile == IdeMode.no_valid:
            return False
        return self.has_secrets or self.profile == IdeMode.delayed_reveal

    @property
    def has_corr_btn(self):
        """ If True the button to run the corr section instead of the editor will be present. """
        return self.env.in_serve and self.has_corr

    @property
    def has_reveal_btn(self):
        """ If True the button to run the corr section instead of the editor will be present. """
        return self.env.in_serve and self.has_any_corr_rems

    @property
    def has_counter(self):
        """ Define if the counter of attempts left must be shown or not in the UI. """
        return self.has_check_btn and self.has_any_corr_rems



    def __post_init__(self):
        super().__post_init__()
        self.register_ide_for_tests()



    def register_ide_for_tests(self):
        """
        Archive config info about the current IDE and register for testing...
        """
        case = Case.auto_convert_str_to_case(self.test_config)

        some_to_test = self.has_code if case.code else self.has_corr
        fallback     = self.env.testing_empty_section_fallback
        if not some_to_test and fallback:
            setattr(case, fallback, True)

        self.test_config = case

        test = IdeToTest.from_ide(self)
        self.env.archive_ide_to_tests(test)




    def _define_max_attempts_symbols_and_value(self):
        """
        Any MAX value defined in the file takes precedence, because it's not possible to know
        if the value coming from the macro is the default one or not.
        """
        max_ide = str(self.max_attempts)

        # SOFT DEPRECATED (kept in case the user set the logger to `warn` instead of `error`)
        # If something about MAX in the file, it has precedence:
        max_from_file = self.files_data.file_max_attempts
        if max_from_file != "":
            max_ide = max_from_file

        is_inf = (
            max_ide in ("+", "1000")        # "1000": legacy reasons...
            or not self.has_any_corr_rems   #         ...but actually useful for meta files!
            or not self.has_any_tests and self.profile != IdeMode.delayed_reveal
            or self.profile in (IdeMode.no_reveal, IdeMode.no_valid, IdeMode.revealed)
        )

        self.max_attempts, self.max_attempts_symbol = (
            (inf, IdeConstants.infinity_symbol) if is_inf else (int(max_ide), max_ide)
        )



    def _validate_files_config(self):

        msg = ""
        if(
            self.has_check_btn
            and self.env.deactivate_stdout_for_secrets
            and not self.std_key
            and any( 'terminal_message' in section for section in (
                self.files_data.public_tests,  self.files_data.secret_tests,
            ))
        ):
            msg += self._build_error_msg_with_option(
                "Found a call to `terminal_message` in a tests or secrets section with deactivated"
                " stdout, while the STD_KEY argument has not been defined.\nPlease provide a key."
            )

        if self.profile is None:
            if(
                self.env.forbid_secrets_without_corr_or_REMs
                and self.has_secrets and not self.has_any_corr_rems
            ):
                msg += self._build_error_msg_with_option(
                    "A `secrets` section exists without `corr` section, REM or VIS_REM file.",
                    PLUGIN_CONFIG_SRC.get_plugin_path("ides.forbid_secrets_without_corr_or_REMs")
                )
            if(
                self.env.forbid_hidden_corr_and_REMs_without_secrets
                and self.has_any_corr_rems and not self.has_secrets
            ):
                msg += self._build_error_msg_with_option(
                    f"{ self._get_corr_rems_msg() }, but there is no `secrets` section.",
                    PLUGIN_CONFIG_SRC.get_plugin_path(
                        'ides.forbid_hidden_corr_and_REMs_without_secrets'
                    )
                )
            if(
                self.env.forbid_corr_and_REMs_with_infinite_attempts
                and self.has_any_corr_rems and self.max_attempts==inf
            ):
                msg += self._build_error_msg_with_option(
                    f"{ self._get_corr_rems_msg() } but will never be visible because the "
                    "number of attempts is set to infinity.",
                    PLUGIN_CONFIG_SRC.get_plugin_path(
                        'ides.forbid_corr_and_REMs_with_infinite_attempts'
                    )
                )

        elif self.profile not in IDE_MODES:
            msg += f'Invalid MODE argument: { self.profile !r} (choices: { ", ".join(IDE_MODES) })'


        elif self.profile == IdeMode.delayed_reveal:
            bad = [*filter(bool,[
                "\n    No `tests` section should be present."   * self.has_tests,
                "\n    No `secrets` section should be present." * self.has_secrets,
                "\n    The number of attempts shouldn't be infinite." * (self.max_attempts==inf),
            ])]
            if bad:
                msg += self._build_error_msg_with_option(
                    f"Cannot build an IDE with MODE={ IdeMode.delayed_reveal }:" + ''.join(bad)
                )

        self._validation_outcome(msg)



    def exported_items(self):
        yield from super().exported_items()
        yield from [
            ('attempts_left',   self.max_attempts),
            ("auto_log_assert", self.auto_log_assert),
            ('corr_rems_mask',  self.files_data.corr_rems_bit_mask),
            ("export",          self.export),
            ("has_check_btn",   self.has_check_btn),
            ("has_corr_btn",    self.has_corr_btn),
            ("has_reveal_btn",  self.has_reveal_btn),
            ("has_counter",     self.has_counter),
            ("is_vert",         self.MODE == '_v'),
            ("max_ide_lines",   self.max_size),
            ("min_ide_lines",   self.min_size),
            ('profile',         self.profile or ""),    # HAS to be exported => ensure is not None
            ("src_hash",        self._get_src_hash()),
            ("two_cols",        self.two_cols),
            ("std_key",         self.std_key),

            ("is_encrypted",                           self.env.encrypt_corrections_and_rems),
            ("deactivate_stdout_for_secrets",          self.env.deactivate_stdout_for_secrets),
            ("decrease_attempts_on_user_code_failure", self.env.decrease_attempts_on_user_code_failure),    # pylint: disable=line-too-long
            ("show_only_assertion_errors_for_secrets", self.env.show_only_assertion_errors_for_secrets),    # pylint: disable=line-too-long
        ]



    def _get_corr_rems_msg(self, present:bool=True):
        elements = [*filter(bool,(
            "a correction"   * (present == self.has_corr),
            "a REM file"     * (present == self.has_rem),
            "a VIS_REM file" * (present == self.has_vis_rem),
        ))]
        elt_msg = items_comma_joiner(elements, 'and')
        single  = len(elements)==1
        verb    = f"exist{ 's' * (single)}" if present else f"{ 'is' if single else 'are' } missing"
        elt_msg = f"{ elt_msg } { verb }".capitalize()
        return elt_msg



    def _get_src_hash(self):
        """ Generate the sha256 hash of `code + TestToken + tests` """
        content = (
            self.files_data.user_content,
            self.env.lang.tests.msg,
            self.files_data.public_tests
        )
        h = sha256()
        h.update( bytes('\n'.join(content), encoding='utf-8') )
        return h.hexdigest()




    def generate_id(self):
        """
        Generate an id number for the current IDE (editor+terminal), as a "prefix_hash(32bits)".

        This id must be:
            - Unique to every IDE used throughout the whole website.
            - Stable, so that it can be used to identify what IDE goes with what file or what
              localStorage data.

        Current strategy:
            - If the file exists, hash its path.
            - If there is no file, use the current global IDE_counter and hash its value as string.
            - The "mode" of the IDE is appended to the string before hashing.
            - Any ID value (macro argument) is also appended to the string before hashing.

        Uniqueness of the resulting hash is verified and a BuildError is raised if two identical
        hashes are encountered.
        """
        py_path = self.files_data.exo_py
        if py_path:
            path = str(py_path)
        else:
            path = str(self.env.ide_count)

        if self.MODE:
            path += self.MODE       # legacy...

        path_without_id = path

        if self.id is not None:
            path += str(self.id)

        return self.id_to_hash(path, path_without_id)




    def make_element(self) -> str:
        """
        Create an IDE (Editor+Terminal+buttons) within an Mkdocs document. {py_name}.py
        is loaded in the editor if present.
        """
        global_layout = Html.div(
            self.generate_empty_ide(),
            id = f"{ Prefix.global_ }{ self.editor_name }",
            kls = HtmlClass.py_mk_ide,
        )
        solution_div = self.build_corr_and_rems()

        return f"{ global_layout }{ solution_div }\n\n"
            # The solution_div not inside the other because markdown rendering troubles otherwise
            # (because of "md_in_html"). Also it will become useful as "anchor" for IDE extractions
            # and insertions, when/if ever the "full screen" mode is implemented.
            #
            # NOTE: about indentations : global_layout + the beginning of solution_div is a unique,
            #       long-ass string of html only, so everything is still properly indented, as long
            #       as all this is still the very beginning of the returned string.
            #
            # NOTE: DON'T EVER PUT NEW LINES AT THE BEGINNING!!! (breaks indentation contract: the
            #       macro call it'self is not indented properly)



    def generate_empty_ide(self) -> str:
        """
        Generate the global layout that will receive later the ace elements.
        """
        is_v = self.MODE == '_v'
        tip: Tip = self.env.lang.comments
        msg = str(tip)

        shortcut_comment_asserts = Html.span(
            '###' + Html.tooltip(msg, tip.em, shift=95),
            id = Prefix.comment_ + self.editor_name,
            kls = f'{HtmlClass.comment} {HtmlClass.tooltip}',
        )
        display_modes_btns_div = ''.join(
            f'<div class="{ kls } { HtmlClass.tooltip } { HtmlClass.svg_switch_btn } twemoji">{ svg + Html.tooltip(str(tip), tip.em, shift=95) }</div>'
            for kls,svg,tip in [
                ('ide-split-screen', SVG_FULL_SCREEN, self.env.lang.split_screen),
                ('ide-full-screen', SVG_SPLIT_SCREEN, self.env.lang.full_screen),
            ]
        )


        editor_div = Html.div(
            id = self.editor_name,
            is_v = str(is_v).lower(),
            mode = self.MODE,
        )
        editor_wrapper = Html.div(
            editor_div + shortcut_comment_asserts + display_modes_btns_div,
            kls = Prefix.comment_ + HtmlClass.py_mk_wrapper
        )

        terminal_div = self.make_terminal(
            Prefix.term_ + self.editor_name ,
            kls = f"{ HtmlClass.term_editor }{ self.MODE }",
            n_lines_h = self.term_height * (not is_v),
            is_v = is_v,
        )

        ide_and_term = Html.div(
            f"{ editor_wrapper }{ terminal_div }",
            kls = f"{ HtmlClass.py_mk_wrapper }{ self.MODE } md-typeset",
                # Adding md-typeset class for split-screen mode display consistency
        )

        buttons_and_counter = self.generate_buttons_row()

        return ide_and_term + buttons_and_counter





    def build_corr_and_rems(self):
        """
        Build the correction and REM holders. The rendered template is something like the
        following, with the indentation level of the most outer div equal to the indentation
        level of the IDE macro text in the markdown file.
        Depending on the presence/absence of corr, REM and VIS_REM files, some elements may
        be missing, BUT, the outer div will always be created, to simplify the logic on the
        JS layer (this way, the elements are always present in the DOM).

        | var | meaning |
        |-|-|
        | `at_least_one` | corr and/or REM (=> inside admonition) |
        | `anything` | corr or REM or VIS_REM |

        Overall structure of the generated markdown (mixed with html):

                <div markdown="1" id="solution_editor_id"       <<< ALWAYS
                     class="py_mk_hidden" >

                ENCRYPTION_TOKEN                                <<< at least one and encryption ON

                ??? tip "Solution"                              <<< at least one

                    <p></p>                                     <<< Spacer (thx mkdocs... X/ )

                    ```python linenums="1"'                     <<< solution
                    --8<-- "{ corr_uri }"                       <<< solution
                    ```                                         <<< solution

                    ___Remarques :___                           <<< remark & solution

                    --8<-- "{ rem_uri }"                        <<< remark

                --8<-- "{ vis_rem_uri }"                        <<< vis_rem

                ENCRYPTION_TOKEN                                <<< at least one and encryption ON

                </div>                                          <<< ALWAYS


        DON'T FORGET:

            1. DON'T EVER PUT HTML TAGS INSIDE ANOTHER ONE THAT ALREADY HAS THE markdown ATTRIBUTE!
            2. Trailing new lines are mandatory to render the "md in html" as expected.
        """

        # Prepare data first (to ease reading of the below sections)
        sol_title = ' & '.join(compress(*zip(
            (str(self.env.lang.title_corr), self.has_corr),
            (str(self.env.lang.title_rem),  self.has_rem)
        )))
        corr_content = self.files_data.corr_content
        at_least_one = self.has_corr or self.has_rem
        anything     = at_least_one or self.has_vis_rem
        with_encrypt = self.env.encrypt_corrections_and_rems and anything
        extra_tokens = ( IdeConstants.encryption_token, ) * with_encrypt


        # Build the whole div content:
        md_div = [         '',   # Extra empty line to enforce proper rendering of the md around
                           f'<div markdown="1" id="{ Prefix.solution_ }{ self.editor_name }" '
                           f'     class="{ HtmlClass.py_mk_hidden }" data-search-exclude >',
                            *extra_tokens ]
        if at_least_one:
            md_div.append( f'??? tip "{ sol_title }"' )
            md_div.append( '    <p></p>' )  # DON'T use an inner html div : it completely brakes
                                            # md rendering when no LZW compression is used.
        if self.has_corr:
            # Inner indented content must be handled now when building the block. The indentation
            # for the current line
            one_level = '    '
            fence = build_code_fence(
                corr_content,
                one_level + self.indentation,
                title=str(self.env.lang.corr)
            )
            md_div.append(  one_level+fence.strip())

        if self.has_corr and self.has_rem:
            rem = self.env.lang.rem
            md_div.append( f'    <span class="{ HtmlClass.rem_fake_h3 }">{ rem } :</span>')

        if self.has_rem:
            rem = self._rem_inclusion('rem_rel_path')
            md_div.append( f'    { rem }' )

        if self.has_vis_rem:
            vis_rem = self._rem_inclusion('vis_rem_rel_path')
            md_div.append(  vis_rem )

        md_div.extend((     *extra_tokens,
                            '</div>\n\n',
                      ))    # The extra linefeed is there to enforce rendering of next md sections

        # Add extra indentation according to IDE's insertion:
        if self.indentation:
            md_div = [ s and self.indentation + s for s in md_div ]

        # Join every item with extra gaps, to following md rendering requirements
        out = '\n\n'.join(md_div)
        return out



    def _rem_inclusion(self, rem_path_kind:str):
        path_str = str(getattr(self.files_data, rem_path_kind))
        rem_uri  = to_uri( convert_url_to_utf8(path_str) )
        return f'--8<-- "{ rem_uri }"'



    def generate_buttons_row(self) -> str:
        """
        Build all buttons below an "ide" (editor+terminal).
        """
        buttons   = self.list_of_buttons()
        cnt_txt   = self.counter_txt_spans() if self.has_counter else ""
        structure = Html.div(
            ''.join(buttons), kls=HtmlClass.ide_buttons_div
        ) + Html.div(
            Html.div(cnt_txt, kls=HtmlClass.compteur),
            kls=HtmlClass.compteur_wrapper
        )
        return Html.div(structure, kls=HtmlClass.ide_buttons_div_wrapper)


    def list_of_buttons(self):
        """ build a list of all the buttons to add after the IDE. """
        buttons = [
            self.create_button("play"),
            self.create_button("check") if self.has_check_btn else "",
            self.create_button("download", margin_left=1 ),
            self.create_button("upload", margin_right=1 ),
            self.create_button("restart"),
            self.create_button("save"),
        ]

        if self.export:
            buttons.append(
                self.create_button("zip")
            )
        if self.has_corr_btn:           # "mkdocs serve" only:
            buttons.append(
                self.create_button("corr_btn", margin_left=1)
            )
        if self.has_reveal_btn:         # "mkdocs serve" only:
            margin_left = {} if self.has_corr_btn else {"margin_left": 1}
            buttons.append(
                self.create_button("show", **margin_left),
            )

        return buttons


    def counter_txt_spans(self):
        """ Build the html content fot the counter of attempts (inline html: only spans). """
        cnt_txt_span = Html.span(self.env.lang.attempts_left.msg+" : ", kls=HtmlClass.compteur_txt)
        cnt_or_inf   = self.max_attempts_symbol
        cnt_n_span   = Html.span(cnt_or_inf, id=f'{ Prefix.compteur_ }{ self.editor_name }')
        low_span     = Html.span(cnt_or_inf, id=f'{ Prefix.compteur_ }{ self.editor_name }-low')
        full_txt     = f"{ cnt_txt_span }{ cnt_n_span }/{ low_span }"
        return full_txt







@dataclass
class IdeV(Ide):

    MACRO_NAME: ClassVar[str] = "IDEv"
    MODE: ClassVar[ Literal["","_v"] ] = "_v"
