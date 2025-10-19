from flask import render_template,jsonify,request,Blueprint
import app.home.support.manage_aws as aws
import app.home.support.Send_requests as api
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return ('hello-world')
@home_bp.route('/files')
def get_files():
    if request.method == 'GET':
        try :
         data = request.headers.get("authorization").split(" ")[1]
        except Exception as e :
           return  jsonify({"error":"no valid token specified"}), 401
        if data :
             prefix = api.get_prefix (data) 
             if (prefix) :
              content = aws.get_bucket_objects("ftpawsbucket",prefix)
              return jsonify({"test": content}), 200
             else :
              return jsonify({"error":"not valid token"}), 401  
        else :
           return  jsonify({"error":"no token specified"}), 200
@home_bp.route('/transfer', methods=['POST','PUT'])
def transfere_file():
   if request.method == 'POST':
       try :
         data = request.headers.get("authorization").split(" ")[1]
       except Exception as e :
         print(e)
         return  jsonify({"error":e}), 401
       prefix = api.get_prefix (data)
       try : 
          data2 = request.json  
          print(data2) 
          filename = data2.get("filename")  
       except Exception as e :
         return  jsonify({"error":"error"}), 402  
       url=aws.get_presigned_link_post("ftpawsbucket",prefix,filename)
       return(jsonify({"url": url}), 200)
   if request.method == 'PUT':
       try :
         data = request.headers.get("authorization").split(" ")[1]
       except Exception as e :
         return  jsonify({"error":e}), 401
       prefix = api.get_prefix (data)
       try : 
          data2 = request.json 
          print(data2)  
          filename = data2.get("filename") 
       except Exception as e :
         print(e)
         return  jsonify({"error":"error"}), 402   
       url=aws.get_presigned_link_get("ftpawsbucket",prefix,filename)
       return(jsonify({"url": url}), 200)