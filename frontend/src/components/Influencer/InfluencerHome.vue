<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
      <div v-if="isAuthenticated">
          <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
          <h3 class="display-3">Hello @<span class="text-muted">{{ username   }}</span></h3>

          <div class="d-flex gap-5">
            <button @click="goToShowAdRequests" class="btn btn-secondary"><i class="fa-regular fa-eye"></i> Show Ad Requests </button>
            <button @click="goToSearchCampaigns" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i> Search Campaigns </button>
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
        goToShowAdRequests() {
            this.$router.push('/show_ad_requests_inf');
        },
        goToSearchCampaigns(){
            this.$router.push('/search_campaigns');
        },
    }
}
</script>