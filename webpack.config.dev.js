var path = require("path");
var webpack = require("webpack");

module.exports = {
  entry: path.resolve(__dirname, "readthestuff/static/readthestuff/App.js"),
  output: {
    path: path.resolve(__dirname, "readthestuff/static/dist/"),
    filename: "readthestuff.debug.js",
    library: "ReadTheStuff",
    libraryTarget: "umd"
  },

  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader?optional=runtime"
      },
      {
        test: /\.json$/,
        loader: "json-loader"
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    })
  ]
};
