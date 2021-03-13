import Vue from "vue"
import Router from "vue-router"
import Home from "@/components/Home"
import Login from "@/components/Login"
import Register from "@/components/Register"
import Profile from "@/components/Profile"
import Ping from "@/components/Ping"

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/register",
      name: "Register",
      component: Register
    },
    {
      path: "/profile",
      name: "Profile",
      component: Profile
    },
    {
      path: "/ping",
      name: "Ping",
      component: Ping
    },
  ]
})

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem("token")
  // 没有token时访问需要登录的页面直接跳转到登录页面
  if (to.matched.some(record => record.meta.requiredAuth) && !token) {
    next({
      path: "/login",
      query: {redirect: to.fullPath}
    })
  } else if (token && to.name === "login") {
    // 已登录用户不能访问登录页面
    next({
      path: from.fullPath
    })
  } else {
    next()
  }
})

export default router
