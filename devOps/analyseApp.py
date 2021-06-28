from guesslang import Guess
import git 
from git import Repo
import os.path
import glob
import subprocess
from os.path import basename
import requests
import getpass
import json
from urllib.parse import urljoin
from flask import flash
#GITHUB_API = 'https://api.github.com'
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth




def checkIfDirectoryExist(path):
    isdirectory = os.path.isdir(path)
    return isdirectory

def is_git_repo(gitRepo):

    try:
        result=subprocess.check_output(['git','ls-remote',gitRepo]).decode("utf-8")
    except subprocess.CalledProcessError as err:
        result=''
    return result
        

def cloningRepoOrUpdate(path,gitRepo,usernameGithub,token):
    url1=gitRepo[0:8]
    url2=gitRepo[8:]#.replace('/','%2F')
    url=url1+'{}:{}@'.format(usernameGithub,token)+url2
    repo_dir=path+"/"+get_repo_name_from_url(gitRepo)
    if checkIfDirectoryExist(repo_dir):
        # pull
        g = git.cmd.Git(repo_dir)
        g.pull()    
        flash('Pulling Project...',category='success')             
    else:
        # clone
        Repo.clone_from(url,repo_dir)
        flash('cloned!',category='success')
    return repo_dir


def fileContent(listOfFiles,nameOfFile):
    for i in listOfFiles:
        if basename(i)==nameOfFile:
            with open(i,'r') as f:
                
                return (f.read())
    flash(f'no {nameOfFile} found')   
    return ('')        
#rechercher et retourner le contenue de fichier dans une chaine des caracteres

def get_repo_name_from_url(url: str) -> str:#prend lien de repo git et renvoi le non de repo
    last_slash_index = url.rfind("/")#utilisé pour savoir le dossier de clone
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]

def listdirectory(path): #extraire tt les fichiers en ignorant binary files et hidden files
    fichier=[] 
    ext=['.png','.jpg','.jpeg','.txt','.md','.zip','.PNG','.gif']#à ajouter
    for root, dirs, files in os.walk(path): 
        files = [f for f in files if not f[0] == '.' and (os.path.splitext(f))[1] not in ext ]
        #and len((os.path.splitext(f))[1])!=0
        dirs[:] = [d for d in dirs if not d[0] == '.'] 
        for i in files:
            
            fichier.append(os.path.join(root, i)) 
    for i in fichier:
        with open(i,'r') as f:
                if not f.read():
                    fichier.remove(i)
    return fichier

def detectionLang(listOfFiles):#prend la liste des fichiers er retourner dict contenant fichier:prog langage
    guess=Guess()
    b = {'0','1'}
    filesLangages=dict()
    for i in listOfFiles:
        if os.stat(i).st_size != 0:
            with open(i,'r',encoding='latin1',errors='ignore') as f:
                if b!=set(f.read()) and set(f.read())!={'0'} and set(f.read())!={'1'}:
                    #filesLangages[i]=guess.language_name(f.read())
                    filesLangages[i]=subprocess.check_output(['guesslang',i]).decode("utf-8")
                
    return(filesLangages)
            #filesLangages[i]=subprocess.check_output(['guesslang',i])


#listOfFiles=listdirectory(repo_dir)
def languageOfApp(listOfFiles):
    #git.Git(path).clone(gitRepo)
    #listOfFiles=listdirectory(repo_dir)
    filesLangages=detectionLang(listOfFiles)
    
    progLangages=list(filesLangages.values())
    
    s={i for i  in progLangages if 'guesslang.guess WARNING Empty source code' not in i}
    dic={i.split(':')[1]:round(progLangages.count(i)*100/len(progLangages),2) for i in s}
    return (dic)

#entryFile=fileContent(listOfFiles,nameEntryFile)
def detectFrameworkOfApp(dic,entryFile,nameEntryFile,listOfFiles):
    #il faut vérifier si entryFile est vide?
    frameworkOfApp=''
    commandToRunApp=''
    if " Python\n" in dic.keys():
        
        if nameEntryFile=='manage.py':
            if 'DJANGO' or 'django' or 'Django' in entryFile:
                frameworkOfApp='Django'
                commandToRunApp="python {} runserver".format(nameEntryFile)
                
                                   
        elif 'app = Flask(__name__)' or 'from flask import Flask' in entryFile:
            
            frameworkOfApp='Flask'
            commandToRunApp="""export FLASK_APP={}
export FLASK_ENV=development
flask run""".format(nameEntryFile)
    elif " Java\n" in dic.keys():
        if '@SpringBootApplication' in entryFile:
            frameworkOfApp='SpringBoot'
            build='''<build>
        <plugins>
             <plugin>
                 <groupId>org.springframework.boot</groupId>
                 <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
     </build>'''
            commandToRunApp='mvn spring-boot:run'
            pomXML=fileContent(listOfFiles,'pom.xml')
            if build not in pomXML:
                for i in listOfFiles:
                    if basename(i)=='pom.xml':
                        with open("pom.xml", "a") as file_object:
                            file_object.write('\n')
                            file_object.write(build)
                            file_object.close()

    return([frameworkOfApp,commandToRunApp])

                
    
        
        

    

