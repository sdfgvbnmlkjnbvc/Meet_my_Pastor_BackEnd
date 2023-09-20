# Meet_my_Pastor_BackEnd
### api Endpoints
|Status    |    Method    |            EndPoint    |
| :-----:  | :----------: | :--------------------: |
| STARTED  |     post     | base_URL+create_user   |
| STARTED  |     GET      |  base_URL+fetch_alluser|
|  STARTED |     POST     | base_URL+login         |
|!STARTED  |     GET      | base_URL+user          |
|  STARTED |     post     | base_URL+register      |
|  STARTED |     GET      | base_URL+fetch_allpasto|
|  STARTED |     post     | base_URL+pastors       |
| !STARTED |     post     | base_URL+appo_category |
| !STARTED |     GET      | base_URL+appo_category |
| !STARTED |     post     | base_URL+appointment   |
| !STARTED |     GET      | base_URL+appointments  |
|  STARTED |     post     | base_URL+event         |
|  STARTED |     GET      | base_URL+events        |
|  STARTED |     post     | base_URL+testimonies   |
|  STARTED |     GET      | base_URL+testimony     |



#Appointment Details
 - Appointment ID
 - User ID
 - User Names
 - Pastor's Name
 - Reason for Appointment
 - Email

   
#Registration Form
 - First Name
 - Last Name
 - Phone Number
 - Email
 - Password
 - Confirm Password


#Login
 - Email
 - Password


#Contact Us
 - First Name
 - Last Name
 - Phone Number
 - Email
 - Message


#Reports
 - Number of Church Members a Pastor have received so far


#Testmonies
 - name
 - Date
 - image
 - Message For Testimony

#Event
 - Event Name
 - Date 
 - Time
 - location
 - eventDescription
 - image


#Pastor
- title
- Name 
- contact
- image

#Admin
 - Add Pastor
 - Manage Appointments
 - Add Testimony
 - Add Event


 
   
use python to run commmand to create db
from app import db,app
app.app_context().push()
db.create_all()