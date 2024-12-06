## How the scripts are used

When mkdocs starts building the docs, if one of the scripts (or css) files is more recent than the `main.html` file, the latter will be rebuilt, including all the JS/CSS files found in the `mkdocs_theme_pyodide` directory hierarchy.

The files are inserted in lexicographic order of their path, and are inserted in the jinja block matching the suffix of the filename. For example: `custom_dir/.../file-libs.js` is inserted in the libs block of `main.html`.

This allows to control in what order the files are defined, so that all the needed subroutines are defined in appropriate order.

One exception to this: the libs are in their own directory, to make it easier to identify what scripts are defined/used at the very beginning of the document (note: they still have the suffix in their name).