<template>
  <div class="container">
    <alert
      v-if="sharedState.is_new"
      v-bind:variant="alertVariant"
      v-bind:message="alertMessage"
    ></alert>
    <h1>Sign In</h1>
    <div class="row">
      <div class="col-md-4">
        <form v-on:submit.prevent="onSubmit">

          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" v-model="loginForm.username" class="form-control"
                   v-bind:class="{'is-invalid': loginForm.usernameError}" id="username" placeholder="">
            <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.usernameError }}</div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" v-model="loginForm.password" class="form-control"
                   v-bind:class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="">
            <div v-show="loginForm.passwordError" class="invalid-feedback">{{ loginForm.passwordError }}</div>
          </div>

          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
      </div>
    </div>
    <br>
    <p>New User?
      <router-link to="/register">Click to Register!</router-link>
    </p>
    <p>
      Forgot Your Password?
      <a href="#">Click to Reset It</a>
    </p>
  </div>
</template>

<script>
  import Alert from "./Alert"
  import store from "../store"

  export default {
    name: "Login",
    components: {
      alert: Alert
    },
    data() {
      return {
        sharedState: store.state,
        alertVariant: "info",
        alertMessage: "Congratulations, you are now a registered user!",
        loginForm: {
          username: "",
          password: "",
          submitted: false,
          errors: 0,
          usernameError: null,
          passwordError: null,
        }
      }
    },
    methods: {
      onSubmit: function (e) {
        debugger

        // 校验用户名
        if (!this.loginForm.username) {
          this.loginForm.errors++
          this.loginForm.usernameError = "Username required."
        } else {
          this.loginForm.usernameError = null
        }

        // 校验密码
        if (!this.loginForm.password) {
          this.loginForm.errors++
          this.loginForm.passwordError = "Password required."
        } else {
          this.loginForm.passwordError = null
        }

        // 校验未通过不请求后端接口
        if (this.loginForm.errors) {
          return false
        }

        const path = "/tokens"
        let data = {}
        // axios 实现 Basic Auth 需要在 config 中设置 auth 属性
        let config = {
          auth: {
            "username": this.loginForm.username,
            "password": this.loginForm.password,
          }

        }
        this.$axios.post(path, data, config)
          .then((response) => {
            window.localStorage.setItem("blog-token", response.data.token)
            store.resetNotNewAction()
            store.loginAction()


            if (typeof this.$route.query.redirect === "undefined") {
              this.$router.push("/")
            } else {
              this.$router.push(this.$route.query.redirect)
            }
          })
          .catch((error) => {
              if (error.response) {
                if (error.response.status === 401) {
                  this.loginForm.usernameError = "Invalid username or password."
                  this.loginForm.passwordError = "Invalid username or password."
                } else {
                  console.error(error.response)
                }
              } else {
                console.error(error)
              }
            }
          )
      }
    }
  }
</script>

<style scoped>

</style>
