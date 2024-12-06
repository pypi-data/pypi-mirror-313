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
import re
import json
from abc import ABCMeta
from typing import Any, Callable, ClassVar, Dict, List, Optional, TYPE_CHECKING, Type
from dataclasses import dataclass, fields
from functools import reduce

from mkdocs.config import config_options as C
from mkdocs.exceptions import ConfigurationError
from mkdocs.config.base import BaseConfigOption



from ...pyodide_logger import logger
from ...messages.fr_lang import Lang
from ._string_tools import (
    ConfigOptionCode,
    DeprecationTemplate,
    get_python_type_as_code,
    unicode_to_nicer,
)
from .common_tree_src import CommonTreeSrc, DeprecationStatus, YamlSchema

if TYPE_CHECKING:
    from ..pyodide_macros_plugin import PyodideMacrosPlugin




VAR_ARGS     = -1
DEFAULT_LANG = Lang()


GETTERS_WITH_PATH = (
    'args', 'testing'
)






@dataclass
class ConfigOptionSrcDumpable(CommonTreeSrc, metaclass=ABCMeta):
    """
    Define a macro argument, that can be dumped as mkdocs C.OptionItem for a plugin Config.
    """

    # ------------------------------------------------------------------------
    # kwargs only:


    conf_type: Optional[BaseConfigOption] = None
    """
    ConfigOption to use for this argument.
    If not given, use `C.Type(py_type, default=self.default)`.
    """

    default: Optional[Any] = None
    """
    Default value for the conf_type. Ignored if None (use is_optional for this).
    """

    is_optional: bool = False
    """
    If True, add a C.Optional wrapper around the conf_type (given or generated).
    """

    index: Optional[int] = None
    """
    Index of the argument in the `*args` tuple, if it's positional.
    If index is -1, means the argument itself is a varargs.
    """


    @property
    def is_positional(self):
        """ Is a positional argument or a varargs? """
        return self.index is not None

    @property
    def is_varargs(self):
        """ Is a positional argument or a varargs? """
        return self.index is VAR_ARGS



    def __post_init__(self):
        super().__post_init__()

        if self.in_config:

            if self.conf_type is None:
                # Reminder: "default=None" means "required" in mkdocs ConfigOptions.
                self.conf_type = C.Type(self.py_type, default=self.default)

            elif self.default is not None and self.default != self.conf_type.default:
                # NOTE: copy_with requires the second condition so that everything works correctly.
                raise ConfigurationError(
                    f"{self} as a `conf_type` argument, hence it shouldn't have a `default` one."
                )
            else:
                self.default = self.conf_type.default

            if self.is_optional:
                self.conf_type = C.Optional(self.conf_type)



    def copy_with(self, **kw):
        """
        Create a copy of the current instance, possibly changing some things on the fly.
        """
        args = {
            field.name: getattr(self, field.name) for field in fields(self.__class__)
        }
        args.update(kw)
        return self.__class__(**args)



    def to_config(self):
        return self.conf_type












@dataclass
class ConfigOptionSrcMaestroArticulated(ConfigOptionSrcDumpable, metaclass=ABCMeta):
    """
    Handle the articulation between data of ConfigOptionSrc and the PyodideMacroPlugin.
    """


    # None hoping for failure if used at the wrong time...
    maestro_extractor_getter_name: str = None
    """
    MaestroBase property name (ConfigExtractor).
    WARNING: available only after build_accessor has been run!
    """

    value_transfer_processor: Optional[Callable[[Any],Any]] = None
    """
    If the option is not deprecated, this function must be wrapping the ConfigExtractor getter,
    to update the value on the fly (possibly pushing a warning in the logger).
    If the option is deprecated, the function may be used as conversion function, used when
    automatically transferring the value from a deprecated option to it's new location.
    """


    def build_accessor(self, path: List[str]):
        """
        Register the internal properties `config_setter_path` and `maestro_extractor_getter_name`
        for the current instance, given the path of attributes to reach it from the root config
        object.
        """
        super().build_accessor(path)

        getter = self.name
        for special in GETTERS_WITH_PATH:
            if special in path:
                i = path.index(special)
                getter = '_'.join(path[i:])
                break

        self.maestro_extractor_getter_name = self.is_deprecated*'_' + getter



    def get_current_value(self, env:'PyodideMacrosPlugin'):
        """
        Get the current config value for this argument.
        """
        return getattr(env, self.maestro_extractor_getter_name)



    def set_value(self, value:Any, env:'PyodideMacrosPlugin', path:Optional[str]=None):
        """
        Set the current config value for this argument.
        """
        if path:
            *path, name = path.split('.')
        else:
            path, name = self.config_setter_path, self.name

        obj = reduce(getattr, path, env)
        obj[name] = value



    def to_base_maestro_getter_code(self):
        """
        Build the ConfigExtractor code for BaseMaestro class (used from mkdocs_hooks.on_config)
        """
        prop    = self.maestro_extractor_getter_name
        py_type = get_python_type_as_code(self.py_type)
        args    = [
            f"'{ '.'.join( self.config_setter_path )}'",
        ]

        for special in GETTERS_WITH_PATH:
            if special in self.config_setter_path:
                args.append(f"prop='{self.name}'")
                break

        if self.is_deprecated:
            args.append("deprecated=True")

        if self.value_transfer_processor:
            args.append(f"alteration={ self.value_transfer_processor.__name__ }")

        return f"\n    { prop }: { py_type } = ConfigExtractor({ ', '.join(args) })"













@dataclass
class ConfigOptionSrcDynamicLangDefault(ConfigOptionSrcMaestroArticulated, metaclass=ABCMeta):
    """
    Allow to modify the default values of the ConfigOptionSrc instance coming from the Lang
    objects, and its related config_option at runtime: the default values for Lang may change
    depending on:
        - The language selected in `theme.language`.
        - Potential Lang overrides done at macro definition time (`on_config` hook).

    Those values need to be updated _before_ any JS content is dumped to html pages, while
    they cannot be at `ConfigOptionSrc` declaration time.
    """

    # ------------------------------------------------------------------------
    # kwargs only:

    lang_default_access: Optional[str] = None
    """
    Path to access the wanted string in env.lang, for values depending on the theme language,
    as set in mkdocs.yml.
    """


    def __post_init__(self):
        self.assign_lang_default_if_needed()      # To do BEFORE super().__post_init__()
        super().__post_init__()



    def assign_lang_default_if_needed(self, env:Optional['PyodideMacrosPlugin']=None):
        """
        Assign a value as default to the current instance and also to the mkdocs underlying
        plugin config (avoiding the ConfigExtractor setter, which is forbidden).
        """
        if not self.lang_default_access:
            return

        lang         = env.lang if env else DEFAULT_LANG
        prop, msg    = self.lang_default_access.split('.')
        self.default = getattr( getattr(lang, prop), msg)

        if env:
            self.set_value(self.default, env)













@dataclass
class ConfigOptionSrcDeprecationHandler(ConfigOptionSrcMaestroArticulated, metaclass=ABCMeta):
    """
    Deprecation related logistics:

    - Actually deprecated config options.
    - NOT deprecated config options whose the value has to be extracted from another deprecated
      config option, IF it has been set.

    This is implemented for backward compatibility on breaking changes, allowing to define what
    to do on the way:
        1. Only raise warnings
        2. Raise errors
    And in both cases, this allows to give precise feedback to the user about what needs to be
    changed to update their mkdocs.yml file (or meta...) to avoid the warnings/errors.
    """


    moved_to: str = ""
    """
    For DeprecationStatus.moved only: where to transfer the value.
    """


    def __post_init__(self):
        super().__post_init__()

        if self.is_deprecated:

            if self.default is not None:
                raise ConfigurationError(
                    "Something suspicious happened: deprecated options shouldn't have default "
                    f"values: ({ self } with default={ self.default })"
                )
            if not isinstance(self.conf_type, C.Optional):      # Always optional!
                self.conf_type = C.Optional(self.conf_type)

            self.conf_type = C.Deprecated(option_type=self.conf_type)




    def handle_deprecation_or_changes(self, env:'PyodideMacrosPlugin'):
        """
        If an argument/config option isn't deprecated but has a value_transfer_processor callback,
        replace the current value with the original one fed to the callback.

        If the argument.option is deprecated and the value is not None, handle any post processing
        (moving and/or modifying the current value on the fly), and warn the user (either with a
        simple warning, or an error, depending on the configuration).

        NOTE: the caller makes sure `ConfigExtractor.RAISE_DEPRECATION_ACCESS` is False, so that the
              value of the current argument/option can be extracted in the plugin instance.
        """
        if not self.is_deprecated and self.value_transfer_processor:
            value = self.get_current_value(env)
            fresh = self.value_transfer_processor(value)
            self.set_value(fresh, env)
            return

        if self.is_deprecated:
            value = self.get_current_value(env)
            if value is None:
                return

            if self.dep_status == DeprecationStatus.moved:
                target = re.sub(r'^config', 'pyodide_macros', self.moved_to)
                logger.info(f"Reassign { self.py_macros_path } to { target }")

                if self.value_transfer_processor:
                    value = self.value_transfer_processor(value)

                self.set_value(value, env, path=self.moved_to)

            template: str = getattr(DeprecationTemplate, self.dep_status)
            full_msg = template.format(src=self.py_macros_path, moved_to=self.moved_to)
            return full_msg













@dataclass
class ConfigOptionSrcToDocs(ConfigOptionSrcDeprecationHandler, metaclass=ABCMeta):
    """
    Represent the docs related information about an argument of a macro.
    """

    # ------------------------------------------------------------------------
    # kwargs only:

    docs_type: str = ""
    """ String replacement for the types in the docs """


    docs_default_as_type: bool = True
    """ If True, use the default value instead of the type in the as_docs_table output. """


    ide_link: bool=False
    """
    If True, when generating `as_table_row`, an md link will be added at the end, pointing
    toward the equivalent argument in the IDE-details page.
    """

    line_feed_link: bool = True
    """
    Add a line feed or not, before the ide_link when rendering `as_table_row`.
    """


    def __post_init__(self):
        super().__post_init__()
        if self.is_deprecated:
            self.in_macros_docs = False


    @property
    def doc_name_type_min_length(self):
        """
        Compute the length of the `name: type` string.
        """
        return 1 + self.is_varargs + len(self.name) + len(self.get_docs_type())


    def get_type_str(self):
        """
        Return the name of the python type, unless `self.docs_default_as_type` is true and the
        `self.default` is not None: in that case, return `repr(self.default)`.
        """
        if self.docs_default_as_type and self.default is not None:
            return repr(self.default)
        return self.py_type.__name__



    def get_docs_type(self):
        """
        Return the string to use to describe de type of this argument in the docs.
        """
        return self.docs_type or self.py_type.__name__



    def signature(self, size:int=None):
        """
        Build a prettier signature, with default values assignment vertically aligned, of the
        macro call signature.
        """
        length   = self.doc_name_type_min_length
        n_spaces = length if size is None else size - length + 1
        star     = '*' * self.is_varargs
        type_str = self.get_docs_type()
        return f"\n    { star }{ self.name }:{ ' '*n_spaces }{ type_str } = {self.default!r},"



    def as_table_row(self, only=True):
        """
        Generate a md table row for this specific argument.

        @only:  Conditions what is used for arg name, type and value.
                It is `False` when building IDE "per argument tables" (aka, with
                `macro_args_table(..., only=...)`.

                only | False   | True
                col1 | type    | nom argument
                col2 | default | type (or default, depending on docs_default_as_type)
                col3 | docs    | docs + ide_link if needed
        """

        if only:
            col1, col2, col3_doc = (
                f"#!py { self.get_docs_type() }",
                repr(self.default),
                self.docs
            )
        else:
            col1, col2, col3_doc = (
                self.name,
                self.get_type_str(),
                self.docs,
            )
            if self.ide_link:
                col3_doc += "<br>" * self.line_feed_link
                col3_doc += f"_([plus d'informations](--IDE-{ self.name }))_"

        return f"| `{ col1 }` | `#!py { col2 }` | { col3_doc } |"











@dataclass
class ConfigOptionSrcToYaml(ConfigOptionSrcToDocs, metaclass=ABCMeta):
    """
    Handle yaml related conversions:
        - schemas
        - mkdocs config trees
    """
    # pylint: disable=protected-access

    docs_page_relative_url: Path = None


    def to_yml_value(self, *value:Any):
        """ Convert a value to a "json nicer docs representation". """
        value       = value[0] if value else self.default
        json_value  = json.dumps( value )
        nicer_value = unicode_to_nicer(json_value)
        return nicer_value


    def as_mkdocs_yml_line(self):
        value = self.to_yml_value()
        return f"{ self.indent }{ self.name }: { value }"


    #----------------------------------------------------------------------------


    def to_docs_page_header(self):
        type_value = ConfigOptionCode.extract(self.conf_type)
        return (
            f"{'{{'} anchor_redirect(id={ self.mkdocstrings_id !r}) {'}}'}"
            f"`#!py { self.name } = { type_value }`"
        )


    def to_docs_page_content(self):
        return self.docs


    #----------------------------------------------------------------------------


    def _get_builder(self, opt: BaseConfigOption):
        kls_name = opt.__class__.__name__
        builder  = getattr(self, '_'+kls_name.lower())
        return builder


    def build_yaml_schema(self, site_url:Path) -> YamlSchema :
        builder = self._get_builder(self.conf_type)
        sub_dct = builder()
        schema = {
            "markdownDescription": self.get_yaml_schema_md_infos(site_url),
            "title": self.name,
            **sub_dct,
        }

        # NOTE: yaml options with null as default in the schema never show up => just ignore them
        if self.default is not None:
            schema['default'] = self.to_yml_value()

        return schema


    TYPES: ClassVar[ Dict[Type,str] ] = {
        int:    'integer',
        float:  'number',
        str:    'string',
        bool:   'boolean',
    }


    def _type(self, obj:Optional[C.Type]=None):
        typ: C.Type = obj or self.conf_type
        return {'type': self.TYPES[typ._type] }

    def _optional(self, obj:Optional[C.Optional]=None):
        option: C.Optional = obj or self.conf_type
        typ = option.option
        return self._get_builder(typ)(typ)

    def _choice(self, obj:Optional[BaseConfigOption]=None):
        choice: C.Choice = obj or self.conf_type
        enum = choice.choices

        if self.name == 'decrease_attempts_on_user_code_failure':
            enum = tuple( v for v in enum if isinstance(v,str) )

        dct = {'enum': enum }
        if choice.default is not None:
            dct['default'] = choice.default
        return dct

    def _listofitems(self, obj:Optional[BaseConfigOption]=None):
        lst:C.ListOfItems = obj or self.conf_type
        return {
            'type': 'array',
            'items':{
                'type': self.TYPES[ lst.option_type._type ]
            }
        }

    def _dictofitems(self, obj:Optional[BaseConfigOption]=None):
        # lst:C.DictOfItems = self.conf_type
        # return {
        #     'type': 'object',
        #     'properties': [],
        # }
        raise AttributeError('not implemented')








@dataclass
class ConfigOptionSrc(
    ConfigOptionSrcToYaml,
    ConfigOptionSrcToDocs,
    ConfigOptionSrcDeprecationHandler,
    ConfigOptionSrcDynamicLangDefault,
    ConfigOptionSrcMaestroArticulated,
    ConfigOptionSrcDumpable,
):
    """
    Top level concrete class representing a "BaseConfigOption to be" (mixin!).
    """




@dataclass
class ConfigOptionIdeLink(ConfigOptionSrc):
    """ Reduce boiler plate for ConfigOptionSrc instances. """

    def __post_init__(self):
        self.ide_link = True
        super().__post_init__()




@dataclass
class ConfigOptionDeprecated(ConfigOptionSrc):
    """
    Reduce boiler plate for ConfigOptionSrc instances.
    By default, creates an "unsupported" deprecated object.
    """

    def __post_init__(self):
        self.dep_status = self.dep_status or DeprecationStatus.unsupported
        if self.moved_to:
            self.moved_to = f'config.{ self.moved_to }'
            self.dep_status = DeprecationStatus.moved

        super().__post_init__()
