from devOps import db,login_manager
from devOps import bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'tblUser'
    id = db.Column(db.Integer(), primary_key=True)
    public_id= db.Column(db.String(50),unique=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    github_access_token = db.Column(db.String(length=255))
    github_username=db.Column(db.String(length=50))
    admin = db.Column(db.Boolean)
    projects = db.relationship('Application',backref='projectOwner',lazy=True)
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    @property
    def roleOfUser(self):
        return self.admin

    def __init__(self,username,email_address,password_hash,admin,public_id=None):
        if public_id is None:
            self.public_id=str(uuid.uuid4())
        else:
            public_id=public_id   

        
        self.username = username
        self.email_address = email_address
        self.password_hash = generate_password_hash(password_hash, method='sha256')
        self.admin=admin

    
    
    def __repr__(self):
        return f'<User {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
   
	
class Application(db.Model,UserMixin):
    __tablename__ = 'tblApplication'
    id_app = db.Column(db.Integer(), primary_key=True)
    name_app = db.Column(db.String(length=30), nullable=False,unique=True)
    git_repository = db.Column(db.Text(), nullable=False, unique=True)
    jenkins_file = db.Column(db.String(length=100000))
    entry_file = db.Column(db.String(length=60),nullable=False)
    id_frame=db.Column(db.Integer, db.ForeignKey('tblFrameworkOfApp.id_frame'),nullable=False)
    id_user=db.Column(db.Integer, db.ForeignKey('tblUser.id'),nullable=False)

    def __init__(self,name_app,git_repository,entry_file,jenkinsfile,some_framework,current_user):
         
        self.name_app = name_app
        self.git_repository = git_repository
        self.entry_file = entry_file
        self.jenkins_file=jenkinsfile
        self.frameworkOfApp=some_framework
        self.projectOwner=current_user
        
       
        
    
frameworkBlocksJenkins = db.Table('frameworkBlocksJenkins',
       
       db.Column('id_frame', db.Integer, db.ForeignKey('tblFrameworkOfApp.id_frame')),
       db.Column('id_block', db.Integer, db.ForeignKey('tblBlocksJenkins.id_block'))
       
)
class FrameworkOfApp(db.Model,UserMixin):
    __tablename__ = 'tblFrameworkOfApp'
    id_frame = db.Column(db.Integer(), primary_key=True)
    name_frame = db.Column(db.String(length=30), nullable=False,unique=True)
    apps = db.relationship('Application',backref='frameworkOfApp',lazy=True)
    
    
    def __init__(self,name_frame):
        
        self.name_frame = name_frame

    def __repr__(self):
        return f'<Framework {self.name_frame}>'

class BlocksJenkins(db.Model,UserMixin):
    __tablename__ = 'tblBlocksJenkins'
    id_block=db.Column(db.Integer(), primary_key=True)
    block = db.Column(db.String(length=500), unique=True,nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('tblWhichStepOfPipeline.id_step'),
        nullable=False)
    frameworks = db.relationship('FrameworkOfApp', secondary=frameworkBlocksJenkins, backref=db.backref('frameworksOfBlockJenkins', lazy='dynamic'))

    def __init__(self,block,stepOfPipeline):
        
        self.block = block
        self.stepOfPipeline=stepOfPipeline



class WhichStageOfPipeline(db.Model,UserMixin):
    __tablename__ = 'tblWhichStageOfPipeline'
    id_stage=db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    steps = db.relationship('WhichStepOfPipeline', backref='stageOfPipeline', lazy=True)

    def __init__(self,name):
        
        self.name = name

class WhichStepOfPipeline(db.Model,UserMixin):
    __tablename__ = 'tblWhichStepOfPipeline'
    id_step=db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False,unique=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('tblWhichStageOfPipeline.id_stage'),
        nullable=False)
    blocksPipeline = db.relationship('BlocksJenkins', backref='stepOfPipeline', lazy=True)

    def __init__(self,name):
        
        self.name = name