import boto3
from datetime import datetime
from dateutil.tz import tzutc
import os
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
region_name = "eu-west-3"
bucket_name = "ftpawsbucket"
s3_client = boto3.client = boto3.client(
    's3',
    aws_access_key_id= aws_access_key_id,
    aws_secret_access_key= aws_secret_access_key,
    region_name=region_name
)
#response = s3_client.list_objects_v2(Bucket=bucket_name,Prefix="admin")
#response = s3_client.head_object(Bucket="ftpawsbucket", Key="admin/")
#print (response)
def change_date(dt):
    try :
     formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
     return ('Corrupted data')
    return (formatted) 
def get_bucket_objects(Bucket,Prefix):
    l = list()
    dic=dict()
    try:
        obj=s3_client.list_objects_v2(Bucket=Bucket,Prefix=Prefix)
        #print(obj)                             
    except Exception as e:
        print(f"error trying to get object from prefix: {e}") 
        return None
    for file in obj["Contents"] :
        dic[file["Key"]] ={"LastModified":change_date(file["LastModified"]),"Size":file["Size"]}
    print(dic)
    return(dic)
def get_presigned_link_get(Bucket,key,file):
    path = f"{key}/{file}"
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',  
            Params={'Bucket': Bucket, 'Key':path, 'ResponseContentDisposition': f"'attachment; filename={file}'"},
            ExpiresIn=15 
        )
        print(f"Presigned URL: {presigned_url}")
        return(presigned_url)
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
def get_presigned_link_post(Bucket,key,file):
    path = f"{key}/{file}"
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',  
            Params={'Bucket': Bucket, 'Key':path},
            ExpiresIn=3600 
        )
        print(f"Presigned URL: {presigned_url}")
        return(presigned_url)
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
#get_presigned_link_post("ftpawsbucket","admin",r"test2.txt")
#get_bucket_objects(Bucket="ftpawsbucket", Prefix="")
#get_presigned_link_get("ftpawsbucket","admin","test.txt")