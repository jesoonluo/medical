import axios from 'axios'
// import router from '../router'

const CancelToken = axios.CancelToken // 取消请求

// axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://118.24.161.188:8889'
axios.defaults.timeout = 60000 // 超时设置

axios.interceptors.request.use(
  config => {
    // 设置默认请求头

    // config.headers['X-Requested-With'] = 'XMLHttpRequest'
    // 指定允许其他域名访问
    // config.header('Access-Control-Allow-Origin:*')
    // // 响应类型
    // config.header('Access-Control-Allow-Methods','GET, POST, OPTIONS, PUT, PATCH, DELETE');
    // // 响应头设置
    // config.header('Access-Control-Allow-Headers:x-requested-with,content-type')

    let cancelGroupName
    if (config.method === 'post') {
      if (config.data && config.data.cancelGroupName) {
        // post请求ajax取消函数配置
        cancelGroupName = config.data.cancelGroupName
      }
      // config.data = qs.stringify(config.data)
    } else {
      if (config.params && config.params.cancelGroupName) {
        // get请求ajax取消函数配置
        cancelGroupName = config.params.cancelGroupName
      }
    }
    if (cancelGroupName) {
      if (axios[cancelGroupName] && axios[cancelGroupName].cancel) {
        axios[cancelGroupName].cancel()
      }
      config.cancelToken = new CancelToken(c => {
        axios[cancelGroupName] = {}
        axios[cancelGroupName].cancel = c
      })
    }
    return config
  },
  error => {
    console.log('error', error)
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  config => {
    return config
  },
  error => {
    if (error && error.response) {
      switch (error.response.status) {
        case 401:
          // localStorage.removeItem('user_info')
          // router.push('/login')
          break
        case 404:
          // router.push('*')
          break
        case 500:
          error.message = '服务器端出错'
          break
        case 501:
          error.message = '网络未实现'
          break
        case 502:
          error.message = '网络错误'
          break
        case 503:
          error.message = '服务不可用'
          break
        case 504:
          error.message = '网络超时'
          break
        case 505:
          error.message = 'http版本不支持该请求'
          break
        default:
          error.message = `连接错误${error.response.status}`
      }
    } else {
      error.message = '连接到服务器失败'
    }

    return Promise.reject(error)
  }
)

export default axios
