# PolymerBundler

This tries to mimic what [polymer-bundler](https://github.com/Polymer/polymer-bundler) and [crisper](https://github.com/PolymerLabs/crisper) would do (though not entirely). Because the other tools are not yet ready for production environments (as of this writing, Feb 2017) and I have ran into issues using them, I have built this. This tool compiles to `build.html` and `build.js` respectively. It tries to resolve all dependencies in the order in which they are found in each source file, working its way down the dependency tree from the input source files. In other words, for example, if the source file depends on `polymer.html`, `polymer.html` should never be included at the end of the build.html file.

## Command-line Options

- `--build-dir=<path>` The directory to compile to.
- `--source-file=<path>` The file to parse and compile. Can be repeated multiple times for multiple sources.
- `--doc-root=<path>` Folder used for absolute URL paths.

### Example Usage

    python main.py --build-dir="C:\build" --doc-root="C:\www" --source-file="C:\www\components\web-component.html"

For multiple source files:

    python main.py --build-dir="C:\build" --doc-root="C:\www" --source-file="C:\www\components\web-component-1.html" --source-file="C:\www\components\web-components-2.html"
