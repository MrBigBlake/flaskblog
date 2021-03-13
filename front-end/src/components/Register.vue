<template>
  <div class="container">
    <h1>Register</h1>
    <div class="row">
      <div class="col-md-4">
        <form v-on:submit.prevent="onSubmit">

          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" v-model="registerForm.username" class="form-control"
                   v-bind:class="{'is-invalid':registerForm.usernameError}" id="username" placeholder="">
          </div>
          <div class="form-group">
            <label for="email">Email address</label>
            <input type="email" v-model="registerForm.email" class="form-control"
                   v-bind:class="{'is-invalid': registerForm.emailError}" id="email" aria-describedby="emailHelp"
                   placeholder="">
            <small v-if="!registerForm.emailError" id="emailHelp" class="form-text text-muted">We'll never share your
              email with anyone else.</small>
            <div v-show="registerForm.emailError" class="invalid-feedback">{{ registerForm.emailError }}</div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" v-model="registerForm.password" class="form-control"
                   v-bind:class="{'is-invalid': registerForm.passwordError}" id="password" placeholder="">
            <div v-show="registerForm.passwordError" class="invalid-feedback">{{ registerForm.passwordError }}</div>
          </div>

          <button type="submit" class="btn btn-primary">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios"
  import store from "../store"

  export default {
    name: "Register",
    data() {
      return {
        registerForm: {
          username: "",
          email: "",
          password: "",
          submitted: false,  // 是否点击了submit按钮
          errors: 0,  // 是否通过了前端的验证, 0表示没有错误, 验证通过
          usernameError: null,
          emailError: null,
          passwordError: null
        }
      }
    },
    methods: {
      onSubmit: function (e) {
        this.registerForm.submitted = true
        this.registerForm.errors = 0

        // 校验用户名
        if (!this.registerForm.username) {
          this.registerForm.errors++
          this.registerForm.usernameError = "Username required."
        } else {
          this.registerForm.usernameError = null
        }

        // 校验邮箱
        if (!this.registerForm.email) {
          this.registerForm.errors++
          this.registerForm.emailError = "Email required."
        } else if (!this.validEmail(this.registerForm.email)) {
          this.registerForm.errors++
          this.registerForm.emailError = "Valid email required"
        } else {
          this.registerForm.emailError = null
        }

        // 校验密码
        if (!this.registerForm.password) {
          this.registerForm.errors++
          this.registerForm.passwordError = "Password required."
        } else {
          this.registerForm.passwordError = null
        }

        // 校验未通过不请求后端接口
        if (this.registerForm.errors) {
          return false
        }

        // 请求后端注册接口
        const path = "http://localhost:5000/api/users"
        let data = {
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
        }
        axios.post(path, data)
          .then((response) => {
            store.setNewAction()
            this.$router.push("/login")
          })
          .catch((error) => {
            for (var field in error.response.data.message) {
              if (field === "username") {
                this.registerForm.usernameError = error.response.data.message.username
              } else if (field === "email") {
                this.registerForm.emailError = error.response.data.message.eamil
              } else if (field === "password") {
                this.registerForm.passwordError = error.response.data.message.password
              }
            }
          })
      },
      validEmail: function (email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        return re.test(email)
      }
    }
  }
</script>

<style scoped>

</style>
