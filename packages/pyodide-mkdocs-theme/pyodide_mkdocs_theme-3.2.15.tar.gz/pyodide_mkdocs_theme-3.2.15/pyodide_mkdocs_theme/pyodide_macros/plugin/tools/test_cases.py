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
# pylint: disable=multiple-statements, no-member



from typing import ClassVar, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field, fields

from pyodide_mkdocs_theme.pyodide_macros.messages.fr_lang import Lang





@dataclass
class Case:
    """
    Represent a test case for an IDE TEST argument (or profile).
    """

    KEEP_FALSY_EXPORTS: ClassVar[Tuple[str]] = (
        'reveal_corr_rems', 'set_max_and_hide', 'no_clear', 'delta_attempts',
    )

    DESC_SKIPPED: ClassVar[Tuple[str]] = (
        'subcases', 'skip', 'title', 'std_capture_regex', 'not_std_capture_regex',
    )
    """ Not shown in the automatic descriptions. """


    SHORTEN: ClassVar[Dict[str,str]] = {
        'decrease_attempts_on_user_code_failure': 'decrease_condition',
        'deactivate_stdout_for_secrets':          'secrets_std_out',
        'show_only_assertion_errors_for_secrets': 'secrets_only_assert',
    }
    """ Automatic descriptions formatting. """


    # Globals for string definitions (public interface)
    DEFAULT: ClassVar['Case'] = None     # Defined after class declaration
    SKIP:    ClassVar['Case'] = None     # Defined after class declaration
    HUMAN:   ClassVar['Case'] = None     # Defined after class declaration
    FAIL:    ClassVar['Case'] = None     # Defined after class declaration
    NO_CLEAR:ClassVar['Case'] = None     # Defined after class declaration
    CODE:    ClassVar['Case'] = None     # Defined after class declaration

    # Private interface
    REVEAL_SUCCESS:             ClassVar['Case'] = None
    REVEAL_FAIL:                ClassVar['Case'] = None
    ERROR_IN_POST_REVEAL:       ClassVar['Case'] = None
    ERROR_NO_REVEAL:            ClassVar['Case'] = None
    SUCCESS_AFTER_REVEAL:       ClassVar['Case'] = None
    DELAYED_NO_REVEAL:          ClassVar['Case'] = None
    SUCCESS_NOTHING_TO_REVEAL:  ClassVar['Case'] = None


    #--------------------------------------------------------------------------


    human: Optional[bool] = None
    """ Don't test this IDE by default, but it can be selected with the human button
        (to use for tests that require human actions, like up-/downloads).
    """

    skip: Optional[bool] = None
    """ Don't test this IDE """

    fail: Optional[bool] = None
    """ This IDE has to fail the test """

    no_clear: Optional[bool] = None
    """ Don't clear the scope for this test
        NOTE: this is useless unless all the tests are run in order...
    """

    code: Optional[bool] = None
    """ Run the `code` section instead of the `corr` one. """

    description: Optional[str] = None
    """ Quick description of the test (optional). """

    term_cmd: Optional[str] = None
    """
    One command to execute through the terminal. If given, corr/code sections to test are ignored.
    """



    #-------------------------------------------------------------------------
    # Private interface:

    title: Optional[str] = None
    """ Prefix added to the automatic description when no description value given """

    run_play: Optional[bool] = None
    """
    Runs the public tests only. Here, it's still possible to run either the code or the
    corr section, along with the tests section.
    """

    reveal_corr_rems: Optional[bool] = None

    set_max_and_hide: Optional[int] = None
    """ (Use 1000 to get infinite number of attempts) """

    keep_profile: Optional[bool] = None
    """ If True, the "mode" of the IDE is kept during the tests. """

    delta_attempts: Optional[int] = None
    """ Variation of number of attempts (negative or 0, if used). """

    in_error_msg: Optional[str] = None
    """ String that should be found in the error message (test failed if no error message). """

    not_in_error_msg: Optional[str] = None
    """ String that should NOT be found in the error message (success if no error message). """

    all_in_std: Optional[List[str]] = None
    """
    If given, automatically build a regex with all the element for `std_capture_regex`.
    WARNING: this will work on content already formatted by jQuery.terminal output.
    """

    none_in_std: Optional[List[str]] = None
    """
    If given, automatically build a regex with all the element for `not_std_capture_regex`.
    WARNING: this will work on content already formatted by jQuery.terminal output.
    """

    assertions: Optional[str] = None
    """ space separated strings of "boolsy" properties to check. Prefix with '!' to revert. """

    decrease_attempts_on_user_code_failure: Optional[str]  = None
    deactivate_stdout_for_secrets:          Optional[bool] = None
    show_only_assertion_errors_for_secrets: Optional[bool] = None

    clear_libs: List[str] = field(default_factory=list)
    """
    List of names of libs to remove before a test:
        - Remove any matching local files in the FS
        - remove the name from `sys.modules`
    """

    subcases: List['Case'] = field(default_factory=list)

    std_capture_regex: Optional[str] = None
    """ INTERNAL ONLY: DON'T USE THAT AS ARGUMENT """

    not_std_capture_regex: Optional[str] = None
    """ INTERNAL ONLY: DON'T USE THAT AS ARGUMENT """

    #---------------------------------------------------------------------


    def __post_init__(self):
        if self.std_capture_regex or self.not_std_capture_regex:
            raise ValueError(
                "std_capture_regex and not_std_capture_regex properties are internals only "
                "=> don't use them as arguments, use all_in_std or none_in_std instead."
            )

        if self.subcases:
            self.subcases = [*map(self.auto_convert_str_to_case, self.subcases)]


    def times(self, n:int, with_:Dict[int,str]=None):
        if self.subcases:
            raise ValueError(
                "Cannot use `Case.times(n)` method if the instance already has a `subcases` array."
            )
        self.subcases = [ Case(description=f"Run {i+1}") for i in range(n) ]
        if with_:
            for ns,case in with_.items():
                if isinstance(ns,int):
                    ns = (ns,)
                for n in ns:
                    self.subcases[n-1] = case
        return self


    def with_(self, **kwargs):
        """
        Build a new Case instance based on the current one, updating all te values with the
        one of the argument.
        """
        kw = {**self._to_dict(), **kwargs}
        if self.description and kwargs and 'description' not in kwargs:
            kw['description'] += ' | '+', '.join( self.format_item(k,v) for k,v in kwargs.items() )
        return Case(**kw)



    @classmethod
    def auto_convert_str_to_case(cls, case: Union[str,'Case']) -> 'Case':
        """ Convert a string to the related Case instance, or just return the instance. """
        if isinstance(case, Case):
            return case
        if not case:
            return cls.DEFAULT
        return getattr(cls, case.upper())



    @classmethod
    def format_item(cls, k, v):
        """ Used to make some automatic descriptions shorter... """
        return f"{ cls.SHORTEN.get(k,k) }={ repr(v) }"



    def _to_dict(self):
        """ Convert to a dict, without the properties whose the value is None. """
        return { f.name: v for f in fields(self)
                           if (v:=getattr(self, f.name)) is not None
               }


    def as_dict(self, merge_with:dict=None):
        """
        Convert recursively to a dict, removing falsy values.
        """
        is_not_top_level = merge_with is not None

        dct = self._to_dict()
        if merge_with:
            dct = {**merge_with, **dct}
            for p in ('subcases', 'std_capture_regex', 'not_std_capture_regex'):
                dct.pop(p, None)

        if self.all_in_std:
            dct['std_capture_regex']     = r'.*?'.join(self.all_in_std)
        if self.none_in_std:
            dct['not_std_capture_regex'] = r'|'.join(self.none_in_std)


        # Filter falsy values AFTER merging (or lose overrides...):
        dct = {k:v for k,v in dct.items()
                    if v or v is not None and k in self.KEEP_FALSY_EXPORTS
        }

        if self.subcases:
            dct['subcases'] = [ case.as_dict(merge_with=dct) for case in self.subcases ]

        if not self.description:
            dct['description'] = ', '.join(
                self.format_item(k,v)
                    for k,v in dct.items()
                    if k not in self.DESC_SKIPPED           # Don't show irrelevant info
                        and (k!='code' or is_not_top_level) # Useless at top level: already known
                        and k!='description'                # Don't reuse upper level description
            )
            if self.title:
                dct['description'] = f"{ self.title }: { dct['description'] }"

        return dct






CASES_OPTIONS = '', 'skip', 'fail', 'code', 'human', 'no_clear'

Case.DEFAULT  = Case()
Case.SKIP     = Case(skip=True)
Case.FAIL     = Case(fail=True)
Case.CODE     = Case(code=True)
Case.HUMAN    = Case(human=True)
Case.NO_CLEAR = Case(no_clear=True)


LANG = Lang.get_langs_dct()['fr']

Case.REVEAL_SUCCESS = Case(
    description = "Success reveal with: bravo, passé tous les tests, pensez à lire",
    no_clear = True,
    fail = False,
    run_play = False,
    delta_attempts = 0,
    reveal_corr_rems = True,
    assertions = "corrRemsMask hasCheckBtn",
    all_in_std = [LANG.success_head.msg, LANG.success_head_extra.msg, LANG.success_tail.msg],
    none_in_std = [LANG.fail_head.msg],
)

Case.REVEAL_FAIL = Case(
    description = "Fail reveal with: Dommage! and none of the success messages",
    fail = True,
    no_clear = True,
    run_play = False,
    delta_attempts = -1,
    reveal_corr_rems = True,
    assertions = "corrRemsMask hasCheckBtn",
    none_in_std = [LANG.success_head.msg, LANG.success_head_extra.msg, LANG.success_tail.msg],
    all_in_std = [LANG.fail_head.msg],
)

Case.ERROR_IN_POST_REVEAL = Case(
    description = "Assertion in post is a success",
    fail = True,
    no_clear = True,
    run_play = False,
    delta_attempts = 0,
    reveal_corr_rems = True,
    assertions = "corrRemsMask hasCheckBtn",
    none_in_std = [],
    all_in_std = [
        LANG.success_head.msg, LANG.success_head_extra.msg,
        LANG.success_tail.msg,
        'Error:'
    ],
)

Case.ERROR_NO_REVEAL = Case(
    description = "Error without revelation",
    fail = True,
    no_clear = True,
    run_play = False,
    delta_attempts = -1,
    reveal_corr_rems = False,
    assertions = "corrRemsMask hasCheckBtn",
    all_in_std = ['Error:'],
    none_in_std = [ LANG.fail_head.msg,
                    LANG.success_head.msg, LANG.success_head_extra.msg, LANG.success_tail.msg],
)

Case.SUCCESS_AFTER_REVEAL = Case(
    description = "SUCCESS_AFTER_REVEAL",
    no_clear = True,
    fail = False,
    run_play = False,
    delta_attempts = 0,
    reveal_corr_rems = False,
    assertions = "hasCheckBtn",
    none_in_std = [LANG.success_head.msg, LANG.success_head_extra.msg, LANG.fail_head.msg, LANG.success_tail.msg],
)

Case.SUCCESS_NOTHING_TO_REVEAL = Case.SUCCESS_AFTER_REVEAL.with_(
    none_in_std = [LANG.fail_head.msg, LANG.success_tail.msg],
    all_in_std  = [LANG.success_head.msg, LANG.success_head_extra.msg],
)

Case.DELAYED_NO_REVEAL = Case(
    description = "DELAYED_NO_REVEAL",
    no_clear = False,
    fail = False,
    run_play = False,
    keep_profile = True,
    delta_attempts = -1,
    reveal_corr_rems = False,
    assertions = "hasCheckBtn",
    none_in_std = [LANG.success_head.msg, LANG.success_head_extra.msg, LANG.fail_head.msg, LANG.success_tail.msg],
)
