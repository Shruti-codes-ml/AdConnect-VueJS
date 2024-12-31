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

        <h5 class="display-5">Manage Sponsor Flags</h5>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Name</th>
                    <th>Budget</th>
                    <th>Industry</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="sponsor in FlagSponsors" :key="sponsor.id">
                    <td>{{ sponsor.username }}</td>
                    <td>{{ sponsor.name }}</td>
                    <td>{{ sponsor.budget }}</td>
                    <td>{{ sponsor.industry }}</td>
                    <td>
                        <button @click="toggleFlag(sponsor)" :class="sponsor.flagged ? 'btn btn-warning' : 'btn btn-info'">
                            <i class="fa-solid fa-flag"></i> {{ sponsor.flagged ? 'Unflag' : 'Flag' }}
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
            FlagSponsors : [],
            pendingSposnorToHandle:null,
        };
    },
    created(){
        this.fetchSponsors();
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
        fetchSponsors() {
            const accessToken = localStorage.getItem('token');
            axios
                .get('/admin/flag_sponsors', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.FlagSponsors = response.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },  
        toggleFlag(sponsor) {
            const accessToken = localStorage.getItem('token');
            const data = {
                sponsor_id: sponsor.id,
                flagged: !sponsor.flagged,
            };
            axios
                .post('/admin/flag_sponsors', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    console.log(response.data);
                    sponsor.flagged = !sponsor.flagged; // Update local state immediately
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    }
}
</script>