
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from flask import escape
import functions_framework


# cred = credentials.Certificate("key.json")
firebase_admin.initialize_app()
ref = db.reference('py/')
voter = ref.child('voter')
election = ref.child('election')


app = Flask(__name__)



@functions_framework.http
def api_server(request):
    if request.path == '\voterRegister':
        if request.method == 'GET':
            return query_records()
        elif request.method == 'DELETE':
            return deregister()
        elif request.method == 'PUT':
            return editVoter()
        elif request.method == 'GET':
            return voterProfile()
    elif request.path == '\create-election':
        if request.method == 'GET':
            return electionResults()
        elif request.method == 'POST':
            return createElection()
        # elif request.method == 'PUT':
        #     return deregister()
        elif request.method == 'DELETE':
            return deleteElection()
    elif request.path == '\vote':
        if request.method == 'GET':
            return Vote()
        

    # if request_json and 'name' in request_json:
    #     name = request_json['name']
    # elif request_args and 'name' in request_args:
    #     name = request_args['name']
    # else:
    #     name = 'World'
    # return 'Hello {}!'.format(escape(name))




# 1. Registering a student as a voter.
# a. It will be necessary for new students to be registered to vote.

# @app.route('/voterRegister', methods=['GET','POST'])
def query_records():
    name = request.args.get('name')
    id = request.args.get('id')
    phone = request.args.get('phone')
    email = request.args.get('email')
    major = request.args.get('major')

    voter.child(id).set({
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
    })
    
    return jsonify({'status': '200 Ok'})

# 2. De-registering a student as a voter.
# a. A student may need to be de-registered once they leave campus.
# @app.route('/deregister', methods=['GET', 'DELETE'])
def deregister():
    id = request.args.get('id')
    name = request.args.get('name')

    voter.child(id).delete()

    return jsonify({'status': '200 Ok'})  


# 3. Updating a registered voter’s information.
# a. A student’s year group, major or other information might change.
# @app.route('/edit-voter', methods=['GET', 'PUT'])
def editVoter():
    name = request.args.get('name')
    id = request.args.get('id')
    phone = request.args.get('phone')
    email = request.args.get('email')
    major = request.args.get('major')
  
    voter.child(id).set({
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
        })

    return jsonify(voter.child(id).get())

# 4. Retrieving a registered voter.
# @app.route('/voter-profile', methods=['GET'])
def voterProfile():
    id = request.args.get('id')
   
    voter.child(id).get()
    return jsonify(voter.child(id).get())


# 5. Creating an election.
# @app.route('/create-election', methods=['GET', 'POST'])
def createElection():
    id = request.args.get('id')
    Election = request.args.get('Election')
    Year = request.args.get('Year')
    Post = request.args.get('Post')
    Candidate = request.args.get('Candidate')

    election.child(id).set({
        'Election' : Election,
        'id' :id,
        'Year' : Year,
        'Post' : Post,
        'votes' : 0,
        'Candidate' : Candidate
        })
    
    return jsonify({'status': '200 Ok'})

# 6. Retrieving an election (with its details)
# @app.route('/election-results', methods=['GET'])
def electionResults():
    id = request.args.get('id')

    election.child(id).set({
        'id' : id
    })
    
    return jsonify(election.child(id).get())

# 7. Deleting an election.
# @app.route('/delete-election', methods=['GET', 'DELETE'])
def deleteElection():
    id = request.args.get('id')
    name = request.args.get('Election')

    election.child(id).delete()

    return jsonify(election.child(id).get())
    


# 8. Voting in an election
# @app.route('/vote', methods=['GET', 'PUT'])
def Vote():
    Candidate = request.args.get('Candidate')
    id = request.args.get('id')

    election.child(id).set({
        'id' : id
    })

    return jsonify(election.child(id).get())  

if __name__ == '__main__':
    app.debug = True
    app.run()
