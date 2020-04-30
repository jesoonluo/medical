const path = require('path')

function resolve (dir) {
  return path.join(__dirname, dir)
}
const isProduction = process.env.NODE_ENV === 'production'
var vuejs = 'https://cdn-web.weijian.video/static/js/vue.min.js'
if (!isProduction) {
  vuejs = 'https://cdn-web.weijian.video/static/js/vue.js'
}

module.exports = {
  // 部署文件使用的路径
  publicPath: '/',

  runtimeCompiler: true, // 是否使用包含运行时编译器的 Vue 构建版本

  productionSourceMap: false, // 生产环境的 source map

  chainWebpack: (config) => {
    // 修改文件引入自定义路径
    config.resolve.alias.set('@', resolve('src')).set('@img', resolve('src/assets/img'))
    config.resolve.extensions.add('.js', '.json', '.vue', '.scss')

    /* 添加分析工具 */
    if (isProduction) {
      if (process.env.npm_config_report) {
        config
          .plugin('webpack-bundle-analyzer')
          .use(require('webpack-bundle-analyzer').BundleAnalyzerPlugin)
          .end()
        config.plugins.delete('prefetch')
      }
    }

    config.module
      .rule('images')
      .test(/\.(jpg|png|gif)$/)
      .use('url-loader')
      .loader('url-loader')
      .end()
  },
  // 修改webpack的配置
  configureWebpack: {
    // 把原本需要写在webpack.config.js中的配置代码 写在这里 会自动合并

    performance: {
      hints: 'warning',
      // 入口起点的最大体积
      maxEntrypointSize: 50000000,
      // 生成文件的最大体积
      maxAssetSize: 30000000,
      // 只给出 js 文件的性能提示
      assetFilter: function (assetFilename) {
        return assetFilename.endsWith('.js')
      }
    }
  },

  devServer: {
    disableHostCheck: true,
    open: true,
    host: '0.0.0.0',
    port: 8989,
    https: false,
    hotOnly: false,
    // 配置跨域处理,只有一个代理
    proxy: {
      '/': {
        target: 'http://118.24.161.188:8889/',
        changeOrigin: true
      }
    }
  }
}
