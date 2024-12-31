<template>
    <div class="p-4 bg-white bg-opacity-75 rounded shadow mt-3">
        <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
        </div>
        <h1 class="display-1">Hello @<span class="text-muted">{{ username }}</span></h1>
        
        <div class="container">
            <div class="row">
                <div class="col-md-2">
                    <div class="card text-white bg-primary mb-3" style="max-width: 18rem;">
                        <div class="card-header">Registered Influencers</div>
                        <div class="card-body">
                            <h5 class="card-title">{{influencers}}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="card text-white bg-secondary mb-3" style="max-width: 18rem;">
                        <div class="card-header">Registered Sponsors</div>
                        <div class="card-body">
                            <h5 class="card-title">{{sponsors}}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="card text-white bg-success mb-3" style="max-width: 18rem;">
                        <div class="card-header">Private Campaigns</div>
                        <div class="card-body">
                            <h5 class="card-title">{{private_campaigns}}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="card text-white bg-danger mb-3" style="max-width: 18rem;">
                        <div class="card-header">Public Campaigns</div>
                        <div class="card-body">
                            <h5 class="card-title">{{public_campaigns}}</h5>
                        </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="card text-white bg-info mb-3" style="max-width: 18rem;">
                        <div class="card-header">Flagged Influencers</div>
                        <div class="card-body">
                            <h5 class="card-title">{{flagged_influencers}}</h5>
                            </div>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                        <div class="card-header">Flagged Sponsors</div>
                        <div class="card-body">
                            <h5 class="card-title">{{flagged_sponsors}}</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div class="d-flex justify-content-start gap-3">
            <button @click="goToSponsorApproval" class="btn btn-secondary"><i class="fa-solid fa-users-viewfinder"></i> Sponsor Approvals</button>
            <button @click="goToFlagInfluencer" class="btn btn-info"><i class="fa-solid fa-flag"></i> Flag Influencers</button>
            <button @click="goToFlagSponsor" class="btn btn-primary"><i class="fa-solid fa-flag"></i> Flag Sponsors</button>
            <button @click="goToFlagCampaign" class="btn btn-secondary"><i class="fa-solid fa-square-poll-horizontal"></i> Flag Campaigns</button>        
        </div>

        <div class="container mt-5">
            <div class="row">
                <div class="col-md-4">
                    <canvas id="nicheChart" width="500" height="500"></canvas>
                </div>
                <div class="col-md-4">
                    <canvas id="industryChart" width="500" height="500"></canvas>
                </div>
                <div class="col-md-4">
                    <canvas id="nicheDistributionChart" width="500" height="500"></canvas>
                </div>
            </div>
        </div>

    </div>
</template>

<script>

import Chart from 'chart.js/auto';
import axios from 'axios';

export default{
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            influencers:0,
            sponsors:0,
            private_campaigns:0,
            public_campaigns:0,
            flagged_influencers:0,
            flagged_sponsors:0,
            no_of_acc_req: 0,
            no_of_rej_req: 0,
            no_of_pen_req: 0,
            industries: [],
            counts: [], 
            niches: [], 
            niche_counts: [],
        };
    },
    created(){
        this.DashboardStats();
    },
    methods:{
        DashboardStats(){
            const accessToken=localStorage.getItem('token');
            axios.
                get('/admin/dashboard_stats',{
                    headers:{
                        Authorization: `Bearer ${accessToken }`
                    }
                })
                .then((response) => {
                    console.log('Dashboard Stats:', response.data);
                    this.influencers = response.data.influencers;
                    this.sponsors = response.data.sponsors;
                    this.private_campaigns = response.data.private_campaigns;
                    this.public_campaigns = response.data.public_campaigns;
                    this.flagged_influencers = response.data.flagged_influencers;
                    this.flagged_sponsors = response.data.flagged_sponsors;
                    this.no_of_acc_req = response.data.no_of_acc_req;
                    this.no_of_rej_req = response.data.no_of_rej_req;
                    this.no_of_pen_req = response.data.no_of_pen_req;
                    this.industries = response.data.industries; 
                    this.counts = response.data.counts; 
                    this.niches = response.data.niches; 
                    this.niche_counts = response.data.niche_counts; 

                    this.createNicheChart();
                    this.createIndustryChart();
                    this.createNicheDistributionChart();
                })
                .catch((error) => {
                    console.error(error)
                })
        },
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
        createNicheChart() {
            const xValues = ["Accepted", "Rejected", "Pending"];
            const yValues = [this.no_of_acc_req, this.no_of_rej_req, this.no_of_pen_req];
            const barColors = ["#00aba9", "#e8c3b9", "#1e7145"];
            
            new Chart("nicheChart", {
                type: "doughnut",
                data: {
                labels: xValues,
                datasets: [{
                    backgroundColor: barColors,
                    data: yValues
                }]
                },
                options: {
                title: {
                    display: true,
                    text: "Status of Ad Requests"
                }
                }
            });
        },
        createIndustryChart() {
            const industryColors = ["#FF99C8", "#6B8E23", "#87CEEB", "#D2691E"];

            new Chart("industryChart", {
                type: "bar",
                data: {
                labels: this.industries,
                datasets: [{
                    label: "Number of Sponsors",
                    backgroundColor: industryColors,
                    data: this.counts
                }]
                },
                options: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Distribution of Industries in Sponsors"
                },
                scales: {
                    y: {
                    beginAtZero: true
                    }
                }
                }
            });
        },
        createNicheDistributionChart() {
            const nicheColors = [
                "#5F9EA0", "#FF9F40", "#FFC0CB", "#4BC0C0", "#FFD700", "#00FF00", "#F7464A"
            ];

            new Chart("nicheDistributionChart", {
                type: "pie",
                data: {
                labels: this.niches,
                datasets: [{
                    label: "Number of Influencers",
                    backgroundColor: nicheColors,
                    data: this.niche_counts
                }]
                },
                options: {
                title: {
                    display: true,
                    text: "Distribution of Niches in Influencers"
                }
                }
            });
        }
    },
    //     mounted() {
    //     this.createNicheChart();
    //     this.createIndustryChart();
    //     this.createNicheDistributionChart();
    // }
};
</script>