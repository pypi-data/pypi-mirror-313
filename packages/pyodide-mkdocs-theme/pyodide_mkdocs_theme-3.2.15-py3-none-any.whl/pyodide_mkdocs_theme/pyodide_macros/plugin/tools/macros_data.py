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

from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, Optional, Type, TYPE_CHECKING



if TYPE_CHECKING:
    from ..pyodide_macros_plugin import PyodideMacrosPlugin
    from ...macros.ide_manager import IdeManager
    from ...macros.ide_ide import Ide


# All the classes defined here are there to provide autocompletion to the user.
# They are (almost) all generated automatically from the MacroConfigSrc objects
# (among other things...), to ensure they are always in sync with the actual
# implementation.



class MacroDataWithGetters:

    def __init__(self, dct):
        self._data_dct: Dict[str,bool] = dct



class DataGetter:
    """
    Descriptor automatically "tapping" into the inner _data_dct dict.
    Possibly allow to use default values when the property/key is missing.
    """

    def __init__(self, prop=None, default:Any=None, none_as_default=False, wraps:Callable=None):
        self.key = prop
        self.default = default
        self.allow_default = default is not None or none_as_default
        self.wraps = wraps

    def __set_name__(self, _, name:str):
        if self.key is None:
            self.key = name

    def __get__(self, obj:MacroDataWithGetters, _):
        if self.key not in obj._data_dct and self.allow_default:
            value = self.default
        else:
            value = obj._data_dct[self.key]
        return self.wraps(value) if self.wraps else value

    def __set__(self, obj, _value):
        raise ValueError(f"Cannot set { obj.__class__.__name__ } properties ({self.key!r})")








class MacroDataGeneric:
    """
    Generic interface, common to all MacroData objects.
    """
    # All properties declared with a default value to ease the extraction to build the docs...

    macro: str
    """
    Name of the macro that created this object. Notes:

    - `#!py "IDEv"` calls are seen has `#!py "IDE"`.
    - `#!py "IDE_tester"` calls are not gathered.
    """

    args: MacroDataWithGetters
    """
    All values of arguments, as passed in the macro call
    (overridden by child class with the needed class).
    """

    src_uri: str
    """
    Uri of the source file, relative to cwd.
    """

    page_url: str
    """
    As provided by `page.url` (aka, relative to the site_dir and taking in consideration
    the value of `use_directory_urls`).
    """

    full_page_url: str
    """
    Absolute url of the built page holding this element.
    """

    meta: Dict[str,Any]
    """
    Metadata of the source page (allows to store extra informations there, to add logic later
    when building the content).
    """

    abs_link: str
    """
    Absolute url of the element in the built page (defaults to full_page_url).
    """




class MacroDataSpecific:
    """
    Properties of MacroData objects that are defined only when appropriated (generally, for
    macros involving python files, like `IDE`, `IDEv`, `terminal`, `py_btn`).
    """

    storage_id: Optional[str] = None
    """ Id used as key in the localStorage, if the related entry exists, None otherwise. """

    load_py_name: Optional[str] = None
    """
    Python file name used for the download/export machinery of the IDEs (Will generally differ
    from the macro `py_name` argument).
    """

    has_check_btn: Optional[bool] = None
    """
    True if the related element will have a visible validation button in the GUI.
    <br>_Alternative way to access the information in `self.has.check_btn` or
    `self.content.check_btn`_
    """

    content: Optional['Content'] = None
    """
    Object showing the "content" associated with sections or buttons for the generated object.
    <br>_See the detailed interface of the `Content` objects. Support autocompletion when
    defined._
    """

    has: Optional['HasContent'] = None
    """
    Object indicating what sections, files or buttons are present on the generated object.
    <br>_See the detailed interface of the `HasContent` objects. Support autocompletion when
    defined._
    """





class MacroData(MacroDataGeneric, MacroDataSpecific):

    ENV: ClassVar['PyodideMacrosPlugin']
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]]


    @staticmethod
    def register_config(env:'PyodideMacrosPlugin'):
        MacroData.ENV = env
        MacroData.SITE_URL = env.site_url + '/' * (not env.site_url.endswith('/'))


    def __init__(self, macro_name, args_dict):
        self.macro    = macro_name
        self.args     = self.ARGS_CLASS(args_dict)
        self.meta     = self.ENV.page.meta or {}
        self.src_uri  = self.ENV.page.file.src_uri
        self.page_url = self.ENV.page.url
        self.full_page_url = self.SITE_URL + self.page_url
        self.abs_link = self.full_page_url



    def register_macro_manager_data(self, manager:'IdeManager'):
        """
        Update all the infos related to IdeManager instances, once they have been created.
        """
        from pyodide_mkdocs_theme.pyodide_macros.macros.ide_files_data import IdeFilesExtractor

        def get_value(prop:str, target:str):
            val = getattr(manager.files_data, target)
            if 'REM' in prop:
                val = val and val.resolve()     # Resolve Path if exists
            return val

        contents = {
            prop: get_value(prop, target)
            for prop,target in IdeFilesExtractor.PROPS_TO_CONTENTS.items()
        }
        contents['check_btn'] = manager.has_check_btn       # duplicate the way to access the info

        # Fill the Content and HasContent data:
        self.content = Content(contents)
        self.has     = HasContent({ k: bool(v) for k,v in contents.items() })

        self.storage_id    = manager.editor_name
        self.load_py_name  = self.build_name(manager.built_py_name)
        self.has_check_btn = manager.has_check_btn
        self.abs_link      = f"{ self.full_page_url }#{ self.storage_id }"



    def build_name(self, built_py:str):
        if self.args.ID is not None:
            built_py = f'{ built_py[:-3] }-{ self.args.ID }.py'
        return built_py







# vvvvvvvvvvvvvvvvv
# GENERATED CLASSES


class Content(MacroDataWithGetters):
    """ Content of each section (or absolute Path on the disk for REMs files). """

    env: str = DataGetter(default="")
    env_term: str = DataGetter(default="")
    code: str = DataGetter(default="")
    corr: str = DataGetter(default="")
    tests: str = DataGetter(default="")
    secrets: str = DataGetter(default="")
    post_term: str = DataGetter(default="")
    post: str = DataGetter(default="")
    REM: Optional[Path] = DataGetter(none_as_default=True)
    VIS_REM: Optional[Path] = DataGetter(none_as_default=True)
    check_btn: bool = DataGetter(default=False)



class HasContent(MacroDataWithGetters):
    """ Flags to know what sections/elements are defined or not. """

    env: bool = DataGetter(default=False, wraps=bool)
    env_term: bool = DataGetter(default=False, wraps=bool)
    code: bool = DataGetter(default=False, wraps=bool)
    corr: bool = DataGetter(default=False, wraps=bool)
    tests: bool = DataGetter(default=False, wraps=bool)
    secrets: bool = DataGetter(default=False, wraps=bool)
    post_term: bool = DataGetter(default=False, wraps=bool)
    post: bool = DataGetter(default=False, wraps=bool)
    REM: bool = DataGetter(default=False, wraps=bool)
    VIS_REM: bool = DataGetter(default=False, wraps=bool)
    check_btn: bool = DataGetter(default=False)



HAS_CONTENT_PROPS = [p for p in dir(HasContent) if not p.startswith('_')]









class MacroArgsDataIDE(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataIDE macro. """

    py_name: str = DataGetter()
    ID: int = DataGetter(none_as_default=True)
    SANS: str = DataGetter()
    WHITE: str = DataGetter()
    REC_LIMIT: int = DataGetter()
    MERMAID: bool = DataGetter()
    AUTO_RUN: bool = DataGetter()
    MAX: int = DataGetter()
    LOGS: bool = DataGetter()
    MODE: str = DataGetter()
    MIN_SIZE: int = DataGetter()
    MAX_SIZE: int = DataGetter()
    TERM_H: int = DataGetter()
    TEST: str = DataGetter()
    TWO_COLS: bool = DataGetter()
    STD_KEY: str = DataGetter()
    EXPORT: bool = DataGetter()

class MacroDataIDE(MacroData):
    """ Runtime data object for the MacroDataIDE macro. """

    args: MacroArgsDataIDE
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataIDE





class MacroArgsDataTerminal(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataTerminal macro. """

    py_name: str = DataGetter()
    ID: int = DataGetter(none_as_default=True)
    SANS: str = DataGetter()
    WHITE: str = DataGetter()
    REC_LIMIT: int = DataGetter()
    MERMAID: bool = DataGetter()
    AUTO_RUN: bool = DataGetter()
    TERM_H: int = DataGetter()
    FILL: str = DataGetter()

class MacroDataTerminal(MacroData):
    """ Runtime data object for the MacroDataTerminal macro. """

    args: MacroArgsDataTerminal
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataTerminal





class MacroArgsDataPy_btn(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataPy_btn macro. """

    py_name: str = DataGetter()
    ID: int = DataGetter(none_as_default=True)
    SANS: str = DataGetter()
    WHITE: str = DataGetter()
    REC_LIMIT: int = DataGetter()
    ICON: str = DataGetter()
    HEIGHT: int = DataGetter()
    WIDTH: int = DataGetter()
    SIZE: int = DataGetter()
    TIP: str = DataGetter()
    TIP_SHIFT: int = DataGetter()
    TIP_WIDTH: float = DataGetter()
    WRAPPER: str = DataGetter()
    MERMAID: bool = DataGetter()
    AUTO_RUN: bool = DataGetter()

class MacroDataPy_btn(MacroData):
    """ Runtime data object for the MacroDataPy_btn macro. """

    args: MacroArgsDataPy_btn
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataPy_btn





class MacroArgsDataRun(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataRun macro. """

    py_name: str = DataGetter()
    ID: int = DataGetter(none_as_default=True)
    SANS: str = DataGetter()
    WHITE: str = DataGetter()
    REC_LIMIT: int = DataGetter()
    MERMAID: bool = DataGetter()

class MacroDataRun(MacroData):
    """ Runtime data object for the MacroDataRun macro. """

    args: MacroArgsDataRun
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataRun





class MacroArgsDataSection(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataSection macro. """

    py_name: str = DataGetter()
    section: str = DataGetter()

class MacroDataSection(MacroData):
    """ Runtime data object for the MacroDataSection macro. """

    args: MacroArgsDataSection
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataSection





class MacroArgsDataMulti_qcm(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataMulti_qcm macro. """

    questions: Any = DataGetter()
    description: str = DataGetter()
    hide: bool = DataGetter()
    multi: bool = DataGetter()
    shuffle: bool = DataGetter()
    shuffle_questions: bool = DataGetter()
    shuffle_items: bool = DataGetter()
    admo_kind: str = DataGetter()
    admo_class: str = DataGetter()
    qcm_title: str = DataGetter()
    tag_list_of_qs: str = DataGetter()
    DEBUG: bool = DataGetter()

class MacroDataMulti_qcm(MacroData):
    """ Runtime data object for the MacroDataMulti_qcm macro. """

    args: MacroArgsDataMulti_qcm
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataMulti_qcm





class MacroArgsDataPy(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataPy macro. """

    py_name: str = DataGetter()

class MacroDataPy(MacroData):
    """ Runtime data object for the MacroDataPy macro. """

    args: MacroArgsDataPy
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataPy





class MacroArgsDataFigure(MacroDataWithGetters):
    """ Runtime arguments object for the MacroDataFigure macro. """

    div_id: str = DataGetter()
    div_class: str = DataGetter()
    inner_text: str = DataGetter()
    admo_kind: str = DataGetter()
    admo_class: str = DataGetter()
    admo_title: str = DataGetter()
    p5_buttons: str = DataGetter()

class MacroDataFigure(MacroData):
    """ Runtime data object for the MacroDataFigure macro. """

    args: MacroArgsDataFigure
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = MacroArgsDataFigure


# GENERATED CLASSES
# ^^^^^^^^^^^^^^^^^





class IdeToTest(MacroDataIDE):

    _as_dict: dict

    @property
    def rel_dir_url(self):
        """
        Relative url to the directory containing the initial markdown file
        (typically used to redirect links/fetches during the tests).
        """
        dir_step_up = not self.ENV.use_directory_urls or not self.src_uri.endswith('index.md')
        rel_dir_url = str(Path(self.page_url).parent) if dir_step_up else self.page_url
        return rel_dir_url


    @classmethod
    def from_ide(cls, ide:'Ide'):

        # Extract on the fly the very last MacroData added to the env (using a copy to make sure
        # no one messes up my data :p ):
        args_dct = ide.env.all_macros_data[-1].args._data_dct.copy()        # pylint: disable=protected-access

        test = cls(ide.MACRO_NAME, args_dct)
        test.register_macro_manager_data(ide)

        # Rebuild an DIE name to show in the center panel (warning: do not use
        # test.build_py_name which covers a different purpose)
        tail     = "" if test.args.ID is None else f', ID={ test.args.ID }'
        ide_name = f"{ test.page_url.rstrip('/') }/{ test.args.py_name }{ tail }"

        test._as_dict = dict(
            **ide.test_config.as_dict(),
            rel_dir_url = test.rel_dir_url,
            page_url    = test.full_page_url,
            ide_link    = test.abs_link,
            ide_name    = ide_name,
            editor_id   = test.storage_id,
        )
        return test


    def as_dict(self):
        return self._as_dict
