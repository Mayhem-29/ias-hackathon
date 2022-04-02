<template>
  <div
    uk-height-viewport="offset-bottom: 80px"
    class="uk-flex uk-flex-center uk-flex-middle uk-flex-column"
  >
    <router-view></router-view>
  </div>
</template>

<script>
import { AUTH_LOGOUT } from "@/store/actions/auth.js";
export default {
  name: "Home",
  methods: {
    logout: function() {
      this.$store.dispatch(AUTH_LOGOUT).then(() => this.$router.push("/login"));
    },
     downloadJSON: function(){
      var blob = new Blob([ JSON.stringify(this.form_values) ], { "type" : "text/plain" });
      let link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = 'model.json'
      link.click()
    },
  },
  data() {
    return {
      form_values : {}

    }
  },
 
};
</script>
<style lang="scss" scoped>

// .span-float{
//   float:right;
// }
</style>
