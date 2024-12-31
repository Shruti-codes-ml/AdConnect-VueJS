<template>
  <div class="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">AdConnect</router-link>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <div v-if="!isAuthenticated">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/signup" class="nav-link">Sign Up</router-link>
              </li>
            </ul>
          </div>
          <div v-if="isAuthenticated">
              <div v-if="userRole==='admin'">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  <li class="nav-item">
                    <router-link to="/admin_home" class="nav-link">Home</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/admin_profile" class="nav-link">Profile</router-link>
                  </li>
                  </ul>
              </div>
              <div v-if="userRole==='influencer'">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  <li class="nav-item">
                    <router-link to="/influencer_home" class="nav-link">Home</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/influencer_profile" class="nav-link">Profile</router-link>
                  </li>
                </ul>
              </div>
              <div v-if="userRole==='sponsor'">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  <li class="nav-item">
                    <router-link to="/sponsor_home" class="nav-link">Home</router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/sponsor_profile" class="nav-link">Profile</router-link>
                  </li>
                </ul>
              </div>
          </div>
        </div>
      </div>
    </nav>

   
    <!-- Main content area -->
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { mapGetters,mapActions } from 'vuex';
export default {
  name:'App',
  computed:{
    ...mapGetters(['isAuthenticated','userRole'])
  },
  methods:{
    ...mapActions(['login','logout'])
  },
  mounted() {
    // Log the userRole when the component is mounted
    console.log('User Role when app is mounted:', this.userRole);
  }
};
</script>

<style>
body {
  background-image: url('https://picsum.photos/1920/1080');
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.flash-messages .alert {
  margin-top: 10px;
}
</style>
