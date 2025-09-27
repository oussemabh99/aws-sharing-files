from flask import render_template,jsonify,request,Blueprint
import app.auth.support.manage_jwt as tokenMgt
import app.auth.support.manage_db as db
import app.auth.support.Send_requests as api
import base64
auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
@auth_bp.route('/token',methods=['GET', 'POST'])
def mainscript():
    if request.method == 'POST':
        auth = request.headers.get("authorization").split(" ")[1]
        if (not auth ):
           return jsonify({"Error: Username and password should not be Empty":""}), 400
        auth = base64.b64decode(auth).decode('utf-8')
        username = auth.split(":")[0]
        password = auth.split(":")[1]
        if (not username) or (not password) :
            print("Error: Username and password should not be Empty ")
            return jsonify({"Error: Username and password should not be Empty":""}), 400
        if (db.check_user(username,password)):
            prefix = db.get_prefix(username)
            if prefix == False :
               return jsonify({"Error: Unothorized":"cannot find the prefix"}), 403 
            token = tokenMgt.create_jwt(username,prefix)
            if not token :
                return jsonify({"error":""}), 402
            else :
                return jsonify({"token": token}), 200  
        else :
            return jsonify({"Error: Unothorized":""}), 403
    if request.method == 'GET':
        print(request.headers.get("Authorization"))
        data = request.headers.get("authorization").split(" ")[1]
        if data :
             payload = tokenMgt.decode_jwt(data) 
             if (payload) :
              return jsonify({"test": payload}), 200
             else :
              return jsonify({"error":"not valid token"}), 401  
        else :
           return  jsonify({"error":"no token specified"}), 200
@auth_bp.route('/orgs', methods=['POST'])
def manage_org():
    try :
         data = request.headers.get("authorization").split(" ")[1]
    except Exception as e :
         return  jsonify({"error":e}), 401  
    payload = api.get_prefix (data)
    if (payload):
        try : 
          data2 = request.json   
          filename = data2.get("org")  
        except Exception as e :
         return  jsonify({"error":"error"}), 401  
        try:
            rest=db.create_org(filename)
        except Exception as e :
         return  jsonify({"error":"error"}), 403
        if(rest) :
           return jsonify({"error":f"organisation {filename} created"}), 200
        else :
           return jsonify({"error":f"organisation {filename} not created"}), 403