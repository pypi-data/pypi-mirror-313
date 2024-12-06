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



;(function(){

  // For backward compatibility ( < 2.2.0)
  const DEFAULT_FORMATTING_BEFORE_220 = {
    runScript:         'info',
    installStart:      'info',
    installDone:       'info',
    validation:        'info',
    editorCode:        'info',
    publicTests:       'info',
    secretTests:       'info',
    successMsg:        'success',
    successMsgNoTests: 'info',
    unforgettable:     'warning',
    successHead:       'success',
    failHead:          'warning',
  }

  for(const prop in CONFIG.lang){
    const obj = CONFIG.lang[prop]
    const format = obj.format || DEFAULT_FORMATTING_BEFORE_220[prop]

    if(format){
      obj.msg = txtFormat[ format ]( obj.msg )
    }
  }

  CONFIG.lang.tests.as_pattern  = new RegExp(CONFIG.lang.tests.as_pattern, 'i')

  CONFIG.pythonLibs = new Set(CONFIG.pythonLibs)
})()
