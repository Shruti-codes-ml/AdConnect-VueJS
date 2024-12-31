from flask_restful import Resource, reqparse
from model import db,Influencer,Sponsor,Admin,Campaign,AdRequest
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,unset_jwt_cookies,get_jwt
from flask import jsonify, request
from sqlalchemy import func
import re
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def is_valid_password(password):
        # Example password validation, you can extend this with your own rules
        if len(password) < 8:
            return "Password must be at least 8 characters long"
        if not any(char.isdigit() for char in password):
            return "Password must contain at least one number"
        if not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter"
        if not any(char.islower() for char in password):
            return "Password must contain at least one lowercase letter"
        return None

class Signup(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_type",type=str,required=True)
        parser.add_argument("username",type=str,required=True)
        parser.add_argument("password",type=str,required=True)
        parser.add_argument("confirm_password",type=str,required=True)
        parser.add_argument("name",type=str,required=True)
        parser.add_argument("category",type=str)
        parser.add_argument("niche",type=str)
        parser.add_argument("reach",type=float)
        parser.add_argument("budget",type=float)
        parser.add_argument("industry",type=str)
        args=parser.parse_args()

        user_type = args["user_type"]
        username = args["username"]
        password = args["password"]
        confirm_password = args["confirm_password"]
        name = args["name"]

        if not all([user_type, username, password, confirm_password, name]):
            return {"message": "Error: Please fill all required fields"}, 400
        
        if len(username) < 3 or len(username) > 20:
            return {"message": "Error: Username must be between 3 and 20 characters"}, 400
        if not username.isalnum():
            return {"message": "Error: Username must contain only letters and numbers"}, 400

        if password != confirm_password:
            return {"message": "Error: Passwords do not match"}, 400

        password_error = is_valid_password(password)
        if password_error:
            return {"message": f"Error: {password_error}"}, 400

        if not name.replace(" ", "").isalpha():
            return {"message": "Error: Name should contain only alphabetic characters"}, 400


        # Handle user type (Influencer or Sponsor)
        if args['user_type'] == "influencer":
            if not args['category'] or not args['niche'] or not args['reach']:
                return {"message": "Error: Please fill all required fields for influencer"}, 400

            new_user = Influencer(
                username=args['username'],
                passhash=generate_password_hash(args['password']),
                name=args['name'],
                category=args['category'],
                niche=args['niche'],
                reach=args['reach'],
            )

        elif args['user_type'] == "sponsor":
            if not args['budget'] or not args['industry']:
                return {"message": "Error: Please fill all required fields for sponsor"}, 400

            if args['budget'] <= 0:
                return {"message": "Error: Budget must be a positive number"}, 400

            new_user = Sponsor(
                username=args['username'],
                passhash=generate_password_hash(args['password']),
                name=args['name'],
                budget=args['budget'],
                industry=args['industry'],
                approved=False # Assuming sponsors are not approved by default
            )

        else:
            return {"message": "Error: Invalid user type"}, 400

        # Check if the username already exists
        if Influencer.query.filter_by(username=args['username']).first() or Sponsor.query.filter_by(username=args['username']).first():
            return {"message": "Error: Username already taken"}, 400

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"{args['user_type'].capitalize()} successfully registered"}, 201
        
        
class Login(Resource):
    def post(self):
        # Setting up the request parser
        parser = reqparse.RequestParser()
        parser.add_argument("user_type", type=str, required=True)
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        
        args = parser.parse_args()

        user_type = args["user_type"]
        username = args["username"]
        password = args["password"]

        if not all([user_type, username, password]):
            return {"message": "Error: Please fill all required fields"}, 400

        # Mapping user types to respective models
        user_models = {
            "influencer": Influencer,
            "sponsor": Sponsor,
            "admin": Admin
        }

        # Get the model class based on user_type
        user_model = user_models.get(user_type)

        if user_type not in user_models.keys() or not user_model:
            return {"message": "Error: Invalid user type"}, 400

        # Query the user by username
        user = user_model.query.filter_by(username=username).first()

        if not user:
            return {"message": f"Error: {user_type.capitalize()} not registered.",
                    "redirect": "/signup"}, 400
        
        # Check the password
        if not check_password_hash(user.passhash, password):
            return {"message": "Error: Incorrect password"}, 400

        if (user_type!='admin' and user.flagged):
            return {"message": "Your account has been flagged and is restricted from accessing the platform.Please connect with out support team at support.adconnect@gmail.com"}, 403

        if (user_type=='sponsor' and user.admin_rejected == True):
            return {"message": "Admin has rejected your account approval. Feel free to reach out to our support team at support.adconnect@gmail.com for further queries"}, 403

        if (user_type=='sponsor' and user.approved!= True):
            return {"message": "Waiting for admin approval for your account. Feel free to reach out to our support team at support.adconnect@gmail.com for further queries"}, 403

        access_token = create_access_token(identity=user_type,additional_claims={'user_id':user.id}, expires_delta=timedelta(days=1))
        user_info = {
            "id":user.id,
            "username":user.username,
            "role":user_type
        }
        return{'access_token':access_token, "user" : user_info, "message": f"User {username} signed in successfully"},200
        
class Logout(Resource):
    @jwt_required()
    def post(self):
        role=get_jwt_identity()
        print(role)
        resp={
            "message" : "Logged out successfully"
        }
        unset_jwt_cookies(jsonify(resp))
        return resp,200
    
class PendingSponsors(Resource):
    @jwt_required()
    def get(self):
        pending_sponsors = Sponsor.query.filter_by(approved=False, admin_rejected=None).all()
        pending_sponsors_data = []
        for sponsor in pending_sponsors:
            sponsor_data={
                'id' : sponsor.id,
                'username' : sponsor.username,
                'name' : sponsor.name,
                'budget' : sponsor.budget,
                'industry' : sponsor.industry
            }
            pending_sponsors_data.append(sponsor_data)
        return jsonify(pending_sponsors_data)
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        sponsor_id = data.get('sponsor_id')
        status = data.get('status')

        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return jsonify({"message": "Sponsor not found"}), 404

        if status == 'approve':
            sponsor.approved = True
        elif status == 'reject':
            sponsor.approved = False
            sponsor.admin_rejected = True
        else:
            return jsonify({"message": "Invalid status"}), 400

        db.session.commit()
        return jsonify({"message": f"Sponsor {status}d successfully!"})
    
class DashboardStats(Resource):
    @jwt_required()
    def get(self):
        
        industry_distribution = db.session.query(
            Sponsor.industry,
            func.count(Sponsor.id).label('count')
        ).group_by(Sponsor.industry).all()

        niche_distribution = db.session.query(
            Influencer.niche,
            func.count(Influencer.id).label('count')
        ).group_by(Influencer.niche).all()

        niches = [item.niche for item in niche_distribution]
        niche_counts = [item.count for item in niche_distribution]

        # Process industry distribution into dictionaries
        industries = [item.industry for item in industry_distribution]
        counts = [item.count for item in industry_distribution]

        return jsonify({
            'influencers' : int(Influencer.query.count()),
            'sponsors' : int(Sponsor.query.count()),
            'private_campaigns' : int(Campaign.query.filter_by(visibility='private').count()),
            'public_campaigns' : int(Campaign.query.filter_by(visibility='public').count()),
            'flagged_influencers' : int(Influencer.query.filter_by(flagged=True).count()),
            'flagged_sponsors' : int(Sponsor.query.filter_by(flagged=True).count()),
            'no_of_acc_req' : int(AdRequest.query.filter_by(status='Accepted').count()),
            'no_of_rej_req' : int(AdRequest.query.filter_by(status='Rejected').count()),
            'no_of_pen_req' : int(AdRequest.query.filter_by(status='Pending').count()),
            'industries' : industries,
            'counts' : counts,
            'niches' : niches, 
            'niche_counts' : niche_counts,
        })
    
class FlagInfluencers(Resource):
    @jwt_required()
    def get(self):
        influencers = Influencer.query.all()

        all_influencers_data = []
        for influencer in influencers:
            influencer_data={
                'id': influencer.id,
                'username': influencer.username,
                'name': influencer.name,
                'category': influencer.category,
                'niche': influencer.niche,
                'reach': influencer.reach,
                'flagged': influencer.flagged
            }
            all_influencers_data.append(influencer_data)
        return jsonify(all_influencers_data)
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        influencer_id = data.get('influencer_id')
        flagged = data.get('flagged')

        influencer = Influencer.query.filter_by(id=influencer_id).first()
        influencer.flagged = flagged
        db.session.commit()

class FlagSponsors(Resource):
    @jwt_required()
    def get(self):
        sponsors = Sponsor.query.all()

        all_sponsors_data = []
        for sponsor in sponsors:
            sponsor_data={
                'id': sponsor.id,
                'username': sponsor.username,
                'name': sponsor.name,
                'budget':sponsor.budget,
                'industry':sponsor.industry,
                'approved' : sponsor.approved,
                'admin_rejected' : sponsor.admin_rejected,
                'flagged': sponsor.flagged
            }
            all_sponsors_data.append(sponsor_data)
        return jsonify(all_sponsors_data)
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        sponsor_id = data.get('sponsor_id')
        flagged = data.get('flagged')

        sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
        sponsor.flagged = flagged
        db.session.commit()

class FlagCampaigns(Resource):
    @jwt_required()
    def get(self):
        campaigns = Campaign.query.all()

        all_campaigns_data = []
        for campaign in campaigns:
            campaign_data={
                'id': campaign.id,
                'name': campaign.name,
                'description':campaign.description,
                'start_date':campaign.start_date,
                'end_date' : campaign.end_date,
                'budget' : campaign.budget,
                'visibility': campaign.visibility,
                'goals':campaign.goals,
                'payment_amount':campaign.payment_amount,
                'requirements':campaign.requirements,
                'flagged':campaign.flagged
            }
            all_campaigns_data.append(campaign_data)
        return jsonify(all_campaigns_data)
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        flagged = data.get('flagged')

        campaign = Campaign.query.filter_by(id=campaign_id).first()
        campaign.flagged = flagged
        db.session.commit()

class InfluencerProfile(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()  # Access custom claims
        user_id = claims.get("user_id")
        
        influencer = Influencer.query.filter_by(id=user_id).first()
        if not influencer:
            return jsonify({"message": f"Influencer not found"}), 404
        
        return jsonify({
                "id": influencer.id,
                "username": influencer.username,
                "name": influencer.name,
                "category": influencer.category,
                "niche": influencer.niche,
                "reach": influencer.reach
            })
    
    @jwt_required()
    def post(self):
        claims = get_jwt()
        user_id = claims.get("user_id")
        parser = reqparse.RequestParser()

        parser.add_argument("username",type=str,required=True)
        parser.add_argument("current_password",type=str)
        parser.add_argument("new_password",type=str)
        parser.add_argument("confirm_new_password",type=str)
        parser.add_argument("name",type=str,required=True)
        parser.add_argument("category",type=str)
        parser.add_argument("niche",type=str)
        parser.add_argument("reach",type=float)
        
        args=parser.parse_args()

        updated_fields = []
        user_type = get_jwt_identity()

        if not user_type=='influencer':
           return {"message": "You are not authorized to access this page"}, 400 
        
        influencer = Influencer.query.filter_by(id=user_id).first()
        if args['current_password']:
            if check_password_hash(influencer.passhash , args['current_password']):
                if args['username'] and influencer.username != args['username']:
                    if Influencer.query.filter_by(username=args['username']).first():
                        return {"message": "Username already exists."}, 400 
                    elif len(args['username']) < 3 or len(args['username']) > 20:
                        return {"message": "Username must be between 3 and 20 characters."}, 400
                    if not args['username'].isalnum():
                        return {"message": "Username must contain only letters and numbers."}, 400
                    else:
                        influencer.username = args['username']
                        updated_fields.append("Username")

                if args['new_password'] or args['confirm_new_password']: 
                    if args['current_password'] != args['new_password'] and args['new_password'] == args['confirm_new_password']:
                        password_error = is_valid_password(args['new_password'])
                        if password_error:
                            return {"message": "{{password_error}}"}, 400
                        else:
                            influencer.passhash = generate_password_hash(args['new_password'])
                            updated_fields.append("Password")
                    else:
                        return {"message": "New password must be different from the current password and confirm password should match."},400
                
                if args['name'] and influencer.name != args['name']:
                    if not re.match(r"^[A-Za-z\s]+$", args['name']):
                        return {"message": "Name should contain only alphabetic characters"},400
                    influencer.name = args['name']
                    updated_fields.append("Name")

                if args['category'] and influencer.category != args['category']:
                    if not args['category'].isalpha():
                        return {"message": "Category must have only alphabetic characters"},400
                    influencer.category = args['category']
                    updated_fields.append("Category")

                if args['niche'] and influencer.niche != args['niche']:
                    if not args['niche'].isalpha():
                        return {"message": "Niche should have all alphabetic characters"},400
                    influencer.niche = args['niche']
                    updated_fields.append("Niche")

                if args['reach'] and influencer.reach != args['reach']:
                    try:
                        float(args['reach'])
                    except ValueError:
                        return {"message": "Reach should be a number"},400
                    influencer.reach = args['reach']
                    updated_fields.append("Reach")

                if updated_fields:
                    db.session.commit()
                    return {"message": f"{', '.join(updated_fields)} updated successfully!"},200
                else:
                    return {"message": "No new changes made"},200

            else:
                return {"message": "Error : Password is incorrect"},400
        else:
            return {"message": "Verify password to make changes to profile"}, 400 

class SponsorProfile(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()  # Access custom claims
        user_id = claims.get("user_id")
        
        sponsor = Sponsor.query.filter_by(id=user_id).first()
        if not sponsor:
            return jsonify({"message": f"Influencer not found"}), 404
        
        return jsonify({
                "id": sponsor.id,
                "username": sponsor.username,
                "name": sponsor.name,
                "budget": sponsor.budget,
                "industry": sponsor.industry,
            })
    
    @jwt_required()
    def post(self):
        claims = get_jwt()  # Access custom claims
        user_id = claims.get("user_id")
        parser = reqparse.RequestParser()

        parser.add_argument("username",type=str,required=True)
        parser.add_argument("current_password",type=str)
        parser.add_argument("new_password",type=str)
        parser.add_argument("confirm_new_password",type=str)
        parser.add_argument("name",type=str,required=True)
        parser.add_argument("budget",type=str)
        parser.add_argument("industry",type=str)
        
        args=parser.parse_args()

        updated_fields = []
        user_type = get_jwt_identity()

        if not user_type=='sponsor':
           return {"message": "You are not authorized to access this page"}, 400 
        
        sponsor = Sponsor.query.filter_by(id=user_id).first()
        if args['current_password']:
            if check_password_hash(sponsor.passhash , args['current_password']):
                if args['username'] and sponsor.username != args['username']:
                    if Sponsor.query.filter_by(username = args['username']).first():
                        return {"message": "Username already exists."}, 400 
                    elif len(args['username']) < 3 or len(args['username']) > 20:
                        return {"message": "Username must be between 3 and 20 characters."}, 400
                    if not args['username'].isalnum():
                        return {"message": "Username must contain only letters and numbers."}, 400
                    else:
                        sponsor.username = args['username']
                        updated_fields.append("Username")

                if args['new_password'] or args['confirm_new_password']: 
                    if args['current_password'] != args['new_password'] and args['new_password'] == args['confirm_new_password']:
                        password_error = is_valid_password(args['new_password'])
                        if password_error:
                            return {"message": "{{password_error}}"}, 400
                        else:
                            sponsor.passhash = generate_password_hash(args['new_password'])
                            updated_fields.append("Password")
                    else:
                        return {"message": "New password must be different from the current password and confirm password should match."},400
                
                if args['name'] and sponsor.name != args['name']:
                    if not re.match(r"^[A-Za-z\s]+$", args['name']):
                        return {"message": "Name should contain only alphabetic characters"},400
                    sponsor.name = args['name']
                    updated_fields.append("Name")

                if args['industry'] and sponsor.industry != args['industry']:
                    if not args['industry'].isalpha():
                        return {"message": "Industry must have only alphabetic characters"},400
                    sponsor.industry = args['industry']
                    updated_fields.append("Industry")

                if args['budget'] and str(sponsor.budget) != args['budget']:
                    try:
                        float(args['budget'])
                    except ValueError:
                        return {"message": "Budget should be a number"},400
                    sponsor.budget = args['budget']
                    updated_fields.append("Budget")

                if updated_fields:
                    db.session.commit()
                    return {"message": f"{', '.join(updated_fields)} updated successfully!"},200
                else:
                    return {"message": "No new changes made"},200

            else:
                return {"message": "Error : Password is incorrect"},400
        else:
            return {"message": "Verify password to make changes to profile"}, 400 

class AdminProfile(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()  # Access custom claims
        user_id = claims.get("user_id")
        
        admin = Admin.query.filter_by(id=user_id).first()
        if not admin:
            return jsonify({"message": f"Admin not found"}), 404
        return jsonify({
                "id": admin.id,
                "username": admin.username,
                "name": admin.name,
            })
    
    @jwt_required()
    def post(self):
        claims = get_jwt()
        user_id = claims.get("user_id")
        parser = reqparse.RequestParser()

        parser.add_argument("username",type=str,required=True)
        parser.add_argument("current_password",type=str)
        parser.add_argument("new_password",type=str)
        parser.add_argument("confirm_new_password",type=str)
        parser.add_argument("name",type=str,required=True)
        
        args=parser.parse_args()

        updated_fields = []
        user_type = get_jwt_identity()

        if not user_type=='admin':
           return {"message": "You are not authorized to access this page"}, 400 
        
        admin = Admin.query.filter_by(id=user_id).first()
        if args['current_password']:
            if check_password_hash(admin.passhash , args['current_password']):
                if args['username'] and args['username'] != admin.username:
                    return {"message" : "Username cannot be changed"},400
                if args['name'] and args['name'] != admin.name:
                    return {'message' : "Name cannot be changed"},400
                if args['new_password'] or args['confirm_new_password']: 
                    if args['current_password'] != args['new_password'] and args['new_password'] == args['confirm_new_password']:
                        admin.passhash = generate_password_hash(args['new_password'])
                        updated_fields.append("Password")
                    else:
                        return {"message": "New password must be different from the current password and confirm password should match."},400

                if updated_fields:
                    db.session.commit()
                    return {"message": f"{', '.join(updated_fields)} updated successfully!"},200
                else:
                    return {"message": "No new changes made"},200

            else:
                return {"message": "Error : Password is incorrect"},400
        else:
            return {"message": "Verify password to make changes to profile"}, 400 
        
class FetchAdRequests(Resource):
    @jwt_required()
    def get(self):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id = claims.get('user_id')
        ad_requests = []

        if user_type=='sponsor':
            ad_requests = AdRequest.query.filter_by(sponsor_id=user_id).all()
        if user_type=='influencer':
            ad_requests = AdRequest.query.filter_by(influencer_id=user_id).all()

        all_ad_requests_data = []
        for ad_request in ad_requests:
            ad_request_data={
                'id' : ad_request.id,
                'campaign_name': ad_request.campaign.name,
                'influencer_name':ad_request.influencer.username,
                'sponsor_name': ad_request.sponsor.username,
                'messages':ad_request.messages,
                'requirements' : ad_request.requirements,
                'payment_amount' : ad_request.payment_amount,
                'status': ad_request.status,
                'sponsor_accepted':ad_request.sponsor_accepted,
                'influencer_accepted':ad_request.influencer_accepted,
                'payment_status':ad_request.payment_status,
            }
            all_ad_requests_data.append(ad_request_data)
        return jsonify(all_ad_requests_data)
    
class AcceptRequest(Resource):
    @jwt_required()
    def post(self):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id = claims.get('user_id')

        if user_type == 'influencer':
            data = request.get_json()
            ad_request_id = data.get('ad_request_id')
            influencer_accepted = data.get('influencer_accepted')
            messages = data.get('messages')

            ad_request = AdRequest.query.filter_by(id=ad_request_id).first()
            if not ad_request:
                return {"message" : "Ad Request does not exist"},400
            
            if ad_request.influencer_id != user_id:
                return {"message" : "You are not authorized to access this page"},400
            
            if influencer_accepted != None :
                ad_request.influencer_accepted = influencer_accepted
                if ad_request.sponsor_accepted == True and ad_request.influencer_accepted == True:
                    ad_request.status = 'Accepted'
                if ad_request.sponsor_accepted == False or ad_request.influencer_accepted == False:
                    ad_request.status = 'Rejected'
            if messages:
                ad_request.messages = messages

            db.session.commit()
            return {"message" : "Ad request updated successfully"},200
        
        if user_type == 'sponsor':
            data = request.get_json()
            ad_request_id = data.get('ad_request_id')
            sponsor_accepted = data.get('sponsor_accepted')
            messages = data.get('messages')

            ad_request = AdRequest.query.filter_by(id=ad_request_id).first()
            if not ad_request:
                return {"message" : "Ad Request does not exist"},400
            
            if ad_request.sponsor_id != user_id:
                return {"message" : "You are not authorized to access this page"},400
            
            if sponsor_accepted != None :
                ad_request.sponsor_accepted = sponsor_accepted
                if ad_request.sponsor_accepted == True and ad_request.influencer_accepted == True:
                    ad_request.status = 'Accepted'
                if ad_request.sponsor_accepted == False or ad_request.influencer_accepted == False:
                    ad_request.status = 'Rejected'
            if messages:
                ad_request.messages = messages

            db.session.commit()
            return {"message" : "Ad request updated successfully"},200

class FetchCampaigns(Resource):
    @jwt_required()
    def get(self):
        industry = request.args.get('industry', None)
        budget = request.args.get('budget', None)

        query = Campaign.query.filter_by(visibility='public')
        if industry:
            # query=query.join(Campaign.sponsor).filter(Sponsor.industry == industry)
            query=query.join(Campaign.sponsor).filter(Sponsor.industry.ilike(f"%{industry}%"))
        if budget:
            try:
                budget = float(budget)
                query = query.filter(Campaign.budget >= budget)
            except ValueError:
                return {"message": "Invalid budget value"}, 400 
        campaigns = query.all()
        
        all_campaigns_data = []
        for campaign in campaigns:
            campaign_data={
                'id': campaign.id,
                'name': campaign.name,
                'description':campaign.description,
                'start_date':campaign.start_date.strftime('%d %b %Y'),
                'end_date' : campaign.end_date.strftime('%d %b %Y'),
                'budget' : campaign.budget,
                'visibility': campaign.visibility,
                'goals':campaign.goals,
                'payment_amount':campaign.payment_amount,
                'requirements':campaign.requirements,

            }
            all_campaigns_data.append(campaign_data)
        return jsonify(all_campaigns_data)
    
class InfluencerInterested(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        data = request.get_json()
        campaign_id = data.get('campaign_id')

        campaign = Campaign.query.filter_by(id=campaign_id).first()
        existing_ad_request = AdRequest.query.filter_by(campaign_id=campaign_id,sponsor_id=campaign.sponsor_id,influencer_id=user_id).first()
        if existing_ad_request:
            return {"message" : "Ad request already initiated"},200
        
        ad_request = AdRequest(campaign_id = campaign_id, 
                          sponsor_id = campaign.sponsor_id, 
                          influencer_id = user_id, 
                          messages="I am interested", 
                          requirements = campaign.requirements,
                          payment_amount = campaign.payment_amount)
        db.session.add(ad_request)
        db.session.commit()
        return {"message" : "Ad Request sent successfully"},200

class CreateCampaign(Resource):
    @jwt_required()
    def post(self):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id=claims.get("user_id")

        if user_type != 'sponsor':
            return {"message" : "You are not authorized to access this page"},400
        parser = reqparse.RequestParser()
        parser.add_argument("campaign_name", type=str, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("start_date", type=str, required=True)
        parser.add_argument("end_date", type=str, required=True)
        parser.add_argument("budget", type=str, required=True)
        parser.add_argument("visibility", type=str, required=True)
        parser.add_argument("goals", type=str, required=True)
        parser.add_argument("requirements", type=str, required=True)
        parser.add_argument("payment", type=str, required=True)

        args = parser.parse_args()

        if not all([args['campaign_name'],args['description'],args['start_date'],args['end_date'],args['budget'],args['visibility'],args['goals'], args['requirements'],args['payment']]):
            return {"message" :  "Please enter all required fields"},400
        try:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return {"message" : "Invalid date format" },400
        if start_date < datetime.now().date():
            return {"message" : "Start date cannot be before today"},400
        if start_date > end_date:
            return {"message" : "Start date cannot be after end date"},400
        
        try:
            budget = float(args['budget'])
            if budget < 0:
                raise ValueError
        except ValueError:
            return {"message" : "Budget must be a positive number"},400

        if not (args['visibility']=="public" or args['visibility']=="private"):
            return {"message" : "Visibility should be either public or private"} ,400
        
        try:
            payment = float(args['payment'])
            if payment < 0:
                raise ValueError
        except ValueError:
            return {"message" : "Payment amount must be a positive number"},400
        
        campaign = Campaign(name = args['campaign_name'], 
                        description = args['description'], 
                        start_date = start_date, 
                        end_date=end_date,
                        budget=budget, 
                        visibility=args['visibility'],
                        goals = args['goals'],
                        requirements = args['requirements'],
                        payment_amount = payment,
                        sponsor_id = user_id)
    
        db.session.add(campaign)
        db.session.commit()
        return {"message":"Campaign added successfully"},200

class FetchCampaignsSponsor(Resource):
    @jwt_required()
    def get(self):
        claims=get_jwt()
        user_id=claims.get("user_id")
        campaigns=Campaign.query.filter_by(sponsor_id=user_id).all()    
        
        all_campaigns_data = []
        for campaign in campaigns:
            campaign_data={
                'id': campaign.id,
                'name': campaign.name,
                'description':campaign.description,
                'start_date':campaign.start_date.strftime('%d %b %Y'),
                'end_date' : campaign.end_date.strftime('%d %b %Y'),
                'budget' : campaign.budget,
                'visibility': campaign.visibility,
                'goals':campaign.goals,
                'payment_amount':campaign.payment_amount,
                'requirements':campaign.requirements,
                'flagged':campaign.flagged

            }
            all_campaigns_data.append(campaign_data)
        return jsonify(all_campaigns_data)
    
class FetchInfluencers(Resource):
    @jwt_required()
    def get(self):
        influencers = Influencer.query.filter_by(flagged=False).all()  
        
        all_influencers_data = []
        for influencer in influencers:
            influencer_data={
                'id': influencer.id,
                'username':influencer.username,
                'name': influencer.name,
                'category':influencer.category,
                'niche':influencer.niche,
                'reach':influencer.reach,
                'flagged':influencer.flagged

            }
            all_influencers_data.append(influencer_data)
        return jsonify(all_influencers_data)

class CreateAdRequestSponsor(Resource):
    @jwt_required()
    def post(self):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id=claims.get("user_id")

        if user_type != 'sponsor':
            return {"message" : "You are not authorized to access this page"},400
        parser = reqparse.RequestParser()

        parser.add_argument("campaign_id", type=str, required=True)
        parser.add_argument("influencer_id", type=str, required=True)
        parser.add_argument("message", type=str, required=True)
        parser.add_argument("requirements", type=str, required=True)
        parser.add_argument("payment_amount", type=str, required=True)

        args = parser.parse_args()

        if not all([user_id,args['campaign_id'],args['influencer_id'],args['message'],args['requirements'],args['payment_amount']]):
            return {"message" : "Please fill all required fields" },400
        
        campaign = Campaign.query.filter_by(id = args['campaign_id'], sponsor_id=user_id).first()
        
        if not campaign:
            return {"message" : "Invalid campaign. Please select a valid campaign."},400
        if campaign.flagged:
            return {"message" : "This campaign has been flagged. You cannot create ad requests for this campaign. Kindly contact support at support@adconnect.in for more details."},400
        influencer = Influencer.query.filter_by(id=args['influencer_id']).first()
        if not influencer:
            return {"message" : "Invalid influencer. Please select a valid influencer."},400
        if influencer.flagged:
            return {"message" : "This influencer has been flagged. You cannot create ad requests for this influencer. Kindly contact support at support@adconnect.in for more details."},400
        
        try:
            payment_amount = float(args['payment_amount'])
            if payment_amount <= 0:
                return {"message" : "Payment amount be greater than 0"},400
        except ValueError:
            return {"message" : "Invalid payment amount"},400
        
        ad_request = AdRequest(
            campaign_id = args['campaign_id'],
            influencer_id = args['influencer_id'],
            sponsor_id = user_id,
            messages = args['message'],
            requirements = args['requirements'],
            payment_amount = payment_amount
        )
        db.session.add(ad_request)
        db.session.commit()
        return {"message" : "Ad Request sent successfully"},200

class DeleteCampaign(Resource):
    @jwt_required()
    def delete(self,campaign_id):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id = claims.get("user_id")

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=user_id).first()

        if not campaign:
            return {"message": "Campaign not found or you do not have access to this campaign"}, 404
        
        try:
            # Delete the campaign
            db.session.delete(campaign)
            db.session.commit()
            return {"message": "Campaign deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while trying to delete the campaign"}, 500
        
class TrackCampaign(Resource):
    @jwt_required()
    def get(self,campaign_id):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id = claims.get("user_id")

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=user_id).first()
        ad_requests = AdRequest.query.filter_by(campaign_id = campaign_id).all()
        spendings = sum(ad_request.payment_amount for ad_request in ad_requests if ad_request.payment_status == 1)
        unique_platforms = set(ad_request.influencer.niche for ad_request in ad_requests if ad_request.influencer)
        accepted_ad_requests = [ad_request for ad_request in ad_requests if ad_request.status == 'Accepted']
        rejected_ad_requests = [ad_request for ad_request in ad_requests if ad_request.status == 'Rejected']

        if not campaign:
            return {"message": "Campaign not found or you do not have access to this campaign"}, 404
        
        return {
            "campaign_name": campaign.name,
            "campaign_goals": campaign.goals,
            "end_date": str(campaign.end_date),
            "budget": campaign.budget,
            "amount_spent": spendings,
            "no_of_adrequests": len(ad_requests),
            "accepted_ad_requests" : len(accepted_ad_requests),
            "rejected_ad_requests" : len(rejected_ad_requests),
            "unique_platforms" : len(unique_platforms),
        }, 200

class SearchInfluencers(Resource):
    @jwt_required()
    def get(self):
        category = request.args.get('category', None)
        niche = request.args.get('niche', None)
        reach=request.args.get('reach',None)

        query = Influencer.query.filter_by(flagged=False)
        if category:
            query=query.filter(Influencer.category.ilike(f"%{category}%"))
        if niche:
            query=query.filter(Influencer.niche.ilike(f"%{niche}%"))

        if reach:
            try:
                reach = float(reach)
                query = query.filter(Influencer.reach >= reach)
            except ValueError:
                return {"message": "Invalid reach value"}, 400 
        influencers = query.all()
        
        all_influencers_data = []
        for influencer in influencers:
            influencer_data={
                'id': influencer.id,
                'username':influencer.username,
                'name': influencer.name,
                'category':influencer.category,
                'niche':influencer.niche,
                'reach' : influencer.reach
            }
            all_influencers_data.append(influencer_data)
        return jsonify(all_influencers_data)

class FetchInfluencerInfo(Resource):
    @jwt_required()
    def get(self,influencer_id):
        user_type = get_jwt_identity()

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        influencer = Influencer.query.filter_by(id=influencer_id).first()
        if not influencer:
            return {"message" : "Influencer does not exist"}
        return {
            "username": influencer.username,
            "name": influencer.name,
            "category": influencer.category,
            "niche": influencer.niche,
            "reach": influencer.reach,
        }, 200

class FetchCampaignInfo(Resource):
    @jwt_required()
    def get(self,campaign_id):
        user_type = get_jwt_identity()
        claims=get_jwt()
        user_id=claims['user_id']

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=user_id).first()

        if not campaign:
            return {"message" : "Campaign does not exist"},400
        
        return {
            "name": campaign.name,
            "description": campaign.description,
            "start_date" : str(campaign.start_date),
            "end_date": str(campaign.end_date),
            "budget": campaign.budget,
            "visibility": campaign.visibility,
            "goals" : campaign.goals,
            "requirements" : campaign.requirements,
            "payment_amount" : campaign.payment_amount
        }, 200
    
class UpdateCampaign(Resource):
    @jwt_required()
    def post(self):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id=claims.get("user_id")

        if user_type != 'sponsor':
            return {"message" : "You are not authorized to access this page"},400
        parser = reqparse.RequestParser()
        parser.add_argument("campaign_id", type=float, required=True)
        parser.add_argument("campaign_name", type=str, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("end_date", type=str, required=True)
        parser.add_argument("budget", type=str, required=True)
        parser.add_argument("visibility", type=str, required=True)
        parser.add_argument("goals", type=str, required=True)
        parser.add_argument("requirements", type=str, required=True)
        parser.add_argument("payment_amount", type=str, required=True)

        args = parser.parse_args()

        if not all([args['campaign_name'],args['description'],args['end_date'],args['budget'],args['visibility'],args['goals'], args['requirements'],args['payment_amount']]):
            return {"message" :  "Please enter all required fields"},400
        
        campaign=Campaign.query.filter_by(id=args['campaign_id'], sponsor_id=user_id).first()
        if not campaign:
            return {"message":"Campaign does not exist"},400
        
        if campaign.flagged:
            return {"message" : "This campaign has been flagged and cannot be updated. Please contact our support team at support@adconnect.in"}

        try:
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return {"message" : "Invalid date format" },400

        if campaign.start_date > end_date:
            return {"message" : "Start date cannot be after end date"},400
        
        try:
            budget = float(args['budget'])
            if budget < 0:
                raise ValueError
        except ValueError:
            return {"message" : "Budget must be a positive number"},400

        if not (args['visibility']=="public" or args['visibility']=="private"):
            return {"message" : "Visibility should be either public or private"} ,400
        
        try:
            payment = float(args['payment_amount'])
            if payment < 0:
                raise ValueError
        except ValueError:
            return {"message" : "Payment amount must be a positive number"},400
        
        campaign.name = args['campaign_name']
        campaign.description = args['description']
        campaign.end_date = end_date
        campaign.budget = args['budget']
        campaign.visibility = args['visibility']
        campaign.goals = args['goals']
        campaign.requirements = args['requirements']
        campaign.payment_amount = args['payment_amount']
    
        db.session.commit()
        return {"message":"Campaign updated successfully"},200

class FetchAdRequestInfo(Resource):
    @jwt_required()
    def get(self,ad_request_id):
        user_type = get_jwt_identity()
        claims=get_jwt()
        user_id=claims['user_id']

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        adrequest = AdRequest.query.filter_by(id=ad_request_id, sponsor_id=user_id).first()

        if not adrequest:
            return {"message" : "Campaign does not exist"},400
        
        return {
            'influencer_name': adrequest.influencer.username,
            'sponsor_name': adrequest.sponsor.username,
            'campaign_name': adrequest.campaign.name,
            'payment_amount': adrequest.payment_amount,
            'payment_status': adrequest.payment_status,
        }, 200
    
class MakePayment(Resource):
    @jwt_required()
    def post(self,ad_request_id):
        user_type = get_jwt_identity()
        claims=get_jwt()
        user_id=claims['user_id']

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        adrequest = AdRequest.query.filter_by(id=ad_request_id, sponsor_id=user_id).first()

        if not adrequest:
            return {"message" : "Campaign does not exist"},400

        if adrequest.payment_status == True:
            return {"message" : "Payment is already processed"},200
    
        parser = reqparse.RequestParser()
        parser.add_argument("payment_amount", type=float, required=True)
        args = parser.parse_args()

        try : 
            payment_amount = float(args['payment_amount'])
            if payment_amount <= 0:
                raise ValueError
        except ValueError:
            return {"message" : "Invalid payment amount"},400
        
        adrequest.payment_amount = payment_amount
        adrequest.payment_status = True
        db.session.commit()
        return {"message" : "Payment successful!"},200
    
class DownloadInvoice(Resource):
    @jwt_required()
    def get(self,ad_request_id):
        user_type = get_jwt_identity()  
        claims = get_jwt() 
        user_id = claims['user_id']

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        ad_request = AdRequest.query.filter_by(id=ad_request_id, sponsor_id=user_id).first()

        if not ad_request:
            return {"message": "Ad Request not found or you are not authorized to view this request"}, 404

        # Create a buffer to hold the generated PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Styles for the PDF
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontName = 'Times-Roman'
        title_style.fontSize = 20
        title_style.leading = 30
        title_style.alignment = 1

        subtitle_style = styles['Heading2']
        subtitle_style.fontName = 'Times-Roman'
        subtitle_style.fontSize = 14
        subtitle_style.leading = 20
        subtitle_style.alignment = 1

        footer_style = styles['Normal']
        footer_style.fontName = 'Times-Roman'
        footer_style.fontSize = 12
        footer_style.leading = 18
        footer_style.alignment = 1

        header_style = styles['Heading1']
        header_style.fontName = 'Times-Roman'
        header_style.fontSize = 14
        header_style.leading = 18
        header_style.alignment = 1

        # Title and Subtitle
        title = Paragraph("AdConnect", title_style)
        subtitle = Paragraph(f"Invoice for Ad Request #{ad_request.id}", subtitle_style)

        elements.append(title)
        elements.append(Spacer(1, 12))
        elements.append(subtitle)
        elements.append(Spacer(1, 24))

        # Data for the table
        data = [
            ["Description", "Details"],
            ["Campaign Name", ad_request.campaign.name],
            ["Sponsor Name", ad_request.sponsor.username],
            ["Influencer Name", ad_request.influencer.username],
            ["Payment Amount", f"{ad_request.payment_amount:.2f}"],
            ["Status", "Paid" if ad_request.payment_status else "Unpaid"]
        ]

        # Create the table for invoice details
        table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.turquoise),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 24))  # Space between table and footer

        # Footer message
        footer = Paragraph("Thank you for your payment!", footer_style)
        elements.append(footer)

        # Build the PDF
        doc.build(elements)

        # Seek to the beginning of the buffer to send the file
        buffer.seek(0)

        # Send the PDF as an attachment
        return send_file(buffer, as_attachment=True, download_name=f"invoice_{ad_request.id}.pdf", mimetype='application/pdf')
    
class DeleteAdRequest(Resource):
    @jwt_required()
    def delete(self,ad_request_id):
        user_type = get_jwt_identity()
        claims = get_jwt()
        user_id = claims.get("user_id")

        if user_type != 'sponsor':
            return {"message": "You are not authorized to perform this action"}, 400

        adrequest = AdRequest.query.filter_by(id=ad_request_id, sponsor_id=user_id).first()

        if not adrequest:
            return {"message": "Campaign not found or you do not have access to this campaign"}, 404
        
        try:
            # Delete the campaign
            db.session.delete(adrequest)
            db.session.commit()
            return {"message": "Ad request deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while trying to delete the campaign"}, 500