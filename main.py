
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask import escape
import functions_framework
import firebase_admin
from firebase_admin import credentials

# cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app()
db = firestore.client()
voter = db.collection('voter')
election = db.collection('election')

app = Flask(__name__)



@functions_framework.http
def api_server(request):
    if 'voterRegister' in request.path:
        if request.method == 'POST':
            return query_voterProfile()
        elif request.method == 'DELETE':
            return deregister()
        elif request.method == 'PUT':
            return editVoter()
        elif request.method == 'GET':
            return voterProfile()

    elif 'create-election' in request.path:
        if request.method == 'GET':
            return electionResults()
        elif request.method == 'POST':
            return createElection()
        elif request.method == 'DELETE':
            return deleteElection()
    elif 'vote' in request.path:
        if request.method == 'POST':
            return Vote()
    return jsonify({'Error': 'Unknown Path'})




# 1. Registering a student as a voter.
# a. It will be necessary for new students to be registered to vote.

# @app.route('/voterRegister', methods=['POST'])
def query_records():
    request_info = json.loads(request.data)
    name = request_info['name']
    id = request_info['id']
    phone = request_info['phone']
    email = request_info['email']
    major = request_info['major']

    voter.document(id).set({
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
    })
    
    return jsonify({'status': '200 Ok'})

# 2. De-registering a student as a voter.
# a. A student may need to be de-registered once they leave campus.
# @app.route('/deregister', methods=['DELETE'])
def deregister():
    id = request.args.get('id')
    name = request.args.get('name')

    voter.document(id).delete()

    return jsonify({'status': '200 Ok'})  


# 3. Updating a registered voter’s information.
# a. A student’s year group, major or other information might change.
# @app.route('/edit-voter', methods=['PUT'])
def editVoter():
    request_info = json.loads(request.data)
    name = request_info['name']
    id = request_info['id']
    phone = request_info['phone']
    email = request_info['email']
    major = request_info['major']
  
    voter.document(id).set({
        'name' : name,
        'id' : id,
        'phone' : phone,
        'email' : email,
        'major' : major
        })

    return jsonify(voter.document(id).get())

# 4. Retrieving a registered voter.
# @app.route('/voter-profile', methods=['GET'])
def voterProfile():
    userId = request.args.get('id')
   
    # voter.document(id).get()
    user = voter.document(userId).get()

    return jsonify(user.to_dict())


# 5. Creating an election.
# @app.route('/create-election', methods=['POST'])
def createElection():
    request_info = json.loads(request.data)
    _id = request_info['id']
    Election = request_info['Election']
    Year = request_info['Year']
    Post = request_info['Post']
    Candidates = request_info['candidates']

    election.document(_id).set({
        'Election' : Election,
        'id' :_id,
        'Year' : Year,
        'Post' : Post,
        'candidates' : Candidates
        })
    
    return jsonify({'status': '200 Ok'})

# 6. Retrieving an election (with its details)
# @app.route('/election-results', methods=['GET'])
def electionResults():
    elect_id = request.args.get('id')
   
    # voter.document(id).get()
    election_req = election.document(elect_id).get()

    
    return jsonify(election_req.to_dict())

# 7. Deleting an election.
# @app.route('/delete-election', methods=['GET', 'DELETE'])
def deleteElection():
    id = request.args.get('id')
    name = request.args.get('Election')

    election.document(id).delete()

    return jsonify(election.document(id).get())
    



# 8. Voting in an election
# @app.route('/vote', methods=['POST'])
def Vote():
    request_info = json.loads(request.data)
    candidate_name = request_info['candidate']
    election_id = request_info['id']
    election_doc = election.document(election_id)
    election_records = election_doc.get()
    if not election_records.exists:
        return jsonify({"Error": "Election Not Found"}), 404

    election_dict = election_records.to_dict()
    
    for candidate in election_dict['candidates']:
        if candidate['candidate'] == candidate_name:
            candidate["votes"] = int(candidate['votes']) + 1
    
    # Update the candidate's vote count
    db.collection('election').document(election_id).set(election_dict)
    
    return jsonify({'success': True}), 200  


if __name__ == '__main__':
    app.run()