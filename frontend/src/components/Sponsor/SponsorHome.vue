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
      </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
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
    }
}
</script>