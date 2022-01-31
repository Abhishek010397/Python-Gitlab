import json
import boto3
from datetime import datetime,date

iam_client = boto3.client('iam')
secret_client = boto3.client('secretsmanager')

def list_access_key(user):
    keydetails={}
    keydetails=iam_client.list_access_keys(UserName=user)
    for key in keydetails['AccessKeyMetadata']:
        AccessKey=key['AccessKeyId']
        CreateDate=key['CreateDate']
        print(AccessKey)
        check_date(AccessKey,user,CreateDate)
        
        
def check_date(access_key,username,date):
    createday = date
    today=datetime.now()
    diff=today-createday.replace(tzinfo=None)
    if diff.days == 88:
        #send sns notification for Updates
        if diff.days == 90:
            disable_key(username,access_key)
            delete_key(username,access_key)
            create_new_key(username)
        
def disable_key(access_key,username):
    response = iam_client.update_access_key(UserName=username,AccessKeyId=access_key,Status='Inactive')
    print(access_key + "has been disabled")

  
def delete_key(access_key,username):
    response = client.delete_access_key(UserName=username,AccessKeyId=access_key)
    print(access_key + "has been deleted")
    
def create_new_key(username):
    response = client.create_access_key(UserName=username)
    access_key = response['AccessKey']['AccessKeyId']
    secret_key = response['AccessKey']['SecretAccessKey']
    json_data = json.dumps({'AccessKey': access_key, 'SecretKey': secret_key})
    secret_manager_response = client.put_secret_value(SecretId=username,SecretString=json_data)
    #send sns notification for Status has Been 
    
    
        
def lambda_handler(event, context):
    users=iam_client.list_users(MaxItems=300)
    for user in users['Users']:
        username=user['UserName']
        list_access_key(username)
