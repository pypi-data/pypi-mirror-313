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


from abc import ABCMeta
from pathlib import Path
import re
from typing import Any, ClassVar, Dict, List, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field

from mkdocs.exceptions import ConfigurationError

from ...tools_and_constants import AutoDescriptor
from ._string_tools import inline_md


if TYPE_CHECKING:
    from .sub_config_src import ConfOrOptSrc




YamlSchema = Dict[str, 'YamlSchema']




class DeprecationStatus:
    """ All possible deprecation types """

    moved       = AutoDescriptor()
    removed     = AutoDescriptor()
    unsupported = AutoDescriptor()












@dataclass
class CommonTreeSrcBase:
    """
    Properties and/or methods that are common to ConfigOptionSrc and SubConfigSrc classes.

    Note: This is more of a reminder than anything, considering the properties, but it allows
          to enforce the interface when it comes to methods.
    """


    name: str = ''
    """ Element's name in the tree hierarchy. """

    py_type: Any = None
    """
    Type of the actual value, used at runtime in python (see BaseMaestro extractors).
    """

    elements: Tuple['ConfOrOptSrc'] = ()
    """ Sub elements of the current SubConfigSrc  """


    #---------------------------------------------------------------------


    in_config: bool = True
    """
    This is about python runtime internals, NOT presentation to any user (docs, yaml schema, ...).

    If False, this argument will not be added to the Config class/objects.
    Used for things that are implemented or were, or need to be documented, but isn't a valid
    config at runtime, or isn't implemented anymore, ...
    """

    subs_dct: Dict[str,'ConfOrOptSrc'] = field(default_factory=dict)
    """ Children elements (stays empty for ConfigOptionSrc instances). """

    is_config: bool = False
    """ True if the given object is a SubConfigSrc object """

    is_macro: bool = False
    """ True if the given object is a MacroConfigSrc object """

    is_plugin_config: bool = False
    """ True if the given object is a PluginConfigSrc object """


    #---------------------------------------------------------------------
    # All these are suing None, hence triggering failure if used at the wrong time (hopefully)...
    #       => `build_accessor` MUST HAVE BEEN RUN BEFORE USING THOSE.


    config_setter_path: Tuple[str] = None
    """
    "Path" to access the config holding this argument in CopiableConfig objects.
    This allows to modify them on the fly if needed (Lang...).
    """

    depth: int = None
    """ Depth if the current instance in the ConfigSrc tree. """

    py_macros_path: str = None
    """
    Path of attributes to the current element, with "pyodide_macros" as source instead of "config".
    """


    @property
    def indent(self) -> str :
        """ Computed because self.depth doesn't exist at init time. """
        return '    ' * self.depth


    #---------------------------------------------------------------------


    def __post_init__(self):
        """
        (Sink method, to make sure super().__post_init__() is always callable in a child class)
        """

    def __str__(self):
        path_name = '.'.join((self.config_setter_path or ()) + (self.name,))
        return f"{ self.__class__.__name__ }({ path_name })"


    def has(self, sub_name:str):
        """ Check if @sub_name is a sub element of the current object. """
        return sub_name in self.subs_dct


    def yield_invalid_yaml_paths(self, meta_dct:dict):
        """
        Check that the given property name, in the given meta_dct, is actually an option
        or a subconfig of the current instance, and yield an error message when an invalid
        property is found.
        """
        for prop in meta_dct:
            if prop not in self.subs_dct:
                prefix = 15  # "pyodide_macros."
                path   = f"{ self.py_macros_path[prefix:] }.{prop}".lstrip('.')
                yield f"{ path } is not a valid configuration option for pyodide_macros."
            else:
                sub = self.subs_dct[prop]
                if sub.is_config:
                    yield from sub.yield_invalid_yaml_paths(meta_dct[prop])


    def build_accessor(self, path: List[str]):
        """
        Register the internal properties `config_setter_path`.
        """
        self.py_macros_path     = '.'.join( ('pyodide_macros',*path[1:]) )
        self.config_setter_path = tuple(path[:-1])
        self.depth              = len(self.config_setter_path)


    def to_config(self):
        """
        Transform the current class hierarchy to an actual mkdocs plugin Config object,
        or subitems of it.
        """
        raise NotImplementedError()


    def get_base_config_option_classname(self, name:str=""):
        """
        Convert the given name (or self.name) to the name of the concrete mkdocs.config.Config
        name built at runtime (through to_config)

        """
        name = name or self.name
        uppers = map(str.title, name.split('_'))       # split because pyodide_macros... x)
        return f"{ ''.join(uppers) }Config"









@dataclass
class CommonTreeSrcDeprecated(CommonTreeSrcBase, metaclass=ABCMeta):
    """
    Handle deprecation related common logistic.
    """

    dep_status: Optional[DeprecationStatus] = None
    """ Kind of deprecation. Also property of DeprecationTemplate namespace. """

    @property
    def is_deprecated(self):
        """ True if the corresponding ConfigOption is deprecated """
        return bool(self.dep_status)



    def __post_init__(self):
        super().__post_init__()

        if self.is_deprecated:

            wanted = True                   # Change this to modify the global behavior...
            if self.in_config != wanted:
                raise ConfigurationError(
                    "Something suspicious happened: deprecated options should always have "
                    f"`in_config={ wanted }` ({ self })"
                )
            if self.dep_status is None:
                raise ConfigurationError(
                    "Deprecated options should have `dep_status` argument:"
                    f"({ self })"
                )











@dataclass
class CommonTreeSrcWithDocsOrYaml(CommonTreeSrcDeprecated, metaclass=ABCMeta):
    """ Generic behaviors about docs/yaml related data. """


    docs: str = ""
    """ Text to use when building the "summary" args tables in the docs """

    in_macros_docs: bool = True
    """
    If False, this argument will not be present in docs related generated content:
        - tables of arguments
        - signatures
    Note: deprecated options are never in docs (updated automatically).
    """


    in_yaml_docs: bool = True
    """
    If True, this element should be present in the yaml related dumps and in the md config tree.
    The messages used to build those are:

    * `yaml_desc` for the yaml schema (en only).
    * `docs` for the markdown config (Lang).
    """

    yaml_desc: str=""
    """
    Short description that can used in place of self.docs here or there.
    If not given, self.docs is assigned to it.

    WARNING: HAS TO CONTAIN BARE/simple MARKDOWN => NO MACROS CALLS!
    """

    docs_page_url: Path = None
    """
    In the form `docs_page_url = Path("relative_path/#anchor_template")`, then used
    in the following way:

        str( site_url / docs_page_url ).format( name=self.name,
                                                py_macros_path=self.py_macros_path )

    - Usable ONLY for links internal to PMT docs.
    -
    """

    schema_md_link: str = None
    """
    If given replace the one automatically built from site_url and self.docs_page_url.
    """

    mkdocstrings_id: str=None
    """ String to build anchor_redirect for old mkdocstrings like links... """


    DEFAULT_DOCS_URL_TEMPLATE: ClassVar[Path] = None
    """
    Used as default when the docs_page_url argument isn't provided.
    May be replaced on the fly from outside at declaration time, to ease definitions.
    """



    @classmethod
    def with_default_docs(cls, url:Path):
        """
        Method used at instances declaration time, to update more easily the value of the
        DEFAULT_DOCS_URL_TEMPLATE class level property.
        """
        CommonTreeSrcWithDocsOrYaml.DEFAULT_DOCS_URL_TEMPLATE = url
        return cls


    #------------------------------------------------------------------------------------


    def __post_init__(self):
        """
        Reformat and assign the docs and yaml_desc properties.
        """
        super().__post_init__()

        self.docs      = inline_md(self.docs)
        self.yaml_desc = inline_md(self.yaml_desc) if self.yaml_desc else self.docs

        # Things that are not in the config or are deprecated should never be in the docs/yaml
        self.in_yaml_docs *= self.in_config and not self.is_deprecated


        if self.in_yaml_docs and '{{' in self.yaml_desc and self.name!='j2_variable_start_string':
            raise ConfigurationError(
                "`yaml_desc` shouldn't contain macros call:\n"
               f"    { self } -> yaml_desc:\n        {self.yaml_desc!r}"
            )
        if self.in_yaml_docs and '`"!py' in self.yaml_desc:
            raise ConfigurationError(
                "`yaml_desc` shouldn't contain mkdocs python inline linting syntax: `#!py ...`"
            )

        if self.docs_page_url is None:
            self.docs_page_url = self.DEFAULT_DOCS_URL_TEMPLATE



    def build_accessor(self, path: List[str]):

        super().build_accessor(path)

        # Prepare anchor_redirect for old mkdocstrings ids... x/
        #  pyodide_mkdocs_theme.pyodide_macros.plugin.config.IdesConfig.XXX
        re_path = [ 'pyodide_mkdocs_theme.pyodide_macros.plugin', *path ]

        is_pyodide_macro        = self.name == 'config'
        is_original_macros_prop = len(re_path)==3 and not self.is_config

        if not is_pyodide_macro and not is_original_macros_prop:
            re_path[2] = re_path[2].title() + 'Config'      # args -> ArgsConfig

        self.mkdocstrings_id = '.'.join(re_path)



    #----------------------------------------------------------------------------------------



    def to_docs_page_header(self):
        """
        Create the code representation of the current element (used in the header).
        Note: the header level (hashtags) isn't part of the output (handled in the caller).
        """
        raise NotImplementedError()


    def to_docs_page_content(self):
        """ Generate the markdown body of the element. """
        raise NotImplementedError()


    def header_attr_md_id(self):
        return f'#{ self.py_macros_path }'


    def to_docs_page(self, header_lvl:int):
        """
        Convert the current element (not recursively) to mkdocs documentation (mkdocstrings-like).
        """
        header   = self.to_docs_page_header()
        attrs    = f'{ self.header_attr_md_id() } .doc .doc-heading ' + '.fake-h4' * (header_lvl==4)
        markdown = f"""
{ '#' * header_lvl } { header } {'{'} { attrs } {'}'}

{ self.to_docs_page_content() }
"""
        return markdown




    #----------------------------------------------------------------------------------------




    def get_yaml_schema_md_infos(self, site_url:Path) -> str:
        """ Build link toward the related documentation. """

        if self.schema_md_link:
            address = self.schema_md_link
        else:
            address = str( site_url / self.docs_page_url ).format(
                name = self.name,
                py_macros_path = self.py_macros_path,
            )
            # Restore double slash in  "http(s)://" (disappeared because of Path)
            address = re.sub(r'^(https?:/)', r'\1/', address)

        return f"{ self.yaml_desc }\n\n[{ address }]({ address })"


    def as_mkdocs_yml_line(self):
        """
        Render the current object as the equivalent line in the mkdocs.yml file
        (generating the config tree).
        """
        raise NotImplementedError()


    def build_yaml_schema(self, site_url:Path) -> YamlSchema:
        """ Build the yaml schema for the current element. """
        raise NotImplementedError()










@dataclass
class CommonTreeSrc(
    CommonTreeSrcWithDocsOrYaml,
    CommonTreeSrcDeprecated,
    metaclass=ABCMeta
):
    """ Overall interface/class with common logic elements """
