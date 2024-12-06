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


import json
from dataclasses import dataclass
from textwrap import dedent
from typing import Tuple, TYPE_CHECKING

from mkdocs.exceptions import BuildError

from ._string_tools import get_python_type_as_code
from .sub_config_src import SubConfigSrc, ConfigOptionSrc

from ..tools import macros_data


if TYPE_CHECKING:
    from ..pyodide_macros_plugin import PyodideMacrosPlugin












@dataclass
class BaseMacroConfigSrc(SubConfigSrc):

    is_macro: bool = True
    """ Override parent value """

    kwarg_index: int = None     # Failure if not properly computed
    """
    Index of the first kwarg in the macro call (= where to insert a `*,` when
    building the signature).
    """


    def __post_init__(self):

        super().__post_init__()
        elements: Tuple['ConfigOptionSrc'] = self.elements      # linting purpose

        positionals = tuple(
            arg for arg in elements if not arg.is_config and arg.is_positional
        )
        start_args = elements[:len(positionals)]
        if start_args != positionals:
            raise ValueError(dedent(f"""
                Positional arguments in { self } definition should come first:
                    Positional args found: {', '.join(arg.name for arg in positionals)}
                    Order of declaration:  {', '.join(arg.name for arg in elements)}
            """))

        last_pos_arg_is_varargs = positionals[-1].name.startswith('*')
        self.kwarg_index        = 0 if last_pos_arg_is_varargs else len(positionals)



    def as_docs_table(self):
        """
        Converts all arguments to a 3 columns table (data rows only!):  name + type + help.
        No indentation logic is added here.
        """
        return '\n'.join(
            arg.as_table_row(False) for arg in self.subs_dct.values() if arg.in_macros_docs
        )


    def signature_for_docs(self):
        """
        Converts the SubConfigSrc to a python signature for the docs, ignoring arguments that
        are not "in_macros_docs".
        """
        args = [arg for arg in self.subs_dct.values() if arg.in_macros_docs]
        size = max( arg.doc_name_type_min_length for arg in args )
        lst  = [ arg.signature(size) for arg in args ]

        if self.kwarg_index:
            lst.insert(self.kwarg_index, "\n    *,")

        return f"""
```python
{ '{{' } { self.name }({ ''.join(lst) }
) { '}}' }
```
"""


    def config_options_docs_summary(self):
        return ""



    def add_defaults_to_macro_call(self, args:tuple, kwargs:dict, env:'PyodideMacrosPlugin'):
        """
        Modify the args and/or kwargs to add the missing arguments, using the current global
        config (MaestroMeta having swapped the config already, if needed).
        """
        for arg_name, arg in self.subs_dct.items():

            if not arg.in_config:                                   # not handled
                continue

            if arg.is_positional and arg.index >= len(args):        # Add missing varargs
                args += ( arg.get_current_value(env), )

            elif not arg.is_positional and arg_name not in kwargs:  # Add missing kwargs
                kwargs[arg_name] = arg.get_current_value(env)

        return args, kwargs







class MacroConfigSrcToArgsData(BaseMacroConfigSrc):


    def macro_data_class_names(self):
        kls_name = self.name.capitalize() if self.name.islower() else self.name
        kls_name = 'MacroData' + kls_name
        return kls_name, kls_name.replace('Macro', 'MacroArgs')



    def generate_macro_data_classes_code(self, is_code=True):
        """ Generate the code for the related MarcoArgsDataXXX class. """

        def build_property_code(elt:ConfigOptionSrc):
            prop_type = 'Any' if elt.name=='questions' else get_python_type_as_code(elt.py_type)
            with_def  = 'none_as_default=True' if elt.name=='ID' else ""
            getter    = f" = DataGetter({ with_def })" if is_code else ""
            return f"\n    {elt.name}: { prop_type }{ getter }"

        members = ''.join( build_property_code(elt) for elt in self.elements )

        kls_name, args_kls_name = self.macro_data_class_names()
        def_after, def_before   = "", f'''

class { kls_name }(MacroData):
    """ Runtime data object for the { kls_name } macro. """

    args: { args_kls_name }'''

        if is_code:
            def_before, def_after = def_after, def_before
            def_after += f'''
    ARGS_CLASS: ClassVar[Type[MacroDataWithGetters]] = { args_kls_name }'''

        return f'''{ def_before }\n\n
class { args_kls_name }{ "(MacroDataWithGetters)" * is_code }:
    """ Runtime arguments object for the { kls_name } macro. """
{ members }{ def_after }
\n\n'''



    def to_macro_data(self, args:tuple, kwargs:dict, env:'PyodideMacrosPlugin'):
        """
        Convert the given args and kwargs (related to the current macro config source, for the
        current macro call at runtime) to the equivalent MacroData object.
        """
        args_dct    = self._args_to_dict(args, kwargs, env)
        kls_name, _ = self.macro_data_class_names()
        data_kls    = getattr(macros_data, kls_name)
        return data_kls(self.name, args_dct)



    def _args_to_dict(self, args:tuple, kwargs:dict, env:'PyodideMacrosPlugin'):
        dct = {}
        kwargs = kwargs.copy()
        args: list = [*reversed(args)]

        for elt in self.elements:
            if elt.is_varargs:
                args, value = [], tuple(reversed(args))
            elif elt.is_positional:
                value = args.pop()
            elif not elt.in_config and elt.name not in kwargs:
                continue
            else:
                value = kwargs.pop(elt.name)

            dct[elt.name] = value

        # Skip validations in production (relying on the IdeManager validation only), and
        # let SIZE go through, to use the warn_unmaintained logistic (proper error message)
        if env._dev_mode and (args or kwargs and 'SIZE' not in kwargs):
            raise BuildError(
                f"Couldn't generate a valid argument dict for the macro {'{{'}{self.name}(...)"
                "{'}}'}. Remaining:\n\targs: { args }\n\tkargs: { kwargs }"
            )

        return dct







@dataclass
class MacroConfigSrc(
    MacroConfigSrcToArgsData,
    BaseMacroConfigSrc,
):
    """
    Specific class dedicated to represent the config of a macro call, with it's
    arguments and specific behaviors (see pmt_macros, for example).
    """





@dataclass
class MultiQcmConfigSrc(MacroConfigSrc):
    """ Special class handling the json files data for the multi_qcm macro """


    def add_defaults_to_macro_call(
        self, args:tuple, kwargs:dict, env:'PyodideMacrosPlugin'
    ):
        if len(args)==1 and isinstance(args[0],str) and args[0].endswith('.json'):
            args, kwargs = self._extract_json_qcm(args[0], kwargs, env)
        return super().add_defaults_to_macro_call(args, kwargs, env)



    def _extract_json_qcm(self, file:str, kwargs:dict, env:'PyodideMacrosPlugin'):

        target = env.get_sibling_of_current_page(file)
        if not target or not target.is_file():
            raise BuildError(
                f"Couldn't find {file} file for `multi_qcm` macro call ({ env.file_location() })"
            )

        dct: dict = json.loads(target.read_text(encoding='utf-8'))
        args = dct.pop('questions', None)

        if args is None:
            raise BuildError(
                "No questions array found in json data, for `multi_qcm` macro call "
                f"({ env.file_location() })"
            )

        for k,v in dct.items():
            if k not in kwargs:
                kwargs[k] = v

        return args, kwargs
