import datetime
from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import check_password_hash,generate_password_hash
import uuid
import jwt

app=Flask(__name__ )
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='THEPASSCODE1'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'dataBase.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
CORS(app,resources={r"/api/*": {"origins": "*"}},allowed_methods=['POST','GET'])
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    public_id=db.Column(db.String(50),unique=True)
    photo=db.Column(db.String(80))
    name=db.Column(db.String(50))
    password=db.Column(db.String(80))
    contact=db.Column(db.String(80))
    email=db.Column(db.String(80),unique=True)
    admin=db.Column(db.Boolean)
    Todo=db.relationship('Appointment',backref='user',uselist=False)
    Todo=db.relationship('pastor',backref='user',uselist=False)
    Todo=db.relationship('Testimonies',backref='user',uselist=False)
    Todo=db.relationship('Report',backref='user',uselist=False)
    
   

    def __init__(self,public_id,name,password,email,contact,admin):
        self.public_id=public_id
        self.name=name
        self.email=email
        self.contact=contact
        self.password=password
        self.admin=admin







    
class Pastor(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    Pastor_id=db.Column(db.String(50),unique=True)
    user_id=db.Column(db.String(50),db.ForeignKey('user.public_id'))
    Pastor_Name=db.Column(db.String(50))
    title=db.Column(db.String(50))
    Contact=db.Column(db.String(50))
    Image=db.Column(db.String(50))


    def __init__(self,Pastor_id,user_id,Pastor_Name,title,Contact,Image):
        self.Pastor_Name=Pastor_Name
        self.Pastor_id=Pastor_id
        self.title=title
        self.Contact=Contact
        self.user_id=user_id
        self.Image=Image

        

class Appointment(db.Model):
    Appointment_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(50),db.ForeignKey('user.public_id'))
    User_Name=db.Column(db.String(50))
    Pastor=db.Column(db.String(50))
    Reason=db.Column(db.String(50))
    Email=db.Column(db.String(50))
    Date=db.Column(db.String(50))
    ATime=db.Column(db.String(50))
    


    def __init__(self,user_id,User_Name,Pastor,Reason,Email,Date,ATime):
        self.User_Name=User_Name
        self.Pastor=Pastor
        self.Reason=Reason
        self.Email=Email
        self.user_id=user_id
        self.Date=Date
        self.ATime=ATime
        

class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(50),db.ForeignKey('user.public_id'))
    FirstName=db.Column(db.String(50))
    LastName=db.Column(db.String(50))
    Phone=db.Column(db.String(50))
    Email=db.Column(db.String(50))
    Message=db.Column(db.String(50))
    
    def __init__(self,user_id,FirstName,LastName,Phone,Email,Message,) :
        self.user_id=user_id
        self.FirstName=FirstName
        self.LastName=LastName
        self.Phone=Phone
        self.Email=Email
        self.Message=Message
  




class Report(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.String(50),db.ForeignKey('user.public_id'))

 

class Testimonies(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    testimony_id=db.Column(db.String(50))
    image=db.Column(db.String(50))
    name=db.Column(db.String(50))
    date=db.Column(db.String(50))
    message=db.Column(db.String(100))

    
    def __init__(self,testimony_id,image,name,date,message):
        self.name=name
        self.image=image
        self.date=date
        self.message=message
        self.testimony_id=testimony_id


class Event(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    event_id=db.Column(db.String(50))
    image=db.Column(db.String(50))
    name=db.Column(db.String(50))
    date=db.Column(db.String(50))
    time=db.Column(db.String(50))
    location=db.Column(db.String(50))
    eventDescription=db.Column(db.String(100))

    
    def __init__(self,event_id,image,name,date,time,location,eventDescription):
        self.name=name
        self.image=image
        self.date=date
        self.time=time
        self.location=location
        self.eventDescription=eventDescription
        self.event_id=event_id











@app.route('/',methods=['GET'])
def index():
    return "Hello world"


@app.post("/api/user")
def create_user():
    data=request.get_json() 
    name=data["name"]
    email=data["email"]
    contact=data["contact"]
    password=data['password']
    admin=data['admin']

    hashed_password=generate_password_hash(password,method='sha256')
    print(data)
    new_user=User(public_id=str(uuid.uuid4()),name=name,password=hashed_password,email=email,contact=contact,admin=admin)
    try:

      
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New user created"
        }),201
    
    except  Exception as e:
        return jsonify({'status':404,
            'msg':"email already exist",
            "body-error":e
        }),404


@app.post("/api/login")
def login():  
    data=request.get_json()
    #name=data["name"]
    email=data["email"]
    password=data['password']
    print(email,password)
    
    user= User.query.filter_by(email=email).first()
    
    
    if not user:
        return jsonify({'status':401,"msg":'Access denied'}),401
    userData={}
    userData['public_id'] = user.public_id
    userData['name']=user.name
    userData['password']=user.password
    userData['email']=user.email
    userData['admin']=user.admin
    
    if check_password_hash(user.password,password):
        token=jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        # print(token)
        return jsonify({'status':200,'auth_token':token,"user":userData})
    return jsonify({'status':401,"msg":'could wrong credentials'}),401


@app.post("/api/testimony")
def create_testimony():
    data=request.get_json() 
    name=data["name"]
    message=data["message"]
    date=data['date']
    Image=data['Image']


    print(data)
    tesimony=Testimonies(testimony_id=str(uuid.uuid4()),name=name,message=message,date=date,image=Image)
    try:

      
        db.session.add(tesimony)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New pastor created"
        }),201
    
    except  Exception as e:
        return jsonify({'status':404,
            'msg':"pastor already exist",
            "body-error":e
        }),404


@app.get("/api/testimonies")
def  all_testimonies():
    Testimonz=Testimonies.query.all()
    print(Testimonz)
    output=[]
    for Testimony in Testimonz:
        TestimonyData={}
        TestimonyData['id'] = Testimony.id
        TestimonyData['testimony_id'] = Testimony.testimony_id
        TestimonyData['name']=Testimony.name
        TestimonyData['message']=Testimony.message
        TestimonyData['date']=Testimony.date
        TestimonyData['Image']=Testimony.image
        output.append(TestimonyData)

    return jsonify(
        {
            'status':200,'Testimony':output
        }
    ),200
    
@app.post("/api/event")
def create_event():
    data=request.get_json() 
    name=data["name"]
    Image=data['image']
    date=data['date']
    time=data['time']
    location=data["location"]
    message=data["eventDescription"]
    
    


    print(data)
    event=Event(event_id=str(uuid.uuid4()),name=name,eventDescription=message,date=date,image=Image,location=location,time=time)
    try:

      
        db.session.add(event)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New Event created"
        }),201
    
    except  Exception as e:
        return jsonify({'status':404,
            'msg':"Event already exist",
            "body-error":e
        }),404


@app.get("/api/events")
def  all_events():
    event=Event.query.all()
    print(event)
    output=[]
    for event in event:
        eventData={}
       
        eventData['event_id'] = event.event_id
        eventData['name']=event.name
        eventData['Image']=event.image
        eventData['date']=event.date
        eventData['time']=event.time
        eventData['location']=event.location
        eventData['eventDescription']=event.eventDescription
        output.append(eventData)

    return jsonify(
        {
            'status':200,'event':output
        }
    ),200
    
@app.post("/api/pastor")
def create_pastor():
    data=request.get_json() 
    user_id=data["user-id"]
    Pastor_Name=data["Pastor-Name"]
    title=data["title"]
    Contact=data['Contact']
    Image=data['Image']

    print(data)
    new_pastor=Pastor(Pastor_id=str(uuid.uuid4()),Pastor_Name=Pastor_Name,user_id=user_id,title=title,Contact=Contact,Image=Image)
    try:

      
        db.session.add(new_pastor)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New pastor created"
        }),201
    
    except  Exception as e:
        return jsonify({'status':404,
            'msg':"pastor already exist",
            "body-error":e
        }),404

@app.post("/api/contact")
def Contact():
    data=request.get_json()
    user_id=data["user-id"]
    FirstName=data["FirstName"]
    LastName=data["LastName"]
    Phone=data["Phone"]
    Email=data['Email']
    Message=data['Message']
   
    new_data=Contact(user_id=user_id,FirstName=FirstName,LastName=LastName,Phone=Phone,Email=Email,Message=Message)
    
    try:

        db.session.add(new_data)
        db.session.commit()
        return jsonify({"status":201,
            "msg":"Data added"
        }),201
    
    except:
        return jsonify({'status':404,
            'msg':"Error connecting to db or server"
        }),404
    
@app.get("/api/contacts")
def  all_Contact():
    contact=Contact.query.all()
    print(contact)
    output=[]
    for contact in contact:
        contactData={}
       
        contactData['contact-id'] = contact.user_id
        contactData['Fname']=contact.FirstName
        contactData['Lname']=contact.LastName
        contactData['Phone']=contact.Phone
        contactData['Email']=contact.Email
        contactData['Message']=contact.Message
        
        output.append(eventData)

    return jsonify(
        {
            'status':200,'event':output
        }
    ),200
@app.post("/api/appointment")
def appointment():  
    data=request.get_json()
    name=data["name"]
    email=data["email"]
    reason=data['reason']
    time=data["time"]
    date=data["date"]
    pastor=data['pastor']
    user_id=data['user-id']
    print(data)
    
    
    new_appoint=Appointment(user_id=user_id,User_Name=name,Email=email,Date=date,ATime=time,Pastor=pastor,Reason=reason)
    try:

      
        db.session.add(new_appoint)
        db.session.commit()
        return jsonify({'status':201,
            "msg":"New Appointment created"
        }),201
    
    except  Exception as e:
        return jsonify({'status':404,
            'msg':"email already exist",
            "body-error":e
        }),404
    
@app.get("/api/getappointment/<public_id>")
def  getAppointment(public_id):
    
    Appoint=Appointment.query.filter_by(user_id=public_id).first()
    if not Appoint:
        return jsonify({"msg":"No Appoint Found!"})
  
    
    AppointData={}
    AppointData['public_id'] = Appoint.usr_id
    AppointData['name']=Appoint.User_Name
    AppointData['Pastor']=Appoint.Pastor
    AppointData['email']=Appoint.Email
    AppointData['Date']=Appoint.Date
    AppointData['time']=Appoint.ATime
    AppointData['msg']=Appoint.Reason
    

    return jsonify(
        {'status':200,
            'Appointment':AppointData
        }
    ),200

    

@app.get("/api/pastors")
def  all_pastors():
    pastor=Pastor.query.all()
    print(pastor)
    output=[]
    for pastor in pastor:
        pastorData={}
        pastorData['user_id'] = pastor.user_id
        pastorData['Pastor_id'] = pastor.Pastor_id
        pastorData['name']=pastor.Pastor_Name
        pastorData['title']=pastor.title
        pastorData['Contact']=pastor.Contact
        pastorData['Image']=pastor.Image
        output.append(pastorData)

    return jsonify(
        {
            'status':200,'pastor':output
        }
    ),200
    
    
@app.get("/api/users")
def  all_user():
    users=User.query.all()
    print(users)
    output=[]
    for user in users:
        userData={}
        userData['public_id'] = user.public_id
        userData['name']=user.name
        userData['password']=user.password
        userData['email']=user.email
        userData['admin']=user.admin
        output.append(userData)

    return jsonify(
        {
            'status':200,'users':output
        }
    ),200
    

@app.get('/api/user/<public_id>')
def get_one(public_id):
    user=User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"msg":"No user Found!"})
  
    
    userData={}
    userData['public_id'] = user.public_id
    userData['name']=user.name
    userData['password']=user.password
    userData['email']=user.email
    userData['admin']=user.admin
    

    return jsonify(
        {'status':200,
            'user':userData
        }
    ),200


