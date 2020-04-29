import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    upData: 0
  },
  mutations: {
    // 弹框显示隐藏
    modalShow(state, id) {
      var dom = document.getElementById(id)
      dom.classList.add('fade')
      document.body.classList.add('model-open')
    },
    modalHidden(state, id) {
      var dom = document.getElementById(id)
      dom.classList.remove('fade')
      document.body.classList.remove('model-open')
    },
    // 更新数据
    upData(state) {
      state.upData++
    }
  },
  actions: {},
  modules: {}
})
