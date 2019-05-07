const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const AutoPrefixer = require('autoprefixer');

function bundle (appName, entryFiles=['main.js']) {
    /*
    * bundle (appName, entryFiles)
    * Creates a bundle for a particular django app
    * from his name and the entry files it has.
    * 
    * The bundle will be generated from the
    * static/src/ folder inside the application
    * and will be inside the static/dist/<app_name>/
    * folder with the same name of the entry file
    * or the name of the "package" folder where the 
    * file is if the entry file is inside a "package" 
    * folder and is a 'index.js' file. If the entry
    * file has a .css or .scss dependecy, it'll be
    * generated in a separate .css file with the 
    * same name convention as the .js bundle file.
    * 
    * All the app bundles will be tracked in a
    * webpack-stats.json file inside the app folder.
    * This will be the way the django server will
    * be able to reference the bundles using
    * the django-webpack-loader.
    * 
    * OBSERVATION: 
    * the <app_name> folder is generated so that 
    * the files inside the static/ folder of each 
    * application don't collide with each other 
    * when called by the url.
    * 
    * EXAMPLES:
    * imagine you have this directory tree:
    * (despise the other files)
    * 
    * src/
    *   app/static/
    *       src/
    *           my_package/
    *               index.js <- entry point
    *               module_a.js
    *               module_b.jsx
    *               ExampleComponent.vue
    *           index.js <- entry point
    *           module_c.js
    *           styles.scss
    *           my_entry.js <- entry point
    *           module_d.jsx
    * 
    * the dependencies go as follows:
    * my_package/index.js   <- module_a.js, module_b.js, ExampleComponent.vue
    * index.js              <- module_c.js, styles.scss
    * my_entry.js           <- module_d.js
    * 
    * for the system to produce the bundle, set:
    * module.exports = [
    *   bundle('app', ['my_package/index.js', 'index.js', 'my_entry.js'])
    * ];
    * 
    * so after the bundle builds, the 
    * structure will be like:
    * 
    * src/
    *   app/
    *       webpack-stats.json <- keeps track of bundles for django-webpack-loader
    *       static/
    *           build/app/
    *               my_package.js <- named after "package" folder (.vue is acepted)
    *               index.js
    *               index.css <- created extracting all stylesheets from index.js bundle
    *               my_entry.js
    *           src/
    *               my_package/
    *                   index.js <- entry point
    *                   module_a.js
    *                   ExampleComponent.vue
    *               index.js <- entry point
    *               module_c.js
    *               styles.scss
    *               my_entry.js <- entry point
    *               module_d.js
    */
    let entry = {};
    for (entryFile of entryFiles) {
        const parsedEntry = path.parse(entryFile);
        const entryName = (parsedEntry.name == 'index' && parsedEntry.dir)?
            parsedEntry.dir:path.join(parsedEntry.dir, parsedEntry.name)
        entry[entryName] = `./${path.join(appName, 'static/src', entryFile)}`
    }
    
    return {
        context: __dirname,
        entry: entry,
        output: {
            filename: '[name].js',
            path: path.resolve(__dirname, appName, 'static/dist', appName)
        },
        plugins: [
            new BundleTracker({filename: `./${path.join(appName, 'webpack-stats.json')}`}),
            new VueLoaderPlugin(),
            new ExtractTextPlugin({filename: '[name].css'})
            //Extract .css files to be separated from .js file context
        ],
        resolve: {
            modules: ['node_modules'],
            alias: {
                'vue$': 'vue/dist/vue.esm.js' 
                //'vue/dist/vue.common.js' to add the compiler
            }
        },
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: 'babel-loader'
                    /*
                    * Babel Loader permits code being written in ES6 and 
                    * be converted to ES5, compatible with all browsers
                    */
                },
                {
                    test: /\.vue$/,
                    use: 'vue-loader'
                    //Permits loading of .vue files of components
                },
                {
                    test: /\.s?css$/,
                    use: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: [ 'css-loader', 'sass-loader' ]
                    })
                    //Permits loading of sass files and css
                },
                {
                    // Loader for webpack to process CSS with PostCSS
                    test: /\.s?css$/,
                    loader: 'postcss-loader',
                    options: {
                        plugins () {return [AutoPrefixer]}
                    }
                    //Also permits loading of sass files and css
                }
            ]
        }
    }
}

module.exports = [
    bundle('home', ['imports.js', 'basic.js'])
];