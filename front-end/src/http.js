import axios from "axios"
import store from "./store";
import router from "./router";


axios.defaults.timeout = 5000
axios.defaults.baseURL = "http://localhost:5000/api"


// 通过 request interceptor 自动添加 Token 到请求头中
axios.interceptors.request.use(function (config) {
  // 发生请求前
  const token = window.localStorage.getItem("blog-token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, function (error) {
  // 当请求错误时
  return Promise.reject(error)

})


// axios响应钩子函数, 用来处理异常响应
axios.interceptors.response.use(
  function (response) {
    return response
  }, function (error) {
    switch (error.response.status) {
      case 401:
        store.logoutAction()
        if (router.currentRoute.path !== "/login") {
          Vue.toasted.error("401: 认证已失效, 请先登录!", {icon: "fingerprint"})
          router.replace({
            path: "/login",
            query: {redirect: router.currentRoute.path}
          })
        }
        break
      case 404:
        Vue.toasted.error("404: NOT FOUND", {icon: "fingerprint"})
        router.back()
        break
    }
    return Promise.reject(error)
  }
)


export default axios
