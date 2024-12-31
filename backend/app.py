from config import app,db,api
from model import Admin
from werkzeug.security import generate_password_hash
from celery import Celery
from api_views import Signup, Login, Logout, PendingSponsors,DashboardStats,FetchCampaignsSponsor,FetchInfluencers
from api_views import FlagInfluencers,FlagSponsors,FlagCampaigns,InfluencerProfile,InfluencerInterested,FetchCampaignInfo
from api_views import SponsorProfile, AdminProfile,FetchAdRequests,AcceptRequest,FetchCampaigns,CreateCampaign
from api_views import CreateAdRequestSponsor,DeleteCampaign,TrackCampaign,SearchInfluencers,FetchInfluencerInfo,UpdateCampaign
from api_views import FetchAdRequestInfo,MakePayment,DownloadInvoice,DeleteAdRequest

def init_app():
    with app.app_context():
        db.create_all()
        # check if admin exists, else create admin
        admin = Admin.query.first()
        if not admin:
            password_hash = generate_password_hash('admin')
            admin = Admin(username='admin', passhash=password_hash, name='Admin')
            db.session.add(admin)
            db.session.commit()

api.add_resource(Signup,"/signup")
api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")

## admin routes
api.add_resource(PendingSponsors,"/admin/pending_sponsors")
api.add_resource(DashboardStats,"/admin/dashboard_stats")
api.add_resource(FlagInfluencers,"/admin/flag_influencers")
api.add_resource(FlagSponsors,"/admin/flag_sponsors")
api.add_resource(FlagCampaigns,"/admin/flag_campaigns")
api.add_resource(AdminProfile, "/admin_profile")

## influencer routes
api.add_resource(InfluencerProfile,"/influencer_profile")
api.add_resource(FetchAdRequests,"/fetch_ad_requests")
api.add_resource(AcceptRequest,"/accept_requests")
api.add_resource(FetchCampaigns,"/fetch_campaigns")
api.add_resource(InfluencerInterested,"/influencer_interested")

## sponsor routes
api.add_resource(SponsorProfile,"/sponsor_profile")
api.add_resource(CreateCampaign,'/sponsor/create_campaign')
api.add_resource(FetchCampaignsSponsor,'/fetch_campaigns_sponsor')
api.add_resource(FetchInfluencers,"/fetch_influencers")
api.add_resource(CreateAdRequestSponsor,"/sponsor/create_adrequest")
api.add_resource(DeleteCampaign,'/delete_campaign/<int:campaign_id>')
api.add_resource(TrackCampaign,'/track_campaign_info/<int:campaign_id>')
api.add_resource(SearchInfluencers,'/sponsor/search_influencers')
api.add_resource(FetchInfluencerInfo,"/sponsor/fetch_influencer_info/<int:influencer_id>")
api.add_resource(UpdateCampaign,'/sponsor/update_campaign')
api.add_resource(FetchCampaignInfo,'/fetch_campaign_info/<int:campaign_id>')
api.add_resource(FetchAdRequestInfo,'/sponsor/ad_requests/<int:ad_request_id>')
api.add_resource(MakePayment,'/sponsor/make_payment/<int:ad_request_id>')
api.add_resource(DownloadInvoice,'/sponsor/download_invoice/<int:ad_request_id>')
api.add_resource(DeleteAdRequest,'/delete_ad_request/<int:ad_request_id>')

if __name__ == "__main__":
    init_app()
    app.run(debug=True)