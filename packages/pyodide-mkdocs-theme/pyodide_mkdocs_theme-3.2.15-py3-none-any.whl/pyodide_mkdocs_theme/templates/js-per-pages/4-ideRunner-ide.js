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


ace.require("ace/ext/language_tools");

const isWin   = navigator.userAgent.includes('Windows')
const isMacOs = navigator.userAgent.includes('Macintosh')

const somethingFullScreen =()=> Boolean(document.fullscreenElement)

/**Extract the height, as a number, from the css property (by default)
 * */
const cssPx =(jObj,prop='height')=> +jObj.css(prop).slice(0,-2)












class IdeStorageManager extends TerminalRunner {

  /**Process to "re-initiate" the internal state of the IDE (useful for testing) */
  constructor(editorId){
    super(editorId)
    this.storage = null   // updated with the following call...
    this.getStorage()
  }

  // First class, making sure the change of argument if handled
  build(){
    super.build(this.termId)
  }


  _extractWhateverLocalStorageVersion(editorId){
    const  extractForThis = editorId==this.id
    return getIdeDataFromStorage(editorId, extractForThis ? this : null)
  }

  getStorage(){
    let [storage, outdated] = this._extractWhateverLocalStorageVersion(this.id)
    this.storage = storage

    // Enforce update of internal values:
    if( outdated || this.storage.name!=this.pyName || this.storage.zip!=this.export ){
      this.setStorage({name: this.pyName, zip:  this.export})
    }
  }

  setStorage(changes){
    if(changes){
      for(const k in changes) this.storage[k] = changes[k]
    }
    localStorage.setItem(this.id, JSON.stringify(this.storage))
  }


  //-------------------------------------------------------------------------


  announceCodeChangeBasedOnSrcHash(){
    if(this.storage.hash != this.srcHash){
      this.terminalEcho(CONFIG.lang.refresh.msg)
    }
  }


  /**Automatically gives the focus to the ACE editor with the given id.
   * */
  focusEditor(){
    this.editor.focus()
  }


  //-------------------------------------------------------------------------


  _validateKeyStorageAccess(key){
    if(FORBIDDEN_LOCAL_STORAGE_KEYS_WRITE.some(k=>k==key)){
      throw new PythonError(
          `Writing the "${ key }" property of the localStorage is forbidden (already used by PMT).`
      )
    }
  }

  _validateNotFromTerminal(){
    if(this.running === CONFIG.runningMode.cmd) throw new PythonError(
      'Cannot access localStorage data from the terminal'
    )
  }


  /**LocalStorage accessor from pyodide. Returns null if the key doesn't exist.
   * */
  pyodideGetStorage(key){
    this._validateNotFromTerminal()
    return this.storage[key]
  }


  /**List all the keys present in the LocalStorage.
   *
   * IMPORTANT: When called from pyodide, this will send back a JsProxy object.
   *            It should be converted to a python list using `arr.to_py()`
   * */
  pyodideKeysStorage(){
    this._validateNotFromTerminal()
    return Object.keys(this.storage)
  }


  /**LocalStorage mutator from pyodide. Writing the properties used by PMT is forbidden.
   * Accept only strings or numbers.
   * */
  pyodideSetStorage(key, value){
    this._validateNotFromTerminal()
    this._validateKeyStorageAccess(key)
    if(typeof(value)!='string' && typeof(value)!='number'){
      throw new PythonError(
        `Cannot update "${ key }" localStorage property: only numbers and strings are allowed as values.`
      )
    }
    this.setStorage({[key]: value})
  }

  pyodideDelStorage(key){
    this._validateNotFromTerminal()
    this._validateKeyStorageAccess(key)
    if(key in this.storage) delete this.storage[key]
    this.setStorage()
  }
}
















class IdeZipManager extends IdeStorageManager {

  buildZipExportsToolsAndCbk(jBtn){

    // Add drag&Drop behavior for zip archives:
    jBtn.on("dragenter dragstart dragend dragleave dragover drag", e=>e.preventDefault())

    // Doesn't work using jQuery... (again... x/ ):
    jBtn[0].addEventListener('drop', this.dropArchiveFactory(
      this.lockedRunnerWithBigFailWarningFactory(
        CONFIG.runningMode.zipImport,
        this.setupRuntimeZip,
        this.dropArchive,
        this.teardownRuntimeZip,
        true,
      )
    ))

    return this.lockedRunnerWithBigFailWarningFactory(
      CONFIG.runningMode.zipExport,
      this.setupRuntimeZip,
      this.zipExport,
      this.teardownRuntimeZip,
    )
  }


  async setupRuntimeZip(){
    this.terminal.pause()           // Deactivate user actions in the terminal until resumed
    this.terminal.clear()           // To do AFTER pausing...
    const [runtime,] = await this._baseSetupRuntime()
    return runtime
  }

  async teardownRuntimeZip(runtime){
    this.terminal.resume()
    await this._baseTeardownRuntime(runtime)
  }


  _getDataForExportableIdeInPage(){
    const toArchive = []
    const ideThis   = this

    $(`[id^=editor_]`).each(function(){
      if(localStorage.getItem(this.id)===null){
        return    // should never happen... But just in case...
      }
      const [data,] = ideThis._extractWhateverLocalStorageVersion(this.id)
      data.id = this.id
      if(data.zip){             // Exportable
        toArchive.push(data)
      }
    })
    return toArchive
  }


  _buildZipNameFirstChunks(){
    const zipChunks = []

    if(CONFIG.exportZipPrefix){
      zipChunks.push(CONFIG.exportZipPrefix)
    }
    if(CONFIG.exportZipWithNames){
      let names = ""
      while(!names){
        names = window.prompt(CONFIG.lang.zipAskForNames.msg)
      }
      zipChunks.push(names)
    }
    return zipChunks
  }


  async zipExport(_runtime){
    this.terminalEcho('Generate zip for '+location.href)

    const toArchive = this._getDataForExportableIdeInPage()
    const zipChunks = this._buildZipNameFirstChunks()
    const code      = this._buildZipExportPythonCode(toArchive, zipChunks)
    pyodide.runPython(code)
    this.focusEditor()
  }


  _buildZipExportPythonCode(toArchive, zipChunks){
    const pyJson = JSON.stringify(toArchive).replace(/\\/g, '\\\\')
    return `
@__builtins__.auto_run
def _hack_build_zip():

    import shutil, json
    from pathlib import Path
    from itertools import count

    def unique_name(p:Path):
        while p.exists():
            p = p.with_name(f"{ p.stem }_{ p.suffix }")
        return p

    dirname = unique_name(Path('tmp_zip'))
    dirname.mkdir()

    url    = ${ JSON.stringify(location.href) }
    origin = ${ JSON.stringify(location.origin) }
    chunks = ${ JSON.stringify(zipChunks) }

    # Always make sure the url part of the filename is not empty:
    zip_url = url[len(origin):].strip('/').replace('/','_').replace('.','_') or 'home'
    chunks.append(zip_url)

    zip_name = unique_name( Path( '-'.join(chunks) + '.zip') )

    data = json.loads("""${ pyJson }""")
    for ide in data:
        name = dirname / (ide['id'] + '${ CONFIG.ZIP.pySep }' + ide['name'])
        name.write_text(ide['code'], encoding="utf-8")

    shutil.make_archive(zip_name.with_suffix(''), 'zip', dirname)

    pyodide_downloader(
        zip_name.read_bytes(),
        zip_name.name,
        "application/zip"   # "application/x-zip-compressed" on Windaube...?
                            # => no need (probably because in WASM)
    )
    shutil.rmtree(dirname)
    zip_name.unlink()
`
  }

  dropArchiveFactory(asyncRuntimeConsumer){
    return async ev=>{
      ev.preventDefault()
      CONFIG.loadIdeContent = this.loadIdeContent.bind(this)
      await asyncRuntimeConsumer(ev)
    }
  }


  async dropArchive(ev){
    // https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
    // https://stackoverflow.com/questions/43180248/firefox-ondrop-event-datatransfer-is-null-after-update-to-version-52

    const useItems = Boolean(ev.dataTransfer.items)
    const files = [...ev.dataTransfer[ useItems?'items':'files' ]]

    if(files.length!=1){
      this.giveFeedback("Cannot Import multiple archives.")
      return
    }

    files.forEach((itemOrFile) => {
      if(useItems && itemOrFile.kind !== "file"){
        // If dropped items aren't files, reject them
        return
      }
      this.getZipContentAsBytes( useItems ? itemOrFile.getAsFile():itemOrFile)
    })
  }


  getZipContentAsBytes(file){
    const reader = new FileReader();

    reader.onload = function(event){
      const bytesArr = event.target.result
      pyodide.unpackArchive(bytesArr, "zip", {extractDir: CONFIG.ZIP.tmpZipDir})
      pyodide.runPython(`
@__builtins__.auto_run
def _hack_zip_loading():
    from pathlib import Path
    import js
    loadIdeContent = js.config().loadIdeContent

    tmp_dir = Path('${ CONFIG.ZIP.tmpZipDir }')
    for py in tmp_dir.iterdir():
        content = py.read_text(encoding='utf-8')
        loadIdeContent(py.name, content)
        py.unlink()
    tmp_dir.rmdir()
`)
    }
    reader.readAsArrayBuffer(file)
  }


  loadIdeContent(pyName, code){
    const i        = pyName.indexOf(CONFIG.ZIP.pySep)
    const editorId = pyName.slice(0, i)
    const name     = pyName.slice(i+1)
    const jIde     = $('#'+editorId)

    if(!jIde[0]){
      this.giveFeedback(
        `Couldn't find the IDE #${editorId} in the page (associated python name: ${ name })`
      )
    }else{
      ace.edit(editorId).getSession().setValue(code);
      // No save/localStorage handling at this point (I don't have the IdeRunner object in hand :p )
      this.giveFeedback(`Loaded ${ editorId }${ CONFIG.ZIP.pySep }${ name }.`, "none")
    }
  }
}
















/**Mostly handle various GUI troubles, like:
 *    - Incomplete initialization of IDEs that are in hidden `==== "tabs"`
 *    - Wrong terminal dimensions for this or that reason (generally, also tabs...)
 *
 * Also holds the generic routines that will be used for IDE split screen and full screen modes.
 *
 * NOTE: the constructor also takes in charge some definitions needed only for child classes,
 *       to get a better/easier way to see what values are available.
 * */
class IdeGuiManager extends IdeZipManager {

  /**IDE instance currently in "split screen" mode.
   * */
  static SPLITTED = null

  /**Model to clone, to get the extraline numbers in the gutter perfectly overlapped with the
   * ones added by ACE editors.
   * */
  static INNER_LINE_NUMS = $(
    '<span style="display: none;" tabindex="0"></span><span style="display: none;" tabindex="0"><span></span></span>'
  )


  constructor(editorId){
    super(editorId)

    this.global    = $("#global_"+editorId)
    this.termId    = "term_" + editorId
    this.inputIdH  = "#input_" + editorId
    this.counterH  = "#compteur_" + editorId
    this.solutionH = "#solution_" + editorId

    // Various flags OR data related to split.full screen modes management (only)
    this.guiIdeFlags = {
      gutter: false,                  // Ensured the minIdeLines are written in IDE the gutter
      resizedVertTerm: !this.isVert,  // Flag to know if the terminal size dimensions have already been enforced or not.
      splittedLines: 0,               // nLines (gutter) of the IDE in split mode (0 if not splitted)
      splitSlider: null,              // jQuery object
      initTermH: 0,                   // Initial height of the terminal, before entering any screen mode
      initGlobH: 0,                   // Initial height of this.global, before entering any screen mode
      hasObserver: false,             // (should be actually useless, now) Has already built auto-completion MutationObserver or not
      viewport: window.screen.height,
      ideMinWidth: cssPx(this.global,'min-width'),
      fullScreenPadPx: 15,            // Padding added in full screen mode
      internalIsFullScreen: false,    // Inner flag to handle mixed requests between full and split screen.
                                      // DO NOT use as flag to handle fullscreen behaviors themselves...
    }

    this.editor = null  // ACE object
    this.gutter = null  // ACE object child
    this.delay  = 200   // Delay to wait after clearing the terminal content, (user actions)
    this.getCodeToTest = ()=>this.editor.getSession().getValue()
    this._init()
  }


  /**Process to "re-initiate" the internal state of the IDE (useful for testing) */
  _init(){
    super._init()
    this.hiddenDivContent = true
  }


  get splitScreenActivated() { return IdeGuiManager.SPLITTED }

  get isSplitScreen() { return this === IdeGuiManager.SPLITTED }

  setAsSplitted(that) { IdeGuiManager.SPLITTED = that }


  /**Routines to handle partial UI initializations, mostly for IDEs hidden in `=== "tabs"`
   * whe the page is loaded: applies visual updates conditionally, only if they haven't
   * been applied before.
   * Note that the logic is rather intricate with super calls...
   * */
  makeUpYourGui(){
    if(this.global.is(':hidden')) return false    // Nothing to do yet (tabbed content).

    const todo = [
      this.guiUpdateFillAceGutter(),
      this.resizeVertTerm(),
    ]
    return todo.every(Boolean) && super.makeUpYourGui()
  }


  resizeVertTerm(){
    if(this.guiIdeFlags.resizedVertTerm) return true
    jsLogger("[CheckPoint] - Handle terminal window size")

    const divHeight = $('#'+this.id).css('height')
    this.global.find(".term_editor_v").css("height", divHeight)
    return this.guiIdeFlags.resizedVertTerm=true
  }


  /**Fill the entire gutter with minIdeLines line numbers: those won't disappear when the
   * user is deleting lines (probably because they use "remove first match" kind of logic).
   * */
  guiUpdateFillAceGutter(){
    if(!this.guiIdeFlags.gutter){
      this.fillAceGutter(this.minIdeLines)
    }
    return this.guiIdeFlags.gutter = true
  }


  //-----------------------------------------------------------------------------------


  /**When then current IDE is neither in split nor in full screen mode, store the current height
   * of its terminal so that it can be restored exactly when exiting from both modes.
   * This is needed because the terminal's height is tweaked on the fly to make the display nicer,
   * while the term height is also part of determining how many lines the ace gutter needs.
   * And the css margins dynamically changing at times _OTHER_ than when I compute the lines...
   * and without tracking the initial height, you get terminals that get larger and larger when
   * the user is switching from split to full screen, modes repeatedly...
   * */
  storeInitHeightsIfNeeded(){
    if(!somethingFullScreen() && !this.isSplitScreen){
      this.guiIdeFlags.initTermH = cssPx( this.global.find('.term_wrapper') )
      this.guiIdeFlags.initGlobH = cssPx( this.global )
    }
  }


  /**Fill the entire gutter with minIdeLines line numbers: those won't disappear when the
   * user is deleting lines (probably because they use "remove first match" kind of logic).
   * */
  fillAceGutter(nLines){
    const model   = this.gutter.children().first().clone().removeClass('ace_gutter-active-line').addClass('pmt-gutter')
    const numbers = this.gutter.find('.pmt-gutter')
    const height  = cssPx(model)

    const first_missing = numbers.length

    // Remove extra line numbers:
    for(let i=nLines ; i<first_missing ; i++){
      numbers[i] && numbers[i].remove()
    }

    // Add needed line numbers:
    for(let i=first_missing ; i<=nLines ; i++){
      const elt = model.clone().css('top', (i-1)*height+'px').text(i)
      elt.append(IdeGuiManager.INNER_LINE_NUMS.clone())
      this.gutter.append(elt)
    }
  }


  /**Handle the ACE editor gutter display, enforcing options.minLines line umbers so that
   * the editor fills the desired height in `div.global_editor_xxx`.
   * May adapt the terminal height on the fly, if "required".
   *
   * @param options: object with optional properties:
   *    - setup:    default=true (is setting up the mode or not)
   *    - minLines,maxLines: Resulting values to set on the ACE editor. If not given,
   *                computed automatically on the fly.
   *    - topDivH:  The max height space currently available for the #pmt-top-div element.
   * */
  ideScreenModeVerticalResize(options={}){

    let {setup, minLines, maxLines, topDivH, goFullScreen} = {
      setup:true, topDivH:Infinity, goFullScreen:false, ...options
    }
    const exitingScreenMode = minLines !== undefined

    const term  = this.global.find('.term_editor')
    let   termH = this.guiIdeFlags.initTermH

    if(exitingScreenMode){
      this.global.css('padding', '0')

    }else{
      this.global.css('padding', this.guiIdeFlags.fullScreenPadPx)

      const btns  = this.global.find('.ide_buttons_div_wrapper')
      const lineH = cssPx( this.global.find('div.ace_gutter-layer').children().first() )
      const btnsH = cssPx(btns) + cssPx(btns,'margin-top') //+ cssPx(btns,'margin-bottom')

      const globH = - 2 * this.guiIdeFlags.fullScreenPadPx + (
        goFullScreen ? this.guiIdeFlags.viewport : Math.min(cssPx(this.global), topDivH)
      )

      // Do not allow terminal + buttons to fill more than half the height:
      const halfMinusBtns = globH/2 - btnsH
      if( !this.isVert && termH > halfMinusBtns){
        termH = halfMinusBtns
      }

      // Sliders on windaube are HUGE, so reduce by one, whatever the case.
      const availableH = globH - btnsH - termH * !this.isVert
      const nLines     = Math.max(
        3,  // Keep as min, so that the buttons on the editor stay on different lines
        Math.max(1, Math.floor( availableH/lineH )) - isWin
      )

      // Fix the exact terminal height so that the bottom space is always consistent:
      if(!this.isVert){
        termH = Math.max(termH, globH - btnsH - lineH*nLines)
      }

      // Set the actual number of lines to "lock" for the ACE editor:
      minLines = maxLines = nLines

      jsLogger('[ScreenMode]', "Computed minLines =", minLines)
      jsLogger('[ScreenMode]', {globH, termH, btnsH, availableH, lineH})
    }

    this.editor.setOptions({minLines, maxLines})
    this.fillAceGutter(minLines)
    this.editor.resize()

    term.css('resize', setup||this.isVert ? 'unset' : 'vertical')
    term.css("height", (setup ? termH : this.guiIdeFlags.initTermH)+'px')

    jsLogger('[ScreenMode]', "IDE resizing done -", this.editor.getOption('minLines'), this.editor.getOption('maxLines'))
  }
}















class IdeFullScreenGlobalManager {

  static currentIde = null
  static someMenuOpened = false


  /**Identify if the given jQuery node is one related to a context menu (ACE auto-completion,
   * ACE menu, or commands).
   * */
  static isSomeAceMenu(jNode){
    return (
           jNode.children(CONFIG.element.aceSettings).length && "menu"
        || jNode.children(CONFIG.element.aceF1Cmds).length && "F1"
        || jNode.hasClass(CONFIG.element.aceAutoComplete) && "auto-complete"
    )
  }


  static setMenusFlag(isVisibleAndNow) {
    if(isVisibleAndNow){
      IdeFullScreenGlobalManager.someMenuOpened=true
    }else{
      // The menu flag has to be unset with a significant delay, otherwise the keydown event sees
      // the updated status. Note that the delay only applies to an internal state, so it doesn't
      // have any visible effect on the user's side.
      setTimeout(()=>{IdeFullScreenGlobalManager.someMenuOpened=false}, 150)
    }
  }


  /**Handling the various context menus, to try to forbid going full screen when the auto-completion
   * tool, ace settings or ace command window are opened requires to keep track of what is currently
   * or has been added to the body tag.
   *
   * Notes:
   *  - Same logic _while_ in full screen cannot be applied because there is no control over the
   *    escape button keypress event, there.
   *  - The global state must be tracked, because the resolution order of the Escape keypress
   *    closes the menu before the fullscreen related key event is triggered...
   *  - Added once only per page...
   * */
  static buildBodyObserver(){
    new MutationObserver((records)=>{

      for(const record of records) {

        for (const node of record.removedNodes) {
          const kind = this.isSomeAceMenu($(node))
          if(kind && kind!='auto-complete') this.setMenusFlag(false)
          // The auto-complete window will be extracted as soon as it's added, so ignore it.
        }

        for(let node of record.addedNodes) {
          node = $(node)
          const kind = this.isSomeAceMenu(node)
          if(!kind) continue

          this.setMenusFlag(true)
          switch(kind){

            case 'menu':
              node.find('table')
                  .addClass('dummyclass')     // To deactivate css background rule for pmt
                  .css('font-size','10px')
              break

            case 'auto-complete':
              if(!this.currentIde.guiIdeFlags.hasObserver){
                this.currentIde.guiIdeFlags.hasObserver=true
                new MutationObserver(records=>{
                  for(const record of records){
                    const isVisible = $(record.target).css('display')!='none'
                    this.setMenusFlag(isVisible)
                  }
                }).observe(node[0], {attributeFilter:['style']})
              }
              break
          }

          if(somethingFullScreen() || kind=='auto-complete'){
            node.detach().appendTo(this.currentIde.global)
            /* Always move the auto-complete window because:
                  - each IDE has its own window
                  - this allows to add one single style observer the first time the
                    auto-completion tool is used for that IDE */
          }
        }
      }
    }).observe(document.body, {childList: true})
  }
}

IdeFullScreenGlobalManager.buildBodyObserver()












class IdeFullScreenManager extends IdeGuiManager {


  switchFullScreenFromButton(){
    if(!somethingFullScreen()){
      this.requestFullScreen()
    }else{
      document.exitFullscreen()
    }
  }


  /**Finalize the IDE layout once full screen mode has been setup by the browser, then
   * wait for the exit. This is not done through an event, because it might happen in
   * different ways (Esc, click "full screen" or "split screen" buttons), requiring
   * different results/behaviors.
   * */
  requestFullScreen(){
    this.storeInitHeightsIfNeeded()
    this.global[0].requestFullscreen().then(async _=>{
      jsLogger('[ScreenMode]', "Full screen ready")

      const splitScreenBtn = this.global.find(".ide-split-screen")

      // Just in case the user used a button without typing anything in the editor yet.:
      IdeFullScreenGlobalManager.currentIde = this
      splitScreenBtn.addClass('deactivated')
      this.guiIdeFlags.internalIsFullScreen = true
      this.ideScreenModeVerticalResize({goFullScreen: true})

      // Wait forever if needed...
      jsLogger('[ScreenMode]', "Full screen setup - DONE")

      while(somethingFullScreen()) await sleep(50)

      const minLines = this.guiIdeFlags.splittedLines || this.minIdeLines
      const maxLines = this.guiIdeFlags.splittedLines || this.maxIdeLines
      jsLogger('[ScreenMode]', "Full screen reversion", minLines, maxLines)

      this.ideScreenModeVerticalResize({setup:false, minLines, maxLines})
      this.guiIdeFlags.internalIsFullScreen = false
      if(this.splitScreenActivated) splitScreenBtn.removeClass('deactivated')
      IdeFullScreenGlobalManager.currentIde = null

      jsLogger('[ScreenMode]', "Full screen reversion - DONE")
    })
  }
}













class IdeSplitScreenManager extends IdeFullScreenManager {


  /**Set the pmt-top-div height so that it occupies the whole viewport.
   * */
  setupTopDivHeight(topDiv, header){
    topDiv ??= $("#"+CONFIG.element.pmtTopDiv)
    if(!topDiv[0]) return;
    const headerHpx = ( header ?? $('body > header') ).css('height')
    topDiv.css('height', `calc( 100vh - ${ headerHpx })`)
    return cssPx(topDiv)
  }


  async switchSplitScreenFromButton(e, autoScroll=true){

    this.storeInitHeightsIfNeeded()
    const wasFullScreen = somethingFullScreen()

    if(wasFullScreen){
      jsLogger('[ScreenMode]', "Exit full screen mode")
      document.exitFullscreen()

      // Everything is async with various delays/things waiting on ea ch others, so wait
      // for the internal flag instead of document.fullscreenElement, so that the IDE can
      // apply its logic when exiting it.
      while(this.guiIdeFlags.internalIsFullScreen) await sleep(50)
      await sleep(50)  // Extra delay so that the logic in `requestFullScreen.then` finishes

      jsLogger('[ScreenMode]', "Full screen mode exited")
    }

    const swapColumns = e && (e.originalEvent.ctrlKey || isMacOs && e.originalEvent.metaKey)
    this.switchSplitScreen(swapColumns, wasFullScreen, autoScroll)
  }



  /**Go "in" or "out" of "split screen" mode for the current IDE instance, handling
   * the possible initial states, like:
   *
   *    - If currently in full screen:
   *          1. exit full screen
   *          2. set current IDE in split mode
   *    - If another IDE is currently in split screen mode:
   *          1. make it exit split screen
   *          2. set current IDE in split mode
   *    - If the current IDE is in split screen mode:
   *          1. make it exit split screen
   *
   * This involves DOM reorganizations, moving entire parts of it here or there...
   * */
  switchSplitScreen(swapColumns, fromFullScreen, autoScroll=true){

    // Allow to switch from one IDE to another, staying in "split" mode:
    if(this.splitScreenActivated && !this.isSplitScreen){
      jsLogger('[ScreenMode]', "Exit previous splitted")
      this.splitScreenActivated.switchSplitScreen(swapColumns, false)
    }
    const topDivId = CONFIG.element.pmtTopDiv
    const topDiv   = $(document.getElementById(topDivId) ?? `<div id="${ topDivId }"></div>`)

    // Check for columns reversion request only:
    if(this.isSplitScreen && swapColumns){
      topDiv.append(
        topDiv.children().get().map(elt=>$(elt).detach()).reverse()
      )
      return;
    }

    const setup    = !this.isSplitScreen || fromFullScreen
    const header   = $('body > header')
    const page     = $("div.md-container")
    const splitBtn = this.global.find(".ide-split-screen")
    const srcRepl  = this._getPlaceholder()
    const slider   = this._getSlidingElement(topDiv)
    const headerH  = cssPx(header)

    const changes  = setup ? {
      log: 'Setup',
      rearrangeDom: ()=>{ topDiv.insertAfter(header)
                          const order = [page, slider, this.global]
                          if(swapColumns) order.reverse()
                          topDiv.append(order)
                          const topDivH = this.setupTopDivHeight(topDiv, header)
                          srcRepl.insertBefore($(this.solutionH))
                          return {topDivH}
                        },
      ideResizeArgs:      {setup},
      splitBtnClass:     'remove',
      splitIdeClass:     'add',
      SPLITTED_becomes:   this,
      splittedLinesFlag:  this.editor.getOption('minLines'),
      scrollRefBefore:    this.global,
      scrollRefAfter:     srcRepl,
      eltToScroll:        page[0],
    }:{
      log: 'Teardown',
      rearrangeDom: ()=>{ page.insertAfter(header)
                          slider.find('button').off()
                          srcRepl.replaceWith(this.global)
                          topDiv.remove()
                          return {}
                        },
      ideResizeArgs:      {setup, minLines:this.minIdeLines, maxLines:this.maxIdeLines},
      splitBtnClass:     'add',
      splitIdeClass:     'remove',
      SPLITTED_becomes:   null,
      splittedLinesFlag:  0,
      scrollRefBefore:    srcRepl,
      scrollRefAfter:     this.global,
      eltToScroll:        window,
      initHeight:         this.guiIdeFlags.initGlobH,
    }

    //------------------------------------------------------------

    jsLogger('[ScreenMode]', changes.log, "split screen mode")

    // BEFORE detaching anything:
    let topSrc = changes.scrollRefBefore[0].getBoundingClientRect().top


    // Reorganize the DOM:
    page.detach()
    this.global.detach()
    const data = changes.rearrangeDom()


    // Resize the IDE once moved, adding or removing line numbers to fill appropriately
    // the space when needed:
    if('topDivH' in data) changes.ideResizeArgs.topDivH = data.topDivH
    this.ideScreenModeVerticalResize(changes.ideResizeArgs)


    // Update various tracked values or UI element classes:
    splitBtn[    changes.splitBtnClass+'Class' ]('deactivated')
    this.global[ changes.splitIdeClass+'Class' ]('split')
    this.guiIdeFlags.splittedLines = changes.splittedLinesFlag
    this.setAsSplitted(changes.SPLITTED_becomes)


    // Handle the final scroll position once everything is in place, keeping the original placement
    // as much as possible, unless the moved element would end up outside of the viewport.
    if(autoScroll){
      const viewH = window.innerHeight || document.documentElement.clientHeight
      const box   = changes.scrollRefAfter[0].getBoundingClientRect()

      if(topSrc < headerH || topSrc > viewH-50){
        const eltH = changes.initHeight ?? box.height
        topSrc = headerH + Math.max(50, (viewH - eltH) / 2)
      }
      changes.eltToScroll.scrollBy(0, box.top - topSrc)
    }

    jsLogger('[ScreenMode]', "split handling - DONE")
  }


  /**Build or extract the IDE placeholder element (jQuery).
   * */
  _getPlaceholder(){
    const placeholderId  = "pmt-ide-placeholder"
    const placeholderMsg = CONFIG.lang.splitModePlaceholder.msg
    const placeholder    = `<div id="${ placeholderId }">${ placeholderMsg }</div>`
    const jPlaceholder   = $(document.getElementById(placeholderId) ?? placeholder)
    return jPlaceholder
  }


  /**Build or extract the slider element to move the vertical separation (jQuery).
   * */
  _getSlidingElement(topDiv){
    const sliderWrapperID = "pmt-slider-div"
    const sliderId        = "pmt-split-slider"
    const sliderElements  = `<div id="${ sliderWrapperID }-div"><div id="${ sliderWrapperID }"><button id="${ sliderId }"></button></div></div>`
    const limit           = this.guiIdeFlags.ideMinWidth

    let slider = $(sliderWrapperID)
    if(!slider[0]){
      slider = $(sliderElements)
      slider.on('dblclick', function(){topDiv.css('grid-template-columns', `50% min-content auto`)})
      slider.on('mousedown', function(){
        topDiv.on('mouseup', _=>{ topDiv.off() })
        topDiv.on('mousemove', function(e){
          const width = cssPx(topDiv,'width')
          if(width > 2*limit){
            const col1  = Math.min( Math.max(limit, e.originalEvent.pageX), width-limit)
            const col1p = (100 * col1/width).toFixed(1)
            topDiv.css('grid-template-columns', `${ col1p }% min-content auto`)
          }
        })
      })
    }

    return slider
  }
}














/**Handle all elements of logics related to giving some kind of feedback to the user
 * (through terminal, UI colors, ...),
 */
class IdeFeedbackManager extends IdeSplitScreenManager {


  /**Relay method, to transfer stdout content from pyodide to the jQuery.terminal.
   * If @isPrint is true, the call has been done through the `bi_print` python function.
   * If @isPrint is false, then the call has been done through the `terminal_message` function.
   *
   * When the stdout is deactivated and @isPrint is false, the @key argument is required to
   * match the one given through the IDE macro `STD_KEY` argument.
   * */
  termFeedbackFromPyodide(key, msg, format, isPrint=false, newline=undefined){
    const hidden    =  isPrint && !this.allowPrint
    const forbidden = !isPrint && !this.allowPrint && key != this.stdKey
    if(forbidden){
      throw new PythonError("Cannot print to the terminal.")
    }
    if(!(isPrint && hidden)){
      super.termFeedbackFromPyodide(null, msg, format, isPrint, newline ?? !isPrint)
    }
  }


  /**Unconditionally update the counter of attempts with the given value.
   * */
  setAttemptsCounter(nAttempts){
    this.data.attempts_left = nAttempts
    $(this.counterH).text(nAttempts)
  }


  updateValidationBtnColor(done=undefined){
    done ??= this.storage.done
    const color = !done ? "unset" : done<0 ? 'red' : 'green'
    this.global.find("button[btn_kind=check]").css('--ide-btn-color',  color)
  }


  //----------------------------------------------------------------------------------


  /**If the current action has been successful until now, display the appropriate
   * message in the terminal.
   * */
  codeSnippetEndFeedback(runtime, step, code){
    if(runtime.stopped || !step) return

    const playing = this.isPlaying()
    const intro   = playing ? "" : CONFIG.lang.validation.msg
    const section = CONFIG.lang[step].msg
    const ok      = CONFIG.lang.successMsg.msg

    let msg = `${ intro }${ section }: ${ ok }`   // Default section message
    if(!code) msg = ""                            // No default message if no code in the section...
    if(playing && !this.hasCheckBtn){             // ...but ensure the default ending message is shown,
      msg = CONFIG.lang.successMsgNoTests.msg     //    if this is "playing" dans nothing else to do after.
    }

    if(msg) this.terminalEcho(msg)

    // If no error yet and a validation button is present while running the editor's code only,
    // prepare a "very final" message reminding to try the validations:
    if(playing && this.hasCheckBtn){
      runtime.finalMsg = CONFIG.lang.unforgettable.msg
    }
  }



  /**Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
   * is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
   *
   * Do not forget that any error related feedback has already been printed to the console, so
   * when it comes to feedback given in this method, it's only about a potential "final message".
   * */
  handleRunOutcome(runtime, allowCountDecrease){
    const success      = !runtime.stopped
    const isDelayed    = this.profile === CONFIG.PROFILES.delayedReveal
    const someToReveal = this.corrRemsMask && this.hiddenDivContent && (!this.profile || isDelayed)

    jsLogger("[CheckPoint] - handleRunOutcome")
    // console.log("[OutCome]", JSON.stringify({ success, pof:this.profile, revealable, hidden:this.hiddenDivContent, allowCountDecrease: !!allowCountDecrease, mask:this.corrRemsMask, N:this.attemptsLeft}))

    this.setStorage({done: success ? 1:-1 })
    this.updateValidationBtnColor()

    if(allowCountDecrease && (!success || isDelayed)){
      this.decreaseIdeCounter()
    }

    // Reveal if success and not delayed, or if attempts==0 (means last error, are last delayed)
    const isRevelation =  someToReveal && (success && !isDelayed || this.attemptsLeft===0)

    /*If success, a custom final message has to be built:
          - If the revelation already occurred, return no message at all
          - If some profile forbids the revelation, or if nothing to reveal, just congratulate the user.
          - Make sure a success on "delayed" profile doesn't trigger a final message.

      WARNING: someToReveal is different from "already revealed".
     */
    const isSuccessNoReveal = success && this.hiddenDivContent && !isDelayed

    if(isRevelation){
      jsLogger("[OutCome]", 'reveal!', success)
      runtime.finalMsg = success ? this._buildSuccessMessage(someToReveal, isDelayed)
                                 : this._getSolRemTxt(false)
      this.revealSolutionAndRems()

    }else if(isSuccessNoReveal){
      // Always display the "bravo" message on success, if corr&REMs exist but are not revealable
      runtime.finalMsg = this._buildSuccessMessage(someToReveal, isDelayed)
    }
  }


  /**Decrease the number of attempts left, EXCEPT when:
   *    - the solution is already revealed,
   *    - the number of attempts is infinite,
   *    - there are no attempts left (redundant with revelation condition, but hey...).
   */
  decreaseIdeCounter(){
    jsLogger("[CheckPoint] - decreaseIdeCounter")
    if(!this.hiddenDivContent) return    // already revealed => nothing to change.

    // Allow going below 0 so that triggers once only for failure.
    const nAttempts = Math.max(-1, this.attemptsLeft - 1)

    // Update the GUI counter if needed:
    if(Number.isFinite(nAttempts) && nAttempts >= 0){
      this.setAttemptsCounter(nAttempts)
    }
  }


  /**Reveal corr and/or REMs (visible or not) contents.
   * When reaching this method, it is already sure by contract, that the revelation must occur.
   * The only piece of contract this method is holding is that if flags the revelation as done,
   * and it decides if the div content has to be decompressed or not on the way.
   * */
  revealSolutionAndRems(waitForMathJax=false){
    jsLogger("[CheckPoint] - Enter revealSolutionAndRems")
    // Need to check here one more time against hiddenDivContent because of the "show" button logic.
    if(this.hiddenDivContent){
      jsLogger("[CheckPoint] - revealed!")

      const sol_div = $(this.solutionH)

      if(this.isEncrypted){
        const compressed = sol_div.text().trim()
        const content    = compressed && decompressLZW(compressed, "ides.encrypt_corrections_and_rems")
        sol_div.html(content)
        this.data.is_encrypted = false  // Never decompress again
      }
      sol_div.attr('class', '')         // Unhide
      this.hiddenDivContent = false     // Never reveal again (last in case of errors...)

      // Enforce formatting
      if(waitForMathJax){
        subscribeWhenReady(
          "revealOnLoad", mathJaxUpdate, {runOnly:true, waitFor:()=>CONFIG.subscriptionReady.mathJax}
        )
      }else{
        mathJaxUpdate()
      }

      /* DOESN'T WORK
      // Enforce mermaid rendering if any
      try{
        // Need to make an async call, but i don't want to make this method an async one...
        setTimeout(async ()=>console.log('yup?') || await mermaid.run())
      }catch(e){}
      //*/
    }
  }


  /**If @isDelayed is true, there are no tests/secrets, so:
   *    - Do not congratulate the user
   *    - if something revealable, announce the revelation, otherwise say nothing special
   *
   * If @isDelayed is false, build:
   *    - the complete success message if something to reveal
   *    - only the bravo message otherwise.
   */
  _buildSuccessMessage(revealable, isDelayed){
    const moreInfo = revealable ? this._getSolRemTxt(true) : ""
    if(isDelayed){
      return moreInfo && txtFormat.stress(moreInfo)
    }
    const emo = choice(CONFIG.MSG.successEmojis)
    return `${ CONFIG.lang.successHead.msg } ${ emo } ${ CONFIG.lang.successHeadExtra.msg }${ moreInfo }`
  }


  /**Routine building the final success or failure message, assembling the various parts
   * of CONFIG.lang as needed.
   * */
  _getSolRemTxt(isSuccess){
    if(!this.corrRemsMask) return ""

    const hasCorr  = this.corrRemsMask & 1
    const hasRems  = this.corrRemsMask & 2
    const hasBoth  = this.corrRemsMask == 3
    const msg      = []
    const sentence = []

    const pushSentence = (prop,kind='msg') => sentence.push(CONFIG.lang[prop][kind])

    msg.push( isSuccess
      ? "\n"+CONFIG.lang.successTail.msg
      : CONFIG.lang.failHead.msg
    )

    if(hasCorr) pushSentence('revealCorr')
    if(hasBoth) pushSentence('revealJoin')
    if(hasRems) pushSentence('revealRem')

    if(!isSuccess){
      // Ensure capitalization of the beginning of the error feedback
      if(sentence.length){
        sentence[0] = _.capitalize(sentence[0])
      }
      const kind = hasBoth || hasRems ? 'plural':'msg'
      pushSentence('failTail', kind)
    }

    msg.push(...sentence)
    const output = msg.join(' ').trimEnd() + "."

    // console.log("[OutComeSolRemTxt]", JSON.stringify({isSuccess, msg, mask:this.corrRemsMask, sentence, output}))
    return output
  }
}














/**Holds the running/code management logistic for IdeRunner.
 * */
class IdeRunnerLogic extends IdeFeedbackManager {


  /**Is the current action "running the public tests"?
   * */
  isPlaying(){  return this.running.includes(CONFIG.runningMode.play) }

  /**Is the current action "running the validation tests"?
   * */
  isChecking(){ return this.running.includes(CONFIG.runningMode.validate) }


  /**Does nothing, but catch any call on the parent class, which would raise an error
   * because prefillTerm is undefined, for IDEs.
   * */
  prefillTermIfAny(){}


  // @OVERRIDE
  async applyAutoRun(){
    await this._defaultAutoRun()
  }


  /**Add the `tests` section to the given code, joining them with the appropriated
   * string/comment if needed.
   * */
  _joinCodeAndPublicSections(userCode){
    const editorCode = [ userCode, this.publicTests ].filter(Boolean).join(CONFIG.lang.tests.msg)
    return editorCode
  }



  applyCodeToEditorAndSave(exerciseCode, doSave=true){
    exerciseCode ||= ""
    this.editor.getSession().setValue(exerciseCode);
    if(doSave) this.save(exerciseCode)
  }


  /**Build (or extract if allowed) the initial code to put in the editor.
   * */
  getStartCode(attemptLocalStorageExtraction=false){
    let exerciseCode = ""

    if(attemptLocalStorageExtraction){
      exerciseCode = this.storage.code
    }
    if(!exerciseCode){
      exerciseCode = this._joinCodeAndPublicSections(this.userContent)
    }

    // Enforce at least one empty line of code in the editor, so that the terminal prompt
    // is always visible for IDEv:
    exerciseCode = exerciseCode.replace(/\n+$/,'')
    if(!exerciseCode) exerciseCode = '\n'

    return exerciseCode+"\n"
  }


  setStartingCode(options={}){

    const {extractFromLocalStorage, saveOnceApplied} = {
      extractFromLocalStorage:false,
      saveOnceApplied:true,
      ...options
    }
    const code = this.getStartCode(extractFromLocalStorage)
    this.applyCodeToEditorAndSave(code, saveOnceApplied)
    return code
  }


  /**Things to display in the terminal at the very beginning of the executions.
   * */
  terminalDisplayOnIdeStart(){
    this.terminalEcho(CONFIG.lang.runScript.msg)
  }



  async setupRuntimeIDE() {
    jsLogger("[CheckPoint] - setupRuntimeIDE IdeRunner")

    this.terminalAutoWidthOnResize()

    // Save before anything else, in case an error occurs somewhere...
    const editorCode = this.getCodeToTest()
    this.save(editorCode)
    this.storeUserCodeInPython('__USER_CODE__', editorCode)

    this.terminal.pause()             // Deactivate user actions in the terminal until resumed
    this.terminal.clear()             // To do AFTER pausing...
    this.terminalDisplayOnIdeStart()  // Handle the terminal display for the current action
    await sleep(this.delay)           // Terminal "blink", so that the user always sees a change
    this.alreadyRanEnv = true

    return this.setupRuntime()
  }



  async teardownRuntimeIDE(runtime) {
    jsLogger("[CheckPoint] - IdeRunner teardownRuntime")

    // Restore default state first, in case a validation occurred (=> restore stdout behaviors!)
    runtime.refreshStateWith()

    // Handle any extra final message (related to revelation of solutions & REMs)
    if(runtime.finalMsg) this.giveFeedback(runtime.finalMsg, null)

    await this.teardownRuntime(runtime)

    this.storeUserCodeInPython('__USER_CODE__', "")
  }



  //--------------------------------------------------------------------



  /**Build the public tests runner routine.
   * */
  playFactory(runningMan=CONFIG.runningMode.play){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.playThroughRunner,
      this.teardownRuntimeIDE,
    )
  }


  async playThroughRunner(runtime){
    const code = this.getCodeToTest()
    await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, CONFIG.section.editor)
  }



  //--------------------------------------------------------------------



  /**Build the validation tests runner routine.
   * */
  validateFactory(runningMan=CONFIG.runningMode.validate){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.validateThroughRunner,
      this.teardownRuntimeIDE,
    )
  }


  async validateThroughRunner(runtime){

    // env section is behaving like the editor one (should be changed...?)
    let decrease_count = this.canDecreaseAttempts(CONFIG.section.editor)

    // If an error already occurred, stop everything...
    if(runtime.stopped){

      // ... but decrease the number attempts and run teardown if this was AssertionError.
      if(runtime.isAssertErr){
        this.handleRunOutcome(runtime, decrease_count)
      }

    }else{

      const validation_state = {
        autoLogAssert:    this.autoLogAssert,
        purgeStackTrace:  this.showOnlyAssertionErrorsForSecrets,
        withStdOut:      !this.deactivateStdoutForSecrets,
      }
      const toRun = [
        [this.getCodeToTest(), CONFIG.section.editor,  {}],
        [this.publicTests,     CONFIG.section.public,  validation_state],
        [this.secretTests,     CONFIG.section.secrets, validation_state],
      ]

      for(const [code, testSection, state] of toRun){
        jsLogger("[CheckPoint] - Run validation step:", testSection)

        runtime.refreshStateWith(state)
        await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, testSection)

        if(runtime.stopped){
          decrease_count = this.canDecreaseAttempts(testSection)
          break
        }
      }

      // Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
      // is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
      this.handleRunOutcome(runtime, decrease_count)
    }
  }


  /**Return true if the current section allow to decrease the number of attempts,
   * during a validation.
   * */
  canDecreaseAttempts(testSection){
    const wanted      = CONFIG.section[ this.decreaseAttemptsOnUserCodeFailure ]
    const allowedFrom = CONFIG.sectionOrder[ wanted ]
    const currentAt   = CONFIG.sectionOrder[ testSection ]
    const canDecrease = currentAt >= allowedFrom
    return canDecrease
  }



  //--------------------------------------------------------------------



  /**Build the correction validation runner routine.
   * NOTE: the pyodideLock setup is not correct here (swaps done outside of it), but it shouldn't
   *       ever cause troubles, as long as this method is not used in the IdeTester objects.
   * */
  validateCorrFactory(){
    const cbk = this.validateFactory()
    const wrapper = async (e)=>{
      jsLogger("[CheckPoint] - corr_btn start")

      const codeGetter   = this.getCodeToTest
      const currentCode  = this.getCodeToTest()
      const profile      = this.profile
      this.getCodeToTest = ()=>this.corrContent
      this.data.profile  = null    // REMINDER: getters without setters, so need inner update!

      let out
      try{
        out = await cbk(e)
      }finally{
        jsLogger("[CheckPoint] - corr_btn validation done")
        this.data.profile  = profile
        this.getCodeToTest = codeGetter
        this.save(currentCode)     // Ensure the corr content doesn't stay stored in localStorage
      }
      return out
    }
    return wrapper
  }
}















class IdeRunner extends IdeRunnerLogic {


  /**Process to "re-initiate" the internal state of the IDE (useful for testing) */
  _init(){
    super._init()
    this.srcAttemptsLeft = this.attemptsLeft
  }


  // @Override
  build(){

    // Create and define this.editor + fill code content + define all needed listeners:
    this.setupAceEditor()
    this.bindIdeButtons()

    // Try to restore a previous session, or extract default starting code, but skip  localStorage
    // update (this way, the user is not bothered with updates of the starting content of an IDE
    // they didn't even tried yet, when the author is making updates):
    this.setStartingCode({extractFromLocalStorage: true, saveOnceApplied: false})
    this.editor.resize();

    super.build()

    this.announceCodeChangeBasedOnSrcHash()

    // Add the resize listener (because of the intermediate div wrappers, IDE's terminal
    // will not resize automatically):
    window.addEventListener( 'resize', _.throttle(
      this.windowResizeHandler.bind(this), 50, {leading:false, trailing:true}
    ))

    if(this.profile===CONFIG.PROFILES.revealed){
      this.revealSolutionAndRems(true)
    }
    if(this.twoCols){
      this.switchSplitScreenFromButton(null, false)
    }
  }



  /**Create and setup the ACE editor for the current Ide instance.
   * */
  setupAceEditor() {

    // https://github.com/ajaxorg/ace/wiki/Configuring-Ace
    const options = {
        autoScrollEditorIntoView: false,
        copyWithEmptySelection:   true,               // active alt+flèches pour déplacer une ligne, aussi
        enableBasicAutocompletion:true,
        enableLiveAutocompletion: false,
        enableSnippets:           true,
        tabSize:                  4,
        useSoftTabs:              true,               // Spaces instead of tabs
        navigateWithinSoftTabs:   false,              // this is _fucking_ actually "Atomic Soft Tabs"...
        printMargin:              false,              // hide ugly margins...
        maxLines:                 this.maxIdeLines,
        minLines:                 this.minIdeLines,
        mode:                     "ace/mode/python",
        theme:                    getTheme(),
        fontSize:                 CONFIG.editorFontSize,
        fontFamily:               [CONFIG.editorFontFamily, "Monaco", "Menlo", "Ubuntu Mono", "Consolas",
                                   "Source Code pro", "source-code-pro", "monospace"],   // Fix apple troubles...
    }

    this.editor = ace.edit(this.id, options);
    this.runner = this.playFactory()
    this.gutter = this.global.find('div.ace_gutter-layer')

    if(CONFIG._devMode) CONFIG.editors[this.id] = this.editor

    // Kbd shortcuts:
    this.editor.commands.bindKey(
        { win: "Ctrl-Space", mac: "Cmd-Space" }, "startAutocomplete"
    )
    this.editor.commands.addCommand({
        name: "commentTests",
        bindKey: { win: "Ctrl-I", mac: "Cmd-I" },
        exec: this.toggleComments.bind(this),
    })
    this.editor.commands.addCommand({
        name: "runPublicTests",
        bindKey: { win: "Ctrl-S", mac: "Cmd-S" },
        exec: this.runner,
    })
    if(this.hasCheckBtn){
      this.editor.commands.addCommand({
        name: "runValidationTests",
        bindKey: { win: "Ctrl-Enter", mac: "Cmd-Enter" },
        exec: this.validateFactory(),
      })
    }

    // Content of the editor is saved every `CONFIG.ideKeyStrokesSave` keystrokes:
    let nChange = 0;
    this.editor.addEventListener("input", _=>{
        if(nChange++ >= CONFIG.ideKeyStrokesSave){
          nChange=0
          this.save()
        }
    })
  }



  bindIdeButtons(){

    // Register the IDe currently in use
    this.global.on('keydown', ()=>IdeFullScreenGlobalManager.currentIde=this)

    // Add fullscreen activation binding, but NOT through the ACE editor (cannot control the exit)
    this.global.on('keyup', this.respondToEscapeKeyUp.bind(this))

    // Bind editor extra buttons:
    this.global.find(".comment.tooltip" ).on("click", this.toggleComments.bind(this))
    this.global.find(".ide-full-screen" ).on("click", this.switchFullScreenFromButton.bind(this))
    this.global.find(".ide-split-screen").on("click", this.switchSplitScreenFromButton.bind(this))
                                         .addClass('deactivated')


    // Bind all buttons below the IDE
    const ideThis = this
    this.global.find("button").each(function(){
      const btn  = $(this)
      const kind = btn.attr('btn_kind')
      let callback

      switch(kind){
        case 'play':      callback = ideThis.playFactory() ; break
        case 'check':     callback = ideThis.runner = ideThis.validateFactory()
                          ideThis.updateValidationBtnColor()
                          break

        case 'download':  callback = _=>ideThis.download() ; break
        case 'upload':    callback = _=>uploader( txt=>{
                                        ideThis.applyCodeToEditorAndSave(txt)
                                        ideThis.focusEditor()
                                      }) ; break

        case 'restart':   callback = _=>ideThis.restart() ; break
        case 'save':      callback = _=>{ideThis.save(); ideThis.focusEditor()} ; break
        case 'zip':       callback = ideThis.buildZipExportsToolsAndCbk(btn) ; break

        case 'corr_btn':  if(!CONFIG.inServe) return;
                          callback = ideThis.validateCorrFactory() ; break
        case 'show':      if(!CONFIG.inServe) return;
                          callback = ()=>ideThis.revealSolutionAndRems() ; break

        default:          throw new Error(`Y'should never get there, mate... (${ kind })`)
      }
      btn.on('click', callback)
    })
  }


  // @Override
  getTerminalBindings(){

    // Ensure the focus is given back to the terminal after an action triggered from it!
    const asyncTermFocus=(cbk)=>async e=>{
      await cbk(e)
      this.editor.blur()
      this.terminal.focus()
    }
    return ({
      ...super.getTerminalBindings(),
      'CTRL+I': asyncTermFocus(this.toggleComments.bind(this)),
      'CTRL+S': asyncTermFocus(this.playFactory()),
      ...(!this.hasCheckBtn ? {} : {'CTRL+ENTER': asyncTermFocus(this.validateFactory())} ),
    })
  }


  windowResizeHandler(){
    // When going full screen the resize would trigger this logic, hile the computations have
    // already been done correctly (with goFullScreen argument), so skip:
    if(this.isSplitScreen && !somethingFullScreen()){
      const topDivH = this.setupTopDivHeight()
      this.ideScreenModeVerticalResize({topDivH})
    }
    this.terminalAutoWidthOnResize()
  }


  async respondToEscapeKeyUp(event){
    if(event.key!='Escape' || IdeFullScreenGlobalManager.someMenuOpened) return;
    // if(this.splitScreenActivated){
    //   await this.switchSplitScreenFromButton(event)
    //   // This makes impossible to go from split to full screen using Esc+Esc (browser limitation)
    // }else
    if(!somethingFullScreen()){
      this.requestFullScreen()
    }
    // The browser already handles on its own going out of fullscreen with escape => no else needed
  }


  //--------------------------------------------------------------



  /**Extract the current content of the given editor, explore it, and toggle all the LOCs
   * found after the `TestToken` token.
   *
   * Rules for toggling or not are:
   *      - leading spaces do not affect the logic.
   *      - comment out if the first non space character is not "#".
   *      - if the first non space char is "#" and there is no spaces after it, uncomment.
   * */
  toggleComments(e) {
    if(e && e.preventDefault) e.preventDefault()

    const codeLines   = this.getCodeToTest().split('\n')
    const pattern     = CONFIG.lang.tests.as_pattern
    const iTestsToken = codeLines.findIndex(s=>pattern.test(s))

    /// No tests found:
    if(iTestsToken<0) return;

    const toggled = codeLines.slice(iTestsToken+1).map(s=>{
        return s.replace(CONFIG.COMMENTED_PATTERN, (_,spaces,head,tail)=>{
            if(head=='#' && tail!=' ') return spaces+tail
            if(head!='#') return spaces+'#'+head+tail
            return _
        })
    })
    codeLines.splice(iTestsToken+1, toggled.length, ...toggled)
    const repl = codeLines.join('\n')
    this.applyCodeToEditorAndSave(repl)
    this.focusEditor()
  }



  /**Download the current content of the editor to the download folder of the user.
   * */
  download(){   jsLogger("[Download]")

    let ideContent = this.getCodeToTest() + "" // enforce stringification in any case
    downloader(ideContent, this.pyName)
    this.focusEditor()
  }


  /**Reset the content of the editor to its initial content, and reset the localStorage for
   * this editor on the way.
   * */
  restart(){    jsLogger("[Restart]")
    const code = this.setStartingCode({extractFromLocalStorage: false, saveOnceApplied: true})
    this.storage = freshStore(code, this)
    this.updateValidationBtnColor()
    this.setAttemptsCounter(this.srcAttemptsLeft)
    $("#solution_" + this.id).addClass('py_mk_hidden')
    this.hiddenDivContent = true
    this.terminal.clear()
    clearPyodideScope()
    this.focusEditor()
  }



  /**Save the current IDE content of the user, or the given code, into the localStorage
  * of the navigator.
  * */
  save(givenCode=""){   jsLogger("[Save]")
    const currentCode = givenCode || this.getCodeToTest()
    this.setStorage({code: currentCode, hash:this.srcHash})
  }
}



CONFIG.CLASSES_POOL.Ide = IdeRunner
