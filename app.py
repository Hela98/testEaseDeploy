from flask import Flask , render_template, session, redirect, url_for, request
from forms import MyForm
from guesslang import Guess
import git 
import os.path
import glob
import subprocess
from flask import jsonify
from os.path import basename
app = Flask(__name__)
app.config.from_object('config.config')

@app.route('/')
def index():
    return "Hello world !"
@app.route('/index', methods=['GET','POST'])
def home():
    form = MyForm()
    
    if form.validate_on_submit():
           gitRepo = request.form.get('gitRepo')
           path = request.form.get('path')
           print(path)
           git.Git(path).clone(gitRepo)
           fichiers=listdirectory(path+"/"+get_repo_name_from_url(gitRepo))
           print (fichiers)
           stagesJenkinsFile=extractStagesPipeline(foundJenkinsfile(fichiers))
           for i in range(len(stagesJenkinsFile)):
               print('stage n {}:{} \n'.format(i+1,stagesJenkinsFile[i]))
           
           
           
           filesLangages=detectionLang(fichiers)
           
           #for cle, valeur in filesLangages.items():
           result=[cle+"  :  "  +str(valeur) for cle, valeur in filesLangages.items()]
           #print (dic)'''
           
           
           return ("\n".join(result))
    return render_template('index.html', form=form)

def get_repo_name_from_url(url: str) -> str:#prend lien de repo git et renvoi le non de repo
    last_slash_index = url.rfind("/")#utilisé pour savoir le dossier de clone
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]

"""def listdirectory(path):
    
    fichier=[] 
    l = glob.glob(path+'\\*') 
    for i in l:
        if os.path.isdir(i):
            fichier.extend(listdirectory(i)) 
        else:
            #if not (i.endswith(('.txt','.png'))):
                fichier.append(i)"""
def listdirectory(path): #extraire tt les fichiers en ignorant binary files et hidden files
    fichier=[] 
    ext=['.png','.jpg','.jpeg']#à ajouter
    for root, dirs, files in os.walk(path): 
        files = [f for f in files if not f[0] == '.' and (os.path.splitext(f))[1] not in ext]
        dirs[:] = [d for d in dirs if not d[0] == '.'] 
        for i in files:
            
            fichier.append(os.path.join(root, i)) 
    return fichier
            

    #return fichier

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
            
def foundJenkinsfile(listOfFiles):
    for i in listOfFiles:
        if basename(i)=='Jenkinsfile':
            with open(i,'r') as f:
                return (f.read())
    print("no Jenkins file found")           
#retourner le contenue de JenkinsFile dans une chaine des caracteres             

def extractStagesPipeline(strJenkinsFile):#prend comme param chaine de contenue de JenkinsFile
    listPipeline=strJenkinsFile.split('\n')
    stage='stage('    
    return([((i.replace('stage','')).strip("{ )('")).strip('"') for i in listPipeline if stage in i])       
#retourner liste stages de pipeline    


    
         
         
      

if __name__ == "__main__":
    app.run()
