import axios from './index.js'

export function post (url, data) {
  // var url = api_url_conf[url]
  return new Promise((resolve, reject) => {
    axios.post(url, data).then(res => {
      resolve(res)
    }, err => {
      reject(err)
      // if (err.response.data.code != 422 && err.response.data.code < 500) {
      //   this.$store.commit('alertMsg', err.response.data.msg)
      // } else if (err.response.data.code == 422) {
      //   var thisErr = JSON.parse(err.response.data.msg)
      //   this.$store.commit('alertMsg', thisErr[0].error[0])
      // } else {
      //   this.$store.commit('alertMsg', err.message)
      // }
    })
  })
}
export function get (url, data) {
  // var url = api_url_conf[url]

  return new Promise((resolve, reject) => {
    axios.get(url, data).then(res => {
      resolve(res)
    }, err => {
      reject(err)
      // if (err.response.data.code != 422 && err.response.data.code < 500 && err.response.data.code != 401) {
      //   this.$store.commit('alertMsg', err.response.data.msg)
      // } else if (err.response.data.code != 401) {
      //   this.$store.commit('alertMsg', err.message)
      // }
    })
  })
}

export function deleteRun (url, data) {
  return new Promise((resolve, reject) => {
    axios.delete(url, data).then(res => {
      resolve(res)
    }, err => {
      reject(err)

      // if (err.response.data.code != 422 && err.response.data.code < 500 && err.response.data.code != 401) {
      //   this.$store.commit('alertMsg', err.response.data.msg)
      // } else if (err.response.data.code != 401) {
      //   this.$store.commit('alertMsg', err.message)
      // }
    })
  })
}