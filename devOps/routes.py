from devOps.analyseApp import *
from devOps.crudUsers import getAllUsers,getOneUserByPublicID,createUser,updateUser,deleteUser
from devOps.crudApps import *
from devOps.communicationWithJenkins import *
from devOps import app
from flask import Flask, json , render_template, session, redirect, url_for, request,flash,jsonify,make_response
import uuid #to generate public id 
import datetime
#from requests_oauthlib import OAuth2Session
import os
#from flask.json import jsonify
from functools import wraps
from devOps.forms import *
from devOps import db
from devOps import UsingJWT
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import get_jwt_identity
from devOps.models import User
from werkzeug.security import generate_password_hash, check_password_hash
#from analyseApp import get_repo_name_from_url, listdirectory, detectionLang, languageOfApp

import detect
from flask_jwt_extended import (jwt_required,get_jwt, get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)
import requests
import requests.auth

from flask_github import GitHub
from devOps import github

@app.route('/')
@jwt_required(optional=True)
def home_page():
    
    return render_template('home.html')

@app.route('/getAccessToken')
@jwt_required()
def access_token():
    username=get_jwt_identity()
    current_user = User.query.filter_by(username=username).first()
    code=request.args['code']
    client_id=app.config['GITHUB_CLIENT_ID']
    client_secret=app.config['GITHUB_CLIENT_SECRET']
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://127.0.0.1:5000/getAccessToken'}
    access_token_response = requests.post('https://github.com/login/oauth/access_token', data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    print ("response")
    print (access_token_response.headers)
    print(access_token_response.text)
   
    # we can now use the access_token as much as we want to access protected resources.
    tokens = access_token_response.text.split('&')
    for i in tokens:
        if (i.find('access_token') != -1):
            print('acces token found')
            access_token=i.split('=')[1]
            
            break

    if access_token:
        current_user.github_access_token = access_token
    
        db.session.commit()

        headers = {'Authorization': 'token ' +access_token}

        login = requests.get('https://api.github.com/user', headers=headers)
        print(login)
        dic=login.json()
        print(dic)
        current_user.github_username=dic['login']
        print(current_user.github_username)
    
    return redirect(url_for('analyseApp'))


@app.route('/GetRepo', methods=['GET','POST'])
@jwt_required()
def analyseApp():
    
    form=AddNewProject()
    
    username=get_jwt_identity()
    current_user = User.query.filter_by(username=username).first()
    access_token=current_user.github_access_token
    usernameGithub=current_user.github_username
    print(access_token)
    print(usernameGithub)
    print(current_user.username)
    if form.validate_on_submit():
           nameOfProject=form.nameOfProject.data
           gitRepo = form.gitRepo.data
           path = form.path.data
           nameEntryFile=form.entry_file.data
           #if is_git_repo(gitRepo):
           result=is_git_repo(gitRepo)
           if result:
               
               if checkIfDirectoryExist(path):
                   
                   repo_dir=cloningRepoOrUpdate(path,gitRepo,usernameGithub,access_token)
                   listOfFiles=listdirectory(repo_dir)
                   print(listOfFiles)
                   entryFile=fileContent(listOfFiles,nameEntryFile)
                   jenkinsFile=fileContent(listOfFiles,'Jenkinsfile')
                   print(jenkinsFile)
                   if entryFile:
                       
                       dic=languageOfApp(listOfFiles)
                       listResultOfDetectionOfFramework=detectFrameworkOfApp(dic,entryFile,nameEntryFile,listOfFiles)
                       createApp(nameOfProject,gitRepo,nameEntryFile,jenkinsFile,listResultOfDetectionOfFramework[0],current_user.username)
                       return render_template('languageOfApp.html',dic=dic,listResultOfDetectionOfFramework=listResultOfDetectionOfFramework)
                   else:
                       flash("No entry file found', category='danger")

               else:
                   flash("No such directory found', category='danger")
                
           else:
                flash("No such git repository found', category='danger") 

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a new project: {err_msg}')        

    return render_template('GetRepo.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        
        if user and user.verify_password(password):
            login_user(user)
            
            flash(f'Success! You are logged in as: {user.username}', category='success')
            return assign_access_refresh_tokens(username , app.config['BASE_URL'])
        else:
            flash('Username and password are not match! Please try again', category='danger')
            
    else:
        print(form.errors)

    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    username = form.username.data
    password = form.password1.data
    email = form.email_address.data
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if not user:
            createUser(username,email,password,False)

        return redirect(url_for('login_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return unset_jwt(), 302




#crud for Users
@app.route('/user', methods=['GET', 'POST'])
@jwt_required(fresh=True)
def get_all_users():

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    
    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page')) 


    output = getAllUsers()

    if request.method == 'POST':
        public_id = request.form.get("public_id")
        if request.form['action'] == 'more' :
            return redirect(f'/user/{public_id}')
        elif request.form['action'] == 'update' :
            return redirect(f'/user/{public_id}/update')
        elif request.form['action'] == 'delete':
            return redirect(f'/user/{public_id}/delete')
        elif request.form['action'] == 'create':
            return redirect('/user/create')
        else:
            
            return redirect(url_for('get_all_users'))
        
    return render_template("allUsers.html", data=output)


@app.route('/user/<public_id>', methods=['GET'])
@jwt_required(fresh=True)
def get_one_user(public_id):

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    
    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page'))

    user_data=getOneUserByPublicID(public_id)
    
    return render_template('oneUser.html', user_data = user_data)


@app.route('/user/create', methods = ['GET','POST'])
@jwt_required(fresh=True)
def create_user():
    #csrf_token = {}.get("csrf")
    usernameUser=get_jwt_identity()
    current_user = User.query.filter_by(username=usernameUser).first()
    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page'))

    form = CreateUser(request.form)
    
    username = form.username.data
    password = form.password.data
    email = form.email_address.data
    admin=form.admin.data 
    
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=username).first()
        if not user:
            createUser(username,email,password,admin)
    
        return redirect(url_for('get_all_users'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('createUser.html', form=form)
    
    

@app.route('/user/<public_id>/update', methods = ['GET','POST'])
@jwt_required(fresh=True)

def update_user(public_id):

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()

    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page'))

    new_user = User.query.filter_by(public_id=public_id).first()

    if not new_user:
        return f"User with public id ={public_id} not found"

    form = UpdateUser()
    username = form.username.data
    password = form.password.data
    email = form.email_address.data
    admin=form.admin.data 
    if form.validate_on_submit():
        #db.session.delete(user)
        #db.session.commit()
        user = User.query.filter_by(username=username).first()
        if not user:
            updateUser(new_user,username,email,password,admin)
            return redirect(url_for('get_all_users'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with updating the user: {err_msg}')
    
    return render_template('updateUser.html', form=form)

 


@app.route('/user/<public_id>/delete', methods=['GET','POST'])
@jwt_required(fresh=True)
def delete_user(public_id):

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()

    form = DeleteUser()
    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page'))

    user = User.query.filter_by(public_id=public_id).first()
    if form.validate_on_submit():
        if user:
            deleteUser(user)
            return redirect(url_for('get_all_users'))    
    
    return render_template('deleteUser.html', form=form)
    

@app.route('/token/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    # Refreshing expired Access token
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    resp = make_response(redirect(app.config['BASE_URL'] + '/login', 302))
    set_access_cookies(resp, access_token)
    return resp

def assign_access_refresh_tokens(user_id, url):
    access_token = create_access_token(identity=str(user_id), fresh = True)
    refresh_token = create_refresh_token(identity=str(user_id))
    resp = make_response(redirect(url, 302))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp

def unset_jwt():
    resp = make_response(redirect(app.config['BASE_URL'] + '/login', 302))
    unset_jwt_cookies(resp)
    return resp


@app.route('/authenticationToGitHub', methods=["GET", "POST"])
@jwt_required()
def authentication_GitHub():
   
    return github.authorize()


@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        
        return redirect(next_url)
    
    flash("Authorization succeeded")
    #current_user.github_access_token = oauth_token
    #print (request.args['oauth_token'])
    #db.session.commit()
    
    
    return redirect(next_url)



@github.access_token_getter
def token_getter():
    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    
    if current_user is not None:
        return current_user.github_access_token


#cruf for apps

@app.route('/allProjects', methods=['GET', 'POST'])
@jwt_required(fresh=True)
def get_all_projects():

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    
    if not current_user.admin:
        flash('Please login as an administrator')
        return redirect(url_for('login_page')) 


    output = getAllApps()

    if request.method == 'POST':
        name_app = request.form.get("name_app")
        projectOwner=request.form.get("projectOwner")
        if request.form['action'] == 'more' :
            return redirect(f'/project/{name_app}')
        elif request.form['action'] == 'update':
            return redirect(f'/project/{projectOwner}/update')
        elif request.form['action'] == 'delete':
            return redirect(f'/project/{name_app}/delete')
        elif request.form['action'] == 'create':
            return redirect('/GetRepo')
        else:
            
            return redirect(url_for('get_all_projects'))
        
    return render_template("allProjects.html", data=output)   

@app.route('/myProjects', methods=['GET', 'POST'])
@jwt_required()
def get_my_projects():

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()
    
    
    output = getAppsByUser(current_user)

    if request.method == 'POST':
        name_app = request.form.get("NameOfProject")
        
        if request.form['action'] == 'more' :
            return redirect(f'/project/{name_app}')
        elif request.form['action'] == 'update':
            return redirect(f'/project/{current_user}/update')
        elif request.form['action'] == 'delete':
            return redirect(f'/myProject/{name_app}/delete')
        elif request.form['action'] == 'create':
            return redirect('/GetRepo')
        else:
            
            return redirect(url_for('get_my_projects'))
        
    return render_template("allProjects.html", data=output)   


@app.route('/project/<name_app>', methods=['GET'])
@jwt_required(fresh=True)
def get_one_project(name_app):

    
    app_data=getOneProjectByName(name_app)
    
    return render_template('oneProject.html', app_data = app_data)

 

@app.route('/project/<name_app>/delete', methods=['GET','POST'])
@jwt_required(fresh=True)
def delete_app(name_app):

    username=get_jwt_identity()

    current_user = User.query.filter_by(username=username).first()

    form = DeleteProject() 
    if form.validate_on_submit():
        deleteApp(name_app)
        return redirect(url_for('get_all_projects'))    
    
    return render_template('deleteProject.html', form=form)

@app.route('/myProject/<name_app>/delete', methods=['GET','POST'])
@jwt_required()
def delete_myapp(name_app):

    username=get_jwt_identity()

    form = DeleteProject() 
    if form.validate_on_submit():
        deleteApp(name_app)
        return redirect(url_for('get_my_projects'))    
    
    return render_template('deleteProject.html', form=form)
    
@app.route('/project/<projectOwner>/update', methods = ['GET','POST'])
@jwt_required()

def update_project(git_repository,projectOwner):
 

    form = UpdateProject()
    if form.validate_on_submit():
        nameOfProject=form.nameOfProject.data
        gitRepo = form.gitRepo.data
        path = form.path.data
        nameEntryFile=form.entry_file.data
        result=is_git_repo(gitRepo)
        if result and checkIfDirectoryExist(path) and projectOwner.github_access_token and projectOwner.github_username:
            repo_dir=cloningRepoOrUpdate(path,gitRepo,projectOwner.github_username,projectOwner.github_access_token)
            listOfFiles=listdirectory(repo_dir)
            entryFile=fileContent(listOfFiles,nameEntryFile)
            jenkinsFile=fileContent(listOfFiles,'Jenkinsfile')
            if entryFile:
                
                dic=languageOfApp(listOfFiles)
                listResultOfDetectionOfFramework=detectFrameworkOfApp(dic,entryFile,nameEntryFile,listOfFiles)
                updateApp(nameOfProject,gitRepo,entryFile,jenkinsFile,listResultOfDetectionOfFramework[0],projectOwner)
                return render_template('languageOfApp.html',dic=dic,listResultOfDetectionOfFramework=listResultOfDetectionOfFramework)

        
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with updating the project: {err_msg}')
    
    return render_template('updateProject.html', form=form)

@app.route('/getJobConfig')
@jwt_required()
def get_job_config():
    server=authenticationToJenkins(app.config['JENKINS_URL'],app.config['JENKINS_USERNAME'],app.config['JENKINS_PASSWORD'])
    new_config=getJobConfig(server,'yalla')
    jobInfo=getJobInfo(server,'flaskex-pipeline')
    print("here job informations")
    print(type(jobInfo))
    print(jobInfo)
    print("debug job info")
    print (type(server.debug_job_info('flaskex-pipeline')))
    print(server.debug_job_info('flaskex-pipeline'))
    print('test report')
    print(getBuildTestReport(server,'flaskex-pipeline',5))
    create_job_jenkins(server,'helloo',new_config)
    number=getNumberOfJobs(server)
    print(number)
    deleteJobJenkins(server,'test4')
    return render_template('home.html')



