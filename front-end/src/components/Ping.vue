<template>
 <div class="container">
   <button type="button" class="btn btn-primary">{{ msg }}</button>
 </div>
</template>

<script>
  import axios from "axios"

  export default {
    name: "Ping",
    data() {
      return {
        msg: ""
      }
    },
    methods: {
      getMessage() {
        const path = "http://localhost:5000/api/ping"
        let that = this
        axios.get(path)
          // 这里的 this 为 undefined
          .then(function (response) {
            that.msg = response.data
          })
          .catch(function (error) {
            console.error(error)
          })

      }
    },
    created() {
      this.getMessage()
    }
  }
</script>
