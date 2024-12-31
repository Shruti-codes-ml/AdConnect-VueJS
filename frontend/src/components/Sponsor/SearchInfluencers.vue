<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
      <div v-if="isAuthenticated">
          <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
          <h3 class="display-3">Hello @<span class="text-muted">{{ username }}</span></h3>

          <div class="d-flex gap-5">
            <button @click="goToCreateCampaign" class="btn btn-primary"><i class="fa-solid fa-plus"></i> Create Campaign </button>
            <button @click="goToShowCampaigns" class="btn btn-secondary"><i class="fa-solid fa-list"></i> Show Campaigns </button>
            <button @click="goToSearchInfluencer" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i> Search Influencers </button>
            <button @click="goToCreateAdRequest" class="btn btn-info"><i class="fa-solid fa-plus"></i> Create Ad Request </button>
            <button @click="goToShowAdRequests" class="btn btn-success"><i class="fa-regular fa-eye"></i> Show ad requests </button>
          </div>

          <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
            <h5 class="display-5">Search Influencers</h5>
            <form @submit.prevent="fetchInfluencers(category,niche,reach)">
                <div class="d-flex gap-5">
                    <label for="category">Category</label>
                    <input type="text" v-model="category" class="form-control">
                    <label for="niche">Niche</label>
                    <input type="text" v-model="niche" class="form-control">
                    <label for="reach">Reach</label>
                    <input type="number" v-model="reach" class="form-control" min="0">
                </div>

                <button class="btn btn-primary"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
            </form>

            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Niche Date</th>
                        <th>Reach</th>
                        <th>View</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="Influencers.length === 0">
                        <td colspan="5" class="text-center">No influencers found</td>
                    </tr>
                    <tr v-for="influencer in Influencers" :key="influencer.id">
                        <td>{{influencer.name}}</td>
                        <td>{{influencer.category}}</td>
                        <td>{{influencer.niche}}</td>
                        <td>{{influencer.reach}}</td>
                        <td>
                            <button @click.prevent="ViewInfluencer(influencer)" class="btn btn-success"><i class="fa-regular fa-eye"></i> View Profile </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>  

      </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            category:"",
            niche:"",
            reach : 0,
            Influencers:[],
            successMessage: '',
            errorMessage: ''
        } 
    },
    created(){
        this.fetchInfluencers();
    },
    computed:{
        ...mapGetters(['isAuthenticated'])
    },
    methods:{
        goToCreateCampaign() {
            this.$router.push('/sponsor/create_campaign');
        },
        goToShowCampaigns() {
            this.$router.push('/sponsor/show_campaigns');
        },
        goToSearchInfluencer() {
            this.$router.push('/sponsor/search_influencers');
        },
        goToCreateAdRequest() {
            this.$router.push('/sponsor/create_ad_request_sponsor');
        },
        goToShowAdRequests() {
            this.$router.push('/sponsor/show_ad_requests');
        },
        fetchInfluencers(category='',niche='',reach=''){
            const accessToken = localStorage.getItem('token');
            axios
                .get('/sponsor/search_influencers', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                    params: { 
                        category: category,
                        niche: niche,
                        reach:reach
                    }
                })
                .then((response) => {
                    this.Influencers = response.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch influencers.";
                });
        },
        ViewInfluencer(influencer){
            this.$router.push(`/sponsor/view_influencer/${influencer.id}`);
        }
    }
}
</script>