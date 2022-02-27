from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_cors import CORS

import datetime
import random
import sqlite3
import bcrypt
import os

app = Flask(__name__)
CORS(app)


#==============================================================#
#config database


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'some_random_jwt_secret_key'

db = SQLAlchemy(app)

app.secret_key = 'random secret key'
jwt = JWTManager(app)



"""


DATABASES:
===========================


customer: id, phone, first_name, Last_name, email, password,  |

owner: id, phone, first_name, last_name, email, password, |

company: id, owner_id, company_name, phone,ref |

zone: id, company_id, country, county, subcounty, location, estate,  price, status |

collection_days: id, zone_id, company_id, day, garbage_type , time_from, time_to, |

subscription: id, company_id, zone_id, customer_id, created_at, expire_at , price,  status, |

Top-Up; id, mpesa_code, phone, amount, status |

Withdraw: id, mpesa_code, phone, service_charge ,amount, amount_received, owner_id, status | 

Report: id, ref, subscription_id, report, |

twilio: id, account_sid, auth_token


Customer:
==========================
Subcribe to Zone
Search Zone
Top up using phone number as account number to paybill | Done
view subscription and deposit history
view zone details & company 
Report company
CRUD profile |Done


OWNER:
==========================
Withdraw Funds
view withdraws
CRUD Zones
view subscription per zones
Edit profile


COMPANY:
=========================
CRUD Company



"""





#===============================#
#       DATABASE MODELS         #
#===============================#


#Customer class db model
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,first_name,last_name,email,phone,password,created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.created_at = created_at


#Owners class db model
class Owners(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,first_name,last_name,email,phone,password,created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.created_at = created_at


#Company class db model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.String)
    company_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    ref = db.Column(db.String, unique=True)
    created_at = db.Column(db.String)



    def __init__(self,owner_id,company_name,email,phone,ref,created_at):
        self.owner_id = owner_id
        self.company_name = company_name
        self.email = email
        self.phone = phone
        self.ref = ref
        self.created_at = created_at


#Zone class db model
class Zones(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    company_id = db.Column(db.Integer)
    county = db.Column(db.Integer)
    subcounty = db.Column(db.String)
    location = db.Column(db.String)
    estate = db.Column(db.String)
    price = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,company_id, county, subcounty,location,estate,price,status, created_at):
        self.company_id = company_id 
        self.county = county
        self.subcounty = subcounty
        self.location = location
        self.estate = estate
        self.price = price
        self.status = status
        self.created_at = created_at


#Collection Days db model
class CollectionDays(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    company_id = db.Column(db.Integer)
    zone_id = db.Column(db.Integer)
    customer_id= db.Column(db.Integer)
    day = db.Column(db.String)
    garbage_type = db.Column(db.String)
    time_from = db.Column(db.String)
    time_to = db.Column(db.String)
    created_at = db.Column(db.String)
    


    def __init__(self,company_id, zone_id, customer_id, day, garbage_type, time_from, time_to, created_at):
        self.company_id = company_id 
        self.zone_id = zone_id
        self.customer_id = customer_id
        self.day = day
        self.garbage_type = garbage_type
        self.time_from = time_from
        self.time_to = time_to
        self.created_at = created_at


#Subscription db model
class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    company_id = db.Column(db.Integer)
    zone_id = db.Column(db.Integer)
    customer_id= db.Column(db.Integer)
    status = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.String)
    expire_at = db.Column(db.String)
    


    def __init__(self,company_id, zone_id, customer_id, status, price, expire_at, created_at ):
        self.company_id = company_id 
        self.zone_id = zone_id
        self.customer_id = customer_id
        self.status = status
        self.price = price
        self.expire_at = expire_at
        self.created_at = created_at


#Top up class
class Topups(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    mpesa_code = db.Column(db.String, unique=True)
    amount= db.Column(db.Integer)
    phone = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.String)



    def __init__(self,mpesa_code, amount, phone,status,created_at):
        self.mpesa_code = mpesa_code
        self.amount = amount
        self.status = status
        self.phone = phone
        self.created_at = created_at


#Withdraw class
class Withdraws(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    mpesa_code = db.Column(db.String, unique=True)
    amount= db.Column(db.Integer)
    phone = db.Column(db.String)
    service_charge = db.Column(db.Integer)
    amount_received = db.Column(db.Integer)
    status = db.Column(db.String)
    created_at = db.Column(db.String)

    def __init__(self,mpesa_code, amount,phone,service_charge,amount_received,status,created_at):
        self.mpesa_code = mpesa_code
        self.amount = amount
        self.phone = phone
        self.service_charge = service_charge
        self.amount_received = amount_received
        self.status = status
        self.created_at = created_at


#Reports class and db model
class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.Integer, unique=True)
    subscription_id = db.Column(db.Integer)
    report = db.Column(db.String)
    created_at = db.Column(db.String)    

    def __init__(self, ref, subscription_id,report, created_at):
        self.ref = ref
        self.subscription_id = subscription_id
        self.report = report
        self.created_at = created_at

#Twilio db model
class Twilio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_sid = db.Column(db.String, unique=True)
    auth_token = db.Column(db.String, unique=True)

    def __init__(self,account_sid,auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token


   

@app.route('/')
def garbage_collection():
    return 'Garbage collection REST API'

#customers register
@app.route('/customer/register', methods=['POST'])
def customer_register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    try:
        new_customer = Customers(first_name,last_name, email, phone, password_hashed, created_at)
        db.session.add(new_customer)
        db.session.commit()

        user_profile = Customers.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"id": user_profile.id})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406


#customers login
@app.route('/customer/login', methods=['POST'])
def customer_login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Customers.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == True):
            
            access_token = create_access_token(identity={"id": user_profile.id})
            return {"access_token":access_token, "Message":"Okay"}, 200

        else:

            return {"message":"Authentication failed"}, 406
    except:
        return 'Email does not exist', 409


#customers forget password
@app.route('/customer/forgot-password', methods=['PUT'])
def pass_forgot_password():
    try:
        email = request.json['email']
        user_email = Customers.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'


#customer change password
@app.route('/customer/change-password', methods=['PUT'])
@jwt_required()
def pass_edit_password():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Customers.query.filter_by(id=id).first()
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'


#customer profile
@app.route('/customer/profile', methods=['GET'])
@jwt_required()
def pass_profile():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Customers.query.filter_by(id=id).first()

        #return session["user_id"]
    
        return jsonify(        
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone, 
            email=user.email  
            )
    except:
       return {"message":"Please Login"}, 200    


#pass edit names
@app.route('/customer/edit', methods=['PUT'])
@jwt_required()
def pass_edit_names():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Customers.query.filter_by(id=id).first()
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()
        return 'record updated', 200
    except:
        return 'login to edit profile'



#top up account
@app.route('/customer/topup', methods=['POST'])
@jwt_required()
def pass_topup():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Customers.query.filter_by(id=id).first()
        phone = user.phone
        amounts = int (request.json['amount'])

        if( amounts > 0):
            amount = int(amounts)
        else:
            return 'Numbers only', 403
        status = 'Complete'
        #mpesa_code = 'Pending12'

        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

       
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        mpesa_gen = easy_password.join(e)
        mpesa_code = mpesa_gen[:7]
    
        new_topup = Topups(mpesa_code,amount,phone,status,created_at)
        db.session.add(new_topup)
        db.session.commit()
              
        return 'Top Up successful', 200

    except:
        return 'Something went wrong or mpesa code exists', 309
        





'''
=========================================
OWNER END POINTS
=========================================
'''


#owner register
@app.route('/owner/register', methods=['POST'])
def owner_register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date


    try:
        new_owner = Owners(first_name,last_name, email, phone, password_hashed, created_at)
        db.session.add(new_owner)
        db.session.commit()

        user_profile = Owners.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"ref": user_profile.ref})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406


#owner login
@app.route('/owner/login', methods=['POST'])
def owner_login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Owners.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == 'True'):
            
            access_token = create_access_token(identity={"id": user_profile.id})
            return {"access_token":access_token, "Message":"Okay"}, 200

        else:

            access_token = create_access_token(identity={"id": user_profile.id})
            return {"access_token":access_token, "Message":"Okay"}, 200
    except:
        return 'Email does not exist', 409


#owner forget password
@app.route('/owner/forgot-password', methods=['PUT'])
def owner_forgot_password():
    try:
        email = request.json['email']
        user_email = Owners.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'


#owner change password
@app.route('/owner/change-password', methods=['PUT'])
@jwt_required()
def owner_edit_password():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Owners.query.filter_by(id=id).first()
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'


#owner profile
@app.route('/owner/profile', methods=['GET'])
@jwt_required()
def owner_profile():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Owners.query.filter_by(id=id).first()

        #return session["user_id"]
    
        return jsonify(        
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone, 
            email=user.email  
            )
    except:
       return {"message":"Please Login"}, 200    


#owner edit names
@app.route('/owner/edit', methods=['PUT'])
@jwt_required()
def owner_edit_names():
    try:
        users = get_jwt_identity()
        id = users['id'] 
        user = Owners.query.filter_by(id=id).first()
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        user.first_name = first_name
        user.last_name = last_name
        db.session.commit()
        return 'record updated', 200
    except:
        return 'login to edit profile'




'''
==================================
COMPANY END POINTS
==================================
'''

#owner add company
@app.route('/owner/company', methods=['POST'])
@jwt_required()
def add_company():
    try:
        users = get_jwt_identity()
        owner_id = users['id']
        
        company_name = request.json['company_name'] 
        email = request.json['email'] 
        phone = request.json['phone'] 

        ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
        random.shuffle(ref_seed)
        ref_seed_empty = "" 
        ref_gen = ref_seed_empty.join(ref_seed)
        ref = ref_gen[:5]



        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

        new_company = Company(owner_id,company_name, email, phone, ref, created_at)
        db.session.add(new_company)
        db.session.commit()

        return 'Company Listed'
    except:
        return 'Something went wrong'



'''
ZONES END POINTS:
====================================

'''

#owner add zone to company
@app.route('/owner/company/<ref>', methods=['POST'])
@jwt_required()
def add_zone(ref):
    try:
        users = get_jwt_identity()
        owner_id = users['id']
        
        company_search = Company.query.filter_by(ref=ref).first()
        company_id = company_search.id

        county = request.json['county'] 
        subcounty = request.json['subcounty'] 
        location = request.json['location'] 
        estate = request.json['estate']
        price = request.json['price']
        status = 'Active'
        



        x = datetime.datetime.now()
        current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
        current_date = str(current_time)
        created_at = current_date

        new_zone = Zones(company_id, county, subcounty, location, estate, price, status, created_at)
        db.session.add(new_zone)
        db.session.commit()

        return 'Zone Listed'
    except:
        return 'Something went wrong'





if __name__ == "__main__":
    
    app.run(debug=True)
