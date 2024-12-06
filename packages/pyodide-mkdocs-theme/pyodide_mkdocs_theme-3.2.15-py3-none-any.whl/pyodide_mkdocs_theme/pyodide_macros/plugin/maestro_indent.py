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


import re
from typing import Callable, ClassVar, Dict, List, Optional, Tuple


from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.exceptions import BuildError

from pyodide_mkdocs_theme.pyodide_macros.parsing import add_indent


from ..exceptions import (
    PyodideConfigurationError,
    PyodideMacrosParsingError,
    PyodideMacrosTabulationError,
    PyodideMacrosIndentError,
)
from ..tools_and_constants import MACROS_WITH_INDENTS
from ..pyodide_logger import logger
from .maestro_base import BaseMaestro
from .config import PLUGIN_CONFIG_SRC



# pylint: disable-next=pointless-string-statement, line-too-long
'''
- Macros are run in "reading order" of the original document, included content also being used
  this way => fully predictable
- WARNING with md_include, which interleaves other calls in the "current context"... => needs
  an external md page parser
- Process:
    1. remove raw markers. NOTE: nested raw markups aren't allowed => easy
    2. tokenize (longest tokens first)
    3. _carefully parse the thing_, keeping in mind that the input is md text, not actual python...
       and store the indents of the calls to multiline macros in a reversed stack (store a pair
       indent/macro name, to enforce validity of executions on usage).
    4. Each time a macro starts running (spotted through the custom macro decorator), pop the
       current indent to use, AND STACK IT, because of potential nested macro calls: A(BCD)
       => when going back to A, there is no way to know if the macro will reach for the
       indentation value of A, for example, so the value must be accessible.
       Each time the macro returns, pop the current indent from the current stack.
    5. For nested macros, add the included indentation data on top of the current reversed stack.
'''







class MaestroIndent(BaseMaestro):
    """ Manage Indentation logistic """


    _parser: 'IndentParser'

    _indents_store: List[Tuple[str,int]]
    """
    List of all indentations for the "macro with indents" calls throughout the page, in
    reading order (=dfs).
    Data are stored in reversed fashion, because consumed using `list.pop()`.
    """

    _indents_stack: ClassVar[List[str]] = []
    """
    Stack the current indentation level to use, the last element being the current one.
    This allows the use of macros through multi layered inclusions (see `md_include`),
    getting back the correct indentations when "stepping out" of the included content.
    """

    _macros_calls_stack: ClassVar[List[str]] = []
    """ Same as before, but for the macro currently applied... """

    @property
    def _running_macro(self) -> Optional[str]:
        """
        Name of the macro currently running. None if no macro running.
        """
        return self._macros_calls_stack[-1] if self._macros_calls_stack else None



    def on_config(self, config:MkDocsConfig):
        logger.info("Configure the IndentParser for multiline macros with the user settings.")

        nope = [ w for w in self.macros_with_indents if not w.isidentifier() ]
        if nope:
            raise PyodideConfigurationError(
                "Invalid macros_with_indents option: should be a list of identifiers, but found: "
                f"{ ', '.join(map(repr,nope)) }"
            )

        self._parser = IndentParser(
            self.j2_block_start_string    or '{%',
            self.j2_block_end_string      or '%}',
            self.j2_variable_start_string or '{{',
            self.j2_variable_end_string   or '}}',
            self.j2_comment_start_string  or '{#',
            self.j2_comment_end_string    or '#}',
            self.is_macro_with_indent,
        )

        super().on_config(config)   # MacrosPlugin is actually "next in line" and has this method

        # After the super call, all macros have been registered, so MACROS_WITH_INDENTS isn't
        # empty anymore:
        macros = [*MACROS_WITH_INDENTS] + self.macros_with_indents
        self._macro_with_indent_pattern = re.compile('|'.join(macros))



    def on_page_markdown(
        self,
        markdown:str,
        page:Page,
        config:MkDocsConfig,
        site_navigation=None,
        **kwargs
    ):

        file_loc     = self.file_location(page)
        indentations = self._parser.parse(markdown, file_loc, tab_to_spaces=self.tab_to_spaces)

        self._indents_store = [*reversed(indentations)]
        self._indents_stack.clear()
        self._macros_calls_stack.clear()

        out = super().on_page_markdown(
            markdown, page, config, site_navigation=site_navigation, **kwargs
        )
        self._ensure_clean_outcome(file_loc)
        return out



    def _ensure_clean_outcome(self, file_loc):
        """
        Make sure all indentation data have been properly consumed.
        """

        if self._indents_store:
            content = ''.join( f"\n    {name}: {n}" for name,n in reversed(self._indents_store) )
            raise PyodideMacrosIndentError(
                "Registered macros calls with indents have not been entirely consumed for "
                f"{ file_loc }. The remaining store content is:{ content }"
            )

        if self._indents_stack:
            raise PyodideMacrosIndentError(
                "Indentations stack inconsistency when rendering the markdown page for "
                f"{ file_loc }. The remaining stack content is:\n    {self._indents_stack!r}"
            )

        if self._macros_calls_stack:
            raise PyodideMacrosIndentError(
                "Macros calls stack inconsistency when rendering the markdown page for "
                f"{ file_loc }. The remaining stack content is:\n    {self._macros_calls_stack!r}"
            )



    #----------------------------------------------------------------------------



    def apply_macro(self, name, func, *a, **kw):
        """
        Gathers automatically the name of the macro currently running (for better error
        messages). Also validate the call config for macros with indents
        """
        need_indent = self.is_macro_with_indent(name)

        self._macros_calls_stack.append(name)
        if need_indent:
            call,indent = self._indents_store.pop()
            if call != name:
                raise BuildError(
                    f"Invalid indentation data: expected a call to `{call}`, but was `{name}`"
                )
            self._indents_stack.append(indent * ' ')

        out = super().apply_macro(name, func, *a, **kw)

        if need_indent:
            self._indents_stack.pop()
        self._macros_calls_stack.pop()
        return out



    def file_location(self, page:Optional[Page]=None):
        """
        Path to the current file, relative to the cwd, including the current running macro if any.
        """
        out = super().file_location(page)
        if self._running_macro:
            out += f" (in macro: { self._running_macro })"
        return out



    def is_macro_with_indent(self, macro_call:str=None) -> bool:
        """
        Return True if the given macro call requires to register indentation data.
        This is using a white list, so that user defined macro cannot cause troubles.

        If no argument, check against the currently running macro
        """
        return bool(self._macro_with_indent_pattern.fullmatch(
            macro_call or self._running_macro
        ))


    def get_macro_indent(self):
        """
        Extract the indentation level for the current macro call.
        """
        if not self._indents_stack:
            macros_with_indents = PLUGIN_CONFIG_SRC.build.macros_with_indents.py_macros_path
            raise BuildError(
                f"No indentation data available while building the page {self.file_location()}.\n"
                "This means a macro calling `env.indent_macro(text)` or `env.get_macro_indent()`"
                f" has not been registered in:\n    `mkdocs.yml:plugins.{ macros_with_indents }`."
            )
        return self._indents_stack[-1]


    def indent_macro(self, code:str):
        """
        Automatically indent appropriately the given macro output markdown, leaving empty
        lines untouched.
        """
        indent   = self.get_macro_indent()
        out_code = add_indent(code, indent)
        return out_code










class IndentParser:
    """
    Build a markdown parser class, extracting the indentations of macros calls requiring
    indentation, and taking in consideration jinja markups (skip {% raw %}...{% endraw %},
    properly parse complex macro calls, ignore macro variables).

    The result of the method `IndentParser(content).parse()` is a list of `Tuple[str,int]`:
    `(macro_name, indent)`, in the order they showed up in the content.
    """

    STR_DECLARATIONS: ClassVar[Tuple[str]] = '"""', "'''", '"', "'"

    __CACHE: ClassVar[Dict[str,List]] = {}

    def __init__(self,
        open_block:str,
        close_block:str,
        open_var:str,
        close_var:str,
        open_comment:str,
        close_comment:str,
        is_macro_with_indent:Callable[[str],bool],
    ):
        self.is_macro_with_indent = is_macro_with_indent

        # Build the delimiters according to the user config of the MacrosPlugin:
        self.open_block    = open_block
        self.close_block   = close_block
        self.open_var      = open_var
        self.close_var     = close_var
        self.open_comment  = open_comment
        self.close_comment = close_comment
        self.open_raw      = f'{open_block} raw {close_block}'
        self.close_raw     = f'{open_block} endraw {close_block}'
        self.pairs         = {}

        raw_open_close = [
            [self.open_raw,      self.close_raw],
            [self.open_block,    self.close_block],
            [self.open_var,      self.close_var],
            [self.open_comment,  self.close_comment],
            *( [s,s] for s in self.STR_DECLARATIONS),
            ['(', ')'],
            ['[', ']'],
            ['{', '}'],
        ]
        tokens = []
        for o,c in raw_open_close:
            self.pairs[o] = c
            tokens += [o,c]

        tokens.sort(key=len, reverse=True)

        self.pattern = re.compile(
            '|'.join(
                [re.escape(s).replace('\\ ',r'\s*') for s in tokens]
                +[ r'\w+', r'\n', r'[\t ]+', r'\\', '.' ]
            ), flags=re.DOTALL
        )

        self.gatherers = {
            self.open_var:     self._gather_jinja_var,
            self.open_raw:     lambda: self._eat_until(self.close_raw),
            self.open_block:   lambda: self._eat_until(self.close_block),
            self.open_comment: lambda: self._eat_until(self.close_comment),
        }

        # Defined later in self.parse(...):
        self.tab_to_spaces = -1
        self.src_file = None
        self.i        = 0
        self.tokens   = []
        self.indents  = []
        self.current  = None        # current macro call




    def parse(self, content:str, src_file=None, *, tab_to_spaces=-1):
        """
        Parse the given content and extract all the indentation levels for each macro call
        identified as being a "macro_with_indent".

        - Returns a copy of the result.
        - Results are cached in between builds.
        """
        # pylint: disable=attribute-defined-outside-init, multiple-statements

        self.src_file = src_file
        self.tab_to_spaces = tab_to_spaces

        if content not in self.__CACHE:
            self.i = 0
            self.tokens = self.pattern.findall(content)
            self.indents = []

            while self.i < len(self.tokens):
                tok = self._eat()
                if tok in self.gatherers:
                    self.gatherers[tok]()

            self.__CACHE[content] = self.indents

        return self.__CACHE[content][:]


    #-------------------------------------------------------------
    #                       Error feedback
    #-------------------------------------------------------------


    def _error_info(self, info:str, tok:str):
        macro = ''
        indents = "No indents found so far."

        if self.current:
            i,msg = self.current
            macro = (
                f"\nMacro being parsed during the error (index : { i }/{ len(self.tokens) }):\n"
                f"    { msg }\n"
            )
        if self.indents:
            indents = "\nKnown indents so far: " + ''.join(
                f"\n\t{name}: {n}" for name,n in self.indents
            )

        return (
            "Parsing error while looking for macro calls indentation data.\n"
            "The parser might EOF when strings in a macro call are improperly written, so double "
            "check there are no unescaped delimiters inside strings used in the macro call.\n"
            f"With \033[31m>>tok<<\033[0m denoting the tokens of interest:\n\n"
            f"\033[34m{ info }, in { self.src_file }\033[0m\n{ macro }\n"
            f"Tokens around the error location (index: { self.i }/{ len(self.tokens) }):\n"
            f"    { self.__location_info(tok) }\n"
            f"\n{ indents }"
        )


    def __location_info(self, tok, i:Optional[int]=None):
        i = self.i if i is None else i
        return f"{ self.__extract(i,-10) }\033[31m>>{tok}<<\033[0m{ self.__extract(i,10) }"


    def __extract(self, i_src, di):
        i,j = (i_src+di, i_src) if di<0 else  (i_src+1, i_src+1+di)

        # Enforce " is always used (otherwise, might end up with ' on one side and " on the other)
        a,b = ('"', '') if di<0 else ('', '"')
        rpr = repr(''.join(self.tokens[i:j]))[1:-1].replace('"','\\"')
        out = a + rpr + b

        return out


    #-------------------------------------------------------------
    #                     Parsing machinery
    #-------------------------------------------------------------


    def _taste(self) -> Optional[str] :
        return self.tokens[self.i] if self.i<len(self.tokens) else None

    def _eat(self,reg:str=None, msg:str=None):
        tok = self._taste()
        if tok is None or reg is not None and not re.fullmatch(reg, tok):
            tok = 'EOF' if tok is None else repr(tok)
            reg = reg or msg
            msg = 'Reached EOF' if not reg else f'Expected pattern was: {reg!r}, but found: {tok}'
            raise PyodideMacrosParsingError( self._error_info(msg, tok) )
        self.i+=1
        return tok

    def _walk(self):
        while (tok := self._taste()) and tok.isspace():
            self.i += 1

    def _eat_until(self, target, apply_backslash=False):
        while True:
            tok = self._eat(msg=target)
            if tok==target:
                return
            elif tok=='\\' and apply_backslash:
                self._eat()



    def _consume_code_until(self, target:str):
        """
        Recursively consumed code in jinja context, reasoning on matched tokens:
                ( -> )
                [ -> ]
                " -> "
                ''' -> '''
                ...

        String content is properly ignored/correctly identified, to ensure the whole code will
        be consumed even if a string contains ')' or '}}'. Same applies for arrays, dicts, ...

        The different kinds of strings and their possible nesting is also properly handled.

        Syntax errors will be spotted at some point, giving feedback on the macro that triggered
        the error in the error message.
        """
        while True:
            tok = self._eat(msg=target)
            if tok==target:
                break
            elif tok in self.pairs:
                is_str_declaration = tok in self.STR_DECLARATIONS
                closing = self.pairs[tok]
                if is_str_declaration:
                    self._eat_until(closing, True)
                else:
                    self._consume_code_until(closing)


    def _gather_jinja_var(self):
        start = self.i-1        # index of the '{{' token, to compute indentation later
        self._walk()

        tok = self._taste()
        if tok and tok.isidentifier():

            i_name   = self.i
            name     = self._eat()
            self._walk()
            tok      = self._taste()
            is_macro = tok=='('

            # Store "debugging purpose" data:
            self.current = i_name, self.__location_info(name, i_name)

            if is_macro and self.is_macro_with_indent(name):
                self._store_macro_with_indent(start, name)
                self._eat()     # consume the current '(' (would cause an error in _consume_code)
                self._consume_code_until(')')

        self._consume_code_until(self.close_var)


    def _store_macro_with_indent(self, start:int, name:str):
        i = max(0, start-1)
        while i>0 and self.tokens[i].isspace() and self.tokens[i] != '\n':
            i -= 1

        tok = self.tokens[i]
        if i and tok not in ('\n',self.open_var):
            raise PyodideMacrosParsingError( self._error_info(
               f"Invalid macro call:\nThe {name!r} macro is a `macros_with_indents` but a "
                "call to it has been found with characters on its left. This is not possible.\n"
                "This happened",
                tok
            ))

        i += tok=='\n'
        indent = ''.join(self.tokens[i:start])
        if '\t' in indent:
            if self.tab_to_spaces<0:
                raise PyodideMacrosTabulationError(
                   f"In { self.src_file }:\n"
                    "A tabulation character has been found on the left of a multiline macro call."
                    "\nThis is considered invalid. Solutions:\n"
                    "    - Configure your IDE to automatically convert tabulations into spaces.\n"
                    "    - Replace them with spaces characters manually.\n"
                    "    - Or set the `build.tab_to_spaces: integer` option of the plugin (NOTE:"
                    " depending on how the macros calls have been written, this might not always"
                    " work).\n"
                    "      If done so, warnings will be shown in the console with the locations of"
                    " each of these updates, so that they can be checked and fixed."
                )
            else:
                indent = indent.replace('\t', ' '*self.tab_to_spaces)
                logger.warning(
                    f"Automatic conversion of tabs to spaces in { self.src_file }, for the macro "
                    f"call: { self.current[1] }"
                )
        n_indent = len(indent)
        self.indents.append( (name, n_indent) )
