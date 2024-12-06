/*
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
*/






/**To access CONFIG data from pyodide (mermaid, cutFeedback, ...).
 * */
function config(){ return CONFIG }


const pyodideFeatureCode=(()=>{

    const PYODIDE_SNIPPETS = {

    autoRunCleaner: `__builtins__.auto_run.clean()`,

    autoRun: `
def _hack_auto_run():

    G = globals()

    class AutoRunner:
        run = set()
        def __call__(self, func):
            func()
            self.run.add(func.__name__)     # Skips registration if failure in func
        def clean(self):
            for k in self.run:
                if k in G: del G[k]
            self.run.clear()
        def __repr__(self):
            return "AutoRunner()"

    # Keep uncleaned elements:
    runner = AutoRunner()
    if hasattr(__builtins__, 'auto_run'):
        runner.run |= __builtins__.auto_run.run
    __builtins__.auto_run = runner


    def as_builtin(name_or_func):
        """
        Automatically add the decorated function in the builtins module. Usage:

        \`\`\`python
        @as_builtin
        def func(...): pass     # declare __builtins__.func

        @as_builtin("actual_name")
        def func(...): pass     # declare __builtins__.actual_name = func
        \`\`\`
        """

        if not isinstance(name_or_func, str):
            return as_builtin(name_or_func.__name__)(name_or_func)
        return lambda func: setattr(__builtins__, name_or_func, func) or func


    __builtins__.as_builtin = as_builtin


    @as_builtin
    def wraps_builtin(
        *args,
        source=None,
        store=True,
        name="",
    ):
        """
        Build a singleton object that mimics as much as possible an original builtin,
        defining repr, str, dir, __name__ and __qualname__ behaviors of the builtin function.
        Can also be used with user defined functions, to get a custom \`repr\` value which
        doesn't show some horrible \`<function _hack_xxx.<locals>.some_func>\` to the user
        when printed in the terminal.

        \`type\` and \`help\` give slightly different behaviors:
            * \`type(func)\` is showing the BuiltinWrapperXxx name
            * \`help(func)\` is showing the original docstring of func if defined, or the builtin's
               help message, wrapped inside the BuiltinWrapperXxx class layout

        @source:        The function to "mimic". Generally a builtin, but might be any function
                        that needs to have custom str and repr behaviors.
        @store=True:    If True, added to __builtins__ with builtin.__name__ as property name.
        """

        def wrapper(func):

            builtin_src = f"__{ func.__name__ }_src__"
            is_builtin  = hasattr(__builtins__, builtin_src)

            if is_builtin:
                src       = source or getattr(__builtins__, f"__{ func.__name__ }_src__")
                func_name = name or getattr(src, '__name__', func.__name__)
            else:
                src       = source or func
                func_name = name or getattr(src, '__name__', func.__name__)


            class BuiltinWrapper:

                def __init__(self):
                    self.func = func
                    self.__name__ = self.__qualname__ = func_name

                    # Keep any already defined docstring:
                    self.__class__.__doc__ = func.__doc__ or source and source.__doc__

                def __call__(self, *a,**kw):  return self.func(*a,**kw)
                def __dir__(self):            return dir(src)
                def __repr__(self):
                    if is_builtin and func_name!='help':
                        return repr(src)
                    return f"<function {func_name}>"

            kls_name = "BuiltinWrapper" + func_name.capitalize()
            BuiltinWrapper.__name__ = BuiltinWrapper.__qualname__ = kls_name

            wrapped = BuiltinWrapper()
            if store:
                as_builtin(func_name)(wrapped)
            return wrapped


        if len(args)>1 or args and (not callable(args[0]) or source or name):
            raise ValueError(
                "Invalid call for @wraps_builtin: shouldn't be used with positional arguments,"
                " unless it's the function to wrap."
            )
        return wrapper(args[0]) if args else wrapper

_hack_auto_run()
del _hack_auto_run
`,


    version: `
def version():
    """ Print to the console the current version number of pyodide-mkdocs-theme. """
    print("pyodide-mkdocs-theme v${ CONFIG.version }")
`,


    localStorageRelays: `
@auto_run
def _hack_local_storage_routines():
    import js

    for prop in 'get set del'.split():
        routine = getattr(js, prop+'Storage')
        as_builtin(prop+'_storage')(routine)

    @as_builtin
    def keys_storage():
        return js.keysStorage().to_py()
`,


    ioStuff: `
@auto_run
def _hack_io_stuff():

    import js, re
    from pydoc import render_doc
    from typing import Any

    @wraps_builtin
    def input(question:str="", beginning:str=""):
        question = question or ""           # Original is using None so, just in case...
        result = js.prompt(f"{ beginning }{ question }")
        print(f"{ question }{ result }")    # Must ensure string conversion of result
        return result


    @wraps_builtin
    def help(object_or_function):
        """
        Replace the original help function, which doesn't work as expected within pyodide.
        """

        class_name = getattr(type(object_or_function), '__name__', '')
        prefix     = 'BuiltinWrapper'
        if class_name.startswith(prefix):
            func_name = class_name[len(prefix):].lower()
            if func_name == 'help':
                object_or_function = object_or_function.func
            else:
                src_name = f"__{ func_name }_src__"
                object_or_function    = getattr(__builtins__, src_name, None) or object_or_function.func

        doc = render_doc(object_or_function)
        print(re.sub(r"\x08.", "", doc))



    @wraps_builtin
    def terminal_message(key, msg:Any, *_:Any, format:str="none", new_line=True, **__):
        """
        Display the given message directly into the terminal, without using the python stdout.
        This allows to give informations to the user even if the stdout is deactivated during
        a validation.

        @key:    Value to pass to allow the use of the function when the stdout is deactivated.
        @msg:    The message to display. Can be a multiline string.
        @format: The name of one of the predefined formatting for the terminal:
                 "error", "warning", "info", "italic", "stress", "success", "none" (default)
        @new_line: if False, no new line character is added after the @msg content.
        """
        # _ and __ are used as sinks for use of terminal_message as a replacement for print in
        # p5 codes converted from Basthon.
        # This is also the reason why the automatic conversion to string + join has been added.
        # Use of end=... is just ignored.
        # NOTE: keep these info outside of PMT public documentation...

        msg = __.get('sep',' ').join(map(str, (msg, *_)))
        try:
            js.config().termMessage(key, msg, format, False, new_line)
        except Exception as e:
            raise ValueError(str(e)) from None
`,


    copyFromServer: `
@auto_run
def _hack_copy_from_server():

    @as_builtin
    async def copy_from_server(
        src: str,
        dest: str = ".",
        name: str = "",
    ):
        from pyodide.http import pyfetch
        from pathlib import Path
        from urllib.error import URLError



        response = await pyfetch(src)
        if not response.ok:
            raise URLError(f"Failed request for { src }.")

        content  = await response.bytes()
        target   = Path(dest) / (name or Path(src).name)
            # Note: Path(src).name works to extract the name file on urls, but the path
            #       is actually invalid as an url: "http://xx" givers "http:/xx".
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
`,


    exclusionsTools: `
@auto_run
def _hack_exclusions_tools():

    type = __builtins__.type      # avoid restrictions troubles

    @wraps_builtin
    def __move_forward__(x):
        treasure = __builtins__.__builtins___
        if type(x) is str and x in treasure:
            return treasure[x][0]

    @as_builtin
    class ExclusionError(Exception):
        @staticmethod
        def throw(that:str):
            raise ExclusionError(f"${ CONFIG.MSG.exclusionMarker }: don't use {that}")
`,


    refresher: `
@auto_run
def _hack_scope_cleaner():

    # Avoid restrictions troubles:
    set = __builtins__.set
    globals = __builtins__.globals

    @wraps_builtin
    def clear_scope(keep=()):
        """
        Remove any new function or variable from the global scope, keeping only:

        - Variables and functions that were defined after the start of the environment.
        - Elements present in the @keep argument (Iterable).
        """
        keeper = set(keep) | {
            '__name__', '__doc__', '__package__', '__loader__', '__spec__',
            '__annotations__', '__builtins__', '_pyodide_core', 'version'
        }
        g_dct = globals()
        for k in set(g_dct) - keeper:
            del g_dct[k]
`,

    clearScope: `clear_scope()`,


    wantedImports: `
@auto_run
def _hack_find_imports():
    from pyodide.code import find_imports
    __builtins__.imported_modules = find_imports({FORMAT_TOKEN})

__builtins__.imported_modules
`,


    alreadyImported: `
@auto_run
def _hack_imported():
    import sys
    __builtins__.loaded_modules = " ".join(sys.modules.keys())

__builtins__.loaded_modules
`,


    upDownLoader: `
@auto_run
def _hack_uploader_downloader():

    import js
    from pyodide.ffi import create_proxy
    from typing import Callable, Any, Literal
    from argparse import Namespace


    class ReadAs(Namespace):
        txt = 'readAsText'
        bytes = 'readAsArrayBuffer'
        img = 'readAsDataURL'

        @classmethod
        def get_props(cls):
            return ', '.join(
                repr(p) for p in dir[cls] if not p.startswith('_') and p != 'get_props'
            )


    def wrapping(
        cbk: Callable[[str],Any],
        *,
        read_as: Literal["txt","bytes","img"] = 'txt',
        with_name:bool = False,
        multi:bool = False,
    ):
        read_method = getattr(ReadAs, read_as, None)
        if not read_method:
            raise ValueError(
                f"Invalid read_as argument: {read_as!r}. Available options are: {ReadAs.get_props()}"
            )

        def wrapper(content:str, filename:str, is_last:bool):

            if read_method == ReadAs.bytes:
                content = bytes(js.Uint8Array.new(content))

            args = (content, filename) if with_name else (content,)
            out.append(cbk(*args))

            if is_last:
                proxy_cbk.destroy()

        proxy_cbk = create_proxy(wrapper)    # Does NOT work when using pyodide.ffi.create_once_callable
        out = []

        return (proxy_cbk, read_method, multi), lambda: out


    @as_builtin
    async def pyodide_uploader_async(*args, **kw) -> Any :
        js_args, out_getter = wrapping(*args, **kw)
        await js.uploaderAsync(*js_args)
        out = out_getter()
        if kw.get('multi'):
            return tuple(out)
        return out.pop() if out else None

    @as_builtin
    def pyodide_uploader(*args, **kw) -> None :
        js_args, _ = wrapping(*args, **kw)
        js.uploader(*js_args)


    @as_builtin
    def pyodide_downloader(content:str|bytes|list[int], filename:str, type="text/plain"):
        if not isinstance(content, str):
            content = js.Uint8Array.new(content)
        js.downloader(content, filename, type)
`,


    // GENERATED (modify the root project file instead)
    pyodidePlot: `
@auto_run
def _hack_plot():
    # THIS IS A PLOT TOKEN

    import matplotlib
    import matplotlib.pyplot as plt
    from typing import Callable, Sequence


    import js
    matplotlib.use("module://matplotlib_pyodide.html5_canvas_backend")


    class PyodidePlot:
        """
        Helper class, to draw figures from pyodide runtime, into a specified html element.
        If no argument is provided, the default \`div_id\` is used (arguments configuration of
        the plugin).

        \`\`\`python
        import matplotlib.pyplot as plt
        PyodidePlot().target()

        plt.plot(xs, ys, ...)
        plt.title("...")
        plt.show()
        \`\`\`

        ---

        In case you want to target more than one figure in the same page, pass the html id of the
        div tag to target to the \`PyodidePlot\` constructor:

        \`\`\`python
        fig1 = PyodidePlot("figure_id1")
        fig2 = PyodidePlot("figure_id2")

        fig1.target()       # Draw in "figure_id1"
        plt.plot(...)

        fig2.target()       # Draw in "figure_id2"
        plt.plot(...)
        \`\`\`

        ---
        """

        def __init__(self, div_id:str=''):
            self.div_id = div_id or js.config().argsFigureDivId

        def __getattr__(self, prop:str):
            return getattr(plt, prop)


        def target(self, keep_fig=False):
            """
            Close any previously created figure, then setup the current run to draw in
            the div tag targeted by the current instance.
            If keep_fig is set to True, the automatic \`Figure N\` will be kept, above the
            drawn figure.
            """
            for _ in plt.get_fignums():
                plt.close()
            div = js.document.getElementById(self.div_id)
            js.document.pyodideMplTarget = div
            div.textContent = ""
            if not keep_fig:
                plt.gcf().canvas.manager.set_window_title('')
            return plt

        refresh = target        # backward compatibility



        def plot_func(
            self,
            func:Callable,
            rng:Sequence,
            fmt:str=None,
            title:str=None,
            *,
            show:bool=True,
            keep_figure_num: bool = False,
            **kw
        ):
            """
            Draw an automatic graph for the given function on the given range, then "show"
            automatically the resulting graph in the correct figure element in the page.

            Arguments:
                func:  Callable, func(x) -> y
                rng:   Sequence of xs
                fmt:   Curve formatting (just like \`pyplot.plot\`)
                title: If given, will be added as title of the graph.
                show:  Call \`pyplot.show()\` only if \`True\`. This allows to customize the graph
                       before applying show manually.
                keep_figure_num: if False (by default), the \`Figure N\` above the drawing is
                       automatically removed.

            """
            self.target(keep_figure_num)

            xs = list(rng)
            ys = [*map(func, rng)]
            args = (xs,ys) if fmt is None else (xs,ys,fmt)
            out = plt.plot(*args, **kw)

            if title:
                plt.title(title)
            if show:
                plt.show()
            return out



        def plot(self, *args, keep_figure_num:bool=False, **kw):
            """
            Generic interface, strictly equivalent to \`pyplot.plot\`, except the \`PyodidePlot\`
            instance will automatically apply the drawing to the desired html element it is
            related to.

            _Use specifically this method to "plot"_ ! You then can rely on \`pyplot\` to finalize
            the figure as you prefer.
            """
            self.target(keep_figure_num)
            out = plt.plot(*args, **kw)
            return out



# THIS IS A PLOT TOKEN
    __builtins__.PyodidePlot = PyodidePlot      # don't use the decorator because auto-updated code
`,


    mermaidDrawer: `
@auto_run
def _hack_mermaid():
    import js

    @as_builtin
    def mermaid_figure(div_id:str=None):
        """
        Create a Callable[[str],None] that will draw the given mermaid code into the wanted figure div.
        """
        div_id = div_id or js.config().argsFigureDivId

        def to_mermaid(code:str, debug=False):
            if debug: print(code)
            code = f'<pre class="mermaid">{ code }</pre>'
            js.document.getElementById(div_id).innerHTML = code

        return to_mermaid

    try:
        if js.config().needMermaid:
            js.mermaid

        else:
            @as_builtin
            def mermaid_figure(*_,**__):
                raise ValueError(
                     "The function mermaid_figure cannot be used because there is no mermaid "
                    +"registration in the page.\\nDon't forget to mark the markdown page "
                    +"by using the argument 'MERMAID=True' in one of the macros (IDE, IDEv, "
                    +"terminal or py_btn)"
                )
    except:
        raise ValueError(
            "Cannot create mermaid logistic: the js mermaid object doesn't exist."
            +"\\nDon't forget to mark the markdown page by using the argument "
            +"'MERMAID=True' in one of the macros (IDE, IDEv, terminal or py_btn)"
        )
`,


    setupStdIO: `
@auto_run
def _hack_stdout_up():
    import sys, io, js

    @wraps_builtin
    def print(*a,**kw):     # Note: wraps doesn't seem to work... Dunno why...)

        # First, blindly print to the actual stdout (in case the author is using it)
        __print_src__(*a,**kw)

        # Then print to the one used to get proper formatting, but with a "per call" logic:
        kw['file'] = per_call_stdout
        __print_src__(*a,**kw)

        # Extract the stuff to transfer to the terminal, then empty per_call_stdout:
        txt_to_term = per_call_stdout.getvalue()
        per_call_stdout.truncate(0)
        per_call_stdout.seek(0)

        js.config().termMessage(None, txt_to_term, 'none', True)


    # Different object allowing to spot what to print exactly, for one single call to print:
    __builtins__.per_call_std_out = per_call_stdout = io.StringIO()

    # For backward compatibility, keep a StringIO object there (this also allow to enforce a flush
    # of the stdout content in between runs/sections, on user's side!)
    # NOTE: users wanting to test against the user stdout WILL USE THIS!
    __builtins__.src_stdout = sys.stdout
    sys.stdout = io.StringIO()
`,


    getFullStdIO:`
@__builtins__.auto_run
def _hack_stdout_down():
    import sys

    # Store to send the result to JS layer at the end:
    __builtins__._stdout_value = sys.stdout.getvalue()

    sys.stdout.close()
    sys.stdout = __builtins__.src_stdout
    del __builtins__.src_stdout

    __builtins__.per_call_std_out.close()
    __builtins__.print = __builtins__.__print_src__

__builtins__._stdout_value
`,
    }

    return (option, repl=null)=>{
        jsLogger('[CheckPoint] - Pyodide feature:', option)
        let code = PYODIDE_SNIPPETS[option]
        if(code===undefined) throw new Error(`Unknown snippet: ${option}`)
        if(repl!==null){
            code = code.replace(/\{FORMAT_TOKEN\}/g, JSON.stringify(repl))
        }
        return code+"\n"
    }
})()








/*
------------------------------------------------------------------
          Manage python stdout redirection in terminal
------------------------------------------------------------------
*/


const pyodideFeatureRunCode=(name, repl=null)=>{
    const code = pyodideFeatureCode(name, repl)
    return pyodide.runPython(code)
}


/**Use a StringIO stdout, so that the full content can be extracted later.
 * */
const setupStdIO =_=>{
    pyodideFeatureRunCode('autoRun')
    pyodideFeatureRunCode('setupStdIO')
}

const getFullStdIO =_=>{
    const stdout = pyodideFeatureRunCode('getFullStdIO') || ''
    return escapeSquareBrackets(stdout)
}

const clearPyodideScope=()=>{
    pyodideFeatureRunCode('autoRun')
    pyodideFeatureRunCode('refresher')
    pyodideFeatureRunCode('clearScope')
}






/*
------------------------------------------------------------------
                      Manage code exclusions
------------------------------------------------------------------
*/


/**Put in place code exclusions. Are handled:
 *   - builtin function calls
 *   - imports
 *   - method calls (done through a simple string check in the code, in runPythonCodeWithOptionsIfNoStdErr)
 *
 *
 * ## RATIONALS:
 *
 * To forbid the use of some functions or packages, replace them in the global scope by "functions"
 * that look "more or less the same", but will raise an error when called, or when used in the
 * wrong way (imports).
 *
 *
 * ## PROBLEMS & CONTEXT:
 *
 * 1. Pyodide itself uses various functions to run python code:
 *      - eval is used in pyodide.runPython
 *      - reversed and/or min and/or max may be used when building a stacktrace when an error is
 *        thrown in python
 * 2. This forbids to replace the __builtins__ versions of those functions (see about imports)...
 * 3. ...but the __main__ script is run separately of pyodide actual "python runtime".
 *
 *
 * ## SOLUTION FOR BUILTINS FUNCTIONS:
 *
 * - Redeclare forbidden things in the global scope, through `globals()`, using an object that
 *   will systematically throw an ExclusionError when it's called.
 * - Since those are in the global scope, they are visible through `dir()`, so add some make up
 *   to them, using a class that redefines its __qualname__ and __repr__, so that they are less
 *   obvious as "anti-cheats" (it will still remain obvious for those who know enough. But if they
 *   can find about that, they probably could solve the problem the right way anyway...).
 * - Pyodide runtime won't see those globals, so it is not affected in any way, only the user's
 *   and tester's codes are.
 * - The (hidden) function `__move_forward__('builtin_name')` (see documentation) can be used in
 *   the tests to get back the original builtin. If used, it must be done inside a closure, so
 *   that the original builtin doesn't override the "Raiser" in the global scope (see below).
 * - Since the hacked versions are available to the user in the global runtime, they could just
 *   delete them to get back the access to the original builtins. To limit this risk, an extra
 *   check is done after the user's code and tests has been run, verifying that the hacked
 *   functions are still defined in the global scope, and that they still are the original
 *   Raiser objects.
 *
 *
 * ## SOLUTION FOR IMPORTS
 *
 * The problem with `import` is that they actually go directly through `__builtins__.__import__`.
 * So in that case, there is no other choice than hacking directly the builtin, and then put it
 * back in place when not useful anymore.
 *
 *
 * ## RECURSION LIMIT
 *
 * The sys module function is directly hacked, then put back in place: meaning, the function
 * setrecursionlimit is also replaced at user's runtime with a Raiser object.
 *
 * */
const setupExclusions =(excluded, recLimit)=>{
    // Store None in the __builtins___ dict for things that aren't builtin functions, aka, names
    // of forbidden module.

    /** WARNING!
     *  Keep in mind that the code of the Raiser instances will run "in context".
     *  This means it will be subject to existing exclusions, so it must never use a function that
     *  could be forbidden. Possibly...
     *  For this reason, copies of all the builtins used in the Raiser code are stored locally, to
     *  be sure the Raiser won't use Raiser instances... XD
     * */
    const code = `
    @__builtins__.auto_run
    def _hack_exclusions_setup():

        class Raiser:
            __name__ = __qualname__ = 'function'

            def __init__(self, key):  self.key = key

            def __repr__(self): return f"<built-in function {self.key}>"

            def __call__(self, *a, **kw):
                key = self.key

                head = a and base_isinstance(a[0],base_str) and a[0].split(".")[0]

                is_forbidden = (
                    key != '__import__' or
                    key == '__import__' and head in dct
                )
                if is_forbidden:
                    that = key if key!='__import__' else head
                    ExclusionError.throw(that)

                # if reaching this point, the call is a valid import, so apply it:
                return base_import(*a,**kw)


        # Store the originals used here to avoid troubles with exclusions at runtime:
        base_import = __import__
        base_str = str
        base_isinstance = isinstance


        dct = __builtins__.__builtins___ = {}
        raiser_import = Raiser('__import__')
        dct['__import__'] = [base_import, raiser_import]
        __builtins__.__import__ = raiser_import


        glob_dct = globals()
        exclusions = ${ JSON.stringify(excluded) }
        for key in exclusions:
            stuff = getattr(__builtins__, key, None)
            dct[key] = [stuff, None]
            # => the dict will store [None,None] for module names

        if ${ recLimit } != -1:
            import sys
            sys.setrecursionlimit(${ recLimit })
            dct['setrecursionlimit'] = [sys.setrecursionlimit, None]

        for key,lst in dct.items():
            stuff = lst[0]
            if callable(stuff) and key!='__import__':       # import has already been handled
                # Store the reference of the raiser in lst, to check against it later:
                glob_dct[key] = lst[1] = Raiser(key)

        # auto_run added for verification purpose only, but it must stay usable:
        dct['auto_run'] = auto_run
`
    pyodide.runPython(code)
}



/**Cancel the code exclusions (done as soon as possible, to restore pyodide's normal behaviors).
 * */
const restoreOriginalFunctions = exclusions =>{

    // Don't use auto_run, in case someone messes with it...
    const code = `
def _hack_unexclude():
    dct = __builtins__.__builtins___
    G = globals() if "globals" not in dct else dct['globals']()

    # Handle special behavior of auto_run:
    key = "auto_run"
    auto_run = dct.pop(key)
    bad_auto_run = G.get(key, __builtins__.auto_run) is not auto_run
    __builtins__.auto_run = auto_run

    # Restore everything before raising anything:
    not_ok = []
    for key,(func,raiser) in dct.items():

        if key == '__import__':
            __builtins__.__import__ = func

        else:
            if raiser is not None and raiser is not G.get(key):
                not_ok.append(key)
            if func is not None:
                if key in G:
                    del G[key]  # "Unshadow" the builtin
                if key == 'setrecursionlimit':
                    func(1000)

    if bad_auto_run:
        ExclusionError.throw("the auto_run tool...")
    if not_ok:
        ExclusionError.throw("${ exclusions }")

_hack_unexclude()
del _hack_unexclude
`
    pyodide.runPython(code)
}
