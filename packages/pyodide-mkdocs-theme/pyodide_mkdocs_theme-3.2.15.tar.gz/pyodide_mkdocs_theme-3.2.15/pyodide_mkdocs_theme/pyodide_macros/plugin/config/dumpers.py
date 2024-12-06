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

# pylint: disable=multiple-statements


from abc import ABCMeta
from typing import Any, Dict, List, TYPE_CHECKING, Optional, Union
from dataclasses import dataclass, field
from functools import wraps


if TYPE_CHECKING:
    from .sub_config_src import ConfOrOptSrc

# pylint: disable=signature-differs









@dataclass
class Dumper(metaclass=ABCMeta):
    """
    Generic interface to transform a SubConfigSrc tree into... something else.
    Generally, something like a linearized version of the tree content.
    """

    was_option: bool
    """ The last exited element was... """


    @classmethod
    def apply(cls, start:'ConfOrOptSrc', *extra_init:Any, **kw_init):
        """
        Entry point, to apply the given logic to the source config hierarchy tree.
        """
        dumper = cls(False, *extra_init, **kw_init)

        travel_out = dumper.travel_with_dumper(start)
        return dumper.finalize(travel_out)




    def travel_with_dumper(self, obj:'ConfOrOptSrc') -> Union[None, Any] :
        """
        Generic routine to transform a config tree into something else.
        Useful to convert the tree to something that is essentially "linear" 'code, text, ...)

        If it returns something, the output of the top level call will be passed to the finalize
        method, but it's generally not necessary (useful only for recursive outputs).
        """
        raise NotImplementedError()

    def finalize(self, travel_out: Any=None):
        """ Return the actual output at the end of executions """
        raise NotImplementedError()


    #---------------------------------------------------------------------------------------
    # Generic iteration ordering methods:


    def _ordered_iter(self, obj: 'ConfOrOptSrc', sort_all=False):
        """ Generic ordering tool. """

        is_in_args = obj.name=='args' or 'args' in obj.config_setter_path
        children   = obj.elements
        if children and not is_in_args or sort_all:
            children = sorted(children, key=self.ordering)

        return children


    @staticmethod
    def ordering(obj:'ConfOrOptSrc'):
        """ Sub config first, deprecated last, then lexicographic. """
        return not obj.is_config, obj.is_deprecated, obj.name


    #---------------------------------------------------------------------------------------
    # Generic observers/mutators to know when the recursion exits a leaf SubConfigSrc:
    # (Interesting to build flatten content from the tree)


    @staticmethod
    def spot_exiting_leaf_config(method:callable):
        """
        Decorator taking in charge the evolution of `self.was_option`.
        Use it to decorate the `travel_with_dumper(obj) -> None` method of the child class where
        you need to use `is_closing_leaf_config(obj)`.
        """
        @wraps(method)
        def wrapper(self:Dumper, obj:'ConfOrOptSrc') -> None:
            method(self, obj)
            self.was_option = not obj.is_config
        return wrapper


    def is_closing_leaf_config(self, obj:'ConfOrOptSrc'):
        """
        Return True if, when exiting the current object, it is a "leaf SubConfigSrc", meaning
        the previously exited element was a ConfigOptionSrc.

        WARNING: relies on the SubConfigSrc being first in the iteration process.
        """
        return obj.is_config and self.was_option











@dataclass
class AccessorsDumper(Dumper):
    """
    Mutate the tree to build all the accessors:
        - config_setter_path
        - depth
        - maestro_extractor_getter_name
    """

    options: List['ConfOrOptSrc']
    macros:  Dict[str,'ConfOrOptSrc']

    path: List[str] = field(default_factory=list)


    def finalize(self, _):  pass

    def travel_with_dumper(self, obj:'ConfOrOptSrc'):

        # Enter:
        self.path.append(obj.name)

        obj.build_accessor(self.path)
        if not obj.is_config:  self.options.append(obj)
        if obj.is_macro:       self.macros[ obj.name ] = obj

        # Recurse:
        for child in obj.elements:
            self.travel_with_dumper(child)

        # Exit:
        self.path.pop()











@dataclass
class BaseMaestroGettersDumper(Dumper):
    """
    Generate the code of all the ConfigExtractor getters for BaseMaestro.
    """

    code:  List[str] = field(default_factory=list)
    """ Global lines of code for all getters (formatted and ordered) """

    stack: List[List[str]] = field(default_factory=list)
    """ Groups of ConfigOptionSrc being converted """


    def travel_with_dumper(self, obj:'ConfOrOptSrc'):

        # Enter:
        if obj.is_config:
            self.stack.append([])

        elif obj.in_config:
            getter = obj.to_base_maestro_getter_code()
            self.stack[-1].append(getter)

        # Recurse:
        for child in self._ordered_iter(obj, sort_all=True):
            if child.in_config:
                self.travel_with_dumper(child)

        # Exit:
        if obj.is_config:
            group = self.stack.pop()
            if group:
                aligned = self._align_group(group)
                self.code.extend(aligned)
                self.code.append('\n')


    def finalize(self, _):
        self.code.pop()             # Suppress trailing empty line
        return ''.join(self.code)


    @staticmethod
    def _chr_indices(getter:str):
        """ Finds the indices of `:` (+1) and `=` in the code of the getter """
        i = 1 + getter.find(':')
        j = getter.find('=', i)
        return i, j


    def _align_group(self, lst:List[str]):
        ij_s = [*map(self._chr_indices, lst)]
        right_most = max(j for _,j in ij_s)
        aligned = [ f"{ s[:i] }{ ' '*(right_most-j) }{ s[i:] }" for s,(i,j) in zip(lst, ij_s) ]
        return aligned











@dataclass
class ConfigYamlTreeDumper(Dumper):
    """
    Generate the complete tree of the plugin config for the docs (code block).
    """

    code:  List[str] = field(default_factory=list)
    """ Global lines of code for all getters (formatted and ordered) """


    @Dumper.spot_exiting_leaf_config
    def travel_with_dumper(self, obj:'ConfOrOptSrc'):

        # Enter:
        if not obj.in_yaml_docs:
            return

        line = obj.as_mkdocs_yml_line()
        self.code.append(line)

        # Recurse:
        for child in self._ordered_iter(obj):
            self.travel_with_dumper(child)

        # Exit:
        if self.is_closing_leaf_config(obj):
            self.code.append('')


    def finalize(self, _):
        joined    = '\n    '.join(self.code).rstrip()
        yml_block = f'```yaml\nplugins:\n    { joined }\n```\n'
        return yml_block









@dataclass
class ConfigOptionsSummaryDumper(Dumper):
    """
    Generate the complete tree of the plugin config for the docs (code block).
    """

    code: List[str] = field(default_factory=list)
    """ Global lines of code for all getters (formatted and ordered) """


    def travel_with_dumper(self, obj:'ConfOrOptSrc', depth=0):
        if not obj.in_yaml_docs:
            return

        if not depth:
            # Recurse:
            for child in self._ordered_iter(obj):
                self.travel_with_dumper(child, 1)
        else:
            line = f"| [`{ obj.name }`](#{ obj.py_macros_path }) | `#!yaml { obj.to_yml_value() }` |"
            self.code.append(line)


    def finalize(self, _):
        options = '\n    '.join(self.code)
        return f'''
<br><br><br>

| Options disponibles | Valeur par défaut |
|-|:-:|
{ options }

---

<br>

'''











@dataclass
class MkdocstringsPageDocsDumper(Dumper):
    """
    Converts the tree to an equivalent of mkdocstrings markdown content/page.

    @header_lvl: Starting point for the header level. The depth of the current element
                    is ignored and this value is increased by one at each recursive call.
    @recurse:    If False, render only the current element.
    """

    header_lvl: int  = 3
    recurse:    bool = True
    limit_depth: int = -1

    markdown:  List[str] = field(default_factory=list)
    """ Global content of the page (lines or §). """


    def travel_with_dumper(self, obj:'ConfOrOptSrc', header_lvl:Optional[int]=None):
        if not self.limit_depth:
            return
        if not obj.in_yaml_docs:
            raise ValueError("oops... Deprecated!")

        if header_lvl is None:
            header_lvl = self.header_lvl

        # Enter
        md = obj.to_docs_page(header_lvl)
        self.markdown.append(md)

        # Recurse
        if self.recurse:
            for child in self._ordered_iter(obj):
                if child.in_yaml_docs:
                    self.limit_depth -= 1
                    self.travel_with_dumper(child, header_lvl+1)
                    self.limit_depth += 1


    def finalize(self, _):
        return '\n\n'.join(self.markdown)
