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
            <h5 class="display-5">My Ad requests</h5>
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Campaign</th>
                        <th>Influencer</th>
                        <th>Message</th>
                        <th>Requirement</th>
                        <th>Payment</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ad_request in AdRequests" :key="ad_request.id">
                        <td>{{ad_request.campaign_name}}</td>
                        <td>{{ad_request.influencer_name}}</td>
                        <td>{{ad_request.messages}}</td>
                        <td>{{ad_request.requirements}}</td>
                        <td>{{ad_request.payment_amount}}</td>
                        <td>
                            <span v-if="ad_request.sponsor_accepted && ad_request.influencer_accepted === null">
                            Sponsor Accepted
                            </span>
                            <span v-else-if="ad_request.sponsor_accepted === null && ad_request.influencer_accepted">
                            Influencer Accepted
                            </span>
                            <span v-else-if="ad_request.sponsor_accepted === false && ad_request.influencer_accepted === null">
                            Sponsor Rejected
                            </span>
                            <span v-else-if="ad_request.sponsor_accepted === null && ad_request.influencer_accepted === false">
                            Influencer Rejected
                            </span>
                            <span v-else>
                            {{ ad_request.status }}
                            </span>
                        </td>
                        <td>
                            <button @click="goToProcessPayment(ad_request.id)" v-if="ad_request.sponsor_accepted === true && ad_request.influencer_accepted === true" 
                                    :class="{
                                        'btn btn-secondary': ad_request.payment_status !== true, 
                                        'btn btn-success': ad_request.payment_status === true 
                                    }" 
                                    :disabled="ad_request.payment_status === true">
                                <i :class="ad_request.payment_status === true ? 'fa-solid fa-thumbs-up' : 'fa-solid fa-money-bill'"></i>
                                {{ ad_request.payment_status === true ? 'Payment Done' : 'Process Payment' }}
                            </button>
                            <button v-else-if="ad_request.sponsor_accepted && ad_request.influencer_accepted !== false" class="btn btn-success" disabled>
                                <i class="fa-regular fa-circle-check"></i> Accepted
                            </button>
                            <button v-else-if="ad_request.influencer_accepted === false || ad_request.sponsor_accepted === false" class="btn btn-danger" disabled>
                            <i class="fa-regular fa-circle-xmark"></i> Rejected
                            </button>
                            <div v-else>
                            <form @submit.prevent="acceptRequest(ad_request)">
                                <button type="submit" class="btn btn-success">
                                <i class="fa-regular fa-circle-check"></i> Accept
                                </button>
                            </form>
                            <form @submit.prevent="rejectRequest(ad_request)">
                                <button type="submit" class="btn btn-danger">
                                <i class="fa-regular fa-circle-xmark"></i> Reject
                                </button>
                            </form>
                            <form @submit.prevent="openNegotiationModal(ad_request)">
                                <button type="submit" class="btn btn-info">
                                <i class="fa-regular fa-handshake"></i> Negotiate
                                </button>
                            </form>
                            <button @click="openDeleteModal(ad_request)" class="btn btn-danger"><i class="fas fa-trash"></i> Delete  </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>

      <div v-if="isNegotiating" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5)">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Negotiate Ad Request</h5>
                        <button type="button" class="btn-close" @click="closeNegotiationModal"></button>
                    </div>
                    <div class="modal-body">
                        <textarea v-model="negotiationMessage" class="form-control" placeholder="Enter your negotiation message..."></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeNegotiationModal">Close</button>
                        <button type="button" class="btn btn-primary" @click="negotiateRequest">Submit</button>
                    </div>
                </div>
            </div>
        </div>


        <div v-if="isDeleting" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5)">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Ad Request</h5>
                        <button type="button" class="btn-close" @click="closeDeleteModal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete the ad request ?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Close</button>
                        <button type="button" class="btn btn-primary" @click="deleteAdRequest">Submit</button>
                    </div>
                </div>
            </div>
        </div>

      <button @click="goToSponsorHome" class="btn btn-primary mt-3"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            AdRequests : [],
            errorMessage : "",
            successMessage : "",
            isNegotiating: false,   
            negotiationMessage: "",
            currentAdRequest: null,
            isDeleting: false 

        } 
    },
    created(){
        this.fetchAdRequests();
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
        goToSponsorHome(){
            this.$router.push('/sponsor_home');
        },
        goToProcessPayment(ad_request_id){
            this.$router.push(`/sponsor/process_payment/${ad_request_id}`);
        },
        fetchAdRequests() {
            const accessToken = localStorage.getItem('token');
            axios
                .get('/fetch_ad_requests', {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.AdRequests = response.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },  
        acceptRequest(ad_request){
            const accessToken = localStorage.getItem('token');
            const data = {
                ad_request_id: ad_request.id,
                sponsor_accepted : true,
                messages : ""
            };
            axios
                .post('/accept_requests', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    if (response.data.message) {
                        this.successMessage = response.data.message || "Update successful!";
                        this.errorMessage = "";
                        setTimeout(() => {
                            this.fetchAdRequests();
                        }, 2000);
                    }
                })
                .catch((error) => {
                    this.successMessage = "";
                    this.errorMessage = error.response.data.message || "Error updating ad request.";
                });
        },
        rejectRequest(ad_request){
            const accessToken = localStorage.getItem('token');
            const data = {
                ad_request_id: ad_request.id,
                sponsor_accepted : false,
                messages : ""
            };
            axios
                .post('/accept_requests', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    if (response.data.message) {
                        this.successMessage = response.data.message || "Update successful!";
                        this.errorMessage = "";
                        setTimeout(() => {
                            this.fetchAdRequests();
                        }, 2000);
                    }
                })
                .catch((error) => {
                    this.successMessage = "";
                    this.errorMessage = error.response.data.message || "Error updating ad request.";
                });
        },
        openNegotiationModal(ad_request) {
            this.currentAdRequest = ad_request;
            this.isNegotiating = true;
        },
        closeNegotiationModal() {
            this.isNegotiating = false;
            this.negotiationMessage = "";
            this.currentAdRequest = null;
        },
        negotiateRequest(){
            if (this.negotiationMessage.trim() === "") {
                this.errorMessage = "Message cannot be empty!";
                return;
            }

            const accessToken = localStorage.getItem('token');
            const data = {
                ad_request_id: this.currentAdRequest.id,
                messages : this.negotiationMessage,
                sponsor_accepted : null
            };
            axios
                .post('/accept_requests', data, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                })
                .then((response) => {
                    if (response.data.message) {
                        this.successMessage = response.data.message || "Update successful!";
                        this.errorMessage = "";
                        this.isNegotiating = false, 
                        setTimeout(() => {
                            this.fetchAdRequests();
                        }, 2000);
                    }
                })
                .catch((error) => {
                    this.successMessage = "";
                    this.errorMessage = error.response.data.message || "Error updating ad request.";
                });
        },
        openDeleteModal(ad_request) {
            this.currentAdRequest = ad_request;
            this.isDeleting = true;
        },
        closeDeleteModal() {
            this.isDeleting = false;
            this.currentAdRequest = null;
        },
        deleteAdRequest() {
            const accessToken = localStorage.getItem('token');
            axios
                .delete(`/delete_ad_request/${this.currentAdRequest.id}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.successMessage = response.data.message || "Ad Request deleted successfully!";
                    this.errorMessage = '';
                    this.isDeleting = false;
                    this.currentAdRequest = null;
                    setTimeout(() => {
                        this.fetchAdRequests(); // Refresh the campaigns list
                        }, 1000);
                     
                })
                .catch((error) => {
                    this.errorMessage = error.response?.data?.message || "Failed to delete campaign.";
                    this.successMessage = '';
                });
        },
    }
}
</script>

<style scoped>
/* Additional styling for modal (optional) */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1050;
    display: block;
}
</style>