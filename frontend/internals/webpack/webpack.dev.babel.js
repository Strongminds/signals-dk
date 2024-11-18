// SPDX-License-Identifier: MPL-2.0
// Copyright (C) 2018 - 2021 Gemeente Amsterdam
// @ts-check
const path = require('path')

const CircularDependencyPlugin = require('circular-dependency-plugin')
const CopyPlugin = require('copy-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const template = require('./template')
const { baseConfig, merge } = require('./webpack.base.babel')

const devConfig = /** @type { import('webpack').Configuration } */ {
  mode: 'development',

  // Add hot reloading in development
  entry: [
    path.join(process.cwd(), 'src/app.js'), // Start with js/app.js
  ],

  // Don't use hashes in dev mode for better performance
  output: {
    filename: '[name].js',
    chunkFilename: '[name].chunk.js',
  },

  optimization: {
    usedExports: true,
  },

  // Add development plugins
  plugins: [
    new HtmlWebpackPlugin({
      inject: true, // Inject all files that are generated by webpack, e.g. bundle.js
      ...template,
    }),

    new HtmlWebpackPlugin({
      filename: 'manifest.json',
      inject: false,
      templateContent: template.manifestContent,
    }),

    new CircularDependencyPlugin({
      exclude: /a\.js|node_modules/, // exclude node_modules
      failOnError: false, // show a warning when there is a circular dependency
    }),

    new CopyPlugin({
      patterns: [
        { from: path.join(process.cwd(), 'src/sw-proxy.js') },
        {
          from: path.join(process.cwd(), 'src/sw-proxy-config.js'),
          force: true,
        },
      ],
    }),
  ],

  // Emit a source map for easier debugging
  // See https://webpack.js.org/configuration/devtool/#devtool
  devtool: 'cheap-module-source-map',

  devServer: {
    static: './public',
    watchFiles: ['public/locales/**/*.json'], // Watch translation files
    hot: true, // Enable hot module replacement
  },
}

module.exports = merge(baseConfig, devConfig)
