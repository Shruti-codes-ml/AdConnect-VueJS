<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3" >
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
        
        <h5 class="display-5">Manage Sponsor Approvals</h5>
        <table class="table table-hover" v-if="pendingSponsors.length>0">
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
                <tr v-for="sponsor in pendingSponsors" :key="sponsor.id">
                    <td>{{ sponsor.username }}</td>
                    <td>{{ sponsor.name }}</td>
                    <td>{{ sponsor.budget }}</td>
                    <td>{{ sponsor.industry }}</td>
                    <td>
                        <button @click="confirmApproval(sponsor)" class="btn btn-success"> Approve </button>
                        <button @click="rejectApproval(sponsor)" class="btn btn-danger">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-else>No new sponsors</p>

        <div v-if="showConfirmationModel">
            <div>
                <h2>{{ confirmationTitle }}</h2>
                <p>{{ confirmationMessage }}</p>
                <div>
                    <button @click="handleConfirmation(true)" class="btn btn-success">Confirm</button>
                    <button @click="handleConfirmation(false)" class="btn btn-danger">Cancel</button>
                </div>
            </div>
        </div>
        <button @click="goToAdminHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
    </div>
</template>

<script>
import axios from 'axios';


export default{
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            user_id : JSON.parse(localStorage.getItem('user')).id,
            pendingSponsors : [],
            showConfirmationModel:false,
            confirmationTitle:'',
            pendingSponsorToHandle:null,
        }
    },
    created(){
        this.fetchPendingSponsors();
    },
    methods:{
        goToSponsorApproval() {
            this.$router.push('/admin/sponsor_approval');
        },
        goToAdminHome() {
            this.$router.push('/admin_home');
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
        fetchPendingSponsors(){
            const accessToken=localStorage.getItem('token');
            axios.
                get('/admin/pending_sponsors',{
                    headers:{
                        Authorization: `Bearer ${accessToken }`
                    }
                })
                .then((response) => {
                    this.pendingSponsors = response.data;
                })
                .catch((error) => {
                    console.error(error)
                })
        },
        handleSponsorAction(sponsorId,status){
            const accessToken = localStorage.getItem('token');
            const data={
                sponsor_id : sponsorId,
                status:status,
            };
            axios.post('/admin/pending_sponsors',data,{
                headers:{
                    Authorization: `Bearer ${accessToken}`,
                },
            })
            .then(() => {
                this.pendingSponsors = this.pendingSponsors.filter(
                (sponsor) => sponsor.id !== sponsorId
            );
            })
            .catch((error) => {
                console.error(error)
            })
        },
        confirmApproval(sponsor){
            this.pendingSponsorToHandle=sponsor;
            this.confirmationTitle='Approve Sponsor';
            this.confirmationMessage=`Approve ${sponsor.username}'s approval request`;
            this.showConfirmationModel=true;
        },
        rejectApproval(sponsor){
            this.pendingSponsorToHandle=sponsor;
            this.confirmationTitle='Reject Sponsor';
            this.confirmationMessage=`Reject ${sponsor.username}'s approval request`;
            this.showConfirmationModel=true;
        },
        handleConfirmation(isConfirmed){
            if (isConfirmed){
                if (this.confirmationTitle == 'Approve Sponsor'){
                    this.handleSponsorAction(this.pendingSponsorToHandle.id,'approve');
                } else{
                    this.handleSponsorAction(this.pendingSponsorToHandle.id,'reject');
                }
            }
            this.showConfirmationModel = false;
        }
    }
}

</script>