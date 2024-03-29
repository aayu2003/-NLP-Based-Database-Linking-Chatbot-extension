from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials,db
app = Flask(__name__)
cred=credentials.Certificate({
  "type": "service_account",
  "project_id": "user-ca5fe",
  "private_key_id": "e39f548996fcec1feadebb4b6d0aa1fef0fe4789",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQD14XD9UquQ0Nzs\nKQG+7Tix7Q0U9m+lUAL0KrbL9S0qMTO4zGBto5bvtXOrbs6Hj5JnvM6AyfYrtPw8\n0Fgo1mauL1lne41+7ky6G8iC2ZUo9u1UCGI0mshmcohUAFnBv/30IK7hjEj5dTyH\n/QsjpUHjT5qNaeLBVyezMTZUwZKhy49+DhNv2oIPzXYPznul9RliDyhQk9Ur6lLy\nqNJ+dUVmA8Loxb9rYCdYIOa6BZL8y99/sW3nZJ+BwiKsM8HUdn0nrfFnL6YeOOOs\nk+cWzzWh+HYQ9hOalVfccIv9ZLZ8ZR2iPfVPHDrJIOygLuJ37uhQLDk7hTakOb4z\n6nPhPSXdAgMBAAECggEAHWojtRJ47Cv9ued/9MzL7bErpviCS7cCMMk+sVtP1Lkq\ndFmdfDrypBOY1lySVYejSUi+NYxeUu/lsGAbo9Wzq/PbJgo9rP5/bFDwOwMiQ9J3\n0DKT47IpS47jveowKAG6tO6yAnvgq63O7ip4n4I2GyZF7tPzfhNZ8FHGAPwKpCiK\nJDJmwv2TPbkD5CNZdbsSrG06lYvCkol08MtzaPTsUZOqbLmXo9xk2xjxIU3AkOnk\nEFn2cM31Kyjzt4WrHWxq73I9MkG2EtF93lEu0g+WWjRXPITpZvb4i0UsXMaslhhR\nINxitSiTHtqySVbq1dWrw1Lo0SgItEvRxIc708s0uwKBgQD/6K8cZ+XmaV6zuJ53\ncQVd43gXH1gPy3TV5AysT3cCIfWf4Wdcmvx7oaXYnR6kmz0U0cJ5nQfuQuzu8e2j\nXU5Y5+lcILJBkxgKN/6/LTHF3y39gGsngdLCQRnsHyq3yOEiEWLuC4npLqNua9B7\n4h5DIWS17pSTlZQiMxLdonQIpwKBgQD199f52oUFmOrGSViSqpvsHovd9nFKMQUA\neB0BShbYsEKeuZcXWx4EJCJJpX8HuCc8R60csy9YNDuySJqXdhQFfriunoHdwOeW\nYJpoj81eHRh5VMG8vQ373x9/XUJm5wiETBmhsR81xmysI8vlDOzajDmL84a+kodv\nv3uhtJEp2wKBgHz2IFwcl/S1S1szMZ5dgCNiqgeQdK3xybGQVGfnvdM6xfg2VwSv\nYc71Fkj6IDZ834zFCNPdzDuaTpw3YrU9IL7lL9ye0qyWqUyEH083QHDBFHIPPUPj\nbwkQRRo59eAcpWK/XrGizMsizQdkej+kIObi7YyxXbfbeKRikDnN1B9NAoGABEN3\niu0uwRoVd7ptvp0WdtFQu1g6Pn77BzcNyafvHXJwtS+iXtVFf+zga0ZjHU8j3vef\nGJBCkdTV9BEuHNH/Jtk7ektlFOLzILgr9QQJG0iF1BSUByF/zI3hjeOf8wiuLRzk\nlNjtIZF+8LzuG9pNgLxNgw+FlmgT0OwQyIzIt2ECgYAX7yTufODXQu8Fnc7gHWZ0\nekCZME3x7fTJFv1jFAsLgcYAqqVgTDoHB8SYc7awblCHmQdbAz6HfZs1GPhfZD2Y\n3CdY8yZPLmHz6mD6YV+1juDm9/Qv9ACx4ZvGXVd2DfWIopedafuFZYSlWEALko/6\nULqDHIdfLIfD8YuQcNiz9g==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-32tmz@user-ca5fe.iam.gserviceaccount.com",
  "client_id": "102584866704779936514",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-32tmz%40user-ca5fe.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred, {'databaseURL': 'https://user-ca5fe-default-rtdb.firebaseio.com/'})
# Define a route that returns a JSON response
@app.route('/pie/<cred>', methods=['GET'])
def login(cred):

    labels=[]
    size=[]
    a=cred.split("-")
    for i in a:
        url="/"+i
        labels.append(i)
        data_ref=db.reference(url)
        size.append(data_ref.get())
    return jsonify({'mylist':size})
@app.route('/info',methods=['GET'])
def info():
    l=[]
    data_ref=db.reference('/')
    d={'value':None}
    for i in data_ref.get():
        l.append(i)
        d['value']=l
    return d

if __name__ == '__main__':
    app.run(debug=True)
