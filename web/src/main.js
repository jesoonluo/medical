import Vue from 'vue'
import App from './App.vue'
import router from '../router'
import store from '../store'
import {
  Button,
  Select,
  Tree,
  Input,
  Form,
  FormItem,
  Radio,
  RadioGroup,
  RadioButton,
  Checkbox,
  CheckboxGroup,
  CheckboxButton,
  Switch,
  Col,
  option,
  DatePicker,
  TimePicker
} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/assets/css/reset.scss'
import '@/assets/css/index.scss'
import axios from '@/axios/index.js'

Vue.config.productionTip = false
Vue.prototype.$axios = axios

Vue.use(Button)
Vue.use(Input)
Vue.use(Tree)
Vue.use(Select)
Vue.use(Form)
Vue.use(Radio)
Vue.use(FormItem)
Vue.use(RadioButton)
Vue.use(RadioGroup)
Vue.use(Checkbox)
Vue.use(CheckboxButton)
Vue.use(CheckboxGroup)
Vue.use(Col)
Vue.use(Switch)
Vue.use(option)
Vue.use(TimePicker)
Vue.use(DatePicker)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
