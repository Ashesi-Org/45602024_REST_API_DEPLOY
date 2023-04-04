import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://eunny99-8e388-default-rtdb.firebaseio.com/"})
ref = db.reference('py/')
voter_ref = ref.child('voter')
election_ref = ref.child('election')
voterId = "1"

# Set new voter, POST
voter_ref.child(voterId).set({'1':{
    "name": "Atingane Awaka",
     "email": "atin@m.com", 
     "yeargroup": "2024", 
     "contact": "+223206252066", 
     "major": "Computer Science"},

     '2':{
    "name": "Amiah Adagwine",
     "email": "amiaha@m.com", 
     "yeargroup": "2025", 
     "contact": "+223206258710", 
     "major": "Business"
     }
     })


# Update Data, PUT
voter_ref.child(voterId).update({
    "name":"Joshua Amiah",
    "email": "josami@m.com" })


# Read data, GET
print(voter_ref.child(voterId).get())

# Delete data, DELETE
# voter_ref.child(voterId).delete()