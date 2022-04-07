<template>
  <div class="auth-page loading">
    <main>
      <div class="content content--side">
        <header class="codrops-header uk-flex uk-flex-center">
          <h1 class="uk-margin-remove uk-text-center">
           {{ $store.getters.appName }}
          </h1>
          <p class="">Fill in the form and get started today!</p>
        </header>
        <div class="form">
          <div class="form__item">
            <label class="form__label" for="email">Email Address</label>
            <input
              class="form__input"
              type="email"
              v-model="email"
              id="email"
            />
          </div>
          <div class="form__item">
            <label class="form__label" for="password">Password</label>
            <div class="form__input-wrap">
              <input
                class="form__input"
                type="password"
                v-model="password"
                id="password"
              />
              <p class="form__password-strength" id="strength-output"></p>
            </div>
          </div>
          <div class="form__item">
            <label class="form__label" for="role">Role</label>
            <div class="form__input-wrap">
              <select
                v-model="role"
                id="role"
              >
              <option>Data Scientist</option>
              <option>Platform Admin</option>
              <option>App Developer</option>
              <option>End User</option>
              </select>
              
            </div>
          </div>
          <div class="form__item form__item--actions">
            <span
              >Don't have an account?
              <router-link class="form__link" to="/register"
                >Register here</router-link
              >
            </span>
            <button-spinner ref="loadingButton" @click="login()"
              >Log in</button-spinner
            >
          </div>
        </div>
      </div>
      <div class="content content--side">
        <div class="poster" :style="'background-image:url(' + img + ')'"></div>
        <div class="canvas-wrap">
          <canvas></canvas>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
.login {
  display: flex;
  flex-direction: column;
  width: 300px;
}
</style>

<script>
import img from "./img/login.jpg";
import { AUTH_REQUEST } from "@/store/actions/auth";
export default {
  name: "Login",
  data() {
    return {
      email: "johndoe@example.com",
      password: "securepassword",
      role: 'Data Scientist',
      img: img
    };
  },
  methods: {
    login() {
      this.$refs.loadingButton.startLoading();
      const { email, password,role } = this;
      this.$store
        .dispatch(AUTH_REQUEST, { email, password,role })
        .then(() => {
          console.log(this.$store.getters.role);
          this.$refs.loadingButton.stopLoading();
          if(this.$store.getters.role=='Data Scientist')
          this.$router.push('/datascientist');
          else if(this.$store.getters.role=='End User')
          this.$router.push('/enduser');
          else if(this.$store.getters.role=='App Developer')
          this.$router.push('/appdeveloper');
          else if(this.$store.getters.role=='Platform Admin')
          this.$router.push('/platformadmin');

        })
        .catch(error => {
          this.$refs.loadingButton.stopLoading();
          this.$snack.danger({
            text: error.message
          });
        });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "./../styles/auth-styles";
</style>
