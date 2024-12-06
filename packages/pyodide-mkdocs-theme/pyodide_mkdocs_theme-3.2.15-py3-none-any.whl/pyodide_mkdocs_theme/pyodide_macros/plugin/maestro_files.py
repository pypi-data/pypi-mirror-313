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



from collections import defaultdict
from operator import attrgetter
from typing import Dict, List, Optional, Set
from pathlib import Path

from mkdocs.exceptions import BuildError
from mkdocs.structure.files import Files, File, InclusionLevel
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Navigation


from ..pyodide_logger import logger
from ..exceptions import PyodideMacrosPyLibsError
from ..tools_and_constants import PmtTests
from .tools.maestro_tools import PythonLib
from .maestro_base import BaseMaestro









class MaestroPyLibs(BaseMaestro):
    """
    Handles anything related to files managed on the fly, including python_libs management.
    """


    libs: List[PythonLib] = None        # added on the fly
    """
    List of PythonLib objects, representing all the available custom python libs.
    """

    base_py_libs: Set[str] = None       # added on the fly
    """
    Set of all the python_libs paths strings, as declared in the plugins config (meta or not).
    """

    python_libs_in_pyodide: List[str] = None
    """
    Names of the each python_lib, as it will be imported from pyodide.
    """


    def on_config(self, config: MkDocsConfig):

        super().on_config(config)

        logger.info("Prepare python_libs.")
        self._conf.watch.extend(
            str(py_lib.absolute()) for py_lib in map(Path, self.python_libs)
                                   if py_lib.exists()
        )

        self.libs: List[PythonLib] = sorted(
            filter(None, map(PythonLib, self.python_libs)),
            key=attrgetter('abs_slash')
        )
        self._check_libs()
        self.base_py_libs = set(p.lib for p in self.libs)
        self.python_libs_in_pyodide = [lib.lib_name for lib in self.libs]




    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        """
        If python libs directories are registered, create one archive for each of them.
        It's on the responsibility of the user to work with them correctly...
        """
        logger.info("Create python_libs archives.")
        for lib in self.libs:
            # Remove any cached files to make the archive lighter (the version won't match
            # pyodide compiler anyway!):
            for cached in lib.path.rglob("*.pyc"):
                cached.unlink()
            file = lib.create_archive_and_get_file(self)
            files.append(file)

        return super().on_files(files, config=config)




    # Override
    def on_post_build(self, config: MkDocsConfig) -> None:
        """
        Suppress the python archives from the CWD.
        """
        logger.info("Remove python_libs archives.")
        for lib in self.libs:
            lib.unlink()

        super().on_post_build(config)





    def _check_libs(self):
        """
        Add the python_libs directory to the watch list, create the internal PythonLib objects,
        and check python_libs validity:
            1. No python_lib inside another.
            2. If not a root level, must not be importable.
            3. No two python libs with the same name (if registered at different levels)
        """

        libs_by_name: Dict[str, List[PythonLib]] = defaultdict(list)
        for lib in self.libs:
            libs_by_name[lib.lib_name].append(lib)


        same_names = ''.join(
            f"\nLibraries that would be imported as {name!r}:" + ''.join(
                f'\n\t{ lib.lib }' for lib in libs
            )
            for name,libs in libs_by_name.items() if len(libs)>1
        )
        if same_names:
            raise PyodideMacrosPyLibsError(
                "Several custom python_libs ending with the same final name are not allowed."
                + same_names
            )

        parenting = ''.join(
            f"\n\t{ self.libs[i-1].lib } contains at least { lib.lib }"
                for i,lib in enumerate(self.libs)
                if i and self.libs[i-1].is_parent_of(lib)
        )
        if parenting:
            raise PyodideMacrosPyLibsError(
                "Custom python libs defined in the project cannot contain others:" + parenting
            )












class MaestroTesting(BaseMaestro):


    _testing_file: Optional[File] = None
    """
    MkDocs File instance of the test_ides page, if used (allows to "transfer" data/logic from
    `on_files` to `on_nav`).
    """

    tests_on_built_site:  bool = False
    """ Check if the build is done for the online website or not (ie. local/serve) """

    do_add_testing_page:  bool = False
    """
    Decide if the test_ides page must be included in the build or not:
        - Always included if the mkdocs.yml is configured to create it on the built site.
        - Only include during serve if configured for serve only.
    """

    is_mermaid_available: bool = False




    def on_config(self, config: MkDocsConfig):
        super().on_config(config)

        self.is_mermaid_available = self._is_mermaid_available()
        self.tests_on_built_site  = self.testing_include == PmtTests.site
        self.do_add_testing_page  = (
            self.tests_on_built_site                                      # site + serve
            or self.in_serve and self.testing_include == PmtTests.serve   # serve only
        )


    def _is_mermaid_available(self):
        mdx_conf      = self._conf.mdx_configs
        custom_fences = mdx_conf.get('pymdownx.superfences', {}).get('custom_fences', [])
        return any( fences['name']=='mermaid' for fences in custom_fences)





    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        """
        If python libs directories are registered, create one archive for each of them.
        It's on the responsibility of the user to work with them correctly...
        """
        if self.do_add_testing_page:
            logger.info("Add IDEs testing page to documentation.")
            self._testing_file = self._build_testing_page(config)
            files.append(self._testing_file)

        return files


    def _build_testing_page(self, config:MkDocsConfig):

        from ..macros.ide_tester import IdeTester       # pylint: disable=import-outside-toplevel

        page_name = self._build_and_validate_testing_page_name()
        content   = IdeTester.get_markdown(self.is_mermaid_available)
        inclusion = InclusionLevel.NOT_IN_NAV if self.tests_on_built_site else InclusionLevel.INCLUDED
        file      = File.generated(config, page_name, content=content, inclusion=inclusion)
        return file


    def _build_and_validate_testing_page_name(self):

        name = self.testing_page
        if not name.endswith('.md'):
            name += '.md'

        file_path = Path(name)

        if name != file_path.name:
            raise BuildError(
                'The page to test all IDEs should be at the top level of the documentation '
                f'but was: { name }'
            )
        if file_path.exists():
            raise BuildError(
                'Cannot create the page to test all IDEs: a file with the target name already '
                f'exists: { name }.'
            )
        return name




    def on_nav(self, nav: Navigation, /, *, config: MkDocsConfig, files: Files):

        if not self._testing_file:
            return

        page = self._testing_file.page

        # Make sure the title will stay the short version in the navigation
        # (because, awesome-pages plugin):
        page.title = page.file.name

        # Awesome-pages plugin _MIGHT_ add the page to the nav automatically if the author
        # is using patterns to find pages, so need to check if that happened already:
        i_tests     = next((i for i,p in enumerate(nav.items) if p is page), None)
        in_nav      = i_tests is not None
        is_not_last = in_nav and i_tests != len(nav.items)-1
        add_to_nav  = not self.tests_on_built_site or self.in_serve

        if add_to_nav:
            logger.info("Add IDEs testing page to navigation")
            if not in_nav:
                nav.items.append(page)
                # Note: it seems useless to add it to the nav.pages list.

            elif is_not_last:
                # Awesome page might have ordered the test page in whatever way it wants...
                nav.items.pop(i_tests)
                nav.items.append(page)

        elif in_nav:
            logger.info("Remove IDEs testing page from navigation")
            # Never leave the test_ides page in the nav on the built site (awesome-pages plugin
            # might have already added it to the nav if the author is using patterns):
            nav.items.pop(i_tests)

        return nav










class MaestroFiles(
    MaestroPyLibs,
    MaestroTesting,
):
    """
    Handles anything related to files managed on the fly, including python_libs management.
    """
