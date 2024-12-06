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

from mkdocs.config import config_options as C

from pyodide_mkdocs_theme.pyodide_macros.tools_and_constants import (
    HtmlClass,
    IdeMode,
    IDE_MODES,
    P5_BTNS_LOCATIONS,
)
from pyodide_mkdocs_theme.pyodide_macros.parsing import items_comma_joiner

from ...tools.test_cases import CASES_OPTIONS
from ..config_option_src import ConfigOptionIdeLink, ConfigOptionSrc, VAR_ARGS
from ..sub_config_src import SubConfigSrc
from ..macro_config_src import MacroConfigSrc, MultiQcmConfigSrc

from .docs_dirs_config import (
    to_page,
    DOCS_CONFIG,
    DOCS_FIGURES,
    DOCS_IDE_DETAILS,
    DOCS_PY_BTNS,
    DOCS_RUN_MACRO,
    DOCS_QCMS,
    DOCS_RESUME,
    DOCS_TERMINALS,
)




OP,CLO = '{{', '}}'





PY_GLOBAL = SubConfigSrc.with_default_docs(
    to_page(DOCS_IDE_DETAILS) / '#IDE-{name}'
)(
    '', elements=(

    ConfigOptionIdeLink(
        'py_name', str, default="", index=0, in_yaml_docs=False,
        docs = """
            Chemin relatif (sans l'extension du fichier) vers le fichier `{exo}.py` et les
            éventuels autres fichiers annexes, sur lesquels baser l'IDE.
        """,
        yaml_desc="""
            Relative path (no extension) toward the `{exo}.py` file for an IDE, terminal, ...
        """
    ),
    ConfigOptionIdeLink(
        'ID', int, in_config=False, docs_type="None|int",
        docs = """
            À utiliser pour différencier deux IDEs utilisant les mêmes fichiers
            [{{annexes()}}](--ide-files), afin de différencier leurs sauvegardes
            (nota: $ID \\ge 0$).
        """,
        yaml_desc="Disambiguate different macro calls using the same underlying files."
    ),
    ConfigOptionIdeLink(
        'SANS', str, default="",
        docs="""
            Pour interdire des fonctions builtins, des méthodes ou des modules : chaîne de noms
            séparés par des virgules et/ou espaces.
        """,
        yaml_desc="""
            Used to forbid the use of builtins, methods or packages in the python code
            (space or comma separated identifiers).
        """
    ),
    ConfigOptionIdeLink(
        'WHITE', str, default="",
        docs="""
            (_\"White list\"_) Ensemble de noms de modules/packages à pré-importer avant que les
            interdictions ne soient mises en place (voir argument `SANS`. _L'argument `WHITE` est
            normalement {{ orange('**obsolète**') }}_).
        """,
        yaml_desc="""
            Names of packages to import automatically in the global scope (to avoid troubles with
            forbidden modules).
        """,
        # yaml_desc="""
        #     Noms de modules/packages à pré-importer avant que les interdictions ne soient mises
        #     en place.
        # """,
    ),
    ConfigOptionIdeLink(
        'REC_LIMIT', int, default=-1,
        docs="""
            Pour imposer une profondeur de récursion maximale. Nota: ne jamais descendre en-dessous
            de 20. La valeur par défaut, `#!py -1`, signifie que l'argument n'est pas utilisé.
        """,
        yaml_desc="Limit the recursion depth (do not use values below 20).",
        # yaml_desc="Limite de la profondeur de récursion (ne pas descendre en-dessous de 20).",
    ),
    ConfigOptionIdeLink(
        'MERMAID', bool, default=False,
        docs="""
            Signale qu'un rendu de graphe mermaid sera attendu à un moment ou un autre des
            exécutions.
            <br>Nota : l'extension markdown `pymdownx.superfences` doit être configurée pour
            accepter les blocs de code `mermaid`. Voir la configuration par défaut du mkdocs.yml
            via les scripts du thème, par exemple avec : `python -m pyodide_mkdocs_theme --yml`.
        """,
        yaml_desc="Mark a page as containing dynamic Mermaid graphs built during executions."
    ),
    ConfigOptionIdeLink(
        'AUTO_RUN', bool, default=False,
        docs="Lance automatiquement le code après avoir affiché la page.",
        yaml_desc="Run the python code on page load or not.",
    ),
))






def _py_globals_copy_gen(**replacements:ConfigOptionIdeLink):
    return (
        (arg if name not in replacements else replacements[name]).copy_with()
        for name,arg in PY_GLOBAL.subs_dct.items()
    )



MOST_LIKELY_USELESS_ID = PY_GLOBAL.ID.copy_with(docs="""
    À utiliser pour différencier deux appels de macros différents, dans le cas où vous tomberiez
    sur une collision d'id (très improbable, car des hachages sont utilisés. Cet argument ne
    devrait normalement pas être nécessaire pour cette macro).
""")

*PY_BTN_POSITIONAL, PY_BTN_MERMAID, PY_BTN_AUTO_RUN = (

    arg.copy_with(in_macros_docs=arg.name in ('py_name', 'ID', 'MERMAID'))

    for arg in _py_globals_copy_gen(
        ID = MOST_LIKELY_USELESS_ID,
        py_name = PY_GLOBAL.py_name.copy_with(docs="""
            Crée un bouton isolé utilisant le fichier python correspondant
            (uniquement `env` et `ignore`).
        """)
    )
)

# Ensure order is as expected...:
assert PY_BTN_MERMAID.name == 'MERMAID', "Wrong PY_GLOBAL elements order... (MERMAID)"
assert PY_BTN_AUTO_RUN.name == 'AUTO_RUN', "Wrong PY_GLOBAL elements order... (AUTO_RUN)"





#----------------------------------------------------------------------------------------





BS_MACRO = '" + back_slash() + "'
"""
The pretty well named... XD
Necessary to bypass jinja deprecation warning when using backslashes where it doesn't like it...
"""



IDE = MacroConfigSrc(
    'IDE',
    docs = "Valeurs par défaut pour les arguments des macros `IDE` et `IDEv`.",
    yaml_desc = "Default values for arguments used in the `IDE` and `IDEv` macros.",
    docs_page_url = to_page(DOCS_IDE_DETAILS),
    elements = (

    *_py_globals_copy_gen(
        AUTO_RUN = PY_GLOBAL.AUTO_RUN.copy_with(
            docs=PY_GLOBAL.AUTO_RUN.docs.rstrip('.')+" (lance uniquement les tests publics).")
    ),
    ConfigOptionIdeLink(
        'MAX', int, default=5, docs_type="int|'+'",
        docs="""
            Nombre maximal d'essais de validation avant de rendre la correction et/ou les
            remarques disponibles.
        """,
        yaml_desc="Maximum number of attempts before revealing correction and remarks.",
    ),
    ConfigOptionIdeLink(
        'LOGS', bool, default=True,
        docs="""
            {{ red('Durant des tests de validation') }}, si LOGS est `True`, le code complet
            d'une assertion est utilisé comme message d'erreur, quand l'assertion a été écrite
            sans message.
        """,
        yaml_desc = """
            Build or not missing assertion messages for failed assertions in the secret tests
        """,
        # yaml_desc="""
        #     Construit ou non les messages manquant pour les assertions échouées lors des
        #     validations.
        # """,
    ),
    ConfigOptionIdeLink(
        'MODE', str, is_optional=True,
        conf_type = C.Choice(IDE_MODES),
        docs_type='None|str',
        docs_default_as_type=True,
        line_feed_link=False,
        docs = f"""
            Change le mode d'exécution des codes python. Les modes disponibles sont :<br>
            { OP } ul_li([
                "`#!py None` : exécutions normales.",
                "`#!py {IdeMode.delayed_reveal!r}` : pour des IDEs n'ayant pas de tests (pas de
                section `tests` ni `secrets`) mais dont on ne veut pas que la solution s'affiche
                dès la première exécution (typiquement, des exercices turtle ou p5). Chaque
                validation fait décroître le nombre'essais et les solutions et remarques, si elles
                existent, sont révélées une fois tous les essais consommés (une erreur est levée
                durant le build, si l'IDE  a des sections `tests` ou `secrets`, ou s'il a un nombre
                d'essais infini).",
                "`#!py {IdeMode.no_reveal!r}` : exécutions normales, mais les solutions et
                remarques, si elles existent, ne sont jamais révélées, même en cas de succès.
                Le compteur d'essais est ${ BS_MACRO }infty$.",
                "`#!py {IdeMode.no_valid!r}` : quels que soient les fichiers/sections
                disponibles, le bouton et les raccourcis de validations sont inactifs.
                Le compteur d'essais est ${ BS_MACRO }infty$.",
                "`#!py {IdeMode.revealed!r}` : les solutions et remarques, si elles existent,
                sont révélées dès le chargement de la page.
                Le compteur d'essais est ${ BS_MACRO }infty$.",
            ]) { CLO }
        """,
        yaml_desc = f"""
            Change the execution  mode of an IDE (`{IdeMode.no_reveal!r}`, `{IdeMode.no_valid!r}`,
            by default: `null`).
        """,
        # yaml_desc = f"""
        #     Change le mode d'exécution de l'IDE (`{IdeMode.no_reveal!r}`, `{IdeMode.no_valid!r}`,
        #     `null` par défaut).
        # """,
    ),
    ConfigOptionIdeLink(
        'MIN_SIZE', int, default=3,
        docs = "Nombre de lignes minimal de l'éditeur.",
        yaml_desc = "Minimum number of lines of an editor.",
    ),
    ConfigOptionIdeLink(
        'MAX_SIZE', int, default=30,
        docs = "Impose la hauteur maximale possible pour un éditeur, en nombres de lignes.",
        yaml_desc = "Maximum number of lines of an editor.",
    ),
    ConfigOptionIdeLink(
        'TERM_H', int, default=10,
        docs = "Nombre de lignes initiales utilisées pour la hauteur du terminal (approximatif).",
        yaml_desc="Initial number of lines of a terminal (approximative).",
    ),
    ConfigOptionIdeLink(
        'TEST', str, conf_type=C.Choice(CASES_OPTIONS, default=''),
        docs = """
            Définit la façon dont l'IDE doit être géré lors des tests dans [la page générée
            automatiquement pour tester tous les IDEs de la documentation](--redactors/IDE-tests-page/).
            <br>{{ ul_li([
                "Depuis un fichier de configuration, un fichier" + meta() + " ou l'entête d'une page
                markdown : " + cases_options_as_yaml_str()+ ".",
                "Depuis un appel de macro: les mêmes, ou bien utiliser un object `Case`, défini dans
                l'environnement, pour plus de possibilités."
            ])}}
        """,
        yaml_desc = """
            Configuration to use when testing this IDE (more options through macro call arguments)
        """,
    ),
    ConfigOptionIdeLink(
        'TWO_COLS', bool, default=False,
        docs = """
            Si `True`, cet IDE pass automatiquement en mode "deux colonnes" au chargement de la page.
        """,
        yaml_desc="Automatically goes in split screen mode if `true`.",
    ),
    ConfigOptionIdeLink(
        'STD_KEY', str, default="",
        docs = """
            Clef à passer en argument de [`terminal_message`](--IDEs-terminal_message) pour
            autoriser son utilisation lorsque la sortie standard est désactivée pendant les
            tests.
        """,
        yaml_desc="""
            Key to pass as first argument of the `terminal_message` python function (in pyodide),
            to allow to print messages directly in the terminal of an IDE, when the stdout is
            deactivated.
        """,
    ),
    ConfigOptionIdeLink(
        'EXPORT', bool, default=False,
        docs = """
            Définis si le contenu de l'éditeur de cet IDE doit être ajouté à l'archive zip
            récupérant les codes de tous les IDEs de la page.
        """,
        yaml_desc="""
            Add the content of this editor to the zip archive, when extracting all the codes
            of the IDEs in the page.
        """,
    ),
))










TERMINAL = MacroConfigSrc.with_default_docs(
    to_page(DOCS_TERMINALS) / '#signature'
)(
    'terminal',
    docs = "Valeurs par défaut pour les arguments de la macro `terminal`.",
    yaml_desc = "Default values for arguments used in the `terminal` macro.",
    elements=(

    *_py_globals_copy_gen(
        ID = MOST_LIKELY_USELESS_ID,
        py_name = PY_GLOBAL.py_name.copy_with(docs="""
            Crée un terminal isolé utilisant le fichier python correspondant (sections
            autorisées: `env`, `env_term`, `post_term`, `post` et `ignore`).
        """)
    ),
    ConfigOptionIdeLink(
        'TERM_H', int, default=10,
        docs = "Nombre de lignes initiales utilisées pour la hauteur du terminal (approximatif).",
        yaml_desc="Initial number of lines of a terminal (approximative).",
    ),
    ConfigOptionSrc(
        'FILL', str, default='',
        docs = """
            Commande à afficher dans le terminal lors de sa création.
            <br>{{ red('Uniquement pour les terminaux isolés.') }}
        """,
        yaml_desc="Command used to prefill the terminal (isolated terminals only).",
        # yaml_desc="Commande pour préremplir le terminal (terminaux isolés uniquement).",
    ),
))










PY_BTN = MacroConfigSrc.with_default_docs(
    to_page(DOCS_PY_BTNS) / '#signature'
)(
    'py_btn',
    docs = "Valeurs par défaut pour les arguments de la macro `py_btn`.",
    yaml_desc = "Default values for arguments used in the `py_btn` macro.",
    elements=(

    *( arg.copy_with() for arg in PY_BTN_POSITIONAL ),
    ConfigOptionSrc(
        'ICON', str, default="",
        docs = """
            Par défaut, le bouton \"play\" des tests publics des IDE est utilisé.
            <br>Peut également être une icône `mkdocs-material`, une adresse vers une image
            (lien ou fichier), ou du code html.<br>Si un fichier est utiliser, l'adresse doit
            être relative au `docs_dir` du site construit.
        """,
        yaml_desc="Image of the button (by default: `play`  / file path / :icon-material: / url).",
        # yaml_desc="Image pour le bouton (`play` par défaut / fichier / :icon-material: / lien).",
    ),
    ConfigOptionSrc(
        'HEIGHT', int, is_optional=True, docs_type="None|int",
        docs = "Hauteur par défaut du bouton.",
        yaml_desc="Default height for the button",
    ),
    ConfigOptionSrc(
        'WIDTH', int, is_optional=True, docs_type="None|int",
        docs = "Largeur par défaut du bouton.",
        yaml_desc="Default width for the button",
    ),
    ConfigOptionSrc(
        'SIZE', int, is_optional=True, docs_type="None|int",
        docs = "Si définie, utilisée pour la largeur __et__ la hauteur du bouton.",
        yaml_desc="If given, define the height and the width for the button",
    ),
    ConfigOptionSrc(
        'TIP', str, lang_default_access='py_btn.msg',
        docs = "Message à utiliser pour l'info-bulle.",
        yaml_desc="Tooltip message",
    ),
    ConfigOptionSrc(
        'TIP_SHIFT', int, default=50,
        docs = """
            Décalage horizontal de l'info-bulle par rapport au bouton, en `%` (c'est le
            décalage vers la gauche de l'info-bulle par rapport au point d'ancrage de
            la flèche au-dessus de celle-ci. `50%` correspond à un centrage).
        """,
        yaml_desc="Horizontal leftward shifting of the tooltip (%)",
        # yaml_desc="Décalage horizontal de l'info-bulle vers la gauche (%)",
    ),
    ConfigOptionSrc(
        'TIP_WIDTH', float, default=0.0,
        docs = "Largeur de l'info-bulle, en `em` (`#!py 0` correspond à une largeur automatique).",
        yaml_desc="Tooltip width (in em units. Use `0` for automatic width)",
    ),
    ConfigOptionSrc(
        'WRAPPER', str, default='div',
        docs = "Type de balise dans laquelle mettre le bouton.",
        yaml_desc = "Tag type the button will be inserted into",
    ),
    PY_BTN_MERMAID.copy_with(),
    PY_BTN_AUTO_RUN.copy_with(),
))











AUTO_RUN = MacroConfigSrc.with_default_docs(
    to_page(DOCS_RUN_MACRO) / '#signature'
)(
    'run',
    docs      = "Valeurs par défaut pour les arguments de la macro `run`.",
    yaml_desc = "Default values for arguments used in the `run` macro.",
    elements  = tuple(
        arg if arg.name!='py_name' else arg.copy_with(docs="""
            Chemin relatif vers le fichier python (sans extension) à exécuter au chargement de
            la page (section `env` uniquement).
        """)
        for arg in (*PY_BTN_POSITIONAL, PY_BTN_MERMAID)
    ),
)








SECTION = MacroConfigSrc.with_default_docs(
    to_page(DOCS_RESUME) / '#section'
)(
    'section',
    docs = "Valeurs par défaut pour les arguments de la macro `terminal`.",
    yaml_desc = "Default values for arguments used in the `section` macro.",
    in_yaml_docs = False,
    elements = (

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    PY_GLOBAL.py_name.copy_with(
        docs="[Fichier python {{ annexe() }}](--ide-files).",
    ),
    ConfigOptionSrc(
        'section', str, index=1, is_optional=True,
        docs = "Nom de la section à extraire.",
        yaml_desc="Name of the section to extract.",
    ),
))








PY = MacroConfigSrc.with_default_docs(
    to_page(DOCS_RESUME) / '#py'
)(
    'py',
    docs = "Valeurs par défaut pour les arguments de la macro `py`.",
    yaml_desc = "Default values for arguments used in the `py` macro.",
    in_yaml_docs = False,
    elements = (

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    ConfigOptionSrc(
        'py_name', str, is_optional=True, index=0,
        docs = "Fichier source à utiliser (sans l'extension).",
        yaml_desc="Relative path, but without extension, of the python file to use.",
    ),
))








MULTI_QCM = MultiQcmConfigSrc.with_default_docs(
    to_page(DOCS_QCMS) / '#arguments'
)(
    'multi_qcm',
    docs = "Valeurs par défaut pour les arguments de la macro `multi_qcm`.",
    yaml_desc = "Default values for arguments used in the `multi_qcm` macro.",
    elements = (

    # Required on the python side, but should never be given through "meta": must not be blocking:
    ConfigOptionSrc(
        'questions', list, index=VAR_ARGS, in_config=False, docs_default_as_type=False,
        docs = """
            Chaque argument individuel est une [liste décrivant une question avec ses choix
            et réponses](--qcm_question).
            <br>Il est également possible de passer en unique argument un [chemin relatif vers un
            fichier `.json`](--qcms-json) comportant une configuration complète (ou partielle) pour
            déclarer un `multi_qcm`.
        """,
        yaml_desc = """
            Varags: each element is a list representing the data for one question (3 or 4 elements),
            or use one single relative path to a `.json` file.
        """,
    ),
    ConfigOptionSrc(
        'description', str, default='',
        docs = """
            Texte d'introduction (markdown) d'un QCM, ajouté au début de l'admonition, avant
            la première question. Cet argument est optionnel.
        """,
        yaml_desc="Introduction text at the beginning of the quiz admonition.",
        # yaml_desc="Texte d'introduction au début de l'admonition du QCM.",
    ),
    ConfigOptionSrc(
        'hide', bool, default=False,
        docs = """
            Si `#!py True`, un masque apparaît au-dessus des boutons pour signaler à l'utilisateur
            que les réponses resteront cachées après validation.
        """,
        yaml_desc = """
            Indicates whether correct/incorrect answers are visible or not after validation.
        """,
        # yaml_desc="Indique si les réponses correctes/incorrects sont visibles à la correction.",
    ),
    ConfigOptionSrc(
        'multi', bool, default=False,
        docs = """
            Réglage pour toutes les questions du qcm ayant une seule bonne réponse, indiquant si
            elles doivent être considérées comme étant à choix simple ou multiples.
        """,
        yaml_desc="Disambiguate MCQ and SCQ if not automatically decidable.",
        # yaml_desc="Permet de clarifier entre QCM et QCU quand ambiguë.",
    ),
    ConfigOptionSrc(
        'shuffle', bool, default=False,
        docs = "Mélange les questions et leurs choix ou pas, à chaque fois que le qcm est joué.",
        yaml_desc="Shuffle questions and their items or not.",
    ),
    ConfigOptionSrc(
        'shuffle_questions', bool, default=False,
        docs = "Mélange les questions uniquement, à chaque fois que le qcm est joué.",
        yaml_desc="Shuffling or not, questions only.",
    ),
    ConfigOptionSrc(
        'shuffle_items', bool, default=False,
        docs="Mélange seulement les items de chaque question, à chaque fois que le qcm est joué.",
        yaml_desc="Shuffling the items of each question or not.",
    ),
    ConfigOptionSrc(
        'admo_kind', str, conf_type=C.Choice(('!!!', '???', '???+', None), default="!!!"),
        docs = """
            Type d'admonition dans laquelle les questions seront rassemblées :{{ul_li([
                "`#!py '!!!'` : classique,",
                "`#!py '???'` : dépliable,",
                "`#!py '???+'` : repliable,",
                "`None` : pas d'admonition autour du qcm."
            ])}} `None` permet d'ajouter du contenu markdown autour du qcm de manière plus
            fine, si besoin.{{pmt_note("À noter que l'admonition restera visible dans le markdown généré
            par la macro : elle sera supprimée dans la couche JS, au moment de l'affichage de
            la page html")}}.
        """,
        yaml_desc="Type of the admonition wrapping the whole MCQ (`!!!`, ...).",
        # yaml_desc="Type d'admonition pour le QCM complet (`!!!`, ...).",
    ),
    ConfigOptionSrc(
        'admo_class', str, default="tip",
        docs = """
            Pour changer la classe d'admonition. Il est également possible d'ajouter d'autres
            classes si besoin, en les séparant par des espaces (exemple : `#!py 'tip inline end
            my-class'`).
        """,
        yaml_desc="Html class(es) for the admonition wrapping the whole MCQ (default: `tip`).",
        # yaml_desc="Classe(s) utilisée(s) pour l'admonition du QCM complet (défaut: `tip`).",
    ),
    ConfigOptionSrc(
        'qcm_title', str, lang_default_access="qcm_title.msg",
        docs = "Pour changer le titre de l'admonition.",
        yaml_desc="Override the default title of the MCQ admonition.",
    ),
    ConfigOptionSrc(
        'tag_list_of_qs', str, conf_type=C.Choice(('ul', 'ol')), is_optional=True,
        docs = """
            {{ ul_li([
                '`#!py None` : automatique (défaut).',
                '`#!py "ol"` : questions numérotées.',
                '`#!py "ul"` : questions avec puces.',
            ]) }}
            Définit le type de liste html utilisée pour construire les questions.
            <br>Si la valeur est `None`, '`#!py "ol"` est utilisé, sauf s'il n'y a qu'une
            seule question pour le qcm, où c'est alors `#!py "ul"` qui est utilisé.
        """,
        yaml_desc="Enforce the list tag used to build the questions in a MCQ.",
    ),
    ConfigOptionSrc(
        'DEBUG', bool, default=False,
        docs = "Si `True`, affiche dans la console le code markdown généré pour ce qcm.",
        yaml_desc="""
            If `True`, the generated markdown of the MCQ will be printed to the console
            during mkdocs build.
        """,
    ),
))









FIGURE = MacroConfigSrc.with_default_docs(
    to_page(DOCS_FIGURES) / '#signature'
)(
    'figure',
    docs = "Valeurs par défaut pour les arguments de la macro `figure`.",
    yaml_desc = "Default values for arguments used in the `figure` macro.",
    elements = (

    # Required on the python side, but should never be given through "meta": must not be blocking:
    ConfigOptionSrc(
        'div_id', str, default="figure1", index=0,
        docs = """
            Id html de la div qui accueillera la figure ou l'élément inséré dynamiquement.
            <br>À modifier s'il y a plusieurs figures insérées dans la même page.
        """,
        yaml_desc="""
            Html id of the `div` tag that will hold the dynamically generated figure
            (default: `\"figure1\"`).
        """,
    ),
    ConfigOptionSrc(
        'div_class', str, default=HtmlClass.py_mk_figure,
        docs = """
            Classe html à donner à la div qui accueillera la figure.<br>Il est possible d'en
            changer ou d'en mettre plusieurs, selon les besoins. Il est aussi possible de
            surcharger les règles css de la classe par défaut, pour obtenir l'affichage voulu.
        """,
        yaml_desc="Html class of  `div` tag that will hold the dynamically generated figure.",
        # yaml_desc="Classe html à donner à la div qui accueillera la figure.",
    ),
    ConfigOptionSrc(
        'inner_text', str, lang_default_access="figure_text.msg",
        docs = "Texte qui sera affiché avant qu'une figure ne soit tracée.",
        yaml_desc="Text used as placeholder before any figure is inserted.",
    ),
    ConfigOptionSrc(
        'admo_kind', str, default="!!!",
        docs = """
            Type d'admonition dans laquelle la figure sera affichée (`'???'` et `'???+'`
            sont également utilisables).
            <br>Si `admo_kind` est `''`, la `<div>` sera ajoutée sans admonition, et les
            arguments suivants seront alors ignorés.
        """,
        yaml_desc="Type of the admonition wrapping the generated figure (`!!!`, ...).",
        # yaml_desc="Type d'admonition pour la figure (`!!!`, ...).",
    ),
    ConfigOptionSrc(
        'admo_class', str, default="tip",
        docs = """
            Pour changer la classe d'admonition. Il est également possible d'ajouter d'autres
            classes si besoin, en les séparant par des espaces (exemple : `#!py 'tip inline end
            my-class'`).
        """,
        yaml_desc = """
            Html class(es) of the admonition wrapping the generated figure (default: `tip`).
        """,
        # yaml_desc="Classe(s) utilisée(s) pour l'admonition de la figure (défaut: `tip`)."
    ),
    ConfigOptionSrc(
        'admo_title', str, lang_default_access="figure_admo_title.msg",
        docs = "Pour changer le titre de l'admonition.",
        yaml_desc="Admonition title.",
    ),
    ConfigOptionSrc(
        'p5_buttons', str, conf_type=C.Choice(P5_BTNS_LOCATIONS), is_optional=True,
        docs = f"""
            Si défini, ajoute les boutons start/step/stop pour gérer les animations construites avec
            [p5](--p5_processing/how_to/).
            <br>Les boutons sont ajoutés sur le côté indiqué du canevas, les valeurs possibles étant
            { items_comma_joiner(['`#!py "'+loc+'"`' for loc in P5_BTNS_LOCATIONS]) }.
        """,
        yaml_desc="""
            Add start, step and stop buttons for p5 animations, on the given side of the canvas.
        """,
    ),
))






ARGS_MACRO_CONFIG = SubConfigSrc(
    'args',
    docs_page_url = to_page(DOCS_CONFIG) / '#{py_macros_path}',
    docs = """
        Réglages des arguments par défaut accessibles pour les différentes macros du thème.
        Explications détaillées dans la page [Aide rédacteurs/Résumé](--redactors/resume/).
    """,
    yaml_desc = """
        Configurations of default values for arguments used in `PyodideMacrosPlugin` macros.
    """,
    # yaml_desc = "Configurations des arguments par défaut pour les différentes macros du thème.",
     elements = (
        IDE,
        TERMINAL,
        PY_BTN,
        AUTO_RUN,
        SECTION,
        MULTI_QCM,
        PY,
        FIGURE,
     )
)
