import {
  AUTH_REQUEST,
  AUTH_SIGNUP,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT
} from "@/store/actions/auth";
import { USER_REQUEST } from "../actions/user";
import { apiCall, api_routes } from "@/utils/api";
import router from "./../../router";

const state = {
  token: localStorage.getItem("user-token") || "",
  status: "",
  hasLoadedOnce: false,
  role:"Data Scientist"
};

const getters = {
  isAuthenticated: state => state.token?true:false,
  authStatus: state => state.status,
  role: state=>state.role,
};
const delay =(ms) => new Promise((resolve)=>setTimeout(resolve,ms));
const wait =async () =>{
  await delay(3000);
  return {'token':'dgffgfgfgffefe'};
  // return {
  //   'user-token':'#dgffgfgfgf'
  // };

}
const actions = {
  [AUTH_REQUEST]: ({ commit, dispatch }, user) => {
    return new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      // apiCall({ url: api_routes.user.login, data: user, method: "post" })
      wait()
        .then(resp => {
          resp.role = user.role;
          // resp = {'user-token':'234rft4etgdfst5r56rt6566'}

          localStorage.setItem("user-token", resp.token);
          // Here set the header of your ajax library to the token value.
          // example with axios
          // axios.defaults.headers.common['Authorization'] = resp.token
          commit(AUTH_SUCCESS, resp);
          console.log(resp.token);
          dispatch(USER_REQUEST);
          // router.push('/').catch(()=>{});
          resolve(resp);
        })
        .catch(err => {
          commit(AUTH_ERROR, err);
          localStorage.removeItem("user-token");
          reject(err);
        });
    });
  },
  [AUTH_SIGNUP]: ({ commit }, user) => {
    return new Promise((resolve, reject) => {
      commit(AUTH_REQUEST);
      apiCall({ url: api_routes.user.signup, data: user, method: "post" })
        .then(resp => {
          resolve(resp);
        })
        .catch(err => {
          reject(err);
        });
    });
  },
  [AUTH_LOGOUT]: ({ commit }) => {
    return new Promise(resolve => {
      commit(AUTH_LOGOUT);
      localStorage.removeItem("user-token");
      // router.push("/login");
      resolve();
    });
  }
};

const mutations = {
  [AUTH_REQUEST]: state => {
    state.status = "loading";
  },
  [AUTH_SUCCESS]: (state, resp) => {
    state.status = "success";
    state.token = resp.token;
    state.hasLoadedOnce = true;
    state.role = resp.role;
    Event.$emit("user-authenticated");
  },
  [AUTH_ERROR]: state => {
    state.status = "error";
    state.hasLoadedOnce = true;
  },
  [AUTH_LOGOUT]: state => {
    state.token = "";
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
