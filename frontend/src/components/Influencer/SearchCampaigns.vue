<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
      <div v-if="isAuthenticated">
          <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
          <h3 class="display-3">Hello @<span class="text-muted">{{ username   }}</span></h3>

          <div class="d-flex gap-5">
            <button @click="goToShowAdRequests" class="btn btn-secondary"><i class="fa-regular fa-eye"></i> Show Ad Requests </button>
            <button @click="goToSearchCampaigns" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i> Search Campaigns </button>
          </div>

          <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
            <h5 class="display-5">Public Campaigns</h5>
            <form @submit.prevent="fetchCampaigns(industry,budget)">
                <div class="d-flex gap-5">
                    <label for="industry">Industry</label>
                    <input type="text" v-model="industry" class="form-control" min="0">
                    <label for="budget">Budget</label>
                    <input type="number" v-model="budget" class="form-control" min="0">
                </div>

                <button class="btn btn-primary"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
            </form>

            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Goals</th>
                        <th>Requirements</th>
                        <th>Payment Amount</th>
                        <th>Budget</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="campaign in Campaigns" :key="campaign.id">
                        <td>{{campaign.name}}</td>
                        <td>{{campaign.description}}</td>
                        <td>{{campaign.start_date}}</td>
                        <td>{{campaign.end_date}}</td>
                        <td>{{campaign.goals}}</td>
                        <td>{{campaign.requirements}}</td>
                        <td>{{campaign.payment_amount}}</td>
                        <td>{{ campaign.budget }}</td>
                        <td>
                            <button @click.prevent="InfluencerInterested(campaign)" class="btn btn-success"> Interested </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <button @click="goToInfluencerHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
            </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    data(){
        return{
            username: JSON.parse(localStorage.getItem('user')).username,
            industry: '',   
            budget: '',     
            Campaigns: [],  
            successMessage: '',
            errorMessage: ''
        }  
    },
    created(){
        this.fetchCampaigns();
    },
    computed:{
        ...mapGetters(['isAuthenticated'])
    },
    methods:{
        goToShowAdRequests() {
            this.$router.push('/show_ad_requests_inf');
        },
        goToSearchCampaigns(){
            this.$router.push('/search_campaigns');
        },
        goToInfluencerHome(){
            this.$router.push('/influencer_home');
        },
        fetchCampaigns(industry='',budget=''){
            const accessToken = localStorage.getItem('token');
            axios
                .get('/fetch_campaigns', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                    params: { 
                        industry: industry,
                        budget: budget
                    }
                })
                .then((response) => {
                    this.Campaigns = response.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch campaigns.";
                });
        },
        InfluencerInterested(campaign){
            const accessToken = localStorage.getItem('token');
            const data = {
                campaign_id: campaign.id,
            };
            axios
                .post('/influencer_interested', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    if (response.data.message) {
                        this.successMessage = response.data.message || "Update successful!";
                        this.errorMessage = "";
                    }
                })
                .catch((error) => {
                    this.successMessage = "";
                    this.errorMessage = error.response.data.message || "Error updating ad request.";
                });
        },
    }
}
</script>