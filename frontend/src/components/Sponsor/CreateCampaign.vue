<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
        <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
          </div>
          <div v-if="this.successMessage" class="alert alert-success mt-3">
                {{ successMessage }}
          </div>
      <div v-if="isAuthenticated">
          <h3 class="display-3">Hello @<span class="text-muted">{{ username }}</span></h3>

          <div class="d-flex gap-5">
            <button @click="goToCreateCampaign" class="btn btn-primary"><i class="fa-solid fa-plus"></i> Create Campaign </button>
            <button @click="goToShowCampaigns" class="btn btn-secondary"><i class="fa-solid fa-list"></i> Show Campaigns </button>
            <button @click="goToSearchInfluencer" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i> Search Influencers </button>
            <button @click="goToCreateAdRequest" class="btn btn-info"><i class="fa-solid fa-plus"></i> Create Ad Request </button>
            <button @click="goToShowAdRequests" class="btn btn-success"><i class="fa-regular fa-eye"></i> Show ad requests </button>
          </div>

          <form @submit.prevent="CreateCampaign">
            <h5 class="display-5">Create Campaign</h5>

            <div class="form-group p-2">
                <label for="name" class="form-label">Name of the Campaign</label>
                <input type="text" v-model="campaign_name" class="form-control" required>
            </div>
            <div class="form-group p-2">
                <label for="description" class="form-label"> Description </label>
                <input type="text" v-model="description" class="form-control" required>
            </div>
            <div class="form-group p-2">
                <label for="start_date" class="form-label">Start Date</label>
                <input type="date" v-model="start_date" class="form-control" required>
            </div>
            <div class="form-group p-2">
                <label for="end_date" class="form-label">End Date</label>
                <input type="date" v-model="end_date" class="form-control" required>
            </div>
            <div class="form-group p-2">
                <label for="budget" class="form-label">Budget</label>
                <input type="number" v-model="budget" class="form-control" min="0" required>
            </div>
            <div class="form-group p-2">
                <label for="visibility" class="form-label">Visibility</label>
                <select v-model="visibility" class="form-select">
                    <option selected value="public">Public</option>
                    <option value="private">Private</option>
                </select>
            </div>
            <div class="form-group p-2">
                <label for="goals" class="form-label">Goals</label>
                <input type="text" v-model="goals" class="form-control">
            </div>
            <div class="form-group p-2">
                <label for="requirements" class="form-label">Requirements</label>
                <input type="text" v-model="requirements" class="form-control" required>
            </div>
            <div class="form-group p-2">
                <label for="payment" class="form-label">Payment</label>
                <input type="number" v-model="payment" class="form-control" min="0" required>
            </div>

            <div class="d-flex p-2 gap-3">
                <button class="btn btn-info"><i class="fa-solid fa-plus"></i> Create Campaign </button>
                <button @click="goToSponsorHome" class="btn btn-primary"><i class="fa fa-arrow-circle-left"></i> Go Back</button>
            </div>

          </form>
      </div>
      
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
    data(){
        const today = new Date();
        const yyyy = today.getFullYear();
        let mm = today.getMonth() + 1; // Months start at 0!
        let dd = today.getDate();

        // Add leading zero if necessary
        if (mm < 10) mm = '0' + mm;
        if (dd < 10) dd = '0' + dd;

        const todayDateString = `${yyyy}-${mm}-${dd}`;
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            campaign_name : "",
            description : "",
            start_date : todayDateString,
            end_date : todayDateString,
            budget:0,
            visibility:"public",
            goals:"",
            requirements:"",
            payment:0,
            successMessage: "",
            errorMessage: ""

        } 
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
        goToSponsorHome() {
            this.$router.push('/sponsor_home');
        },
        CreateCampaign(){
            const accessToken = localStorage.getItem('token');
            const data = {
                campaign_name: this.campaign_name,
                description : this.description,
                start_date : this.start_date,
                end_date : this.end_date,
                budget : this.budget,
                visibility : this.visibility,
                goals : this.goals,
                requirements : this.requirements,
                payment : this.payment
            };
            axios
                .post('/sponsor/create_campaign', data, {
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