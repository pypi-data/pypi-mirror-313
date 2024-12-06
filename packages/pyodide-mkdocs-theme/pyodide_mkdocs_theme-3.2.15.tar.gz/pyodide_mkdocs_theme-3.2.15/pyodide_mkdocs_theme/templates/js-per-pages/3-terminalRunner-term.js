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




class _TerminalHandler extends PyodideSectionsRunner {

  constructor(id){
    super(id)
    this.terminal      = null     // jQuery.terminal object
    this.termWrapper   = null     // Html element
    this.termEnabled   = false    // Flag to enforce activation of the terminal (admonitions+tabbed troubles)
    this.isIsolated    = id.startsWith("term_only")
    this.cmdChunk      = ""
    this.cmdOnTheRun   = ""
    this.joinTerminalLines = false
    this._init()                  // Will cause a second call if coming from an iDE, but "whatever"...
  }

  _init(){
    super._init()
    this.alreadyRanEnv = false    // Specific to terminals, but defined "for everyone"
  }


  /**Build a jQuery terminal and bind it to the underlying pyodide runtime.
   *
   * WARNING:  If this is an IdeEditorHandler, this.id is the id of the editor div, not
   *           the id of the terminal div ! (hence the use of the termId argument)
   * */
  build(termId=null){
    if(!termId) termId = this.id
    const jqTermId = '#' + termId

    jsLogger("[Terminal] - build " + jqTermId)

    this.runnerTerm = this.getAsyncPythonExecutor()
    const termOptions = {
      greetings: "",                            // Cancel terminal banner (welcome message),
      completionEscape: false,
      prompt: CONFIG.MSG.promptStart,
      outputLimit: this.stdoutCutOff,           // this.terminal.settings().outputLimit=value (to change dynamically)
      enabled: false,                           // GET RID OF THE DAMN AUTO-SCROLL!!!!!!
      // wrap: getWrapTerms(),                  // This also deactivate colors... FUCK THIS!
      keymap: this.getTerminalBindings(),
      completion: function (command, callback) {  // AUTO-completion
        callback(pyFuncs.pyconsole.complete(command).toJs()[0]);
      },
      mousewheel: function(){ return true },    // Seems enough to fix the "no mouse wheel" troubles on terminals
      onBlur: function(){},                     // Allow to leave the textarea, focus-wise.
    }                                           // DO NOT PUT ANY CODE INSIDE THIS !! (I don't understand what's going
                                                // on here, but  this is the only way I found to make all this work...)

    this.terminal    = $(jqTermId).terminal(this.runnerTerm, termOptions)
    this.termWrapper = this.terminal.parent()
    this.terminal.history().clear()     // Clear the history from localeStorage.

    if(CONFIG._devMode) CONFIG.terms[termId]=this.terminal

    this.addEventToRunOnce(
      this.terminal, this.ensureTerminalActivationOnClick.bind(this), true
    )
    this.termWrapper.on(
      'click', this.attemptAtResolvingTerminalUiTroubles.bind(this)
    )
    this.termWrapper.find(".stdout-wraps-btn").on(
      'click', this.swapTerminalLinesJoinerForCopies.bind(this)
    )
    this.termWrapper.find(".stdout-ctrl").on(
      'click', _=>{ this.updateStdoutCutFeedback(!this.cutFeedback) }
    )
    this.updateStdoutCutFeedback(this.cutFeedback)

    this.prefillTermIfAny()

    super.build()   // Nothing done there so far, but for consistency...
  }



  /**Update the UI button status and the inner state of cutFeedback to the given value.
   * */
  updateStdoutCutFeedback(to){
    this.data.cut_feedback = CONFIG.cutFeedback = to
    const method = to ? 'removeClass' : 'addClass'
    $(this.termWrapper).find(".stdout-x-ray-svg")[method]('py_mk_hidden')
  }



  swapTerminalLinesJoinerForCopies(){
    this.joinTerminalLines = !this.joinTerminalLines
    const classMethod = this.joinTerminalLines ? 'removeClass' : 'addClass'
    this.termWrapper.find(".stdout-wraps-btn")[classMethod]('deactivated')
  }


  /**Because terminals are created deactivated, add an EventListener for click to reactivate them.
   * Using the async lock so that the user cannot resume a terminal while it's running (could
   * occur on first click/run).
   *
   * - Does nothing if the terminal already got activated by other means.
   * - If a selection exists, do not enable the terminal or the selection gets lost.
   * */
  ensureTerminalActivationOnClick(){
    if(!this.termEnabled){
      if(!getSelectionText()){
        this.terminal.focus(true)
        this.terminal.enable()
      }
      this.termEnabled = true
    }
  }


  /**Transfer user's resize operations to the terminal wrapper, so that the content stays
   * confined to the wrapping div.
   * */
  terminalAutoWidthOnResize(){
    const wrapperWidth = this.termWrapper.width()
    if(wrapperWidth != this.terminal.width()){
      this.terminal.width(wrapperWidth)
    }
  }


  /**This routine tries to fix the following bugs with terminals:
   *    - The 0px width terminals on tab change (markdown: `=== "tabbed"`):
   *    - The FILL content lost when the user changed of tab anywhere in the page...
   * */
  attemptAtResolvingTerminalUiTroubles(){
    const w = this.termWrapper.css('width')
    if(w != this.terminal.css('width')){
      this.terminal.css('width', w)
    }
    const h = this.termWrapper.css('height')
    if(h != this.terminal.css('height')){
      this.terminal.css('height', h)
    }
    if(this.isIsolated && this.prefillTerm && !this.terminal.get_command()){
      this.prefillTermIfAny()
    }
  }


  /**Routine adding the given callback on a jQuery @target click event, with an automatic
   * "unsubscription on first click" wrapping logic.
   * If @withLock is true, the routine is using the Pyodide async lock, to avoid messing
   * with the global state of the page.
   * */
  addEventToRunOnce(target, cbk, withLock=false, event='click'){
    let clickHandler = async _=>{
      target.off(event, clickHandler)
      cbk()
    }
    if(withLock){
      clickHandler = withPyodideAsyncLock('term_'+event, clickHandler)
    }
    target.on(event, clickHandler)
  }



  /**Hook returning the configuration for terminal keyboard shortcuts bindings.
   * To override in child classes when needed.
   *
   * Handled here: transfer KeyInterrupt from DOM to python runtime (note: actually
   * useless as long as no worker used!).
   * */
  getTerminalBindings(){
    return ({
      "CTRL+C": async (e) => {
        let txt = getSelectionText()

        // Skip if some text is selected (=> copy!)
        if (!txt) {
          let currentCmd = this.terminal.get_command();
          pyFuncs.clear_console();    // Looks like it does nothing...? :/
          this.terminal.echo(CONFIG.MSG.promptStart + currentCmd);
          this.terminal.echo(txtFormat.error("KeyboardInterrupt"));
          this.terminal.set_command("");
          this.terminal.set_prompt(CONFIG.MSG.promptStart);
          return
        }
        e.preventDefault()
        e.stopPropagation()
        if(this.joinTerminalLines){
          txt = txt.replace(/\n/g, '')
        }
        await navigator.clipboard.writeText(txt)
      }
    })
  }


  getAsyncPythonExecutor(){
    throw new Error('Should be overridden in the child class.')
  }


  prefillTermIfAny(){
    if(this.prefillTerm) this.terminal.set_command(this.prefillTerm)
  }


  setupGlobalConfig(){
    super.setupGlobalConfig()
    CONFIG.cutFeedback = this.cutFeedback
    CONFIG.termMessage = this.termFeedbackFromPyodide.bind(this)
  }


  /**When a terminal is available, display stdout and errors in it, if any.
   *
   *  @format: by default `"error"`. Formatting to use for the jQuery.terminal.
   * If @format is `null`, the @content is already formatted for the terminal and no txtFormat
   * option must be applied anymore.
   * */
  giveFeedback(content, format='error'){
    if(content){
      if(format!==null) content = txtFormat[format](content)
      this.terminalEcho(content)
    }
  }


  /**Feedback coming from pyodide, one way or another...
   * Any call reaching this method is about a content to unconditionally show in the terminal.
   *
   * If @isPrint is true, the call comes from a print statement and is a stdout redirection.
   * the child method already decided if the message must be displayed or not.
   * If @isPrint is false, the call is a direct one to terminal_message, from an author or a user,
   * and the key argument has to match the STD_KEY argument
   *
   * @throws: Error if isPrint is false and the key isn't the expected one, of if the `format`
   *          option is unknown.
   */
  termFeedbackFromPyodide(_key, msg, format, isPrint=false, newline=false){
    if(!txtFormat[format]){
      throw new Error(`Unknown formatting option: ${format}`)
    }
    msg = textShortener(msg)
    this.terminalEcho(txtFormat[format](msg), {newline})
  }


  /**Internal hook, allowing to capture all the content sent to the terminal from a parent class
   * (aka, IdeTester...).
   * WARNING: at this point, the content is already formatted with jQuery.terminal syntaxes.
   * */
  terminalEcho(content, options){
    this.terminal.echo(content, options ?? {newline:true})
  }
}












class TerminalRunner extends _TerminalHandler {


  /**Generate the async-locked callback used to run commands typed into the terminal.
   * */
  getAsyncPythonExecutor(running=CONFIG.runningMode.cmd){
    return this.lockedRunnerWithBigFailWarningFactory(
      running,
      this.setupRuntimeTerminalCmd,
      this.runTermCommand,
      this.teardownRuntimeTerminalCmd,
    )
  }

  async applyAutoRun(){
    await this.runnerTerm(this.prefillTerm)
  }



  /**Definitions of `command`, `cmdOnThRun` and general context about `PyodideConsole`:
   * ----------------------------------------------------------------------------------
   *
   *
   * All those properties, but especially `cmdChunk`, are trickier than they seem.
   * This is essentially because the hidden/inner PyodideConsole is actually running totally
   * independently of the jQuery.terminal object itself.
   *
   * Concretely, the PyodideConsole is handling the code itself without troubles, but anything
   * other than "just run that code" (aka, installations/imports, exclusions, ...) still has to
   * be done around the console.
   *
   * Problems arise when you need to know on the JS/Theme side if the cmdChunk is complete or not.
   * To do so, you need to send the current @cmdChunk to the PyodideConsole, and that _fucking
   * little bastard_ will automatically schedule the async execution of any complete instruction
   * as soon as you call `pyconsole.push(chunk)`, before you can even know it is complete or not
   * on the JS/Theme side...
   *
   *
   * On top of this, what a @cmdChunk means (brain-wise), might sometimes be quite different of
   * what a terminal might actually be sending here as argument:
   *
   * @cmdChunk: This is the string content that is passed through _WHEN THE USER HITS `Enter` in
   *           the terminal without holding Shift key_. This implies @cmdChunk could concretely
   *           be a lot of different things:
   *                - A single line command, just like you'd expect:
   *                      `a = 45+6`
   *                - A multiline command, potentially with several "commands" in it (two, here):
   *                      ```
   *                      globs = {}
   *                      def func(k):
   *                          return globs.get(k, 42)
   *                      ```
   *                - The CONTINUATION of a multiline command started earlier (here it gets messy):
   *                      Previously:   `>>> """ Starting the multi thing`
   *                      Previously:   `... continue it`
   *                      Now:          `... third line`
   *
   *                      After hitting `Enter`, @cmdChunk will be `"third line"` ONLY.
   *
   *                - Any mix of all these two last...
   *
   *
   * Now, _IF_ the exclusions are already in place before the PyodideConsole execute the complete
   * command, builtins or imports exclusions are already handled because the console uses the
   * global scope.
   *
   * BUT, methods exclusions have to be checked, and missing packages might need to be installed.
   *
   * Considering the UX, it seems highly questionnable to drop exclusions related errors right in
   * the middle of an incomplete command. Even worse: to start installing a package right in the
   * middle of a multiline command... :roll-eyes:
   *
   *
   * Summarizing:
   *
   * 1. Exclusions (builtins & imports), if any, have to be put in place before the current
   *    `cmdChunk` is passed to the PyodideConsole, even if the current "command" is not complete.
   *
   * 2. Methods exclusions and missing packages installation have to be done only when the "current
   *    command" is complete, so the TerminalRunner must keep track of previously entered cmdChunks
   *    and track properly when it is "fully complete", syntax error, ...
   *    This is where `cmdOnTheRun` enters the game.
   *
   *        ----------------------------------------------------------------------------------------
   *        TODO: the implementation about imports actually does not match this description anymore
   *        ----------------------------------------------------------------------------------------
   *
   * 3. When the `PyodideConsole` announce a complete command:
   *      - It's execution in pyodide is already scheduled, but the result stills need to be run
   *        with an async call.
   *      - Before that, excluded methods and missing packages have to be handled, so pass the
   *        `cmdOnTheRun` content to `runPythonCodeWithOptionsIfNoStdErr`, replacing the code
   *        executor method with an async callback that will actually just  await the result
   *        from the internal `PyodideConsole`.
   *
   *
   * IMPLICATIONS:
   *
   * Because of all this, a lot of operations have to be applied each time the user strikes `Enter`
   * in the terminal, even if the command is not complete yet (since, you cannot know upfront...).
   * This is the reason for env_term and post_term executions, for example.
   *
   * */
  async setupRuntimeTerminalCmd(cmdChunk){

    /*
    !!! WARNING !!!

        Any ASYNC potential calls to setupRuntime HAVE to be done before the pyconsole.push,
        otherwise, because of async loop scheduling, the environment is setup from JS AFTER
        the user command has been run indie pyodide...
        Because of this, need the commandBuffer to update the __USER_CMD__ variable, and
        _also_ because of this, the env section will also run on incomplete commands, and
        _also_ because of this, any import done through the console must be checked now...
    */
    this.cmdChunk     = cmdChunk
    this.cmdOnTheRun += this.cmdOnTheRun ? '\n'+cmdChunk : cmdChunk
    this.storeUserCodeInPython('__USER_CMD__', this.cmdOnTheRun)
    this.terminal.pause()

    // If an IDE-terminal is run before the IDE itself, it must run the env/post sections.
    // If env already run before, envTerm HAS to run independently, so remove the dependency.
    let runtime
    if(!this.alreadyRanEnv){
      runtime = await this.setupRuntime()
      this.alreadyRanEnv = !runtime.stopped

    }else{
      runtime = this.buildRunConfig()
      runtime.changeDependency('envTerm', 'start')  // Make envTerm runnable on its own!
      this.setupGlobalConfig()                      // Make sure CONFIG.termMessage is properly bound
    }

    await runtime.runWithCtx('envTerm')
    return runtime
  }



  /**Specific teardown steps when using a terminal command (isolated or IDE's terminal).
   * */
  async teardownRuntimeTerminalCmd(runtime){
    try{
      await runtime.runWithCtx('postTerm')
    }finally{
      // If ever postTerm failed, post might still have to run:
      await this.teardownRuntime(runtime)
    }
  }



  /**Generic terminal teardown actions (common to isolated and IDEs' terminals)
   * */
  async teardownRuntime(runtime) {
    jsLogger("[CheckPoint] - TerminalRunner teardownRuntime")
    this.terminal.resume()
    await super.teardownRuntime(runtime)
    this.storeUserCodeInPython('__USER_CMD__', "")
  }



  /**Main command routine execution logic.
   * */
  async runTermCommand(runtime){
    jsLogger("[CheckPoint] - Terminal - start running command")

    if(runtime.stopped){
      jsLogger("[CheckPoint] - Terminal - Skipped!")
      return
    }

    // Must be done BEFORE creating the future, otherwise, async scheduling troubles, and the
    // exclusions end up being applied AFTER the user's command has been run...
    await runtime.runWithCtx({
      code:          this.cmdChunk,
      section:      'cmd',
      isEnvSection:  false,
      logConfig:    {code:this.cmdChunk, autoAssertExtraction: false, purgeTrace: runtime.purgeStackTrace},
      method:        this.installAndImportMissingModules,
      methodArgs:   [this.cmdOnTheRun, runtime],
    })

    if(runtime.stopped){
      this.cmdOnTheRun = ""
      return
    }

    const done = async (future)=>{
      jsLogger("[CheckPoint] - Terminal - done step. Awaited:", futureAwaited)
      this.cmdOnTheRun = ""
      if(!futureAwaited){
        try{ await future }catch(e){
          // console.warn(e)    // Might fail but result is useless => sink.
        }
      }
      future.destroy()    // to destroy only if it got awaited first
      await sleep()       // Enforce GUI update, going through the next tick
    }

    let futureAwaited = false   // Flag to know if the future has been awaited or not, in the loop
    const lines = this.cmdChunk.split("\n")   // Split multiline commands (useful when pasting)

    for (let line of lines) {
      jsLogger("[CheckPoint] - Terminal - current cmd line:", line)

      /* NOTE: putting future inside an array slightly changes the behaviors about the
         "PyodideConsole future exception was never retrieved" warnings... => might be better...
         BUT... this doesn't resolve the troubles about async scheduling in any way (I checked),
         so the overall "mostly broken" setup must be kept... */
      let [future] = [pyFuncs.pyconsole.push(line)]
      futureAwaited = false

      // Set the next line prompt beginning in the terminal (command: ">>>" or continuation:"...")
      const isIncompleteExpr = future.syntax_check=="incomplete"
      const headLine = isIncompleteExpr ? CONFIG.MSG.promptWait : CONFIG.MSG.promptStart
      this.terminal.set_prompt(headLine)

      switch (future.syntax_check) {

        case "complete":
          jsLogger("[CheckPoint] - Terminal - future complete")

          // Prepare the needed runner, which will handle the `futureAwaited` flag:
          const oldRunner = this.pythonCodeRunnerWithCtx
          this.pythonCodeRunnerWithCtx = async _=>{
            jsLogger("[CheckPoint] - Terminal - awaiting future")
            futureAwaited = true
            await pyFuncs.await_fut(future)
          }

          try{
            /*NOTE: nothing can be awaited in between the future "creation" and the execution
              of this.pythonCodeRunnerWithCtx, otherwise the event loop will actually compute
              the result of the python command (which is now stored in the event loop) before
              the restrictions are put in place in the environment).
              Everything is "synch" up to this point!
            */
            await this.runPythonCodeWithOptionsIfNoStdErr(this.cmdOnTheRun, runtime)
              // NOTE: this.cmdOnTheRun argument has actually no other use than to check against
              //       methods exclusions (imports are checked again, but with no result, since
              //       already done if needed).

          }finally{
            this.pythonCodeRunnerWithCtx = oldRunner
            await done(future)
          }
          continue

        case "incomplete":
          jsLogger("[CheckPoint] - Terminal - future incomplete")
          continue

        case "syntax-error":
          jsLogger("[CheckPoint] - Terminal - future syntax error")
          this.terminal.error(future.formatted_error.trimEnd());
          await done(future)
          return

        default:
          await done(future)
          throw new Error(`Unexpected state ${future.syntax_check}`);
      }
    }
  }
}

CONFIG.CLASSES_POOL.Terminal = TerminalRunner
