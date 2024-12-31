import { createStore } from "vuex";
import router from "@/router";
import { jwtDecode } from "jwt-decode";
// import axios from "axios";


export default createStore({
    state : {
        token : localStorage.getItem('token') || '',
        user : JSON.parse(localStorage.getItem('user')) || null,
    },
    getters : {
        isAuthenticated : state =>  !!state.token,
        userRole: (state) =>{
            if (state.token){
                const decoded = jwtDecode(state.token);
                // console.log("Decoded state in store : " , decoded.sub)
                return decoded.sub;
            }
            return null
        }
    },
    mutations:{
        setToken(state,token){
            state.token = token;
            if (token){
                localStorage.setItem('token',token);
            } else {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        },
        setUser(state, user) {
            state.user = user;
            if (user) {
              localStorage.setItem("user", JSON.stringify(user));
            } else {
              localStorage.removeItem("user");
            }
          },
        logout(state){
            state.token = '';
            state.user=null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            
        },
    },
    actions:{
        login({ commit }, { token, user }) {
            commit('setToken', token);
            commit('setUser', user);
          },
        logout({commit}){
            commit('logout');
            router.push('/login');
        }
    }
})