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

          <h5 class="display-5">Create Ad Request</h5>

          <form @submit.prevent="createAdRequest">
                <div class="form-group p-2">
                    <label for="campaign_id" class="form-label">Campaign Name</label>
                    <select id="campaign_id" v-model="campaign_id" class="form-select">
                        <option value=""></option>
                        <option
                            v-for="campaign in campaigns"
                            :key="campaign.id"
                            :value="campaign.id"
                            :data-requirements="campaign.requirements"
                            :data-payment="campaign.payment_amount"
                        >
                        {{ campaign.name }}
                        </option>
                    </select>
                </div>
                <div class="form-group p-2">
                    <label for="influencer_name" class="form-label">Influencer Name</label>
                    <select v-model="influencer_id" class="form-select">
                        <option
                            v-for="influencer in influencers"
                            :key="influencer.id"
                            :value="influencer.id"
                        >
                            {{ influencer.name }}
                        </option>
                    </select>
                </div>
                <div class="form-group p-2">
                    <label for="messages" class="form-label">Message</label>
                    <input type="text" class="form-control" v-model="message" name="messages" />
                </div>
                <div class="form-group p-2">
                    <label for="requirements" class="form-label">Requirements</label>
                    <input type="text" id="requirements" class="form-control" v-model="requirements"/>
                </div>
                <div class="form-group p-2">
                    <label for="payment_amount" class="form-label">Payment Amount</label>
                    <input type="number" id="payment_amount" class="form-control" v-model="paymentAmount" min="0" required/>
                </div>

                <div class="d-flex gap-5">
                    <button class="btn btn-success mt-3"><i class="fa-solid fa-plus"></i> Create Ad Request</button>
            </div>
          </form> 
          <button @click="goToSponsorHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            campaigns: [],  
            influencers:[],
            successMessage: '',
            errorMessage: '',
            campaign_id:null,
            influencer_id:null,
            message:"",
            requirements:"",
            paymentAmount:0
        } 
    },
    created(){
        this.fetchCampaigns();
        this.fetchInfluencers();
    },
    computed:{
        ...mapGetters(['isAuthenticated'])
    },
    methods:{
        goToSponsorHome(){
            this.$router.push('/sponsor_home');
        },
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
        goToSponsoreHome(){
            this.$router.push('/sponsor_home');
        },
        fetchCampaigns(){
            const accessToken = localStorage.getItem('token');
            axios
                .get('/fetch_campaigns_sponsor', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.campaigns = response.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch campaigns.";
                });
        },
        fetchInfluencers(){
            const accessToken = localStorage.getItem('token');
            axios
                .get('/fetch_influencers', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.influencers = response.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch campaigns.";
                });
        },
        createAdRequest(){
            const accessToken = localStorage.getItem('token');
            const data = {
                campaign_id: this.campaign_id,
                influencer_id : this.influencer_id,
                message : this.message,
                requirements : this.requirements,
                payment_amount : this.paymentAmount,
            };
            axios
                .post('/sponsor/create_adrequest', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    if (response.data.message) {
                        this.successMessage = response.data.message || "Update successful!";
                        console.log(this.successMessage)
                        this.errorMessage = "";
                    }
                    setTimeout(() => {
                        this.$router.push("/sponsor_home");
                    }, 2000);
                })
                .catch((error) => {
                    this.successMessage = "";
                    this.errorMessage = error.response.data.message || "Error updating ad request.";
                });
        }
    }
}
</script>