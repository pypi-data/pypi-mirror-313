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



/**Decorator like function factory, managing the global pyodide lock.
 * If a call is done while pyodide is locked, it is delayed until the lock is available.
 * */
var withPyodideAsyncLock = (_=>{

    /* Everything is run async but single threaded, so a global lock can be added, using
     * a simple simple boolean flag, declared inside a closure to avoid a user messing
     * with the variable... */
    let pyodideLocked = false

    return function(name, asyncCallback){
        const logName = asyncCallback.name||name

        const wrapper = async function(...args){
            await waitForPyodideReady()

            jsLogger("[LOCK?] -", logName, pyodideLocked)
            while(pyodideLocked){
                await sleep(60)
            }
            jsLogger("[LOCK ACQUIRE] -", logName)
            pyodideLocked = true
            let ret;
            try{
                ret = await asyncCallback.apply(this, args)
            }catch(e){
                console.error(e)    // Always keep that, otherwise errors in JS are just swallowed
                                    // (impossible to rethrow them, not sure why... async probably)
            }finally{
                jsLogger("[LOCK RELEASE] -", logName)
                pyodideLocked = false
            }
            return ret
        }
        return wrapper
    }

})()



/**Allow to delay the executions of various functions, until the pyodide environment
 * is done loading.
 * */
async function waitForPyodideReady(){

    const maxWaitingTime = 20  // in seconds
    const attempts = 80
    const step_ms = Math.round(1000 * maxWaitingTime / attempts)

    let counter = 0
    while(!globalThis.pyodideIsReady){
        await sleep(step_ms);
        if(++counter == attempts){
            throw new Error(`Couldn't access to pyodide environment in time (${maxWaitingTime}s)`)
        }
    }
}




/**Auto-subscription routine to document changes.
 * If the subscription is not possible yet (readyForSubscription[waitOn] is falsy), try again
 * @delay later until it works.
 *
 * @waitId :  Property to observe in readyForSubscription global object.Also used as subscription
 *            identifier.
 * @callback: Routine to run when the document changes
 * @options : An object with optional fields:
 *      .delay (=50): Time interval (in ms) to wait in between two subscription attempts.
 *      .now (=false): If true, ignore the CONFIG.subscriptionReady property and subscribe at call
 *              time. If false, a callback will be returned by the `subscribeWhenReady` function,
 *              that the caller can use to signal when the subscription is ready.
 *      .waitFor (=null): If given, it must be a boolean provider or a jquery identifier string,
 *              which will result in a function checking for the existence of that element in
 *              the DOM. This function will be called every .delay ms and the subscription will
 *              be delayed until it returns true. This has precedence over the .now option.
 *      .runOnly: if truthy, run the callback when ready, but do not subscribe to document changes.
 *      .maxTries: if not given 20 tries allowed.
 *
 * @throws: Error if maxTries subscriptions attempts are done without success.
 * */
function subscribeWhenReady(waitId, callback, options={}){

    let {now, delay, waitFor, runOnly, maxTries} = {
        delay: 50,
        now: false,
        waitFor: null,
        runOnly: false,
        maxTries: 20,
        ...options
    }
    now = now && !waitFor                       // has to wait if waitFor is used
    CONFIG.subscriptionReady[waitId] = now

    const checkReady = !waitFor                  ? ()=>null
                     : typeof(waitFor)=='string' ? ()=>{ CONFIG.subscriptionReady[waitId] = $(waitFor).length>0 }
                                                 : ()=>{ CONFIG.subscriptionReady[waitId] = waitFor() }
    const isNotReady =()=>{
        checkReady()
        return !CONFIG.subscriptionReady[waitId] || !globalThis.document$
    }

    function autoSubscribe(){

        if(isNotReady()){
            const nTries = CONFIG.subscriptionsTries[waitId]+1 || 1
            if(nTries==maxTries){
                throw new Error(`Impossible to subscribe to ${ waitId } in time: too many tries.`)
            }
            CONFIG.subscriptionsTries[waitId] = nTries
            setTimeout(autoSubscribe, delay)

        }else{
            jsLogger('[Subscribing] -', waitId)
            const wrapper=function(){
                try{
                    callback()
                }catch(e){
                    console.error(e)
                }
            }
            if(runOnly){
                wrapper()
            }else{
                const subscript = document$.subscribe(wrapper)
                document.addEventListener(CONFIG.onDoneEvent, function(){
                    jsLogger("[Unsubscribing] -", waitId)
                    subscript.unsubscribe()
                })
            }
        }
    }

    autoSubscribe()

    if(!now) return ()=>{ CONFIG.subscriptionReady[waitId]=true }
}








/**Square brackets in "rich text format" must be escaped, otherwise they are messing up the
 * terminal formatting informations.
 * */
function escapeSquareBrackets(msg){
    return msg.replace(/\[/g, CONFIG.MSG.leftSafeSqbr)
              .replace(/\]/g, CONFIG.MSG.rightSafeSqbr)
}


/**Formatting function factory, for messages used in the jquery terminal.
 *
 * WARNING: the input message will be "escapeSquareBrackets"-ed.
 * */
function richTextFormat(content, style, color="", background="") {
    content = escapeSquareBrackets(content)
    return `[[${ style };${ color };${ background }]${ content }]`;
}

const txtFormat = {
    error:   (content) => richTextFormat(content, "b", "red"),
    warning: (content) => richTextFormat(content, "ib", "orange"),
    info:    (content) => richTextFormat(content, "i", "grey"),
    italic:  (content) => richTextFormat(content, "i"),
    stress:  (content) => richTextFormat(content, "b"),
    success: (content) => richTextFormat(content, "ib", "green"),
    none:    escapeSquareBrackets,  // To override the defaults, if needed (see post processing)
}




/**Extract full information when something gets VERY wrong... */
function youAreInTroubles(err){
  return `${ err }\n\n${ err.stack || '[no stack]' }\n${ CONFIG.MSG.bigFail }`
}




function toSnake(msg){
    return msg.replace(/[A-Z]/g, m=>'_'+m.toLowerCase())
}



/**Takes a string and cut the "middle chunk" of them if it is considered too long (length > 1750),
 * shortening it in the following way:
 *   - keep the 500 first and 300 last chars
 *   - replace the middle with a message
 * */
function textShortener(text){
    if(CONFIG.cutFeedback && text.length > CONFIG.feedbackShortener.limit){
        const head = text.slice(0,CONFIG.feedbackShortener.head)
        const tail = text.slice(-CONFIG.feedbackShortener.tail)
        text = `${ head }\n...\n${ CONFIG.feedbackShortener.msg }\n...\n${ tail }`
    }
    return text
}



/**Create a button with tooltip, just like the python _html_builder one.
 * */
function buttonWithTooltip(options, content){
    options = {
        buttonId: "",
        shift: 50,          // %
        fontSize: 1.5,      // em
        tipWidth: 15,       // em
        tipText: "",
        ...options
    }
    options.tipWidth = options.tipWidth>0 ? `style="width:${ options.tipWidth }em;"` : ""
    const buttonId = !options.buttonId ? "" : `id="${ options.buttonId }" `
    return `
<button ${ buttonId }class="tooltip header-btn" type="button"
 style="--tool_shift:${ options.shift }%; font-size:${ options.fontSize }em;">
    <span class="tooltiptext" ${options.tipWidth}>${ options.tipText }</span>
    ${ content }
</button>
`
}



/**Randomly pick a value from an array.
 * @throws Error if the array is empty.
 * */
function choice(arr){
    if(!arr.length){
        throw new Error("Cannot pick from an empty array")
    }
    const i = Math.random() * arr.length | 0
    return arr[i]
}



/**NO_HTML and ALPHA (TOME_BASE in the python source) constants automatically transferred
 * from python during dev_ops/mkdocs_hooks operations.
 *
 * ****************************
 * * !!! DO NOT EDIT HERE !!! *
 * ****************************
 * */
const NO_HTML = '\'"&#><\n\t\r\\'
const ALPHA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%()*+,-./:;=?@^_`{|}~ "
const TOME_B = [...ALPHA].reduce((o,c,i)=>(o[c]=i,o), {})


const unBase =s=> [...s].reduce((v,c)=>v*ALPHA.length + TOME_B[c], 0)


/**@txt: CONFIG.LZW separated lines, with:
 *      1. A dot + dots separated unicode codePoints
 *      2. regular alpha
 *      3. compressed data, size 2
 *      4. ..., size 3,
 *      5. ...
 *
 * The compressed text always has one leading and one trailing dot:
 *      1. they allow to trim safely the encoded content, without any risk to trim spaces from
 *         the encoding alphabet.
 *      2. The leading dot allows to disambiguate the "big" section content of the alphabet,
 *         when no emojis are used in the original content.
 * */
const decompressLZW=(compressed, compressOptionSrc)=>{

    // console.log(JSON.stringify(compressed))

    const [bigs, smalls, ...chunks] = compressed.trim().slice(0,-1).split(CONFIG.LZW)
    const tome = [
        [...NO_HTML],
        bigs=='.' ? [] : bigs.slice(1)
                             .split('.')
                             .map(n=>String.fromCodePoint(+n)),
        [...smalls],
    ].flat()

    let txt=[], size=1, out=[]
    chunks.forEach(chunk=>{
        size++
        if(chunk.length%size){
            throw new Error(
                `Wrong chunk during decompression: size=${size}, length=${chunk.length}.\n` +
                `You can deactivate the compression by using setting the pyodide_macros plugin ` +
                `option ${ compressOptionSrc } to false, until the theme gets fixed.`
            )
        }
        for(let i=0 ; i<chunk.length ; i+=size){
            txt.push(unBase(chunk.slice(i,i+size)))
        }
    })
    txt.forEach((iBase,i)=>{
        const s = tome[iBase]
        const fresh = s + (tome[txt[i+1]] || s)[0]
        out.push(s)
        tome.push(fresh)
    })
    return out.join('')
}


/**Decompress PAGE_IDES_CONFIG content if not already done.
 * */
function decompressPagesIfNeeded(){
    if(typeof(PAGE_IDES_CONFIG)!='string') return;

    jsLogger('[CheckPoint] - decompress page LZW')
    PAGE_IDES_CONFIG = decompressAndConvert(PAGE_IDES_CONFIG)
}


/**Decompress LZW encoded string to a JSON object.
 * */
function decompressAndConvert(compressed){
    const decompressed = decompressLZW(compressed, "build.encrypted_js_data")
    const outcome      = JSON.parse(
        decompressed, (key,val)=>key=='attempts_left' && val=="Infinity" ? Infinity : val
    )
    return outcome
}



const escapeSqBrackets=msg=>{
    return msg.replace(CONFIG.ESCAPE_SQ_B, c=>SqBs[c])
}

const unEscapeSqBrackets=msg=>{
    return msg.replace(CONFIG.UNESCAPE_SQ_B, c=>SqBs[c]||c)
}

/**Async sleep (time given in milliseconds / must be awaited by the caller)
 * */
function sleep(ms=0) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}



// Code inspired by https://stackoverflow.com/questions/5379120/get-the-highlighted-selected-text
function getSelectionText() {
    let text = "";
    if(window.getSelection) {

        const extractTxtIfExists=(section, jRule, inline="")=>{
            const i = copied.length
            section.find(jRule).each(function(){ copied.push(this.innerText) })
            if(inline){
                section.find(inline).each(function(){ copied[i] = this.innerText + copied[i] })
            }
        }

        /**Return the first matching extraction logic, (broadest to smallest) */
        const getTxtFromSection=(section)=>{

            /* Search top level selection: several groups and/or the prompt thing.
               Notes:
                * For multiline commands, only the last one is in the "cmd/prompt" part. Previous/
                  incomplete lines are already in the structure with [data-index] attributes.
                * The prompt (beginning of the currently written command) must be extracted on its
                  own then added at the beginning of the actual command content.
            */
            extractTxtIfExists(section, 'div[data-index]>div')
            extractTxtIfExists(section, 'div.cmd-cursor-line', 'span.cmd-prompt')
            if(copied.length) return;


            // Search different lines inside one div[data-index].
            extractTxtIfExists(section, 'div')
            if(copied.length) return;

            // At this point, only bare text in a single element has been selected
            copied.push(section.text())
        }

        const selection = window.getSelection()
        const copied = []
        for(let iR=0;iR<selection.rangeCount;iR++){
            const section = $( selection.getRangeAt(iR).cloneContents() )
            copied.push( getTxtFromSection(section) )
        }
        text = copied.join('\n')

    }else if(document.selection && document.selection.type != "Control") {
        console.warn("Unsupported copy from PMT terminal.")
        text = document.selection.createRange().text;
    }

    // Just like usual, jQuery terminals are messing with the content, replacing spaces with \u00a0...:
    text = text.replace(/\u00a0/ug, " ")

    return text;
}






/**Apply a "download" action, given the content, name and type of the file to download.
 * See https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
 * about MIME types.
 * */
function downloader(content, filename, mimeType="text/plain"){
    let blob = new Blob([content], {type: mimeType})
    let link = document.createElement("a")
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.click()
    URL.revokeObjectURL(link.href)
    link.remove()
}




/**Routine reusing the very same input[type=file] element (hidden in <head>) to upload content.
 * It must receive a callback that will handle the action to do with the content of the uploaded
 * file.
 * Returns a curried event executor: (cbk)=>[event executor function}
 * */
var [uploader, uploaderAsync] = (function(){

    // https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications#example_showing_thumbnails_of_user-selected_images

    let jInput         = null
    let readMethod     = null       // readAsText / readAsDataURL / readAsArrayBuffer / readAsBinaryString
    let contentHandler = null       // Replaced on the fly at runtime
    let errorHandler   = null       // first error thrown during the reading process

    const inputId      = 'pyodide-file-uploader'
    const resumeHandler=_=>{ contentHandler = null }

    ;(_=>{
        // Defined in an isolated scope, to avoid the mistaken use of stuff defined here...
        jInput = $(`<input id="${ inputId }" name="file-uploader" type="file">`)
        $(document.head).append(jInput)

        jInput.on("cancel", resumeHandler)
        jInput[0].addEventListener(         // Doesn't wanna work through jQuery...
            "change",
            function(changeEvent){
                let iFile=1
                for(const file of changeEvent.target.files){

                    const reader  = new FileReader();
                    const isLast  = changeEvent.target.files.length==iFile++

                    reader.onabort = function(event){
                        resumeHandler()
                        throw errorHandler
                    }
                    reader.onload = function(event){
                        try{
                            contentHandler(event.target.result, file.name, isLast)
                        }catch(e){
                            errorHandler ||= e
                            reader.abort()
                        }
                        if(isLast) resumeHandler()      // to spot end of execution in async way
                    }
                    reader[readMethod](file)
                }
            },
            false
        )
    })()


    /**The showPicker method will raise an error, so possible to warn the user about what to do.
     * But it's not compatible with all browsers, so keep the orignal click logic anyway...
     * (but users wont' get any info about what's going wrong, in that case)
     * */
    const triggerInputFile=_=>{
        if(!jInput[0].showPicker){
            jInput[0].click()           // This is actually "async" (event!)
            return
        }
        try{
            jInput[0].showPicker()      // This is actually "async" (event!)
        }catch(e){
            // NOTE: Only the showPicker error should ever go there. Other errors aren't thrown
            //       in the same context...
            resumeHandler()     // Ensure release of the terminal, if async call
            if(!e.toString().includes('HTMLInputElement.showPicker')) throw e
            window.alert(CONFIG.lang.pickerFailure.msg)
        }
    }

    const uploader = (cbk, readAs='readAsText', multi=false)=>{
        contentHandler = cbk
        readMethod     = readAs
        jInput.prop('multiple', multi)
        triggerInputFile()
    }

    const uploaderAsync = async (...args)=>{
        errorHandler = null
        uploader(...args)
        // Wait until the upload is done, so that the uploaded content is usable during current run
        while(contentHandler){
            await sleep(200)
        }
        if(errorHandler){
            throw errorHandler  // propagate the error logic to the pyodide runtime environment
        }
    }

    return [uploader, uploaderAsync]
})()







/**Extract the given ID data from the localStorage, checking if it's not an outdated
 * or invalid structure.
 * @returns: [storage_data, outdated]
 * */
function getIdeDataFromStorage(editorId, forThis=null){

    let storage  = localStorage.getItem(editorId) || ""
    let upToDate = false
    try{
      const obj = JSON.parse(storage || '{}')
      upToDate  = "hash code done name zip".split(' ').every(k=> k in obj)
      if(upToDate) storage=obj
    }catch(_){}

    if(!upToDate){
        // Here, `storage` is the user code itself (initial implementation of the localStorage)
        storage = freshStore(storage, forThis)
      }
    return [storage, !upToDate]
}


/**Forbid writing these properties from pyodide. */
const FORBIDDEN_LOCAL_STORAGE_KEYS_WRITE = Object.freeze(`
    code
    done
    hash
    name
    zip
`.trim().split(/\s+/))

function freshStore(code, forThis=null){
    return {
      code: code || "",
      done: 0,            // -1: fail, 0: unknown, 1:success
      ...( !forThis ? {}:{
          hash: forThis.srcHash,
          name: forThis.pyName,
          zip:  forThis.export,
        })
    }
}




/**Special JS Error: methods calls exclusions are tested from the JS runtime, instead of pyodide.
 * So, JS has to throw a special error that will mimic ("enough"...) the pattern of pyodide errors
 * and hance, will be considered legit errors.
 */
class PythonError extends Error {
    toString(){ return "Python" + super.toString() }
}
