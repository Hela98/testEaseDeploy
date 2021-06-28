from devOps import db
from devOps.models import Application,FrameworkOfApp,User
from devOps.communicationWithJenkins import getJobConfig,authenticationToJenkins,deleteJobJenkins
from flask import Flask ,flash

#some_framework=FrameworkOfApp.query.filter_by(name='Django').first()
#app.owners.append(user)
#
def createApp(nameApp,gitRepository,entryFile,jenkinsfile,framework,username):

    current_user = User.query.filter_by(username=username).first()
    some_framework=FrameworkOfApp.query.filter_by(name_frame=framework).first()
    app = Application.query.filter_by(git_repository=gitRepository,projectOwner=current_user).first()
    if not app:
        app = Application(nameApp,gitRepository,entryFile,jenkinsfile,some_framework,current_user)
        db.session.add(app)
        db.session.commit()
    #,frameworkOfApp=some_framework,projectOwner=current_user
    else: 
        return (updateApp(nameApp,gitRepository,entryFile,jenkinsfile,some_framework,current_user))
    
        
        
def updateApp(nameApp,gitRepository,entryFile,jenkinsfile,some_framework,current_user):

    app = Application.query.filter_by(git_repository=gitRepository,projectOwner=current_user).first()
    
    if app: 
        app.name_app=nameApp
        app.entry_file=entryFile
        app.frameworkOfApp=some_framework
        app.jenkins_file=jenkinsfile
        #server=authenticationToJenkins(app.config['JENKINS_URL'],app.config['JENKINS_USERNAME'],app.config['JENKINS_PASSWORD'])
        #deleteJobJenkins(server,app.name_app)
        #create new job jenkins
        db.session.commit()
        flash("Application successfully updated!")
 


def deleteApp(nameApp):

    app = Application.query.filter_by(name_app=nameApp).first()
    if app:
        #server=authenticationToJenkins(app.config['JENKINS_URL'],app.config['JENKINS_USERNAME'],app.config['JENKINS_PASSWORD'])
        #deleteJobJenkins(server,nameApp)
        db.session.delete(app)
        db.session.commit()
        flash("Application successfully deleted!")
   

def getAllApps():
    apps = Application.query.all()

    output = []

    for app in apps:
        apps_data = {}
        apps_data['name_app'] = app.name_app
        apps_data['git_repository'] = app.git_repository
        apps_data['entry_file'] = app.entry_file
        
            
        apps_data['jenkins_file'] = app.jenkins_file

        apps_data['frameworkOfApp'] = app.frameworkOfApp.name_frame
        apps_data['projectOwner'] = app.projectOwner
        output.append(apps_data)
    return (output)

def getAppsByUser(user):

    projectsOfUser=user.projects
    list_user_apps=[]
    if projectsOfUser:
        for app in projectsOfUser:
            project_data={}
            project_data['NameOfProject']=app.name_app
            project_data['FrameworkOfProject']=app.frameworkOfApp.name_frame
            project_data['GitRepository']=app.git_repository
            project_data['EntryFile']=app.entry_file
            project_data['jenkins_file']=app.jenkins_file
            list_user_apps.append(project_data)
    return list_user_apps   

def getOneProjectByName(name_app):

    app = Application.query.filter_by(name_app=name_app).first()

    if not app:
        
        return f"Project with name ={name_app} not found"

    app_data = {}
    app_data['NameOfProject']=app.name_app
    app_data['FrameworkOfProject']=app.frameworkOfApp.name_frame
    app_data['GitRepository']=app.git_repository
    app_data['EntryFile']=app.entry_file  
    app_data['ProjectOwner']=app.projectOwner.username
    if app.jenkins_file:
        app_data['jenkins_file']=app.jenkins_file

    return app_data