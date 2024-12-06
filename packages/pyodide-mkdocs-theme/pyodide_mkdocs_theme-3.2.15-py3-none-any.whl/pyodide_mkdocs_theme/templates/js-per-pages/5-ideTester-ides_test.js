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





class IdeTesterGuiManager extends IdeRunner {

  constructor(editorId){
    super(editorId)
    this.globalTestsJq = $("#py_mk_test_global_wrapper")
    this.delay       = 0     // Override: no pause when starting the executions
    this.conf        = null
    this.testing     = false
    this.toSwap      = [this.data, ()=>""] // nothing to swap...
    this.ides_cache  = {}
    this.test_cases  = []   // List[conf]: Linearized version of CASES_DATA
    this.std_capture = []   // Full stdout+stdErr capture, AFTER any jQuery.terminal formatting
    this.counters    = {skip:0, remaining:0, failed:0, success:0}
    this.stopTests   = false
    this.fullCode    = ""   // Initial loaded code (associated to one conf/test)
  }


  // @Override
  announceCodeChangeBasedOnSrcHash(){}


  // @Override
  build(){
    super.build()

    this.finalizeFilters()
    this.finalizeControllers()

    // Configure all the tests before the counters, so that counts are up to date
    const confsArr = Object.values(CASES_DATA)
    confsArr.forEach( conf=>this.setupOneConfCaseAndAllSubcases(conf) )

    this.finalizeCounters(confsArr.length, this.test_cases.length)
  }



  finalizeFilters(){
    const ideThis = this
    $(".filter-btn").each(function(){

      const jBtn = $(this)
      const kind = this.id.split('-')[1]
      ideThis.globalTestsJq.css(`--display-${ kind }`, 'unset')

      jBtn.find(".status_filter").html(CONFIG.QCM_SVG).addClass([CONFIG.qcm.multi, kind])

      jBtn.on('click', function(){
        const state = 1 ^ +jBtn.attr('state')
        jBtn.attr('state', state)
        ideThis.globalTestsJq.css(`--display-${ kind }`, state?'unset':'none')
      })
    })
  }



  finalizeControllers(){

    // configure "run all" button:
    this.global.parent()
                     .find('button[btn_kind=test_ides]')
                     .on('click', ()=>this.runAllTests())
                     .parent()
                     .find('button[btn_kind=test_stop]')
                     .on('click', ()=>this.stopTests=true)


    // Configure global buttons (select-all, unselect-all):
    ;[ [false, ''], [true, 'un'] ].forEach(([state,prefix])=>{
      $(`button#${ prefix }select-all`).on('click', _=>{
        this.test_cases.forEach(o=>{
          o.skip = state
          this.setSvgAndCounters(o, prefix+'checked')
        })
        this.displayCounters()
      })
    })

    // Configure 'human" global button:
    $(`button#toggle-human`).on('click', _=>{
      this.test_cases.forEach(o=>{
        if(!o.human) return;
        o.skip = !o.skip
        this.setSvgAndCounters(o, o.skip?CONFIG.qcm.unchecked:CONFIG.qcm.checked)
      })
      this.displayCounters()
    })
  }



  setupOneConfCaseAndAllSubcases(conf){
    const batchOfTests = []

    if(!conf.subcases){
      // Simple case (one test only):
      this.registerOneTestAndSetupUI(conf, batchOfTests)

    }else{
      // If subcases are defined:
      const propsToReport = 'editor_id ide_link ide_name page_url rel_dir_url'.split(' ')
      conf.subcases.forEach( (subConf, i)=>{
        if(i) subConf.no_clear ??= true            // Keep original choice
        for(const prop of propsToReport){
          subConf[prop] = conf[prop]
        }
        this.registerOneTestAndSetupUI(subConf, batchOfTests, i+1)

        // Bind subcases "play" buttons: "run all subcases until this one"
        $(`#play${i+1}-${ conf.editor_id } > button[btn_kind=test_1_ide]`).on(
          'click', ((testsUpTo)=> ()=>this.runAllTests(testsUpTo) )(batchOfTests.slice())
        )
        $(`#play${i+1}-${ conf.editor_id } > button[btn_kind=load_ide]`).on(
          'click', this.loadFactory(conf)
        )
      })
    }

    // Bind the top level case buttons:
    $(`#test-btns-${ conf.editor_id } > button[btn_kind=test_1_ide]`).on(
      'click', ()=>this.runAllTests(batchOfTests)
    )
    $(`#test-btns-${ conf.editor_id } > button[btn_kind=load_ide]`).on(
      'click', this.loadFactory(conf)
    )
  }


  registerOneTestAndSetupUI(conf, batchOfTests, tailId=""){

    this.test_cases.push(conf)
    batchOfTests.push(conf)

    this.testConfStandardization(conf, tailId)

    const [countProp, setupClass] = conf.skip ? ['skip',      CONFIG.qcm.unchecked]
                                              : ['remaining', CONFIG.qcm.checked]
    this.counters[countProp]++

    const jDiv = $(conf.divSvgBtnsId)
      .html(CONFIG.QCM_SVG)
      .addClass([ 'multi', setupClass])
      .on( 'click', _=>{
        if(this.testing) return;
        this.setSvgAndCounters(conf, conf.skip ? CONFIG.qcm.checked : CONFIG.qcm.unchecked)
        this.displayCounters()
      })
    this.updateItemVar(jDiv, setupClass)
  }



  /**Initial conversion steps, to finalize the python->JS transfer of the tests data.
   * */
  testConfStandardization(conf, tailId){

    conf.divSvgBtnsId = `#status${ tailId }-${ conf.editor_id }`

    conf.fail = Boolean( conf.fail || conf.in_error_msg || conf.not_in_error_msg )
    conf.skip = Boolean( conf.skip || conf.human )

    // `reveal_corr_rems:undefined` means this won't be tested:
    if('reveal_corr_rems' in conf){
      conf.reveal_corr_rems = Boolean(conf.reveal_corr_rems)
    }
    // Initialize the test state flag (to know if it has been done in the tests or not):
    conf.revealedCorrRems = false

    ;'std_capture_regex not_std_capture_regex'.split(' ').forEach( prop=>{
      try{
        if(conf[prop]) conf[prop] = new RegExp(conf[prop], 'si')
      }catch(e){
        throw new PythonError(`Invalid Regex generation for ${ prop }, using ${ conf[prop] }`)
      }
    })

    conf.assertions = !conf.assertions ? [] : conf.assertions.split(' ').map(rule=>{
      const prop = _.camelCase( rule.replace(/^!/, '') )
      const revExpected = rule.startsWith('!')  // Reversing to enforce booleans everywhere
      return (obj) =>{
        if( obj[prop]===undefined ) return prop+' is undefined...'
        return!obj[prop] == revExpected ? "" : `${ prop }: should be ${ !revExpected }\n`
      }
    })
  }




  finalizeCounters(nIdes, nTests){
    // Finalize and display initial counters state, once all the tests have been registered:
    const allHtml = nTests==nIdes ? nIdes : `${ nIdes }<br>(${ nTests } cases)`
    $('#cnt-all').html(allHtml)
    this.displayCounters()
  }


  updateItemVar(jDivSvg, kind){
    const itemVar = jDivSvg.attr('itemVar')
    this.globalTestsJq.css(itemVar, `var(--display-${ kind })`)
  }



  /**Update the html class of the svg container with the given id.
   * */
  setSvgAndCounters(conf, kls){
    const jDiv = $(conf.divSvgBtnsId)
    this.updateItemVar(jDiv, kls)
    this.updateCountersFor(jDiv, -1)
    jDiv.removeClass(CONFIG.qcm_clean_up)
    jDiv.addClass(kls)
    this.updateCountersFor(jDiv, +1)
    conf.skip = jDiv.hasClass(CONFIG.qcm.unchecked)
  }


  updateCountersFor(jDiv, delta){
    if(jDiv.hasClass(CONFIG.qcm.ok))        this.counters.success   += delta
    if(jDiv.hasClass(CONFIG.qcm.wrong))     this.counters.failed    += delta
    if(jDiv.hasClass(CONFIG.qcm.checked))   this.counters.remaining += delta
    if(jDiv.hasClass(CONFIG.qcm.unchecked)) this.counters.skip      += delta
  }


  /**Update the values of each counter.
   * */
  displayCounters(){
    Object.entries(this.counters).forEach( ([cnt,n])=>{ $('#cnt-'+cnt).text(n) })
  }


  // Override
  terminalEcho(content, options){
    this.std_capture.push(content)
    super.terminalEcho(content, options)
  }


  swapConfAndData(data=undefined, codeGetter=undefined){
    if(data!==undefined){
      this.toSwap = [ data, codeGetter ]
    }
    ;[this.data, this.toSwap[0]]          = [this.toSwap[0], this.data]
    ;[this.getCodeToTest, this.toSwap[1]] = [this.toSwap[1], this.getCodeToTest]
  }


  // Override
  terminalDisplayOnIdeStart(){
    this.announceTest(false)
    super.terminalDisplayOnIdeStart()
  }

  announceTest(clearFromTerm){
    if(this.testing){
      if(clearFromTerm) this.terminal.clear()
      this.terminal.echo(`Testing: ${ this.conf.ide_name }`)
    }
  }



  /**Runtime to apply when clicking on a button to "download" all the code of an
   * IDE in the testing one.
   * */
  loadFactory(conf){
    return async ()=>{
      await waitForPyodideReady()
      if(this.testing) return;    // Deactivated during tests (otherwise, big troubles...)

      this.conf = conf
      this.data = await this.getIdeData(conf)   // Update first (see getters)

      this.getCodeToTest =()=> this.editor.getSession().getValue()
      this.applyCodeToEditorAndSave(conf.loadedCode)
      this._applyConfAndData(true)
    }
  }

  // @Override
  /**Reset the content of the editor to its initial content, and reset the localStorage for
   * the editor on the way.
   * */
  restart(){    jsLogger("[RestartTester]")
    let startCode = ""
    if(this.conf){
      startCode = this.conf.loadedCode
      this._applyConfAndData(true)
    }
    this.applyCodeToEditorAndSave(startCode)
    this.updateValidationBtnColor(0)
    this.terminal.clear()
    this.focusEditor()
  }


  _applyConfAndData(onLoad=false){

    const hasSetMaxHide = 'set_max_and_hide' in this.conf
    if(onLoad || hasSetMaxHide){
      this.conf.revealedCorrRems = false
      this.hiddenDivContent      = true
      this.srcAttemptsLeft       = hasSetMaxHide ? this.conf.set_max_and_hide
                                                 : this.conf.srcAttemptsLeft
      this.data.attempts_left    = this.srcAttemptsLeft
    }

    this.terminal.settings().outputLimit = this.stdoutCutOff
    this.updateStdoutCutFeedback(this.cutFeedback)

    this.setAttemptsCounter(this.attemptsLeft, true)
    this._clearStateIfNeededAndReinit(onLoad)
    this.setupFetchers()
    this.clearLibs()
  }


  // @Override
  setAttemptsCounter(n, low=false){
    n = Number.isFinite(n) ? n : "∞"
    if(low){
      $(this.counterH+'-low').text(n)
    }
    super.setAttemptsCounter(n)
  }


  save(_){}


  runAllTests(){ throw new Error('Not implemented') }



  /**Extract the config object for the given IDE, getting rid of the profile data on the way.
   * Data are cached so that a page is requested once only.
   * @returns a copy of the original object (so that it can be modified on the fly by the caller)
   * */
  async getIdeData(conf){

    // Request + store the data for all the IDEs in the related page, if missing:
    if(!this.ides_cache[conf.editor_id]){

      const response = await fetch(conf.page_url)
      const html     = await response.text()

      const reg      = /(?<=PAGE_IDES_CONFIG\s*=\s*['"]).+?(?=["']\s*<\/script>)/
      const compress = html.match(reg)[0]                 // Does always match!
      const fix_comp = compress.replace(/\\x1e/g, "\x1e")
      const configs  = decompressAndConvert(fix_comp)

      Object.entries(configs).forEach( ([editor,data])=>{
        // WARNING, the conf object matches only ONE of the data extracted from one page, so the
        // data object cannot be updated right away with decrease_attempts_on_user_code_failure
        // and so on...
        conf._profile = data.profile
        if(!conf.keep_profile) data.profile = null   // Remove profile info for tests (by default).

        this.ides_cache[editor] = this._prepareData(data)
      })
    }

    // Extract ide's data object, enforcing its existence:
    const data = this.ides_cache[conf.editor_id]

    if(!data) throw new Error(
      `Couldn't extract data for ${ conf.ide_name }.\nIf this is an IDE without python file, `
      +"you should restart mkdocs serve (the ids generator is now out of synch with the "
      +"rendered data). Otherwise, please raise an issue on the project's repository."
    )

    // Update the global values, once only:
    if(!conf.__conf_updated){
      conf.__conf_updated = 1

      ;`decrease_attempts_on_user_code_failure
        deactivate_stdout_for_secrets
        show_only_assertion_errors_for_secrets
      `.trim()
        .split(/\s+/).forEach(prop=>{
        if(prop in conf) data[prop] = conf[prop]
      })

      if('set_max_and_hide' in conf){
        conf.set_max_and_hide = conf.set_max_and_hide==1000 ? Infinity : conf.set_max_and_hide
      }
      conf.srcAttemptsLeft = data.attempts_left

      const sections = [
        this._toSection('env',       data.env_content),
        this._toSection('env_term',  data.env_term_content),
        this._toSection('code',      data.user_content),
        this._toSection('corr',      data.corr_content),
        this._toSection('tests',     data.public_tests),
        this._toSection('secrets',   data.secret_tests),
        this._toSection('post_term', data.post_term_content),
        this._toSection('post',      data.post_content),
      ]
      // Extract the section used during the tests (based on the main conf object...):
      const [codeToTest] = sections.splice(2 + !conf.code, 1)
      const others       = sections.join('').replace(/'''/g, "\\'\\'\\'").trim()
      const commented    = others && `\n\n\n'''\n${ others }\n\n'''\n`
      conf.loadedCode    = codeToTest.trim() + commented
    }


    // Send back a copy, to allow runtime mutation while keeping a clean initial state
    // (no need for a deep copy, so far...)
    const freshData = {...data}
    if('set_max_and_hide' in conf){
      freshData.attemptsLeft = conf.set_max_and_hide
    }
    return freshData
  }


  /**Build a sub section of the original python file.
   * */
  _toSection(py_section, content){
    return content && `\n\n# --- PYODIDE:${ py_section } --- #\n${ content }`
  }

}














class IdeTester extends IdeTesterGuiManager {


  constructor(editorId){
    super(editorId)

    this.runners = {
      play:     this.playFactory(CONFIG.runningMode.testingPlay),
      validate: this.validateFactory(CONFIG.runningMode.testingValid),
      terminal: async ()=>{ await this.runnerTerm(this.conf.term_cmd) },
    }
  }


  async runAllTests(targets){
    if(this.testing) return;
    await waitForPyodideReady()

    this.terminal.clear()
    const start    = Date.now()
    this.testing   = true
    this.stopTests = false

    const confsToRun = (targets ?? this.test_cases).filter( conf =>{
      const skip = (!targets || targets.length!=1) && conf.skip
      if(!skip){
        this.setSvgAndCounters(conf, CONFIG.qcm.checked)
      }
      return !skip
    })

    this.displayCounters()

    /* Running everything in order: it's actually a bit faster (probably because not queueing again
       and again while waiting in getIdeData...?). So don't bother with Promise.all anymore...  */
    let errOrNull=null
    try{
      for(const conf of confsToRun){
        if(this.stopTests) break
        this.conf = conf
        jsLogger('[Testing] - start', conf.ide_name)
        const runningKind = conf.term_cmd!==undefined ? 'terminal'
                          : conf.run_play ? 'play' : 'validate'
        await this.runners[ runningKind ]()
        jsLogger('[Testing] - done', conf.ide_name, '\n')
      }
    }catch(e){ errOrNull=e
    }finally{
      this._endTests(start, errOrNull)
    }
  }


  _endTests(start, error=null){
    this.testing   = false
    this.stopTests = false
    this.conf      = null
    const txt      = !error ? CONFIG.lang.testsDone.msg : txtFormat.error(String(error))
    const elapsed  = ((Date.now() - start) / 1000).toFixed(1)
    this.terminal.echo(txt)
    this.terminal.echo(txtFormat.info(`(Elapsed time: ${ elapsed }s)`))
  }



  buildCodeGetter(){
    const cbk = this.conf.code ? ()=>this.userContent : ()=>this.corrContent
    if(this.conf.run_play){
      return ()=>this._joinCodeAndPublicSections(cbk())
    }
    return cbk
  }


  async setupRuntimeTests(){
    if(!this.testing) return;
    const data = await this.getIdeData(this.conf)
    this.swapConfAndData(data, this.buildCodeGetter())
    this._applyConfAndData()
  }


  /**Note: Do NOT clear the scope in teardownRuntime: this would forbid
   * playing with the terminal afterward.
   * */
  _clearStateIfNeededAndReinit(force=false){
    if(force || !this.conf.no_clear){
      clearPyodideScope()
      this._init()
    }
  }



  async teardownRuntimeTests(runtime){
    if(!this.testing) return;

    this.conf.attempts_end = this.attemptsLeft  // Store before swap
    const testOutcome = this._analyzeTestOutcome(runtime)

    const success     = !testOutcome
    const classToBe   = !success        ? CONFIG.qcm.wrong
                      : !this.conf.fail ? CONFIG.qcm.ok
                                        : [CONFIG.qcm.ok,CONFIG.qcm.failOk]
                                                      // warning: failOk always last!

    this.swapConfAndData()    // Has to always occur
    this.teardownFetchers()   // Has to always occur

    this.setSvgAndCounters(this.conf, classToBe)
    this.displayCounters()
    this.std_capture.length = 0   // Always...

    if(testOutcome){
      if(!runtime) throw new Error(testOutcome)
      else         console.error(testOutcome)
    }
  }



  // @Override
  async setupRuntimeIDE(){
    await this.setupRuntimeTests()
    return await super.setupRuntimeIDE()
  }
  // @Override
  async teardownRuntimeIDE(runtime){
    try{
      await super.teardownRuntimeIDE(runtime)
    }finally{
      await this.teardownRuntimeTests(runtime)
    }
  }

  // @Override
  async setupRuntimeTerminalCmd(cmdChunk){
    if(this.testing){
      this.announceTest(true)
      await this.setupRuntimeTests()
    }
    const runtime = await super.setupRuntimeTerminalCmd(cmdChunk)
    if(this.testing){
      const cmd = this.conf.term_cmd.split('\n').join('\n'+CONFIG.MSG.promptWait)
      this.terminalEcho(CONFIG.MSG.promptStart + cmd)
    }
    return runtime
  }
  // @Override
  async teardownRuntimeTerminalCmd(runtime){
    try{
      await super.teardownRuntimeTerminalCmd(runtime)
    }finally{
      await this.teardownRuntimeTests(runtime)
    }
  }

  // @Override
  getAsyncPythonExecutor(){
    return super.getAsyncPythonExecutor(CONFIG.runningMode.testingCmd)
  }




  // ------------------------------------------------------------




  // Override
  revealSolutionAndRems(){
    if(!this.conf) return;
    this.conf.revealedCorrRems = true
    this.hiddenDivContent = false      // Mimic actual behavior
  }



  _analyzeTestOutcome(runtime){
    if(!runtime) return "Probably failed in the env section..."

    const fullOut = this.std_capture.join('')
    let msg = []

    if(!Number.isFinite(this.srcAttemptsLeft)){
      if(Number.isFinite(this.conf.attempts_end)) msg.push(
        "The number of attempts left should still be infinite, but was: " + this.conf.attempts_end
      )
      if(this.conf.delta_attempts) msg.push(
        `Expected delta_attempts=${ this.conf.delta_attempts } the final number of attempts is: ${ this.conf.attempts_end }`
      )

    }else if(this.conf.delta_attempts!==undefined){
      const actual = this.conf.attempts_end - this.srcAttemptsLeft
      const exp    = this.conf.delta_attempts
      if(exp != actual) msg.push(
        `Delta attempts: ${ actual } should be ${ exp }`
      )
    }


    if(('reveal_corr_rems' in this.conf)){
      if(this.conf.reveal_corr_rems !== this.conf.revealedCorrRems) msg.push(
        this.conf.reveal_corr_rems ? "Corr/REMs should have been revealed."
                                   : "Corr/REMs should NOT have been revealed."
      )
    }


    const failedAssertions = this.conf.assertions.map(check=>check(this)).join('')
    if(failedAssertions) msg.push(failedAssertions)


    if(this.conf.in_error_msg && !runtime.stdErr.includes(this.conf.in_error_msg)){
      msg.push(`The error message should contain; "${this.conf.in_error_msg}"`)
    }
    if(this.conf.not_in_error_msg && runtime.stdErr.includes(this.conf.not_in_error_msg)){
      msg.push(`The error message should NOT contain; "${this.conf.not_in_error_msg}"`)
    }

    if(this.conf.std_capture_regex && !this.conf.std_capture_regex.test(fullOut) ){
      msg.push(
        `The std output/error should match ${ this.conf.std_capture_regex }, but found:\n\n${ fullOut }`
      )
    }
    if(this.conf.not_std_capture_regex && this.conf.not_std_capture_regex.test(fullOut) ){
      msg.push(
        `The std output/error should NOT match ${ this.conf.not_std_capture_regex }, but found:\n\n${ fullOut }`
      )
    }


    if(!msg.length && runtime.stopped === this.conf.fail){
      return ""
    }
    msg = [
      `Test failed for ${this.conf.ide_link} :`,
      runtime.stdErr || "No error raised, but...",
      ...msg
    ]
    return msg.join('\n\n')
  }



  /**Setup the pyodide environment so that requests to relative urls are automatically redirected
   * to the correct (original) locations, and setup various sinks to avoids DOM interactions to
   * fail, typically when trying to update img tags through `PyodidePlot` or `mermaid_figure`.
   * */
  setupFetchers(){

    CONFIG.relUrlRedirect = `${ CONFIG.baseUrl }/${ this.conf.rel_dir_url }/`.replace(/[/]{2}/g, '/')

    pyodide.runPython(`

def __hack_pyfetch():
    import re, js
    from functools import wraps
    import pyodide.http as http

    pure_pyfetch = http.pyfetch
    pure_import  = __import__


    @wraps(pure_pyfetch)
    async def pyfetch(url, *a, **kw):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await pure_pyfetch(url, *a, **kw)
    http.pyfetch = pyfetch


    async def fake_fetch(url, *a):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await js.fetch(url, *a)


    class JsMock(int):
        """ Extends int so that computations when pyplot tries to update the DOM do not
            crash (even if wrong)
        """

        # ASYNC_CALLS = set('uploaderAsync'.split())

        def __getattr__(self, k):
            if k=='fetch':  return fake_fetch

            # if k in self.ASYNC_CALLS:  return self.async_sink_js

            if self is sink_js or k in ('document',):
                return sink_js
            return getattr(js,k)

        async def async_sink_js(self, *a,**kw):
            return sink_js

        def __call__(self, *a, **kw):
            return sink_js

        def __setattr__(self, k,v):
            setattr(js, k, v)

    fake_js = JsMock(1)
    sink_js = JsMock(1)  # HAS to be another instance than fake_js!

    def fake_import(name, *a, **kw):
        if name == 'js':
            return fake_js
        return pure_import(name, *a, **kw)
    __builtins__.__import__ = fake_import


    def teardown_tests():
        http.pyfetch = pure_pyfetch
        __builtins__.__import__ = pure_import
    __builtins__.teardown_tests = teardown_tests


__hack_pyfetch()
del __hack_pyfetch`)
  }


  teardownFetchers(){
    CONFIG.relUrlRedirect = ''
    pyodide.runPython("teardown_tests()")
  }


  clearLibs(){
    if(!this.conf.clear_libs) return
    pyodide.runPython(`
def _hack_remove_libs():
    import sys, shutil
    from pathlib import Path

    to_clear = ${ JSON.stringify(this.conf.clear_libs) }
    for name in to_clear:
        sys.modules.pop(name, None)
        p = Path(name)
        if p.exists():
            shutil.rmtree(p)
_hack_remove_libs()
del _hack_remove_libs
`)
  }
}


CONFIG.CLASSES_POOL.IdeTester = IdeTester
