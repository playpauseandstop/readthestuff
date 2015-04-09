var webpack = require("webpack");

var config = require("./webpack.config.dev.js");

config.output.filename = "readthestuff.js";
config.plugins.push(new webpack.optimize.DedupePlugin());
config.plugins.push(new webpack.optimize.UglifyJsPlugin({
  compress: {
    warnings: false
  }
}));

module.exports = config;
