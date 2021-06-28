from devOps import db
from devOps.models import Application,FrameworkOfApp,BlocksJenkins
from flask import Flask ,flash

#some_framework=FrameworkOfApp.query.filter_by(name='Django').first()
#app.owners.append(user)

def addFramework(nameFramework):


    
    framework = FrameworkOfApp.query.filter_by(name_frame=nameFramework).first()
    if not framework:
        framework = FrameworkOfApp(nameFramework)
        db.session.add(framework)
        db.session.commit()
    else: 
        flash("Framework already exist")
    
        
        
def updateFramework(nameFramework):

    new_framework = FrameworkOfApp.query.filter_by(name_frame=nameFramework).first()
    if not new_framework:
        flash("Framework doesn't exist")
    
    new_framework.name_frame=nameFramework
    db.session.commit()
    flash("Framework successfully updated!")
 

def deleteFramework(nameFramework):

    framework = FrameworkOfApp.query.filter_by(name_frame=nameFramework).first()
    if framework:
        db.session.delete(framework)
        db.session.commit()
        flash("Framework successfully deleted!")
    flash("Framework doesn't exist")

def getFrameworks():
    frameworks = FrameworkOfApp.query.all()

    output = []

    for framework in frameworks:
        framework_data = {}
        framework_data['name_framework'] = framework.name_frame
        output.append(framework_data)
    return (output)