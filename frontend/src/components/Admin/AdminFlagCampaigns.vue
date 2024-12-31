<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
        <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
        </div>

        <h1 class="display-1">Hello @<span class="text-muted">{{ username }}</span></h1>
        
        <div class="d-flex justify-content-start gap-3">
            <button @click="goToSponsorApproval" class="btn btn-secondary"><i class="fa-solid fa-users-viewfinder"></i> Sponsor Approvals</button>
            <button @click="goToFlagInfluencer" class="btn btn-info"><i class="fa-solid fa-flag"></i> Flag Influencers</button>
            <button @click="goToFlagSponsor" class="btn btn-primary"><i class="fa-solid fa-flag"></i> Flag Sponsors</button>
            <button @click="goToFlagCampaign" class="btn btn-secondary"><i class="fa-solid fa-square-poll-horizontal"></i> Flag Campaigns</button>        
        </div>

        <h5 class="display-5">Manage Campaign Flags</h5>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Budget</th>
                    <th>Visibility</th>
                    <th>Goals</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="campaign in FlagCampaigns" :key="campaign.id">
                    <td>{{campaign.name}}</td>
                    <td>{{campaign.description}}</td>
                    <td>{{campaign.start_date}}</td>
                    <td>{{campaign.end_date}}</td>
                    <td>{{campaign.budget}}</td>
                    <td>{{campaign.visibility}}</td>
                    <td>{{campaign.goals}}</td>
                    <td>
                        <button @click="toggleFlag(campaign)" :class="campaign.flagged ? 'btn btn-warning' : 'btn btn-info'">
                            <i class="fa-solid fa-flag"></i> {{ campaign.flagged ? 'Unflag' : 'Flag' }}
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <button @click="goToAdminHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            FlagCampaigns : [],
            pendingCampaignToHandle:null,
        };
    },
    created(){
        this.fetchCampaigns();
    },
    methods:{
        goToSponsorApproval() {
            this.$router.push('/admin/sponsor_approval');
        },
        goToFlagInfluencer(){
            this.$router.push('/admin/flag_influencers');
        },
        goToFlagSponsor(){
            this.$router.push('/admin/flag_sponsors');
        },
        goToFlagCampaign(){
            this.$router.push('/admin/flag_campaigns');
        },
        goToAdminHome() {
            this.$router.push('/admin_home');
        },
        fetchCampaigns() {
            const accessToken = localStorage.getItem('token');
            axios
                .get('/admin/flag_campaigns', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.FlagCampaigns = response.data;
                    console.log(response.data)
                })
                .catch((error) => {
                    console.error(error);
                });
        },  
        toggleFlag(campaign) {
            const accessToken = localStorage.getItem('token');
            const data = {
                campaign_id: campaign.id,
                flagged: !campaign.flagged,
            };
            axios
                .post('/admin/flag_campaigns', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    console.log(response.data);
                    campaign.flagged = !campaign.flagged; // Update local state immediately
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    }
}
</script>