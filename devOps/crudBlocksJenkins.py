from devOps import db
from devOps.models import BlocksJenkins,FrameworkOfApp,WhichStepOfPipeline
from flask import Flask ,flash


def addBlockJenkins(block,NameOfFramework,nameOfStepOfPipeline):

    some_framework=FrameworkOfApp.query.filter_by(name_frame=NameOfFramework).first()
    block_Jenkins = BlocksJenkins.query.filter_by(block=block).first()
    stepOfPipeline=WhichStepOfPipeline.query.filter_by(name=nameOfStepOfPipeline).first()
    if not block_Jenkins:
        block_Jenkins =BlocksJenkins(block,stepOfPipeline)
        db.session.add(block_Jenkins)
        db.session.commit()
        block_Jenkins.frameworks.append(some_framework)
        db.session.commit()

def getAllBlocksJenkins():

    lisOfBlocksJenkins = BlocksJenkins.query.all()

    output = []

    for block in lisOfBlocksJenkins:
        block_data = {}
        block_data['id_block'] = block.id_block
        block_data['block Jenkins'] = block.block
        block_data['Which step of pipeline'] = block.stepOfPipeline
        frameworks=block.frameworks
        if frameworks:
            listFrameworksOfBlockJenkins=[]
            for framework in frameworks:
                
                listFrameworksOfBlockJenkins.append(framework.name_app)
            block_data['Frameworks']=listFrameworksOfBlockJenkins
        output.append(block_data)
    return (output)

def deleteBlockJenkins(id_block):
    blockJenkins=BlocksJenkins.query.get(id_block)
    if blockJenkins:
        db.session.delete(blockJenkins)
        db.session.commit()
        flash("Block Jenkins successfully deleted!")
    flash("Block Jenkins doesn't exist")
      

def updateBlockJenkins(id_block,block,NameOfFramework,nameOfStepOfPipeline):

    some_framework=FrameworkOfApp.query.filter_by(name_frame=NameOfFramework).first()
    block_Jenkins = BlocksJenkins.query.filter_by(id_block=id_block).first()
    stepOfPipeline=WhichStepOfPipeline.query.filter_by(name=nameOfStepOfPipeline).first()
    if block_Jenkins:

        block_Jenkins.block=block
        block_Jenkins.stepOfPipeline=stepOfPipeline
        db.session.commit()
        if some_framework not in block_Jenkins.frameworks:
            block_Jenkins.frameworks.append(some_framework)

        flash("Application successfully updated!")
 
      