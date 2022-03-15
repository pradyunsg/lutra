const { resolve } = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  devtool: "source-map",
  mode: process.env.NODE_ENV,
  entry: {
    lutra: [
      "./src/lutra/assets/scripts/lutra.js",
      "./src/lutra/assets/styles/lutra.css",
    ],
    "lutra-extensions": ["./src/lutra/assets/styles/lutra-extensions.css"],
  },
  output: {
    filename: "scripts/[name].js",
    path: resolve(__dirname, "src/lutra/theme/lutra/static"),
  },
  plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" })],
  optimization: { minimizer: [`...`, new CssMinimizerPlugin()] },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: "css-loader", options: { sourceMap: true } },
          { loader: "postcss-loader", options: { sourceMap: true } },
        ],
      },
    ],
  },
};
