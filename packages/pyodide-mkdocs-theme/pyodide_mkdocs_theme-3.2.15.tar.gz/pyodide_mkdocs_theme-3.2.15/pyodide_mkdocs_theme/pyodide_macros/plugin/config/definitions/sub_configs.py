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



from typing import List
from mkdocs.config import config_options as C


from pyodide_mkdocs_theme.pyodide_macros.plugin.tools.test_cases import CASES_OPTIONS
from pyodide_mkdocs_theme.pyodide_macros.tools_and_constants import PmtTests
from ..common_tree_src import CommonTreeSrc, DeprecationStatus
from ..config_option_src import ConfigOptionDeprecated, ConfigOptionSrc
from ..sub_config_src import SubConfigSrc
from .docs_dirs_config import DOCS_CONFIG, to_page
from ...tools.options_alterations import sanitize_decrease_attempts_on_user_code_failure



# NOTE: must be a single line, otherwise it well mess `dedent` up.
FORBID_SHORT_CONFIG = (
    "Par défaut, cette situation est considérée comme invalide et `BuildError` sera "
    "levée. Si ce comportement est souhaité, passer cette option à `False`."
)
EN_FORBID_SHORT_CONFIG = (
    "By default, this situation is considered invalid and `BuildError` will be raised. "
    "If this is the desired behavior, set this option to false."
)




CommonTreeSrc.DEFAULT_DOCS_URL_TEMPLATE = to_page(DOCS_CONFIG) / '#{py_macros_path}'

BUILD_CONFIG = SubConfigSrc(
    'build',
    docs = """
    Réglages concernant la construction de la documentation ou qui impactent la façon
    dont le contenu des pages est construit.
    """,
    elements = (

    ConfigOptionSrc(
        'deprecation_level', str, conf_type=C.Choice( ('error', 'warn'), default='error'),
        docs = """
            Comportement utilisé lors d'un build/serve lorsqu'une option obsolète est utilisée.
        """,
        yaml_desc="Behavior when a deprecated feature is used."
    ),

    ConfigOptionSrc(
        'encrypted_js_data', bool, default=True,
        docs="""
            Si `True`, les données de configuration des IDEs, terminaux et py_btns sont encodées.
            Si des problèmes de décompression des données sont rencontrés, cette option peut être
            désactivée.
        """,
        yaml_desc="Compress or not configuration data of IDEs, terminals, ...",
        # yaml_desc="Compression ou non des données de configuration des IDEs, terminaux, ...",
        # """
        # If True, the configuration data for IDEs, terminals, py_btns, ... are encrypted.
        # In case of decompression troubles, you may want to deactivate this option.
        #
        # Note that the ides.encrypt_alpha_mode setting also applies to these encryptions.
        # """
    ),

    ConfigOptionSrc(
        'forbid_macros_override', bool, default=True,
        docs="""
            Si `True`, `PyodideMacrosError` est levée lorsque deux macros du même nom sont
            enregistrées par le plugin.
        """,
        yaml_desc="""
            If `True` registering different macros with the same name will raise a
            `PyodideMacrosError`.
        """,
        # """
        # If True, `PyodideMacrosError` is raised when two macros are registered with the same name.
        # """
    ),

    ConfigOptionSrc(
        'ignore_macros_plugin_diffs', bool, default=False,
        docs = """
            Passer à `#!py True` pour éviter la vérification de compatibilité de la
            configuration du plugin `PyodideMacroPlugin` avec celle du plugin original
            des macros, `MacrosPlugin`.

            ??? note "Raisons de cette vérification"

                Le plugin du thème hérite de celui de la bibliothèque `mkdocs-macros-plugin`,
                `PyodideMacros`.

                Or, la configuration du plugin `MacrosPlugin` est faite "à
                l'ancienne", avec `config_scheme`, alors que celle de `PyodideMacroPlugin`
                utilise les classes `Config` disponibles à partir de mkdocs 1.5+.
                Les deux étant incompatibles, cela à imposé de reporter en dur la configuration
                du plugin d'origine dans celle du thème. Ceci fait qu'une modification de la
                configuration du plugin d'origine pourrait rendre celle du thème inopérant sans
                préavis.

                Si une différence est constatée entre les deux configurations, le build est donc
                avorté car il n'y a aucune garantie que le site construit puisse encore être
                correct. Cette vérification permet donc d'assurer que le comportement des objets
                `MacrosPlugin` sera celui attendu.

                Si les modifications de `MacrosPlugin` sont mineures, il est possible qu'un build
                puisse tout de même fonctionner, et passer cette option à `#!py True` permettra
                donc de faire l'essai. À tenter à vos risques et périls...
        """,
        yaml_desc="""
            Deactivate the compatibility check of PyodideMacrosPlugin configuration against the
            MacrosPlugin one.
        """,
        # yaml_desc="""
        #     Désactive la vérification de compatibilité entre PyodideMacrosPlugin et MacrosPlugin
        # """,
        # """
        # Set to True to bypass the compatibility check of the `PyodideMacrosPlugin` config against
        # the original `MacrosPlugin` one.

        # ??? note "Reasons behind this verification"

        #     `MacrosPlugin` is configured the "old fashion" way while `PyodideMacrosPlugin` is
        #     using mkdocs 1.5+ Config classes. This means that the `MacrosPlugin` configuration
        #     had to be hardcoded in the `PyodideMacrosPlugin` config.

        #     Because of this, any config change on the `MacrosPlugin` side could break
        #     `PyodideMacrosPlugin` without warning, so this verification enforces the expected
        #     implementation of the parent class.

        #     If ever something unexpected is found, the build will be aborted, because no
        #     guarantees can be given about the correctness of the build in such situation.

        #     In case of minor changes, this option will allow the build, but use it "at your own
        #     risks".
        # """
    ),

    ConfigOptionSrc(
        'load_yaml_encoding', str, default='utf-8',
        docs="""
            Encodage à utiliser lors du chargement de données YAML avec les fonctionnalités
            originales de MacrosPlugin :

            La méthode d'origine n'utilise aucun argument d'encodage, ce qui peut entraîner des
            comportements différents entre Windows et Linux (typiquement : lors de l'exécution
            d'un pipeline sur la forge EN par rapport au travail local sous Windows).
        """,
        yaml_desc="""
            Encoding used when loading yaml files within the original macros plugin.
        """,
        # yaml_desc="""
        #     Encodage utilisé pour charger des fichiers yaml depuis le plugin des macros.
        # """,
        # """
        # Encoding to use when loading yaml data with the original MacrosPlugin functionalities :

        # The original method doesn't use any encoding argument, which can lead to different
        # behaviors between Windows and Linux (typically: during a pipeline vs working locally
        # with Windows).
        # """
    ),

    ConfigOptionSrc(
        'macros_with_indents', List[str], conf_type=C.ListOfItems(C.Type(str), default=[]),
        docs="""
            Permet d'enregistrer des macros personnalisées (liste de chaînes de caractères), qui
            insèrent du contenu markdown multilignes, pour pouvoir indenter  correctement le
            contenu dans la page :

            Une fois qu'une macro est enregistrée dans cette liste, elle peut appeler la méthode
            `env.indent_macro(markdown)` durant son exécution pour que le contenu généré soit
            indenté correctement par le plugin.
        """,
        yaml_desc="""
            List of macros inserting multiline contents in the pages (allowing to use
            `plugin.indent_macro(markdown)` from them).
        """,
        # yaml_desc="""
        #     Liste de macros insérant des contenus multilignes (permet d'y utiliser
        #     `PyodideMacrosPlugin.indent_macro`).
        # """,
        # """
        # Allow to register external macros, as a list of strings, that will need to insert properly
        # indented multiline contents in the page.
        # Once a macro is registered in this list, it can call `env.get_macro_indent()` at runtime
        # to get the indentation level (as a string of spaces) of the macro call in the markdown
        # source file.
        # """
    ),

    ConfigOptionSrc(
        'meta_yaml_allow_extras', bool, default=False,
        docs="""
            Définit s'il est possible d'ajouter dans les fichiers {{meta()}} des données autres
            que celles relatives au plugin lui-même.

            Lorsque cette valeur est à `#!yaml false`, seules des options du plugin `pyodide_macros`
            sont autorisées, ce qui permet de valider l'intégralité du contenu du fichier, mais
            empêche par exemple de définir des variables pour les macros dans ces fichiers.<br>Si
            la valeur est à `#!yaml true`, il est alors possible d'ajouter d'autres variables,
            mais les fautes de frappes dans les premiers niveaux ne peuvent plus être identifiées
            (exemple : `temrs.cut_feedback` au lieu de `terms.cut_feedback`).
        """,
        yaml_desc="Allow definition of extra variables/options in the `.meta.pmt.yml` files.",
    ),

    ConfigOptionSrc(
        'meta_yaml_encoding', str, default='utf-8',
        docs="Encodage utilisé pour charger les [fichiers `.meta.pmt.yml`](--custom/metadata/).",
        yaml_desc="Encoding to use when loading `.meta.pmt.yml` files."
    ),

    ConfigOptionSrc(
        'python_libs', List[str], conf_type=C.ListOfItems(C.Type(str), default=['py_libs']),
        docs="""
            Liste de répertoires de [bibliothèques python](--custom-libs) qui doivent être
            importables dans Pyodide.

            Une erreur est levée si :

            * Le nom donné ne correspond pas à un répertoire existant (sauf s'il s'agit de la
            valeur par défaut, `#!py "py_libs"`).
            * Le répertoire n'est pas situé à la racine du projet.
            * Le répertoire n'est pas une bibliothèque Python (c'est-à-dire qu'il ne contient
            pas de fichier `__init__.py`).
        """,
        yaml_desc="""
            List of custom python packages to make available at runtime in Pyodide environment.
        """,
        # yaml_desc="""
        #     Liste des bibliothèques personnalisée à rendre disponibles sur le site final.
        # """,
        # """
        # List of directories of python packages that must be importable in Pyodide.

        # An error is raised if:

        # * The given name isn't an existing directory (unless it's the default value, `py_libs`).
        # * The directory isn't at project root level.
        # * The directory isn't a python package (aka: it doesn't have an `__init__.py` file).
        # """
    ),

    ConfigOptionSrc(
        'skip_py_md_paths_names_validation', bool, default=False,
        docs = """
            Par défaut, les noms de chemin de tous les fichiers `.py` et `.md` présents dans
            le `docs_dir` sont vérifiés pour s'assurer qu'ils ne contiennent aucun caractère
            autre que des lettres, des chiffres, des points ou des tirets. Cela garantit le
            bon fonctionnement des macros liées aux IDEs.

            Si des caractères indésirables sont détectés, une erreur de type `BuildError`
            est levée. Cependant, cette vérification peut être désactivée en assignant `True`
            à ce paramètre.
            ... À Utiliser  à vos risques et périls.
        """,
        yaml_desc="Deactivate the sanity check of the directories and files in the `docs_dir`.",
        # yaml_desc="Désactive le contrôle des nom de dossiers et fichiers.",
        # """
        # By default, the path names of all the `.py` and `.md` files present in the docs_dir are
        # checked so that they do not contain any character other than letters, digits, dots or
        # dashes. This ensures the macros related to IDEs will work properly.

        # If unwanted characters are found, a BuildError is raised, but this verification can be
        # turned off by setting this flag to True. Use it at your own risks.
        # """
    ),

    ConfigOptionSrc(
        'tab_to_spaces',int, default=-1,
        docs="""
            Si cette option est définie avec une valeur positive (ou nulle), les tabulations
            trouvées avant un appel à une macro multiligne (voir l'option
            [`macros_with_indent`](--pyodide_macros_build_macros_with_indents)) seront
            automatiquement converties en utilisant ce nombre d'espaces.

            __Aucune garantie n'est alors donnée quant à la correction du résultat__.
            <br>Si une conversion est effectuée, un avertissement sera affiché dans la console
            pour faciliter la localisation et la modification des appels de macros responsables
            du warning.

            !!! warning "Éviter les caractères de tabulation dans la documentation"

                Régler votre éditeur de code de manière à ce qu'il remplace automatiquement les
                tabulations par des espaces.

                Les caractères de tabulation ne sont pas toujours interprétés de la même façon
                selon le contexte d'utilisation du fichier, tandis que les fichiers markdown
                reposent en bonne partie sur les indentations pour définir la mise en page des
                rendus.
                <br>Les tabulations sont donc à proscrire.
        """,
        yaml_desc="""
            Number os space characters used to replace tabulations on the left of multiline
            macro calls.
        """,
        # yaml_desc="""
        #     Nombre d'espaces pour remplacer les tabulation lors de la gestion des macros avec
        #     indentation.
        # """,
        # """
        # If set to a positive value (or 0), tabs characters found in front of a multiline macro
        # call will automatically be converted using this number of spaces (see
        # [`macros_with_indent`]
        # (--pyodide_macros_build_macros_with_indents)
        # option).
        # <br>_There are NO guarantees about the correctness of the result_.

        # If a conversion is done, a warning will be shown in the console to find and modify more
        # easily the problematic macros calls.
        # """
    ),

    ConfigOptionSrc(
        '_pmt_meta_filename', str, default=".meta.pmt.yml", in_yaml_docs=False,
        docs = "Nom des fichiers de configuration des métadonnées pour le thème.",
        yaml_desc="Name used for the Pyodide-MkDoc-Theme meta files."
    ),

    #----------------------------------------------------------------------------

    # ConfigOptionDeprecated(
    #     'encrypt_corrections_and_rems', bool,
    #     moved_to = 'ides.encrypt_corrections_and_rems'
    # ),
    # ConfigOptionDeprecated(
    #     'forbid_secrets_without_corr_or_REMs', bool,
    #     moved_to = 'ides.forbid_secrets_without_corr_or_REMs',
    # ),
    # ConfigOptionDeprecated(
    #     'forbid_hidden_corr_and_REMs_without_secrets', bool,
    #     moved_to = 'ides.forbid_hidden_corr_and_REMs_without_secrets',
    # ),
    # ConfigOptionDeprecated(
    #     'forbid_corr_and_REMs_with_infinite_attempts', bool,
    #     moved_to = 'ides.forbid_corr_and_REMs_with_infinite_attempts',
    # ),
    # ConfigOptionDeprecated(
    #     'bypass_indent_errors', bool, dep_status=DeprecationStatus.removed,
    # ),
))












IDES_CONFIG = SubConfigSrc(
    'ides',
    docs = """
    Réglages spécifiques aux IDEs (comportements impactant l'utilisateur et les exécutions).
    """,
    elements = (

    ConfigOptionSrc(
        'deactivate_stdout_for_secrets', bool, default=True,
        docs="""
            Détermine si la sortie standard (stdout) sera visible dans les terminaux lors
            des tests secrets ou non.
        """,
        yaml_desc="""
            Define if the stdout will be shown in terminals to the user or not, during the
            secret tests.
        """,
    ),

    ConfigOptionSrc(
        'decrease_attempts_on_user_code_failure', bool,
        conf_type=C.Choice(('editor', 'public', 'secrets', True, False), default='editor'),
        value_transfer_processor=sanitize_decrease_attempts_on_user_code_failure,
        docs="""
            En dehors des étapes d'environnement, les validations sont constituées de 3 étapes,
            exécutant les éléments suivants :

            1. `#!py "editor"` : code dans l'éditeur de l'IDE (y compris l'état actuel des
            tests publics).
            1. `#!py "public"` : version __originale__ des tests publics (section `tests`
            dans le fichier python).
            1. `#!py "secrets"` : section `secrets` du fichier python.

            Les exécutions étant stoppées à la première erreur rencontrée, cette option définit
            à partir de quelle étape une erreur doit consommer un essai.

            --8<-- "docs_tools/inclusions/decrease_attempts_on_user_code_failure.md"

            ??? warning "Options booléennes"

                Les valeurs booléennes sont là uniquement pour la rétrocompatibilité et un
                warning apparaîtra dans la console si elles sont utilisées.

                * `True` correspond à `#!py "editor"`
                * `False` correspond à `#!py "secrets"`
        """,
        yaml_desc="""
            Define from which step an error will consume an attempt, during a validation.
        """,
        # yaml_desc="""
        #     Défini si les échecs avant la section `secrets` comptent déjà pour un essai ou non,
        #     lors des validations.
        # """,
        # """
        # If true, any failure when running the user code during a validation will decrease the
        # number of attempts left. Note this means even syntax errors will decrease the count.

        # When this option is set to False, any error raised within the code of the editor will stop
        # the validation process without modifying the number of attempts left.
        # """
    ),

    ConfigOptionSrc(
        'encrypt_alpha_mode', str,
        conf_type=C.Choice(('direct', 'shuffle', 'sort'), default='direct'),
        docs="""
            Les contenus (codes, corrections & remarques) sont transmis de mkdocs aux pages html
            en utilisant des données compressées. L'encodage est réalisé avec l'algorithme LZW,
            et cette option contrôle la manière dont l'alphabet/la table initiale est construit à
            partir du contenu à encoder :

            - `#!py "direct"` : l'alphabet utilise les symboles dans l'ordre où ils sont trouvés
            dans le contenu à compresser (utilisé par défaut).
            - `#!py "shuffle"` : l'alphabet est mélangé aléatoirement.
            - `#!py "sort"` : les symboles sont triés dans l'ordre naturel.
        """,
        yaml_desc="""
            Define in what order the characters of the content are pushed in the LZW compression
            table (by default: `direct`, `shuffle`, `sort`).
        """,
        # yaml_desc="""
        #     Gestion de l'alphabet initial lors des compression LZW (`direct` par défaut, `shuffle`
        #     ou `sort`).
        # """,
        # """
        # Original contents are passed from mkdocs to the JS environment using compressed data. The
        # encoding is done with LZW algorithm, and this option controls how the LZW initial alphabet
        # is built from the content to encode:

        # - `"direct"`: the alphabet is using all symbols in order.
        # - `"shuffle"`: the alphabet is randomized.
        # - `"sort"`: all symbols are sorted in natural order.
        # """
    ),

    ConfigOptionSrc(
        'encrypt_corrections_and_rems', bool, default=True,
        docs="""
            Si activé, le contenu de la div HTML de la correction et des remarques, sous
            les IDEs, sera compressé lors de la construction du site.

            Désactiver ceci peut être utile durant le développement, mais {{ red("cette option
            doit toujours être activée pour le site déployé") }}, sans quoi la barre de recherche
            pourraient suggérer le contenu des corrections et des remarques à l'utilisateur.
        """,
        yaml_desc="""
            Compress or not the solutions and remarks below IDEs (deactivate only for
            debugging purpose).
        """,
        # yaml_desc="""
        #     Compression ou non des corrections et remarques sous les IDEs (désactiver pour
        #     debugging uniquement).
        # """,
        # """
        # If True, the html div containing correction and remarks below IDEs will be encrypted at
        # build time.

        # Passing this to False can be useful during development, but the value should _ALWAYS_
        # be True on the deployed website: keep in mind the search engine can otherwise make
        # surface contents from solutions and remarks as suggestions when the user is using
        # the search bar.
        # """
    ),

    ConfigOptionSrc(
        'export_zip_prefix', str, default="",
        docs="""
            Préfixe ajouté au début du nom des archives zip créées avec les contenus des éditeurs
            des IDEs configurés comme exportable (argument `EXPORT=True`).
            Si `{{config_validator('ides.export_zip_prefix',tail=1)}}` n'est pas une chaîne vide,
            un trait d'union sera ajouté automatiquement entre le préfixe et le reste du nom de
            l'archive.
        """,
        yaml_desc="""
            Prefix for the zip archive containing the editor content of all the exportable IDEs
            in the page.
        """,
    ),

    ConfigOptionSrc(
        'export_zip_with_names', bool, default=False,
        docs="""
            Si `#!py True`, au moment où un utilisateur demandera de créer l'archive zip avec tous
            les codes des IDEs de la page, une fenêtre s'ouvrira lui demandant d'indiquer son nom.
            Une fois le nom renseigné, il sera ajouté entre l'éventuel préfixe (voir {{config_link(
            'ides.export_zip_prefix', tail=1)}}) et le nom normal de l'archive zip, entouré par des
            traits d'union.
        """,
        yaml_desc="""
            Choose if the user has to give a name when building a zip archive of the IDEs contents.
        """,
    ),

    ConfigOptionSrc(
        'forbid_corr_and_REMs_with_infinite_attempts', bool, default=True,
        docs = f"""
            Lors de la construction des IDEs, si une section `corr`, un fichier `REM` ou `
            VIS_REM` existent et que le nombre de tentatives est illimité, ce contenu ne
            sera jamais accessible à l'utilisateur, sauf s'il réussit les tests.

            { FORBID_SHORT_CONFIG }
        """,
        yaml_desc = EN_FORBID_SHORT_CONFIG,
        # """
        # When building IDEs, if a `corr` section, a REM file or a VIS_REM file exist while the
        # number of attempts is infinite, that content will never become accessible to the user,
        # unless they pass the tests.

        # By default, this situation is considered invalid and `BuildError` will be raised.
        # If this is the desired behavior, set this option to false.
        # """
    ),

    ConfigOptionSrc(
        'forbid_hidden_corr_and_REMs_without_secrets', bool, default=True,
        docs=f"""
            Lors de la construction des IDEs, le bouton de validation n'apparaît que si une
            section `secrets` existe.
            <br>Si des sections `corr` ou des fichiers `REM` existent alors qu'aucune section
            `secrets` n'est présente, leur contenu ne sera jamais disponible pour l'utilisateur
            en raison de l'absence de bouton de validation dans l'interface.

            { FORBID_SHORT_CONFIG }
        """,
        yaml_desc = EN_FORBID_SHORT_CONFIG,
        # """
        # When building IDEs, the validation button will appear only when a `secrets` section exist.
        # If none is given while a corr section or REM files exist, their content will never be
        # available to the user because of the lack of validation button in the interface.

        # By default, this situation is considered invalid and `BuildError` will be raised.
        # If this is the desired behavior, set this option to false.
        # """
    ),

    ConfigOptionSrc(
        'forbid_secrets_without_corr_or_REMs', bool, default=True,
        docs = FORBID_SHORT_CONFIG,
        yaml_desc = EN_FORBID_SHORT_CONFIG,
        # """
        # By default, this situation is considered invalid and `BuildError` will be raised.
        # If this is the desired behavior, set this option to false.
        # """
    ),

    ConfigOptionSrc(
        'show_only_assertion_errors_for_secrets', bool, default=False,
        docs="""
            Si activé (`True`), la stacktrace des messages d'erreur sera supprimée et
            seuls les messages des assertions resteront inchangées lorsqu'une erreur
            sera levée pendant les tests secrets.

            | `AssertionError` | Pour les autres erreurs |
            |:-:|:-:|
            | {{ pmt_note("Option à `false`",0) }}<br>![AssertionError: message
            normal](!!show_assertions_msg_only__assert_full_png) | {{ pmt_note("Option à `false`",0)
            }}<br>![Autres erreurs: message normal](!!show_assertions_msg_only__error_full_png) |
            | ![AssertionError: sans stacktrace](!!show_assertions_msg_only_assert_no_stack_png){{
            pmt_note("Option à `true`") }} | ![Autres erreurs sans stacktrace ni
            message](!!show_assertions_msg_only_error_no_stack_png){{ pmt_note("Option à `true`")
            }} |
        """,
        yaml_desc="""
            If True, the stack trace of all error messages will be suppressed and only
            assertion messages will be left unchanged, when an error is raised during the
            secret tests.
        """
        # yaml_desc="""
        #     Réduit drastiquement les informations visibles dans les messages d'erreurs
        #     (suppression stacktrace + pour les erreur autre que `AssertionError`, seulement
        #     le type d'erreur est donné).
        # """,
    ),

    ConfigOptionSrc(
        'editor_font_family', str, default="monospace",
        docs = "Police de caractère à utiliser pour les éditeurs des IDEs.",
        yaml_desc = "Font family used in IDEs' editor.",
    ),

    ConfigOptionSrc(
        'editor_font_size', int, default=15,
        docs = "Taille de la police de caractère les éditeurs des IDEs.",
        yaml_desc = "Font size used in IDEs' editor.",
    ),

    ConfigOptionSrc(
        'ace_style_dark', str, default="tomorrow_night_bright",
        docs = """
            Thème de couleur utilisé pour les éditeurs des IDEs en mode sombre ([liste des
            thèmes disponibles][ace-themes]: utiliser le noms des fichiers `js` sans l'extension).{{
            pmt_note("Ce réglage est écrasé par l'ancienne façon de modifier le thème, en
            définissant `extra.ace_style.slate` dans le fichier mkdocs.yml.")}}
            )}}
        """,
        yaml_desc = "Dark theme for IDEs' editor.",
    ),

    ConfigOptionSrc(
        'ace_style_light', str, default="crimson_editor",
        docs = """
            Thème de couleur utilisé pour les éditeurs des IDEs en mode clair ([liste des thèmes
            disponibles][ace-themes]: utiliser le noms des fichiers `js` sans l'extension).{{
            pmt_note("Ce réglage est écrasé par l'ancienne façon de modifier le thème, en
            définissant `extra.ace_style.default` dans le fichier mkdocs.yml.")}}

        """,
        yaml_desc = "Light theme for IDEs' editor.",
    ),


    #--------------------------------------------------------------------------------

    # ConfigOptionDeprecated(
    #     'show_assertion_code_on_failed_test', bool, moved_to='args.IDE.LOGS',
    # ),
    # ConfigOptionDeprecated(
    #     'max_attempts_before_corr_available', int, moved_to='args.IDE.MAX',
    # ),
    # ConfigOptionDeprecated(
    #     'default_ide_height_lines', int, moved_to='args.IDE.MAX_SIZE',
    # ),
))











QCMS_CONFIG = SubConfigSrc(
    'qcms',
    docs = "Réglages spécifiques aux QCMs.",
    elements = (
    ConfigOptionSrc(
        'forbid_no_correct_answers_with_multi', bool, default=True,
        docs="""
            Si désactivé (`False`), une question sans réponse correcte fournie, mais marquée comme
            `multi=True`, est considérée comme valide. Si cette option est réglée à `True`, cette
            situation lèvera une erreur.
        """,
        yaml_desc = "Allow to disambiguate MCQ and SCQ when needed.",
        # yaml_desc="Permet de clarifier entre QCM et QCU quand ambiguë.",
        # """
        # If False, a question with no correct answer provided, but that is tagged as `multi=True`
        # is considered valid. If this option is set to True, that situation will raise an error.
        # """
    ),

    #-----------------------------------------------------------------------------

    # ConfigOptionDeprecated('hide',    bool, moved_to='args.multi_qcm.hide'),
    # ConfigOptionDeprecated('multi',   bool, moved_to='args.multi_qcm.multi'),
    # ConfigOptionDeprecated('shuffle', bool, moved_to='args.multi_qcm.shuffle')
))











TERMS_CONFIG = SubConfigSrc(
    'terms',
    docs = "Réglages spécifiques aux terminaux.",
    elements = (

    ConfigOptionSrc(
        'cut_feedback', bool, default=True,
        docs="""
            Si activé (`True`), les entrées affichées dans les terminaux sont tronquées si elles
            sont trop longues, afin d'éviter des problèmes de performances d'affichage des outils
            `jQuery.terminal`.
        """,
        yaml_desc="""
            If True, the content printed in the terminal will be truncated if it's too long, to
            avoid performances troubles.
        """
    ),

    ConfigOptionSrc(
        'stdout_cut_off', int, default=200,
        docs="""
            Nombre maximal de lignes restant affichées dans un terminal : si de nouvelles
            lignes sont ajoutées, les plus anciennes sont éliminées au fur et à mesure.

            ??? note "Performances d'affichage des terminaux"

                ___Les éléments `jQuery.terminal` deviennent horriblement lents lorsque le
                nombre de caractères affichés est important.___

                Cette option permet de limiter ces problèmes de performance lorsque la sortie
                standard n'est pas tronquée (voir le bouton en haut à droite du terminal).

                Noter par contre que cette option _ne limite pas_ le nombre de caractères dans
                une seule ligne, ce qui veut dire qu'une page figée est toujours possible,
                tandis que l'option de troncature, `cut_feedback` évitera ce problème aussi.
        """,
        yaml_desc = "Maximum number of lines kept in terminals.",
        # yaml_desc="Nombre de lignes maximales affichables dans les terminaux.",
        # """
        # Maximum number of lines displayed at once in a terminal. If more lines are printed, the
        # lines at the top are removed.

        # NOTE: jQuery.terminals become AWFULLY SLOW when the number of characters they display
        # become somewhat massive. This option allows to limit these performances troubles, when
        # the stdout is not truncated (see terminals upper right corner button). Also note that
        # this option _does not_ limit the number of characters per line, so a frozen page can
        # still occur, while the truncation feature will take care of that.
        # """
    ),

    #--------------------------------------------------------------------------------

    # ConfigOptionDeprecated('default_height_ide_term',      int, moved_to='args.IDE.TERM_H'),
    # ConfigOptionDeprecated('default_height_isolated_term', int, moved_to='args.terminal.TERM_H')
))










TESTING_CONFIG = SubConfigSrc(
    'testing',
    docs = """
        Permet de paramétrer la page pour tester automatiquement tous les IDEs de la documentation.
    """,
    elements = (

    ConfigOptionSrc(
        'page', str, default="test_ides",
        docs="""
            Nom de fichier markdown (avec ou sans l'extension `.md`) utilisé pour générer une page
            contenant le nécessaire pour tester de manière semi-automatisée tous les IDEs de
            la documentation.

            * La page n'est créée que si l'option `{{config_validator("testing.include")}}`
            n'est pas à `#!yaml null`.
            * Une erreur est levée si un fichier du même nom existe déjà.
            * Une erreur est levée si le fichier n'est pas à la racine de la documentation.
        """,
        yaml_desc = "Name of the IDEs testing page. Generated only if given."
    ),
    ConfigOptionSrc(
        'include', str, conf_type=C.Choice(
            (PmtTests.null, PmtTests.serve, PmtTests.site), default=PmtTests.null
        ),
        docs=f"""
            Définit si la page de tests des IDEs doit être générée et de quelle façon.
            {'{{'}ul_li([
                "`#!py '{PmtTests.null}'` : la page de tests n'est pas générée.",
                "`#!py '{PmtTests.serve}'` : la page de tests est générée pendant `mkdocs
                serve`, et est ajoutée automatiquement à la navigation.",
                "`#!py '{PmtTests.site}'` : la page de tests est ajoutée sur le site construit,
                mais n'apparaît pas dans la navigation.",
            ]){'}}'}
        """,
        yaml_desc="""
            Define when and how to generate the page to tests all the IDEs of the documentation.
        """
    ),
    ConfigOptionSrc(
        'load_buttons', bool, is_optional=True,
        docs="""
            Définit si le bouton pour charger l'ensemble des codes associés à un IDE de la page
            des tests sera présent ou non.
            <br>Le comportement par défaut dépend de la valeur de l'option {{ config_link(
            'testing.include') }} :

            * Pour {{ config_validator("testing.include", val="serve") }}, le bouton est présent par défaut.
            * Pour {{ config_validator("testing.include", val="site") }}, le bouton est absent par défaut.
        """,
        yaml_desc = "Name of the IDEs testing page. Generated only if given."
    ),
    ConfigOptionSrc(
        'empty_section_fallback', str,
        conf_type = C.Choice(CASES_OPTIONS, default='skip'),
        docs="""
            Lorsque la page des tests des IDEs est construite et que la section à tester pour
            un IDE donné ne contient pas de code et que `{{config_validator("testing.empty_section_fallback", 1)}}`
            est définie, c'est cette "stratégie" qui sera utilisée à la place.
        """,
        yaml_desc = "Fallback behavior when the `section` normally tested is empty."
    ),

    ),
)







# Kept as archive, but not used anymore:

# OTHERS_CONFIG = SubConfigSrc(
#     '_others',
#     docs = "Réglages provenant de pyodide-mkdocs, mais qui ne sont plus utilisés.",
#     dep_status = DeprecationStatus.unsupported,
#     elements = (
#         ConfigOptionDeprecated('scripts_url', str),
#         ConfigOptionDeprecated('site_root',   str),
#     ),
# )
