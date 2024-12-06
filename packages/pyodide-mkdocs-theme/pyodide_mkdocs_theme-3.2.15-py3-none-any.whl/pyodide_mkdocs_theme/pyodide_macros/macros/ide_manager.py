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


from abc import ABCMeta
import re
import hashlib
from typing import Any, ClassVar, Dict, Optional, Tuple, Union, TYPE_CHECKING
from dataclasses import dataclass
from pathlib import Path

from mkdocs.exceptions import BuildError


from .. import html_builder as Html
from ..pyodide_logger import logger
from ..exceptions import PyodideMacrosNonUniqueIdError
from ..tools_and_constants import HtmlClass, IdeConstants
from ..messages import Tip
from ..paths_utils import get_ide_button_png_path
from ..html_dependencies.deps_class import DepKind
from ..plugin.tools.maestro_tools import macro_name_to_src_and_is_tester
from ..plugin.tools.pages_and_macros_py_configs import MacroPyConfig
from .ide_files_data import IdeFilesExtractor

if TYPE_CHECKING:
    from ..plugin import PyodideMacrosPlugin












@dataclass
class IdeManagerMacroArguments:
    """
    Handle the creation of the underlying object, articulating the inner state with the macros
    actual arguments and performing validation of those.

    Also defines all the instance properties for the object (whatever the inheritance chain).
    """


    KEEP_CORR_ON_EXPORT_TO_JS: ClassVar[bool] = False
    """ Define if the corr section must be exported to the JS layer. """


    KW_TO_TRANSFER: ClassVar[Tuple[ Union[str, Tuple[str,str]]] ]  = ()
    """
    Configuration of the keywords that should be extracted if given in the constructor.
    This makes the "link" between the macros arguments and the actual properties in the python
    object, which often differ. Legacy in action...

    KW_TO_TRANSFER is an iterable of (argument_name, property_name) pairs of strings.
    If an element is a simple string instead, it will be used as (value, value.lower())
    """


    MACRO_NAME: ClassVar[str] = None
    """ Origin of the macro call (for __str__) """


    ID_PREFIX: ClassVar[str] = None
    """ Must be overridden in the child class """

    NEED_INDENTS: ClassVar[bool] = False
    """
    Specify the macro had adding multiline content (so it _will_ consume one indentation data).
    """

    DEPS_KIND: ClassVar[DepKind] = DepKind.pyodide
    """
    Register the kind of js scripts that must be added to the page, for the current object.
    """


    # Defined on instantiation:
    #--------------------------


    env: 'PyodideMacrosPlugin'
    """ The MaestroEnv singleton """

    py_name: str
    """ Base name for the files to use (first argument passed to the macros)
        Partial path from the directory holding the sujet.md file, to the one holding all the
        other required files, ending with the common prefix for the exercice.
        Ex:   "exo" to extract:   "exo.py", "exo_corr.py", "exo_test.py", ...
                "sub_exA/exo" for:  "sub_exA/exo.py", "sub_exA/exo_corr.py", ...
    """

    id: Optional[int]
    """ Used to disambiguate the ids of two IDEs, if the same file is used several times
        in the document.
    """

    excluded: str
    """ String of spaces or coma separated python functions or modules/packages that are forbidden
        at runtime. By default, nothing is forbidden.
            - Every string section that matches a builtin callable forbid that function by
              replacing it with another function which will raise an error if called.
            - Every string section prefixed with a fot forbids a method call. Here a simple
              string containment check is done opn the user's code, to check it does not
              contain the desired method name with the dot before it.
            - Any other string section is considered as a module name and doing an import (in
              any way/syntax) involving that name will raise an error.

        Note that the restrictions are rather strict, and may have unexpected side effects, such
        as, forbidding `exec` will also forbid to import numpy, because the package relies on exec
        for some operations at import time.
        To circumvent such a kind of problems, use the white_list argument.
    """

    white_list: str
    """ String of spaces or coma separated python modules/packages names the have to be
        preloaded before the code restrictions are enforced on the user's side.
    """

    rec_limit: int
    """ If used, the recursion limit of the pyodide runtime will be updated before the user's
        code or the tests are run.
        Note that this also forbids the use of the `sys.setrecurionlimit` at runtime.
    """

    with_mermaid: bool
    """ If True, a mermaid graph will be generated by this IDE/terminal/py_btn, so the general
        setup for mermaid must be put in place.
    """

    auto_run: bool
    """ If True, the underlying python file is executed just after the page has loaded. """

    extra_kw: Optional[Dict[str,Any]] = None
    """
    Any kw left in the original call.
    Should be always be None when reaching IdeManager.__post_init__. This allows subclasses
    to handle the extra (legacy) keywords on their side.
    """


    # defined during post_init or in child class
    #-------------------------------------------

    built_py_name: str = ""
    """
    Extended python file name, prepending with page url data and stuff, to make the name
    more explicit.
    """

    indentation: str = ""
    """ Indentation on the left of the macro call, as str """




    def __post_init__(self):

        if self.MACRO_NAME is None:
            raise NotImplementedError("Subclasses should override the MACRO_NAME class property.")

        if self.ID_PREFIX is None:
            raise NotImplementedError("Subclasses should override the ID_PREFIX class property.")

        # Archive the indentation level for the current IDE:
        if self.NEED_INDENTS:
            self.indentation = self.env.get_macro_indent()

        self.handle_extra_args()        # may be overridden by subclasses.

        self.env.set_current_page_insertion_needs(self.DEPS_KIND)

        if self.with_mermaid:
            self.env.set_current_page_insertion_needs(DepKind.mermaid)

            if not self.env.is_mermaid_available:
                raise BuildError(
                    "\nCannot use MERMAID=True because the superfences markdown extension is not "
                    "configured to accept mermaid code blocks.\n"
                    "Please add the following in your mkdocs.yml file, in the markdown_extension "
                    "section:\n\n"
                    "  - pymdownx.superfences:\n"
                    "      custom_fences:\n"
                    "        - name: mermaid\n"
                    "          class: mermaid\n"
                    "          format: !!python/name:pymdownx.superfences.fence_code_format\n"
                )



    def __str__(self):
        return f"{self.MACRO_NAME}('{self.py_name}', ...), in file { self.env.file_location() }"



    def handle_extra_args(self):
        """
        Assign the extra arguments provided through other keyword arguments, handling only those
        actually required for the child class.
        Also extract default values for properties that are still set to None after handling the
        keyword arguments.
        If some are remaining, after this in self.extra_kw, an error will be raised.
        """
        to_transfer = [
            data if isinstance(data,tuple) else (data, data.lower())
            for data in self.KW_TO_TRANSFER
        ]
        for kw, prop in to_transfer:
            if kw in self.extra_kw:
                value = self.extra_kw.pop(kw)
                setattr(self, prop, value)

        if self.extra_kw:
            raise BuildError(
                f"Found forbidden arguments for { self }:\n"
                + "".join(f"    {k} = {v!r}\n" for k,v in self.extra_kw.items())
            )
















@dataclass
class IdeSectionsManager(IdeManagerMacroArguments):
    """
    Generic logistic related to sections data.

    Implement __getattr__ so that all undefined `has_xxx` properties are automatically
    relayed to the files_data object.
    """

    files_data: IdeFilesExtractor = None

    @property               # pylint: disable-next=all
    def has_any_corr_rems(self):
        return self.has_corr or self.has_rem or self.has_vis_rem

    @property               # pylint: disable-next=all
    def has_check_btn(self): return False

    def __getattr__(self, prop:str):
        """
        Implement all `has_xxx` undefined properties, relaying to the inner IdeFilesExtractor
        object.
        """
        if not prop.startswith('has_'):
            raise AttributeError(prop)
        return getattr(self.files_data, prop)



    def __post_init__(self):
        super().__post_init__()

        self.files_data = IdeFilesExtractor(self.env, self.py_name)

        self._define_max_attempts_symbols_and_value()       # To do before files validation: MAX

        self._validate_files_config()

        if self.rec_limit < -1:         # standardization
            self.rec_limit = -1

        if -1 < self.rec_limit < IdeConstants.min_recursion_limit:
            raise BuildError(
                f"The recursion limit for {self} is set too low and may causes runtime troubles. "
                f"Please set it to at least { IdeConstants.min_recursion_limit }."
            )


    def _define_max_attempts_symbols_and_value(self):
        """ Placeholder, to insert (very...) specific logic for IDEs... """


    def _validate_files_config(self):
        raise NotImplementedError()


    def _build_error_msg_with_option(self, msg:Optional[str], config_opt:Optional[str]=None):
        msg = f"\nInvalid configuration with: {self}\n    {msg}"
        if config_opt:
            msg += (
                f"\n    You can deactivate this check by setting `mkdocs.yml:plugins.{config_opt}:"
                f" false`, or the equivalent in a `{ self.env._pmt_meta_filename }` file, or as "
                "metadata of a markdown documentation page."
            )
        return msg


    def _validation_outcome(self, msg:Optional[str]):
        """
        Routine that can be called from the _validate_files_config implementation, handling how
        the messages must be used (raising/logging).
        """
        if not msg:
            return

        if self.env._dev_mode:       # pylint: disable=protected-access
            logger.error("DEV_MODE (expected x3) - " + msg)
        else:
            raise BuildError(msg)

















@dataclass
class IdeManagerMdHtmlGenerator(IdeSectionsManager):
    """
    Generic html handling (ids, buttons, ...)
    """

    editor_name: str = ''
    """ tail part of most ids, in the shape of 'editor_{32 bits hexadecimal}' """


    def __post_init__(self):
        super().__post_init__()
        self.editor_name = self.generate_id()



    def make_element(self) -> str:
        """
        Create the actual element template (html and/or md content).
        """
        raise NotImplementedError("Subclasses should implement the make_element method.")



    def generate_id(self):
        """
        Generate an id number for the current element, in the form:

            PREFIX_{32 bits hash value}

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

        NOTE: uniqueness most be guaranteed for IDEs (LocalStorage). It's less critical for other
        elements, but they still need to stay unique across a page, at least (especially when
        feedback is involved, like with terminals. Note: maybe not anymore... :thinking: )
        """
        path = path_without_id = str(self.env.generic_count)
        if self.id is not None:
            path += str(self.id)            # kept in case unlucky collision... (yeah, proba... XD )
        return self.id_to_hash(path, path_without_id)



    def id_to_hash(self, clear:str, no_id_path:str):
        """ Hash the "clear version of it" to add as html id tail, prefix it, and check the
            uniqueness of the hash across the whole website.
        """

        hashed  = hashlib.sha1(clear.encode("utf-8")).hexdigest()
        html_id = f"{ self.ID_PREFIX }{ hashed }"

        if not self.env.is_unique_then_register(html_id, no_id_path, self.id):
            raise PyodideMacrosNonUniqueIdError(
                "\nThe same html id got generated twice.\nIf you are trying to use the same "
                "set of files for different macros calls, use their ID argument (int >= 0) "
                "to disambiguate them.\n"
               f"    Problematic call:  { self }\n"
               f"    Generated id:      { html_id }\n"
               f"    ID values already in use: {self.env.get_registered_ids_for(no_id_path) }"
            )
        return html_id



    def create_button(
        self,
        btn_kind:    str,
        *,
        margin_left:    float = 0.2,
        margin_right:   float = 0.2,
        extra_btn_kls:  str   = "",
        **kwargs
    ) -> str:
        """
        Build one button
        @btn_kind:      The name of the JS function to bind the button click event to.
                        If none given, use the lowercase version of @button_name.
        @margin_...:    CSS formatting as floats (default: 0.2em on each side).
        @extra_btn_kls: Additional html class for the button element.
        @**kwargs:      All the remaining kwargs are attributes added to the button tag.
        """
        return self.cls_create_button(
            self.env,
            btn_kind,
            margin_left   = margin_left,
            margin_right  = margin_right,
            extra_btn_kls = extra_btn_kls,
            **kwargs
        )


    @classmethod
    def cls_create_button(
        cls,
        env:           'PyodideMacrosPlugin',
        btn_kind:       str,
        *,
        margin_left:    float = 0.2,
        margin_right:   float = 0.2,
        extra_btn_kls:  str   = "",
        **kwargs
    ) -> str:
        """
        Build one button
        @btn_kind:      The name of the JS function to bind the button click event to.
                        If none given, use the lowercase version of @button_name.
        @margin_...:    CSS formatting as floats (default: 0.2em on each side).
        @extra_btn_kls: Additional html class for the button element.
        @**kwargs:      All the remaining kwargs are attributes added to the button tag.
        """
        png_name, lang_prop, bgd_color = get_button_fields_data(btn_kind)

        lvl_up    = env.level_up_from_current_page()
        img_link  = get_ide_button_png_path(lvl_up, png_name)
        img_style = {}
        if bgd_color is not None:
            img_style = {'style': f'--ide-btn-color:{ bgd_color };'}

        img = Html.img(src=img_link, kls=HtmlClass.skip_light_box, **img_style)

        tip: Tip = getattr(env.lang, lang_prop)
        tip_span = Html.tooltip(tip, tip.em)

        btn_style = f"margin-left:{margin_left}em; margin-right:{ margin_right }em;"
        if 'style' in kwargs:
            btn_style += kwargs.pop('style')

        button_html = Html.button(
            f'{ img }{ tip_span }',
            btn_kind = btn_kind,
            kls = ' '.join([HtmlClass.tooltip, extra_btn_kls]),
            style = btn_style,
            **kwargs,
        )
        return button_html





def get_button_fields_data(btn_kind:str):
    """
    Return the various property names to use for each kind of element (tooltip, image, ...),
    for the given initial button_name.

    @returns:   png_name, lang_prop, js_method, color
    """
    if btn_kind in BTNS_KINDS_CONFIG:
        return BTNS_KINDS_CONFIG[btn_kind]
    return (btn_kind, btn_kind, None)


# btn_kind:       (png,          lang,           color)  (if color is None: apply default)
BTNS_KINDS_CONFIG = {
    'corr_btn':   ('check',      'corr_btn',     'green'),
    'show':       ('check',      'show',         'gray'),

    'test_ides':  ('play',       'test_ides',    'orange'),
    'test_stop':  ('stop',       'test_stop',    'orange'),
    'test_1_ide': ('play',       'test_1_ide',   'orange'),
    'load_ide':   ('download',   'load_ide',     None),

    'p5_start':   ('play',       'p5_start',     None),
    'p5_stop':    ('stop',       'p5_stop',      None),
    'p5_step':    ('step',       'p5_step',      None),
}

















@dataclass
class IdeManagerExporter(IdeManagerMdHtmlGenerator, metaclass=ABCMeta):
    """
    Handle data exportations to JS, through the MacroPyConfig objects (compute only values
    that are not stored on the instance itself).
    """


    def __post_init__(self):
        super().__post_init__()
        self.built_py_name = self._build_py_filename_for_uploads()
        (
            self._excluded,
            self._excluded_methods,
            self._white_list
        ) = self._compute_exclusions_and_white_lists()

        registered = dict(self.exported_items())
        self.env.set_current_page_js_macro_config(
            self.editor_name, MacroPyConfig(**registered)
        )

        name, is_tester = macro_name_to_src_and_is_tester(self.MACRO_NAME)

        # IDE_tester macro is not exported, so exit directly:
        if is_tester: return

        if not self.env.all_macros_data:
            if self.env.is_dirty: return
            raise BuildError("No MacroData instance registered yet! Seeking for "+self.MACRO_NAME)

        macro_data = self.env.all_macros_data[-1]
        if macro_data.macro != name:
            raise BuildError(
                f"Wrong MacroData object: Expected {name} but was {macro_data.macro}"
            )
        macro_data.register_macro_manager_data(self)


    def exported_items(self):
        """
        Generate all the items of data that must be exported to JS.
        """
        yield from [
            ('py_name',          self.built_py_name),
            ("excluded",         self._excluded),
            ("excluded_methods", self._excluded_methods),
            ("rec_limit",        self.rec_limit),
            ("white_list",       self._white_list),
            ("auto_run",         self.auto_run),
            ('python_libs',      [ p.name for p in map(Path,self.env.python_libs) ]),

        ]
        # All data related to files (python, REMs):
        yield from self.files_data.get_sections_data( with_corr=self.KEEP_CORR_ON_EXPORT_TO_JS )



    #-----------------------------------------------------------------------------


    def _build_py_filename_for_uploads(self):
        """
        Guess an explicative enough py_name (when downloading the IDE content)
        """
        root_name = Path(self.env.page.url).stem
        py_path   = Path(self.py_name).stem
        py_name   = f"{root_name}-{py_path}".strip('-') or 'unknown'
        return py_name + '.py'



    def _compute_exclusions_and_white_lists(self):
        """
        Compute all code exclusions and white list of imports
        """
        white_list       = self._exclusion_string_to_list("white_list")
        all_excluded     = self._exclusion_string_to_list("excluded")
        excluded_methods = [ meth for meth in all_excluded if     meth.startswith('.') ]
        excluded         = [ meth for meth in all_excluded if not meth.startswith('.') ]

        if 'globals' in excluded:
            raise BuildError(
                "It's not possible to use `SANS='globals`, because it would break pyodide runner "
               f"itself.\n    { self }"
            )
        return excluded, excluded_methods, white_list



    def _exclusion_string_to_list(self, prop:str):
        """
        Convert a string argument (exclusions or white list) tot he equivalent list of data.
        """
        rule = (getattr(self, prop) or "").strip(' ;,')       # (never allow None)
        lst = re.split(r'[ ;,]+', rule) if rule else []
        return lst














@dataclass
class IdeManager(
    IdeManagerExporter,
    IdeManagerMdHtmlGenerator,
    IdeSectionsManager,
    IdeManagerMacroArguments,
    metaclass=ABCMeta,
):
    """
    Base class managing the information for the underlying environment.
    To be extended by a concrete implementation, providing the actual logistic to
    build the html hierarchy (see self.make_element).
    """
