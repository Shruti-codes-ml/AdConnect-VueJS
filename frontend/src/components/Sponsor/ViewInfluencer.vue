<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
        <div v-if="isAuthenticated">
            <div v-if="errorMessage" class="alert alert-danger">
                    {{ errorMessage }}
            </div>
            <div v-if="successMessage" class="alert alert-success mt-3">
                {{ successMessage }}
            </div>

            <div class="container d-flex justify-content-center align-items-center mt-5">
                <div class="col-md-8 d-inline-block p-4 bg-white bg-opacity-75 rounded shadow">
                
                    <div class="card p-4 bg-white bg-opacity-75">
                        <h1 class="card-title">Influencer Profile</h1>
                        <form @submit.prevent="SendAdRequest(InfluencerId)">
                            
                            <div class="form-group p-2">
                                <label for="username" class="card-text">Username</label>
                                <input type="text" v-model="username" class="form-control" readonly>
                            </div>
                            <div class="form-group p-2">
                                <label for="name" class="card-text">Name</label>
                                <input type="text" v-model="name" class="form-control" readonly>
                            </div>
                            <div class="form-group p-2">
                                <label for="category" class="card-text">Category</label>
                                <input type="text" v-model="category" class="form-control" readonly>
                            </div>
                            <div class="form-group p-2">
                                <label for="niche" class="card-text">Niche</label>
                                <input type="text" v-model="niche" class="form-control" readonly>
                            </div>
                            <div class="form-group p-2">
                                <label for="reach" class="card-text">Reach</label>
                                <input type="text" v-model="reach" class="form-control" readonly>
                            </div>

                            
                            <div class="form-group mt-3 p-2">
                                <button type="submit" class="btn btn-primary"><i class="fa-solid fa-plus"></i> Create ad request</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default{
    data(){
        return{
            username:"",
            name:"",
            category:"",
            niche:"",
            reach:"",
            successMessage: '',
            errorMessage: '',
        } 
    },
    created(){
        this.fetchInfluencerData();
    },
    computed: {
        InfluencerId() {
            return this.$route.params.id;
        },
        ...mapGetters(['isAuthenticated']),
    },
    methods:{
        fetchInfluencerData(){
            const accessToken = localStorage.getItem('token');
            axios
                .get(`/sponsor/fetch_influencer_info/${this.InfluencerId}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    this.username = response.data.username;
                    this.name = response.data.name;
                    this.category = response.data.category;
                    this.niche = response.data.niche;
                    this.reach= response.data.reach;
                })
                .catch((error) => {
                    console.error(error);
                    this.errorMessage = "Failed to fetch influencer.";
                });
        },
        SendAdRequest() {
            this.$router.push('/sponsor/create_ad_request_sponsor');
        },
    }
}
</script>