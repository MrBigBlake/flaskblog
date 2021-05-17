// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'


import "bootstrap/dist/css/bootstrap.css"

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
})

// 注册 vue-toasted 插件
import VueToasted from 'vue-toasted'

Vue.use(VueToasted, {
  // 主题样式
  theme: "bubble",
  // 显示位置
  position: "top-center",
  // 显示时长
  duration: 3000,
  // 图标合集
  iconPack: "material",
  // 支持的动作
  action: {
    text: "Cancel",
    onClick: (e, toastObject) => {
      toastObject.goAway(0)
    }
  }
})


import axios from "./http"

Vue.prototype.$axios = axios

// 导入 moment.js 用来格式化 UTC 时间为本地时间
import moment from "moment"

Vue.prototype.$moment = moment
