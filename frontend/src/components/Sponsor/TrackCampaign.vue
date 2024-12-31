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
            <h5 class="display-5">Track Campaign {{ CampaignsData.campaign_name }}</h5>

            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <div class="alert alert-warning" role="alert" style="gap: 10px;">
                            <h4 class="alert-heading">Campaign Goals </h4> 
                            <p class="lead">{{ CampaignsData.campaign_goals }}</p>
                        </div>
                    </div>
                </div>
                <div class="alert alert-secondary" role="alert">
                    <div class="row">
                        <div class="col-md-4">
                            <p class="lead">End Date : {{CampaignsData.end_date}} </p>
                        </div>
                        <div class="col-md-4">
                            <p class="lead">Budget Allocated : {{CampaignsData.budget}} </p>
                        </div>
                        <div class="col-md-4">
                            <p class="lead">Budget Spent : {{CampaignsData.amount_spent}}</p>
                        </div>
                    </div>
                </div>

                <div class="row">
        
                    <div class="col-md-3">
                        <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                            <div class="card-header">Total Ad Requests</div>
                            <div class="card-body">
                                <h5 class="card-title"> {{ CampaignsData.no_of_adrequests }}  </h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">
                            <div class="card-header">Ad Requests Accepted</div>
                            <div class="card-body">
                                <h5 class="card-title"> {{ CampaignsData.accepted_ad_requests }}  </h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-white bg-success mb-3" style="max-width: 18rem;">
                            <div class="card-header">Ad Requests Rejected</div>
                            <div class="card-body">
                                <h5 class="card-title"> {{ CampaignsData.rejected_ad_requests }}  </h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-white bg-danger mb-3" style="max-width: 18rem;">
                            <div class="card-header">Platforms Covered</div>
                            <div class="card-body">
                                <h5 class="card-title"> {{ CampaignsData.unique_platforms }} </h5>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            
            <button @click="goToSponsorHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
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
            CampaignsData:[],
            successMessage:"",
            errorMessage:""
        } 
    },
    created(){
        this.trackCampaigns();
    },
    computed: {
        campaignId() {
            return this.$route.params.id;
        },
        ...mapGetters(['isAuthenticated']),
        
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
        goToSponsorHome(){
            this.$router.push('/sponsor_home');
        },
        trackCampaigns(){
            const accessToken = localStorage.getItem('token');
            axios
                .get(`/track_campaign_info/${this.campaignId}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.CampaignsData = response.data;
                    console.log("CampaignData : " , response.data)
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch campaigns.";
                });
        }
    }
};
</script>