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

from mkdocs.exceptions import ConfigurationError, BuildError, PluginError



class PyodideConfigurationError(ConfigurationError):
    """ Something went wrong in the Pyodide theme itself """



class PyodideMacrosError(PluginError):
    """
    Some top level mkdocs pages related hooks are not decorated with the
    MaestroMeta.meta_config_swap decorator.
    """

class PyodideMacrosPyLibsError(PyodideMacrosError):
    """
    Problem related to handling the python custom libraries.
    """

class PyodideMacrosDeprecationError(PyodideMacrosError):
    """
    Stuff that shouldn't be used anymore...
    """




class PyodideMacrosParsingError(BuildError):
    """
    Invalid syntax found while parsing a markdown file, when gathering
    information about macros calls indentations in the page.
    """

class PyodideMacrosIndentError(PyodideMacrosParsingError):
    """
    PThe stack of indentations has not been consumed entirely once the page markdown
    has been created.
    """

class PyodideMacrosTabulationError(PyodideMacrosParsingError):
    """
    A tab character has been found in the indentation before a multiline macro call.
    """


class PyodideMacrosMetaError(BuildError):
    """
    Some top level mkdocs pages related hooks are not decorated with the
    MaestroMeta.meta_config_swap decorator.
    """


class PyodideMacrosNonUniqueIdError(BuildError):
    """
    A non unique id has been generated (for an IDE, terminal, ...)
    """
