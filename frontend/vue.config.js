const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  pages: {
    index: {
      // точка входа для страницы
      entry: 'src/main.js',
      // исходный шаблон
      template: 'public/index.html',
      // название в итоговом dist/index.html
      filename: 'index.html',
      // заголовок страницы
      title: 'HabitsLine',
      // блоки, которые будут включены на странице
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    }
  }
})