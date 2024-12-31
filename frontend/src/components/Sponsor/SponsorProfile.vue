<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
      <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
      <div v-if="isAuthenticated">
        <h3 class="display-3">Hello @<span class="text-muted">{{  sponsor.username  }}</span></h3>
          <button class="btn btn-danger" @click="logout">Logout</button>
          <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label for="username" class="card-text">Username</label>
                <input v-model="sponsor.username" type="text" id="username" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="password" class="card-text">Current Password</label>
                <input type="password" v-model="current_password" class="form-control">
            </div>
            <div class="form-group">
                <label for="new_password" class="card-text">New Password</label>
                <input type="password" v-model="new_password" class="form-control" >
            </div>
            <div class="form-group">
                <label for="confirm_new_password" class="card-text">Confirm New Password</label>
                <input type="password" v-model="confirm_new_password" class="form-control" >
            </div>
            <div class="form-group">  
                <label for="name" class="card-text">Name</label>
                <input type="text" v-model="sponsor.name" class="form-control" required>
            </div>

            <div class="form-group">
                <label for="budget" class="card-text">Budget</label>
                <input type="text" v-model="sponsor.budget" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="industry" class="card-text">Industry</label>
                <input type="text" v-model="sponsor.industry" class="form-control" required>
            </div>  
            <div class="form-group mt-3">
                <button type="submit" class="btn btn-primary">Update Profile</button>
            </div>        
          </form>
      </div>
    </div> 
      
</template>
  
  
<script>
  import axios from 'axios';
  import { mapGetters,mapActions } from 'vuex';
  
  export default {
    name: 'SponsorProfile',
    data() {
      return {
        sponsor: {
          username: "",
          name: "",
          budget: "",
          industry: "",
        },
        current_password: "",
        new_password: "",
        confirm_new_password: "",
        successMessage: "",
        errorMessage: "",
      };
    },
    created(){
      this.fetchSponsorDetails();
    },
    computed:{
      ...mapGetters(['isAuthenticated'])
    },
    methods: {
      ...mapActions(['logout']),
      fetchSponsorDetails(){
        const accessToken = localStorage.getItem('token');
        axios.get('/sponsor_profile', {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        })
        .then((response) =>{
          console.log(response.data)
          this.sponsor = response.data;
        })
        .catch((error) => {
            this.errorMessage = error.response.data.message || "Failed to load sponsor details.";
          });
      },
      updateProfile() {
        const accessToken = localStorage.getItem('token');

        const data = {
            username: this.sponsor.username,
            current_password: this.current_password,
            new_password: this.new_password,
            confirm_new_password: this.confirm_new_password,
            name: this.sponsor.name,
            budget: this.sponsor.budget,
            industry: this.sponsor.industry,
          };

        axios
          .post("/sponsor_profile", data, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then((response) => {
            if (response.data.message) {
              this.successMessage = response.data.message || "Profile updated successfully!";
              this.errorMessage = "";
            }
          })
          .catch((error) => {
            this.successMessage = "";
            this.errorMessage = error.response.data.message || "Error updating profile.";
          });
      },
    },
  };
</script>