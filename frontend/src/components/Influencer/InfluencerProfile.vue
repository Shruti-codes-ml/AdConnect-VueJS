<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
      <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
      <h3 class="display-3">Hello @<span class="text-muted">{{ influencer.username   }}</span></h3>
      <button class="btn btn-danger" @click="logout">Logout</button>

      <form @submit.prevent="updateProfile">
        <div class="form-group">
                <label for="username" class="card-text">Username</label>
                <input v-model="influencer.username" type="text" id="username" class="form-control" required>
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
                <input type="text" v-model="influencer.name" class="form-control" required>
            </div>

            <div class="form-group">
                <label for="category" class="card-text">Category</label>
                <input type="text" v-model="influencer.category" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="niche" class="card-text">Niche</label>
                <input type="text" v-model="influencer.niche" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="reach" class="card-text">Reach</label>
                <input type="text" v-model="influencer.reach" class="form-control" required>
            </div>   
            <div class="form-group mt-3">
                <button type="submit" class="btn btn-primary">Update Profile</button>
            </div>        
      </form>
      </div>
      
</template>
  
  
<script>
import axios from 'axios';
import { mapActions } from 'vuex';

export default{
  data() {
    return {
      influencer: {
        username: "",
        name: "",
        category: "",
        niche: "",
        reach: "",
      },
      current_password: "",
      new_password: "",
      confirm_new_password: "",
      successMessage: "",
      errorMessage: "",
    };
  },
  created(){
    this.fetchInfluencerDetails();
  },
  methods: {
    ...mapActions(['logout']),
    fetchInfluencerDetails(){
      const accessToken = localStorage.getItem('token');
      axios.get('/influencer_profile', {
          headers: {
              Authorization: `Bearer ${accessToken}`,
          },
      })
      .then((response) =>{
        console.log(response.data)
        this.influencer = response.data;
      })
      .catch((error) => {
          this.errorMessage = error.response.data.message || "Failed to load influencer details.";
        });
    },
    updateProfile() {
      const accessToken = localStorage.getItem('token');

      const data = {
          username: this.influencer.username,
          current_password: this.current_password,
          new_password: this.new_password,
          confirm_new_password: this.confirm_new_password,
          name: this.influencer.name,
          category: this.influencer.category,
          niche: this.influencer.niche,
          reach: this.influencer.reach,
        };

      axios
        .post("/influencer_profile", data, {
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