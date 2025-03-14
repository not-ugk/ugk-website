const EncodingPlugin = require('encoding-plugin');

module.exports = {
  plugins: [
    new EncodingPlugin({
      encoding: 'iso-8859-1', // Specify the desired encoding
      filename: 'data.json'
    }),
  ],
  entry: './index.js',
  output: {
    filename: 'bundle.js',
    library: "UgkSearch"      
  },
  optimization: {
    minimize: false
  }
};