from devOps import db
from devOps.models import Application,FrameworkOfApp,User
from devOps.crudApps import getAppsByUser
from flask import Flask ,flash

def getAllUsers():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email_address'] = user.email_address
        user_data['password_hash'] = user.password_hash
        user_data['admin'] = user.admin
        output.append(user_data)
    return output

def getOneUserByPublicID(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        
        return f"User with public id ={public_id} not found"

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email_address'] = user.email_address
    user_data['password_hash'] = user.password_hash
    user_data['admin'] = user.admin
    if user.github_access_token:
        user_data['github_access_token'] = user.github_access_token
    if user.github_username:
        user_data['github_username'] = user.github_username

    list_user_apps=getAppsByUser(user)
    if list_user_apps:
        user_data['projects']=list_user_apps
               
    return user_data



def createUser(username,email,password,admin):

    user = User(username,email,password,admin)
    db.session.add(user)
    db.session.commit()

def updateUser(new_user,username,email,password,admin):
    new_user.username=username
    new_user.email_address=email
    new_user.password_hash=password
    new_user.admin=admin
    db.session.commit()

def deleteUser(user):
    db.session.delete(user)
    db.session.commit()

    