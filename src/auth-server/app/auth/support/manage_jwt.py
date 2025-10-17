import jwt
import datetime
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import uuid
import os
crt_data = os.environ.get("PathCrt") 
key_data = os.environ.get("PathKey")
with open(f"{crt_data}", "rb") as certif_file:
   cert_data = certif_file.read()
   certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
public_key1 = certificate.public_key()
with open(f"{key_data}", "rb") as key_file:

    private_key1 = serialization.load_pem_private_key(

       key_file.read(),

        password=None,

  )
private_key = rsa.generate_private_key(
       public_exponent=65537,
       key_size=2048,
       backend=default_backend()
)
public_key = private_key.public_key()
private_pem = private_key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.PKCS8,
       encryption_algorithm=serialization.NoEncryption()
   )
public_pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
   )
def create_jwt(username,prefix):
    if not username or not prefix:
        print("Error: username and connexion id must not be empty or None.")
        return None
    payload={
       'connexion_id':str(uuid.uuid4()),'username': username,'iat': datetime.datetime.now() - datetime.timedelta(hours=1),'exp': datetime.datetime.now() + datetime.timedelta(minutes=30),'prefix': prefix}
    try :
        encoded_token=jwt.encode(payload, private_key1, algorithm='RS256')
        return(encoded_token)
    except Exception as e:
        print (e)
        return None
def decode_jwt(encoded_jwt):
    if not encoded_jwt :
        print("Error: JWT Token must not be Empty !!")
        return None
    try:
        decoded_jwt = jwt.decode(encoded_jwt,public_key1,algorithms=['RS256'])
        return(decoded_jwt)
    except Exception as e :
        print (e)
        return False
