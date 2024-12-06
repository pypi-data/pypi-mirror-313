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
# pylint: disable=line-too-long


from typing import Dict, FrozenSet, List, TYPE_CHECKING, Set, Tuple

from ..tools_and_constants import PageUrl
from ..plugin.tools.pages_and_macros_py_configs import PageConfiguration
from .deps_class import Block, Cdn, Css, Dep, DepKind

if TYPE_CHECKING:
    from ..plugin.pyodide_macros_plugin import PyodideMacrosPlugin





Template = MethodExtraFormatArg = str
BlocksTemplatesData = Dict[Block, Tuple[Template, Tuple[MethodExtraFormatArg, ...]]]



class HtmlDependencies:


    __DEPS_IN_ORDER: List[Dep] = Dep.auto_ordering()

    __URL_TO_TEMPLATE_CACHE: Dict[PageUrl, BlocksTemplatesData] = {}


    @classmethod
    def build_templates(cls, env:'PyodideMacrosPlugin', pages_configs:Dict[PageUrl, PageConfiguration]):
        """
        Build all the templates needed for any page of the documentation, caching them
        """
        needs_to_templates: Dict[FrozenSet[DepKind], BlocksTemplatesData] = {}
        base_needs_to_all_needs: Dict[FrozenSet[DepKind], Set[DepKind]] = {}

        # (covers the weird case weired case where page is None... Might also become useful
        # one day, if ever pages_configs do not reference anymore all the possible pages of the
        # documentation. It currently works because of MaestroMacros.on_page_markdown, where the
        # `if self.does_current_page_need(DepKind.mermaid)` actually inserts all pages on the fly
        # when they don't contain macros calls...)
        default = PageConfiguration(env)
        default.needs.add(DepKind.always)
        all_kinds_of_pages = {None: default, **pages_configs}

        for url, page_config in all_kinds_of_pages.items():

            base_needs = frozenset(page_config.needs)
            if base_needs not in needs_to_templates:

                # Build the complete set of dependencies:
                all_needs = set(base_needs)
                all_needs.add(DepKind.always)
                for need in base_needs:
                    DepKind.resolve_deps_needs(need, all_needs)
                base_needs_to_all_needs[base_needs] = all_needs

                # Separate the wheat from the chaff... :p
                blocks_dct: Dict[Block,List[Dep]] = {b:[] for b in Block.get_blocks()}
                for dep in cls.__DEPS_IN_ORDER:
                    if dep.kind in all_needs:
                        blocks_dct[dep.block].append(dep)

                # Mutate the wheat to templates and extra method calls needed:
                for block, lst_deps in blocks_dct.items():
                    extras_dump_calls = []
                    template = '\n'.join( dep.to_template(extras_dump_calls) for dep in lst_deps )
                    blocks_dct[block] = template, tuple(extras_dump_calls)


                # Register templates and cbks
                needs_to_templates[base_needs] = blocks_dct

            cls.__URL_TO_TEMPLATE_CACHE[url] = needs_to_templates[base_needs]

            # Reassign the page needs with the complete set so that the proper info is
            # available "later" if needed.
            page_config.needs = base_needs_to_all_needs[base_needs]




    @classmethod
    def render_tags_for(cls, block:Block, env:'PyodideMacrosPlugin'):
        cache_key = env.page and env.page.url
        template, extras_dump_calls = cls.__URL_TO_TEMPLATE_CACHE[cache_key][block]
        extras = { method: getattr(env, method)() for method in extras_dump_calls}
        html   = template.format(base_url=env.base_url, **extras)
        return html


    #---------------------------------------------------------


    lodash         = Cdn(Block.libs, DepKind.always, "https://cdn.jsdelivr.net/npm/lodash@4.17.20/lodash.min.js")
    jQuery         = Cdn(Block.libs, DepKind.always, "https://cdn.jsdelivr.net/npm/jquery@3.7.1")
    jQterm         = Cdn(Block.libs, DepKind.term,   "https://cdn.jsdelivr.net/npm/jquery.terminal@2.43.1/js/jquery.terminal.min.js")
    ace            = Cdn(Block.libs, DepKind.ide, {
        'src': "https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.7/ace.min.js",
        'integrity': "sha512-GQpIYSKNIPIC763JKTNALj+t18/nfLdzw5gITgFGa31aK/4NmjyPKsfqrjh7CuzpJaG3nqEleeVcWUhHad9Axg==",
    })
    ace_tools      = Cdn(Block.libs, DepKind.ide, {
        'src': "https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.7/ext-language_tools.min.js",
        'integrity': "sha512-iK7yTkCkv7MbFwTqRgHTbmIqoiiLq6BsyNjymnFyB5a7pEQwYThj9QIgqBy9+XPPwj7+hAEHyR2npOHL1bz4Qg==",
    })
    pyodide        = Cdn(Block.libs, DepKind.pyodide, "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js")

    #vvvvvvvvvvvvvvv
    # GENERATED-libs
    config         = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/0-config.js", extra_dump="dump_to_js_config")
    functools      = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/1-functools.js")
    cfg_process    = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/2-configPostProcess-cfg_process.js")
    jsLogger       = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/jsLogger.js")
    mathjax        = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/mathjax-libs.js")
    global_gui     = Cdn(Block.libs, DepKind.always, "{base_url}/js-libs/z_globalGuiButtons-global_gui.js")
    generic        = Css("{base_url}/pyodide-css/0-generic.css")
    header         = Css("{base_url}/pyodide-css/btns-header.css")
    hourglass      = Css("{base_url}/pyodide-css/hourglass.css")
    ide            = Css("{base_url}/pyodide-css/ide.css")
    qcm            = Css("{base_url}/pyodide-css/qcm.css")
    terminal       = Css("{base_url}/pyodide-css/terminal.css")
    testing        = Css("{base_url}/pyodide-css/testing.css")
    # GENERATED-libs
    #^^^^^^^^^^^^^^^

    jQuery_css     = Css("https://cdn.jsdelivr.net/npm/jquery.terminal@2.43.1/css/jquery.terminal.min.css")
    awesome_font   = Css({
        "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css",
        "integrity": "sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==",
    })

    # Always _after_ the js CONFIG file
    mathjax_tex    = Cdn(Block.libs, DepKind.always, "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js")


    #---------------------------------------------------


    #vvvvvvvvvvvvvvvv
    # GENERATED-pages
    snippets       = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/0-generic-python-snippets-pyodide.js")
    error_logs     = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/1-error_logs-pyodide.js")
    install        = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/1-packagesInstaller-install-pyodide.js")
    runtime        = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/1-runtimeManager-runtime-pyodide.js")
    runner         = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/2-pyodideSectionsRunner-runner-pyodide.js")
    btnRunner      = Cdn(Block.content, DepKind.py_btn,    "{base_url}/js-per-pages/3-btnRunner-py_btn.js")
    terminalRunner = Cdn(Block.content, DepKind.term,      "{base_url}/js-per-pages/3-terminalRunner-term.js")
    ideRunner      = Cdn(Block.content, DepKind.ide,       "{base_url}/js-per-pages/4-ideRunner-ide.js")
    ideTester      = Cdn(Block.content, DepKind.ides_test, "{base_url}/js-per-pages/5-ideTester-ides_test.js")
    qcms           = Cdn(Block.content, DepKind.qcm,       "{base_url}/js-per-pages/qcms-qcm.js")
    start          = Cdn(Block.content, DepKind.pyodide,   "{base_url}/js-per-pages/start-pyodide.js")
    # GENERATED-pages
    #^^^^^^^^^^^^^^^^


    #---------------------------------------------------


    #vvvvvvvvvvvvvvvvvv
    # GENERATED-scripts
    subscriptions  = Cdn(Block.scripts, DepKind.always, "{base_url}/js-scripts/subscriptions.js")
    # GENERATED-scripts
    #^^^^^^^^^^^^^^^^^^
