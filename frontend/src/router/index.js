import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LandingPage from '@/components/LandingPage.vue'
import SignUpUser from '@/components/SignUpUser.vue'
import LoginUser from '@/components/LoginUser.vue'

import AdminHome from '@/components/Admin/AdminHome.vue'
import AdminProfile from '@/components/Admin/AdminProfile.vue'
import AdminSponsorApproval from '@/components/Admin/AdminSponsorApproval.vue'
import AdminFlagInfluencers from '@/components/Admin/AdminFlagInfluencers.vue'
import AdminFlagCampaigns from '@/components/Admin/AdminFlagCampaigns.vue'
import AdminFlagSponsors from '@/components/Admin/AdminFlagSponsors.vue'

import InfluencerProfile from '@/components/Influencer/InfluencerProfile.vue'
import InfluencerHome from '@/components/Influencer/InfluencerHome.vue'
import SearchCampaigns from '@/components/Influencer/SearchCampaigns.vue'
import ShowAdRequests from '@/components/Influencer/ShowAdRequests.vue'

import SponsorProfile from '@/components/Sponsor/SponsorProfile.vue'
import SponsorHome from '@/components/Sponsor/SponsorHome.vue'
import CreateAdRequest from '@/components/Sponsor/CreateAdRequest.vue'
import CreateCampaign from '@/components/Sponsor/CreateCampaign.vue'
import SearchInfluencers from '@/components/Sponsor/SearchInfluencers.vue'
import ShowAdRequestsSponsor from '@/components/Sponsor/ShowAdRequestsSponsor.vue'
import ShowCampaigns from '@/components/Sponsor/ShowCampaigns.vue'
import TrackCampaign from '@/components/Sponsor/TrackCampaign.vue'
import ViewInfluencer from '@/components/Sponsor/ViewInfluencer.vue'
import UpdateCampaign from '@/components/Sponsor/UpdateCampaign.vue'
import ProcessPayment from '@/components/Sponsor/ProcessPayment.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingPage
  },
  {
    path: '/signup',
    name: 'SignUpUser',
    component: SignUpUser
  },
  {
    path: '/login',
    name: 'LoginUser',
    component: LoginUser
  },

//Influencer Routes

  {
    path: '/influencer_home',
    name: 'InfluencerHome',
    component: InfluencerHome,
    meta : {requiresAuth:true,roles:['influencer']}
  },
  {
    path: '/influencer_profile',
    name: 'InfluencerProfile',
    component: InfluencerProfile,
    meta : {requiresAuth:true,roles:['influencer']}
  },
  {
    path: '/show_ad_requests_inf',
    name: 'ShowAdRequests',
    component: ShowAdRequests,
    meta : {requiresAuth:true,roles:['influencer']}
  },
  {
    path: '/search_campaigns',
    name: 'SearchCampaigns',
    component: SearchCampaigns,
    meta : {requiresAuth:true,roles:['influencer']}
  },


//Sponsor Routes

  {
    path: '/sponsor_home',
    name: 'SponsorHome',
    component: SponsorHome,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor_profile',
    name: 'SponsorProfile',
    component: SponsorProfile,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/create_campaign',
    name: 'CreateCampaign',
    component: CreateCampaign,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/show_campaigns',
    name: 'ShowCampaigns',
    component: ShowCampaigns,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/search_influencers',
    name: 'SearchInfluencers',
    component: SearchInfluencers,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/create_ad_request_sponsor',
    name: 'CreateAdRequest',
    component: CreateAdRequest,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/show_ad_requests',
    name: 'ShowAdRequestsSponsor',
    component: ShowAdRequestsSponsor,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/track_campaign_page/:id',
    name: 'TrackCampaign',
    component: TrackCampaign,
    props: true,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/update_campaign/:id',
    name: 'UpdateCampaign',
    component: UpdateCampaign,
    props: true,
    meta : {requiresAuth:true,roles:['sponsor']}
  },
  {
    path: '/sponsor/view_influencer/:id',
    name: 'ViewInfluencer',
    component: ViewInfluencer,
    props: true,
    meta : {requiresAuth:true,roles:['sponsor']}
  },{
    path: '/sponsor/process_payment/:id',
    name: 'ProcessPayment',
    component: ProcessPayment,
    props: true,
    meta : {requiresAuth:true,roles:['sponsor']}
  },



//Admin Routes


  {
    path: '/admin_profile',
    name: 'AdminProfile',
    component: AdminProfile,
    meta : {requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin_home',
    name: 'AdminHome',
    component: AdminHome,
    meta : {requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin/sponsor_approval',
    name: 'AdminSponsorApproval',
    component: AdminSponsorApproval,
    meta : {requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin/flag_influencers',
    name: 'AdminFlagInfluencers',
    component: AdminFlagInfluencers,
    meta : {requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin/flag_sponsors',
    name: 'AdminFlagSponsors',
    component: AdminFlagSponsors,
    meta : {requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin/flag_campaigns',
    name: 'AdminFlagCampaigns',
    component: AdminFlagCampaigns,
    meta : {requiresAuth:true,roles:['admin']}
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to,from,next)=>{
    if (to.meta.requiresAuth){
        if (!store.getters.isAuthenticated){
            next('/login')
        } else {
            const userRole = store.getters.userRole;
            if (to.meta.roles && !to.meta.roles.includes(userRole)){
                next('/login')
            } else {
            // if user is authenticated and role also matched
                next()
            }
        }
    } else { 
      next();
    }
})
export default router
