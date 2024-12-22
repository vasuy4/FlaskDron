const path = require('path');

module.exports = {
  entry: './static/js/script.js', // основной JS-файл
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/dist'), // Папка для собранного файла
  },
  mode: 'development',
  devServer: {
    static: './static',
    port: 3000,
  },
};