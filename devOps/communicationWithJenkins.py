import os.path
import glob
import subprocess

from flask.helpers import flash
import jenkins
from os.path import basename

def extractStagesPipeline(strJenkinsFile):#prend comme param chaine de contenue de JenkinsFile
    listPipeline=strJenkinsFile.split('\n')
    stage='stage('    
    return([((i.replace('stage','')).strip("{ )('")).strip('"') for i in listPipeline if stage in i])       
#retourner liste stages de pipeline  

def generateConfigFileForJenkinsJob(pathFile,begin,pipeline,end):
    xmlFile=begin+pipeline+end
    with open(pathFile,"w")as f:
        f.write(xmlFile)
    return pathFile

def generateShellScriptToCreateJenkinsJob(pathConfigJenkins,pathScript,usernameJenkins,ApiToken,JobName,JenkinsURL):
    scriptShell="""#!/bin/bash
CRUMB=$(curl -s '{}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' -u {}:{})
curl -s -XPOST '{}/createItem?name={}' -u {}:{} --data-binary @{} -H "$CRUMB" -H "Content-Type:text/xml" """.format(JenkinsURL,usernameJenkins,ApiToken,JenkinsURL,JobName,usernameJenkins,ApiToken,pathConfigJenkins)
    with open(pathScript,"w")as f:
        f.write(scriptShell)
    return pathScript     

def createJenkinsJob(pathScript):
    script='.'+pathScript
    subprocess.call(['sudo','chmod','+x',pathScript])
    subprocess.call([pathScript])
         
def authenticationToJenkins(url,username,password):
    server=jenkins.Jenkins(url, username=username, password=password) 
    return server
    #user = server.get_whoami()
#version = server.get_version()
#print('Hello %s from Jenkins %s' % (user['fullName'], version))

def listJobsJenkins(server):
    jobs = server.get_jobs()
    return jobs
#Get list of jobs.

#Each job is a dictionary with ‘name’, ‘url’, ‘color’ and ‘fullname’ keys.

def deleteJobJenkins(server,nameOfJob):
    
    if server.job_exists(nameOfJob):
        server.delete_job(nameOfJob)
        
    

def renameJobJenkins(server,from_name, to_name):
    if server.job_exists(from_name):
        server.rename_job(from_name, to_name)
        return True
    return False

def getNumberOfJobs(server):
    return (server.jobs_count())
    
def create_job_jenkins(server,name,config_xml):
    if not server.job_exists(name):
        server.create_job(name,config_xml)#config_xml str
    else:
        flash("job already exist")
    

def getJobConfig(server,nameOfJenkinsJob):

    if server.job_exists(nameOfJenkinsJob):
        return server.get_job_config(nameOfJenkinsJob) #job configuration (XML format)

def getJobInfo(server,nameOfJenkinsJob):

    if server.job_exists(nameOfJenkinsJob):
        return server.get_job_info(nameOfJenkinsJob, depth=0, fetch_all_builds=True) #return dic

def getDebugJobInfo(server,nameOfJenkinsJob):
    if server.job_exists(nameOfJenkinsJob):
        return server.debug_job_info(nameOfJenkinsJob) #return dic

def setNextBuildNumber(server,nameOfJenkinsJob,number):
    if server.job_exists(nameOfJenkinsJob):
        server.set_next_build_number(nameOfJenkinsJob, number)

def getBuildInfo(server,nameOfJenkinsJob,number):
    if server.job_exists(nameOfJenkinsJob):
        return server.get_build_info(nameOfJenkinsJob, number, depth=0)#return dic

def getBuildTestReport(server,nameOfJenkinsJob,number):
    if server.job_exists(nameOfJenkinsJob):
        return server.get_build_test_report(nameOfJenkinsJob, number, depth=0)
        #return dictionary of test report results, dict or None if there is no Test Report

def getBuildEnvVars(server,nameOfJenkinsJob,number):
    if server.job_exists(nameOfJenkinsJob):
        return server.get_build_env_vars(nameOfJenkinsJob, number, depth=0)
        '''dictionary of build env vars, dict or None for workflow jobs, or if InjectEnvVars plugin not installed'''

    
def reconfigJenkinsJob(server,nameOfJob,config_xml):

    if server.job_exists(nameOfJob):
        server.reconfig_job(nameOfJob, config_xml)#config_xml str

def runGroovyScripts(server,script):
    return server.run_script(script,node=None)

def stopABuild(server,nameOfJob,number):
    if server.job_exists(nameOfJob):
        server.stop_build(nameOfJob,number)

def deleteABuild(server,nameOfJob,number):
    if server.job_exists(nameOfJob):
        server.delete_build(nameOfJob,number)

def getRunningBuilds(server):
    return server.get_running_builds()
    #return list of builds
    
    