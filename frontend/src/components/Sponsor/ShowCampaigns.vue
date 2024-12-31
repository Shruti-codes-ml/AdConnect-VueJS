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
            <h5 class="display-5">My Campaigns</h5>

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
                    <tr v-for="campaign in Campaigns" :key="campaign.id" :class="{'table-danger': campaign.flagged}"> 

                        <td>{{campaign.name}}</td>
                        <td>{{campaign.description}}</td>
                        <td>{{campaign.start_date}}</td>
                        <td>{{campaign.end_date}}</td>
                        <td>{{campaign.goals}}</td>
                        <td>{{campaign.requirements}}</td>
                        <td>{{campaign.payment_amount}}</td>
                        <td>{{ campaign.budget }}</td>
                        <td>
                            <button @click="goToTrackCampaign(campaign)" class="btn btn-info"><i class="fa-solid fa-chart-column"></i> Track  </button>
                            <button @click="goToUpdateCampaign(campaign)" class="btn btn-primary"><i class="fas fa-edit"></i> Update  </button>
                            <button @click="openDeleteModal(campaign)" class="btn btn-danger"><i class="fas fa-trash"></i> Delete  </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <button @click="goToSponsorHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
            </div>

            <div v-if="isDeleting" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5)">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Campaign</h5>
                        <button type="button" class="btn-close" @click="closeDeleteModal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete the campaign {{ this.currentCampaign.name }}?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Close</button>
                        <button type="button" class="btn btn-primary" @click="deleteCampaign">Submit</button>
                    </div>
                </div>
            </div>
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
            username:JSON.parse(localStorage.getItem('user')).username,
            Campaigns: [],  
            successMessage: '',
            errorMessage: '',
            isDeleting: false,
            currentCampaign: null,
        } 
    },
    created(){
        this.fetchCampaigns();
    },
    computed:{
        ...mapGetters(['isAuthenticated'])
    },
    methods:{
        goToTrackCampaign(campaign){
            this.$router.push(`/sponsor/track_campaign_page/${campaign.id}`);
        },
        goToUpdateCampaign(campaign){
            this.$router.push(`/sponsor/update_campaign/${campaign.id}`);
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
        goToSponsorHome(){
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
                    this.Campaigns = response.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch campaigns.";
                });
        },
        openDeleteModal(campaign) {
            this.currentCampaign = campaign;
            this.isDeleting = true;
        },
        closeDeleteModal() {
            this.isDeleting = false;
            this.currentCampaign = null;
        },
        deleteCampaign() {
            const accessToken = localStorage.getItem('token');
            axios
                .delete(`/delete_campaign/${this.currentCampaign.id}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.successMessage = response.data.message || "Campaign deleted successfully!";
                    this.errorMessage = '';
                    this.isDeleting = false;
                    this.currentCampaign = null;
                    setTimeout(() => {
                        this.fetchCampaigns(); // Refresh the campaigns list
                        }, 1000);
                     
                })
                .catch((error) => {
                    this.errorMessage = error.response?.data?.message || "Failed to delete campaign.";
                    this.successMessage = '';
                });
        },
    },
};
</script>