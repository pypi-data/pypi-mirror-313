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



const isExclusionOrAssertionError=(runtime)=>{
  return runtime.stdErr.startsWith(CONFIG.MSG.exclusionMarker) || runtime.isAssertErr
}

// window.addEventListener('keydown', function(e){
//   console.log(e)
// })


class PyodideSectionsRunner {

  no_undefined = prop =>{
      const getter = v => {
        if(v!==undefined) return v
        throw new Error(`Undefined is not allowed: ${this.constructor.name}.${prop}.`)
      }
      return getter
  }

  //JS_CONFIG_DUMP
  get attemptsLeft()      { return this.data.attempts_left }
  get autoLogAssert()     { return this.data.auto_log_assert }
  get autoRun()           { return this.data.auto_run }
  get corrContent()       { return this.data.corr_content }
  get corrRemsMask()      { return this.data.corr_rems_mask }
  get cutFeedback()       { return this.data.cut_feedback }
  get deactivateStdoutForSecrets(){ return this.data.deactivate_stdout_for_secrets }
  get decreaseAttemptsOnUserCodeFailure(){ return this.data.decrease_attempts_on_user_code_failure }
  get envContent()        { return this.data.env_content }
  get envTermContent()    { return this.data.env_term_content }
  get excluded()          { return this.data.excluded }
  get excludedMethods()   { return this.data.excluded_methods }
  get export()            { return this.data.export }
  get hasCheckBtn()       { return this.data.has_check_btn }
  get hasCorrBtn()        { return this.data.has_corr_btn }
  get hasCounter()        { return this.data.has_counter }
  get hasRevealBtn()      { return this.data.has_reveal_btn }
  get isEncrypted()       { return this.data.is_encrypted }
  get isVert()            { return this.data.is_vert }
  get maxIdeLines()       { return this.data.max_ide_lines }
  get minIdeLines()       { return this.data.min_ide_lines }
  get postContent()       { return this.data.post_content }
  get postTermContent()   { return this.data.post_term_content }
  get prefillTerm()       { return this.data.prefill_term }
  get profile()           { return this.data.profile }
  get publicTests()       { return this.data.public_tests }
  get pyName()            { return this.data.py_name }
  get pythonLibs()        { return this.data.python_libs }
  get recLimit()          { return this.data.rec_limit }
  get secretTests()       { return this.data.secret_tests }
  get showOnlyAssertionErrorsForSecrets(){ return this.data.show_only_assertion_errors_for_secrets }
  get srcHash()           { return this.data.src_hash }
  get stdKey()            { return this.data.std_key }
  get stdoutCutOff()      { return this.data.stdout_cut_off }
  get twoCols()           { return this.data.two_cols }
  get userContent()       { return this.data.user_content }
  get whiteList()         { return this.data.white_list }
  //JS_CONFIG_DUMP





  constructor(id){
    jsLogger('[CheckPoint] - Constructor for', this.constructor.name, id)

    decompressPagesIfNeeded()

    this.id = id
    this.data = this._prepareData(PAGE_IDES_CONFIG[id])
    if(CONFIG._devMode)
      CONFIG.objs[this.id] = this
    else{
      delete PAGE_IDES_CONFIG[id]
    }
    this.pythonCodeRunnerWithCtx = async (ctx)=>{ pyodide.runPython(ctx.code) }
    this.getCodeToTest = ()=>""   // If no editor, nothing to test...
    this.running = undefined      // See CONFIG.runningMode
    this.allowPrint = true
    this.isGuiCompliant = false   // All the GUI makeup has been applied (may not be, right at the beginning, for tabbed contents, typically)
  }


  _init(){}   // Sink for super calls...

  _prepareData(data){
    data.python_libs = new Set(data.python_libs)
    return data
  }


  build(){
    // Using setTimeout to be sure the `build` step will be complete (some children classes
    // may have subsequent operations after the super method, aka here, has been called).
    if(this.autoRun){
      setTimeout(async ()=>await this.applyAutoRun())
    }
    this.makeUpYourGui()
  }



  /**Actions to perform when the element becomes "visible" in the page.
   * Here "visible" is "not hidden", CSS-wise (see `=== "tabbed"`, typically).
   * */
  makeUpYourGui(){
    return this.isGuiCompliant = true
  }



  /** Generic call for macros with AUTO_RUN=True (once the runner callback is defined...).
   * */
  async applyAutoRun(){
    await this._defaultAutoRun()
  }

  /**Allow to keep the same implementation for the IDE class, while the intermediate Terminal
   * class has its own logic for autoRun.
   * */
  async _defaultAutoRun(){
    while(!this.runner) await sleep(40)
    await this.runner()
  }


  /** Nothing to do by default (specific to IDEs) */
  codeSnippetEndFeedback(runtime, step, code){}



  /**Store code or command in the python runtime.
   * */
  storeUserCodeInPython(varName, code){
    const showOff = JSON.stringify(code.length>50 ? code.slice(0,50)+' ...' : code)
    jsLogger('[CheckPoint] - Store ', varName, showOff)

    // The double quotes are all escaped to make sure no multiline string will cause troubles
    const escapedCode = code.replace(/"/g, '\\"')
    pyodide.runPython(`__builtins__.${ varName } = """${ escapedCode }"""`)
  }



  /**Runners without any terminal won't ever give feedback, unless it's a critical error.
   * In that case, a window alert will be used, so that it doesn't go unnoticed.
   * */
  giveFeedback(content, format='error'){
    if(content && format=='error'){
      // Format back any escaped square brackets, because window.alert is not the terminal...
      window.alert( unEscapeSqBrackets(content) )
    }
  }




  /**Build the default runtime to pass as argument to the `runPythonCodeWithOptionsIfNoStdErr`
   * function. This object is the "per run" state tracker for the executions.
   *
   * @returns: a RuntimeManager object
   * */
  buildRunConfig(){
    jsLogger('[CheckPoint] - buildConfig (runtime)')
    return new RuntimeManager(this)
  }





  /**Explore the user's code to find missing modules to install. If some are found, load micropip
   * (if not done yet), then install all the missing modules.
   * Also import all the packages present in runtime.whiteList.
   *
   * NOTE: python libs are identified by picking into the global config, but are actually loaded
   *       only if they are available in the instance property (this is to limit the _SAVAGE_
   *       unexpected installations of random packages from PyPI).
   *
   * @code : the python code to run.
   * @runtime : `RuntimeManager` object.
   * @isFromEnv : specify if the current run is for an environment section or not.
   * */
  async installAndImportMissingModules(code, runtime, isFromEnv=false){
    await installPythonPackages(this, code, runtime, isFromEnv)
  }



  /**Creates a generic "action runner", handling the overall security logic, catching exceptions
   * that are thrown up to this point and displaying them in a BigFail-fashion-way in the terminal.
   *
   * Contracts:
   *    - @setup takes the `e` (event) argument only and returns a RuntimeManager instance.
   *      The argument may be:
   *        * either an `Event`: then it has no use.
   *        * or the current terminal command (`string`) that just got validated in the console.
   *    - @action takes the runtime argument and returns nothing
   *    - @finallyTeardown takes the runtime argument and returns nothing.
   *
   * About executions:
   *    - @actionName : CONFIG.runningMode property  to be able to identify what's currently running.
   *    - @setup is always run
   *    - @action is always called, and it is its job to decide if it has to actually run its
   *       logic or not, depending on the `runtime` state.
   *    - @finallyTeardown is always called, and should contain all the operations that HAVE
   *       to be run whatever happened before (success/error). Both are almost guaranteed to
   *       happen, whatever the outcome of the others executions was: the only exception would
   *       be a crash during @setup, that wouldn't return any `runtime` object (this would lead
   *       to a BIG_FAIL error thrown in he JS console).
   * */
  lockedRunnerWithBigFailWarningFactory(
    actionName,       // string, logging purpose + used to identify what's currently running.
    setup,            // async, no args
    action,           // async, args: runtime
    finallyTeardown,  // async, args: runtime (guaranteed to run)
    sendSrcOrEvent=false,
  ){
    const loggerName=`[${actionName}]`

    return withPyodideAsyncLock(actionName, async(eventOrCmd)=>{
      if(eventOrCmd && eventOrCmd.preventDefault) eventOrCmd.preventDefault()
      jsLogger(loggerName)

      this.running = actionName
      let runtime
      try{
        runtime = await setup.call(this, eventOrCmd)
        await action.call(this, sendSrcOrEvent ? eventOrCmd : runtime)

      }catch(e){
        jsLogger("[CheckPoint] - BIG FAIL", actionName)

        // If something didn't get caught, it's very wrong... so dump everything to the console
        const stdErr = youAreInTroubles(e)
        this.giveFeedback(stdErr)

        if(runtime){                  // (`runtime` may be undefined if the error was in setup...)
          runtime.gotBigFail = true
          runtime.stdErr = stdErr
        }
        throw e

      }finally{
        jsLogger("[CheckPoint] - finally", actionName)
        if(runtime){
          await finallyTeardown.call(this, runtime)
        }
        this.running = undefined
      }
    })
  }





  /**Generic main "action" runner for environment code.
   * */
  async installImportsAndRunEnvCode(ctx, runtime){
    if(!ctx.code) return;
    await installPythonPackages(this, ctx.code, runtime, ctx.isEnvSection)
    await pyodide.runPythonAsync(ctx.code, {filename: `<${ toSnake(ctx.section) }>`})
  }



  /**Build the default configuration runtime to use to run the user's code.
   * */
  setupGlobalConfig(){
    CONFIG.runningId      = this.id
    CONFIG.running        = this.running
    CONFIG.termMessage    = ()=>undefined    // sink
    for(const prop of 'get del set keys'.split(' ')){
      const globName = prop+'Storage'
      const method   = `pyodide${ _.capitalize(prop) }Storage`
      globalThis[globName] = this[method].bind(this)
    }
  }

  pyodideGetStorage(key)  { noStorage() }   // sink
  pyodideKeysStorage()    { noStorage() }   // sink
  pyodideSetStorage(k, v) { noStorage() }   // sink
  pyodideDelStorage(key)  { noStorage() }   // sink






  /** 1. Refresh the features defined in pyodide environment, in case the user messed with them
   *     (accidentally or not).
   *  2. Then run the content of the `env` section.
   *
   * @returns: [runtime, isOk].
   *     If isOk is false, an error has been raised: this is a CRITICAL ERROR and executions at
   *     upper level must be stopped.
   * */
  async setupRuntime(){
    jsLogger('[CheckPoint] - setupRuntime PyodideSectionsRunner')

    const [runtime,ctx] = await this._baseSetupRuntime()
    if(ctx.success){
      await runtime.runWithCtx('env')
    }
    return runtime
  }


  async _baseSetupRuntime(){
    this.setupGlobalConfig()
    const runtime = this.buildRunConfig()
    let ctx       = await runtime.runWithCtx({section:'env', method: this.refreshPyodideFeatures})
    return [runtime, ctx]
  }


  refreshPyodideFeatures(){
    ;`
      ioStuff
      version
      localStorageRelays
      copyFromServer
      exclusionsTools
      mermaidDrawer
      refresher
      upDownLoader
    `.trim()
     .split(/\s+/)
     .forEach(pyodideFeatureRunCode)
  }







  /**Takes a user code as argument, and run it in the pyodide environment, using various runtime
   * logics. It mutates the RuntimeManager objects on the way, keeping track of the current state
   * of the executions (error or not, keep running or not, ...).
   *
   * Operations done:
   *    1. Run methods exclusion check (if not needed, the method is called but won't do anything).
   *    2. If the runtime is marked as stopped, stop here.
   *    3. Try to install/import missing packages or python_libs.
   *    4. If the runtime is marked as stopped, stop here.
   *    5. Actually run the given code in Pyodide.
   *
   * @throws: Any JS runtime Error if something went very wrong... (python errors are swallowed
   *          and just printed to the jQuery.terminal)
   * */
  async runPythonCodeWithOptionsIfNoStdErr(code, runtime, testsStep=null){
    jsLogger('[CheckPoint] - Enter generic running function')

    // Do nothing if nothing to do...!
    if(runtime.stopped) return;

    const someCodeToRun = code.trim()
    if(someCodeToRun){

      const baseCtx =(autoAssertExtraction=false)=>({
        code, section: 'code', isEnvSection: false,
        logConfig: {code, autoAssertExtraction, purgeTrace: runtime.purgeStackTrace},
      })

      // Do first the methods exclusions check, to gain some time (avoids loading modules if
      // the error would show up anyway afterward...)
      await runtime.runWithCtx({
        ...baseCtx(),
        method: this.throwIfExcludedMethodsFound,
      })
      if(runtime.stopped) return;

      // Detect possible user imports and install the packages to allow their imports:
      await runtime.runWithCtx({
        ...baseCtx(),
        method: this.installAndImportMissingModules,
        methodArgs: [code, runtime],
      })
      if(runtime.stopped) return;

      await runtime.runWithCtx({
        ...baseCtx(runtime.autoLogAssert),
        method: this.pythonCodeRunnerWithCtx,
        applyExclusionsIfAny: true,
      })
    }

    // Potentially give some feedback in the terminal to the user, about what happened:
    this.codeSnippetEndFeedback(runtime, testsStep, code)
  }



  throwIfExcludedMethodsFound(ctx, runtime){
    const nope = runtime.excludedMethods.filter(methodCall=>ctx.code.includes(methodCall))
    if(nope.length){
      const plural = nope.length>1 ? "s":""
      const nopes = nope.map( s=>s.slice(1) ).join(', ')
      const msg = `${ CONFIG.MSG.exclusionMarker } method${plural}: ${ nopes }`
      throw new PythonError(msg)
    }
  }





  async teardownRuntime(runtime){
    jsLogger("[CheckPoint] - PyodideSectionsRunner teardownRuntime")

    await runtime.runWithCtx('post')
    await this.handleMermaids(runtime)
    await this._baseTeardownRuntime(runtime)
  }

  async _baseTeardownRuntime(runtime){
    jsLogger("[CheckPoint] - teardown pyodide cleaner")
    pyodideFeatureRunCode('autoRunCleaner')
    runtime.cleanup()
  }



  async handleMermaids(runtime){
    jsLogger("[CheckPoint] - teardown mermaid")

    if(!CONFIG.needMermaid || runtime.stopped){
      return
    }

    if(!globalThis.mermaid){
      this.giveFeedback(
        'Cannot convert to mermaid graph: mermaid is not available.\n'
        +'Please contact the author of the exercice.'
      )
    }
    try{
      await mermaid.run()
      // mermaid.run systematically throws an error, even on valid graphs...
      // Worse: If mermaid.run({suppressErrors:true}) is used, nothing is rendered at all...
      //        I love JS...
    }catch(e){}
  }
}
