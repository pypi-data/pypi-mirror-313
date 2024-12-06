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



/**Build a "context" object, holding the various state information for the current
 * "sub-action/step" in the current overall user action (RuntimeManager).
 * (creates a bare object, without methods)
 * */
class Ctx {

  static baseCtx(){
    return {
      success: true,                // false on errors only, not if just "skipped"

      err: null,                    // Error instance
      stdErr: "",                   // Error as string (msg to output, formatted)
      isAssertErr:false,
      stdout: "",
      qualname: "<unknown>",        // "qualified name" of the section + method to run in the current action (debugging purpose)

      keepRunningOnAssert: false,   // If true, consider the section ran successfully on AssertionError (this is env related)
      isEnvSection: true,           // Any of env, env_term, ... => "not user code or cmd"
      applyExclusionsIfAny: false,  // Apply exclusions specifically on this run (if any). Note: `!isEnvSection` is not specific enough!
      section: "<unknown>",         // as in "PYODIDE:{section}", or "unknown" instead. Visible in the stacktrace on errors.
      archiveSuccess: false,        // If true, the section will be registered as ran successfully (if it is so). To use on the last action of the section.
      method: ()=>null,             // Runner method to... run when everything is ready
      code: ".",                    // If empty string, the Runner method won't ever be called. Default is not empty, because some Runner won't need to pass `code` to the ctx to know what to do (or the code needed is not known yet: Features)
      methodArgs: [],               // Additional arguments to pass to the Runner method
      logConfig: {},                // Config for generateErrorLog
    }
  }


  static with(ctx, runtime){
    const baseCtx = Ctx.baseCtx()
    let section   = ctx && ctx.section || baseCtx.section

    if(!ctx) ctx={}                     // no argument

    else if(typeof(ctx)=='string'){     // Environment section name only
      section = ctx
      ctx = {
        archiveSuccess:      true,      // always, with environment codes
        code:                runtime.runner[`${ section }Content`].trim(),
        keepRunningOnAssert: section.startsWith('env'),
        method:              runtime.runner.installImportsAndRunEnvCode,
      }
    }

    return {
      ...baseCtx,
      qualname: `${ section || '?' }_${ ctx.method.name }`,
      ...ctx,
      section,
    }
  }
}









/**Manage the environment when in need to execute some code in pyodide.
 *
 * Holds all the logic to manage all the possible outcomes:
 * Used as "throw away" data structure, once the full user action is done: this allows
 * to mutate "everything you need", being sure it wont affect the original data in the
 * `PythonSectionsRunner` instance.
 * */
class RuntimeManager {

  get excluded()        { return this.runner.excluded }
  get excludedMethods() { return this.runner.excludedMethods }
  get recLimit()        { return this.runner.recLimit }
  get whiteList()       { return this.runner.whiteList }

  constructor(runner){
    this.runner = runner    // PyodideSectionsRunner, or one of its parent class/object

    // --- Python logistic related (may be mutated on the way) ---
    this.autoLogAssert   = null     // default for the PUBLIC tests...
    this.purgeStackTrace = null     // default for the PUBLIC tests...
    this.withStdOut      = null     // default for the PUBLIC tests...
    this.refreshStateWith()         // Apply actual defaults (avoiding defaults duplication)

    // --- Runtime logistic related (may be mutated on the way) ---
    this.stdErr       = ""          // First encountered error message
    this.isAssertErr  = false       // Is the error an assertion error
    this.gotBigFail   = false       // If true, new errors won't replace the current one
    this.finalMsg     = ""          // Potential extra message to display at the very end, if truthy.
                                    //  (will be printed even if this.stopped is true)

    this.ran = {start: true}        // Keep track of the successfully run env sections (or raising assertion errors)
    this.dependencies = {
      env:      'start',
      envTerm:  'env',
      code:     'env',              // (actually not used as a condition for now)
      cmd:      'envTerm',          // (actually not used as a condition for now)
      postTerm: 'envTerm',
      post:     'env',
    }
  }

  get stopped(){ return Boolean(this.stdErr) }


  /**Update the state of the current RuntimeManager with the given data, and use
   * default values for missing fields.
   * */
  refreshStateWith(update={}){
    update = {
      autoLogAssert:   true,
      purgeStackTrace: false,
      withStdOut:      true,
      ...update
    }
    for(const prop in update){
      this[prop] = update[prop]
    }
  }


  /**Update the sections dependency graph, to modify the conditions to run or not a section.
   * */
  changeDependency(source, target){
    if(this.dependencies[source]===undefined){
      throw new Error("Invalid source dependency: " + source)
    }
    this.dependencies[source] = target
  }

  cleanup(){
    return this.runner = this.runCodeAsync = null   // Facilitate GC...
  }





  stillRunnable(ctx){
    let outcome = ctx.isEnvSection
                  ? this.ran[ this.dependencies[ctx.section] ]
                  : !this.stopped
    outcome &&= !this.gotBigFail
    return outcome
  }


  /**Run one Runner method (async), surrounding it with all necessary logics, like:
   *
   *    - setup+teardown stdout
   *    - setup+teardown exclusions
   *    - give feedback
   *    - try/catch where appropriate (handling properly the exclusions removal case)
   *
   * This method should never actually throw, except in "BigFail" cases.
   * Note: NOT this.stdErr, which is more global, while the current run could involve `post`
   *       actions that should potentially occur even if an error has already occur previously
   *       in the current user's action.
   *
   * It uses a ctx object, which holds the local executions data, and will merge the data
   * when appropriate in the RunnerManager (which holds runtime information for the current
   * user's action).
   *
   * Inside this "runWithCtx" call, subsequent methods calls are skipped if an error has been
   * registered in the @ctx object, unless the method is specified as "should `always` happen"
   * */
  async runWithCtx(ctx){
    ctx = Ctx.with(ctx, this)

    if(!this.stillRunnable(ctx)){
      jsLogger('[Runtime] - SKIPPED', ctx.qualname)
      return ctx
    }

    jsLogger('[Runtime] - running ', ctx.qualname)
    // No need for error extra handling: big fails handled in lockedRunnerWithBigFailWarningFactory

    this.runner.allowPrint = this.withStdOut

    await this._runCaught( ctx, this.setupManager)
    await this._runCaught( ctx, this.applyRunnerMethod)
    await this._runCaught( ctx, this.removeExclusions, {always:true})
    await this._runCaught( ctx, this.teardownManager,  {always:true, critical:true})

    this.runner.allowPrint = true
    this.runner.giveFeedback(ctx.stdErr)

    if(ctx.archiveSuccess){
      this.ran[ctx.section] = ctx.success
    }
    jsLogger('[Runtime] - done', ctx.qualname)
    return ctx
  }





  needExclusions(ctx){
    return ctx.applyExclusionsIfAny && (this.excluded.length>0 || this.recLimit > 0)
  }




  /**1. Put the StringIO object in place.
   * 2. IF the method to run is "environment-related", STOP HERE.
   * 3. OTHERWISE, if the ctx is asking for exclusions applications:
   *     1. Put in place exclusions if any
   *     1. Cleanup pyodide environment (`auto_run.clean`)
   * */
  async setupManager(ctx){

    setupStdIO()
    if(ctx.isEnvSection) return;

    if(this.needExclusions(ctx)){
      jsLogger('[CheckPoint] - running - setup exclusions')
      setupExclusions(this.excluded, this.recLimit)
    }
    pyodideFeatureRunCode('autoRunCleaner')
  }


  /**Run the desired Runner method, once all the setup has been managed.
   * If it succeeds (aka, the method doesn't throw any error), the ctx is marked as successful.
   *
   * The Runner method is supposed to take this kind of signature:
   *
   *      method(...ctx.methodArgs, ctx, runtime)
   *
   * Where `ctx.methodArgs` are arguments the RuntimeManager cannot know about in the first place.
   * The two last arguments are always passed but may be ignored on the actual method signature, if
   * it doesn't make use of them.
   * */
  async applyRunnerMethod(ctx){
    jsLogger('[CheckPoint] - running method runner -', ctx.qualname)
    await ctx.method.call(this.runner, ...ctx.methodArgs, ctx, this) // always send extras args (in case useful)
    ctx.success = true
  }


  /**Remove the exclusions.
   * WARNING:     1. Could raise ExclusionError!
   *              2. Must be _absolutely sure_ that they are removed, even if the user's code
   *                 already raised (or the tests)...
   * */
  async removeExclusions(ctx){
    if(this.needExclusions(ctx)){
      jsLogger('[CheckPoint] - running - removing exclusions')
      restoreOriginalFunctions(this.excluded)
    }
  }


  async teardownManager(ctx){
    // let stdout = getFullStdIO()
    // if(!this.withStdOut) stdout = ''
    // else if(!ctx.isEnvSection) stdout = textShortener(stdout)
    // ctx.stdout = stdout

    getFullStdIO()
    this.handleError(ctx)
  }




  /**In case an error has been registered in @ctx
   * */
  handleError(ctx, replLogConf=null){
    if(!ctx.err) return;

    this.finalMsg = ""

    ;[ctx.stdErr, ctx.isAssertErr] = generateErrorLog(ctx.err, replLogConf || ctx.logConfig)

    // If ever multiple errors happen, an assertion error will always be the very
    // first one, so always keep if any (avoid the need to condition the update)
    if(!this.gotBigFail){
      this.isAssertErr ||= ctx.isAssertErr
      this.stdErr        = ctx.stdErr
    }
    ctx.success = ctx.keepRunningOnAssert && ctx.isAssertErr
  }



  async _runCaught(ctx, method, conf={}){
    jsLogger('[Runtime] - _runCaught ', ctx.qualname, method.name)
    if(ctx.err && !conf.always) return
    try{
      await method.call(this, ctx)
    }catch(e){
      jsLogger('[Runtime] - ERROR ', ctx.qualname)
      if(CONFIG.loggerOptions.ACTIVATE) console.error(e)
      ctx.err = e
      if(conf.critical) throw e
    }
  }
}
