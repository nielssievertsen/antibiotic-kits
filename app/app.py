from flask import Flask, render_template
from pymongo import MongoClient
from fabric.api import *


application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.MachineData


@application.route('/')
def showMachineList():
    return render_template("list.html")



@application.route("/addMachine", methods=['POST'])
def addMachine():
    """Insert record to MongoDb"""
    try:
        json_data = request.json['info']
        deviceName = json_data['device']
        ipAddress = json_data['ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']

        db.Machines.insert_one({
            'device':deviceName,'ip':ipAddress,'username':userName
            ,'password':password,'port':portNumber
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getMachineList",methods=['POST'])
def getMachineList():
    """Fetch details from MongoDb via find() API"""
    try:
        machines = db.Machines.find()
        
        machineList = []
        for machine in machines:
            print machine
            machineItem = {
                    'device':machine['device'],
                    'ip':machine['ip'],
                    'username':machine['username'],
                    'password':machine['password'],
                    'port':machine['port'],
                    'id': str(machine['_id'])
                    }
            machineList.append(machineItem)
    except Exception,e:
        return str(e)
    return json.dumps(machineList)

############# New section of tutorial 

@application.route('/updateMachine',methods=['POST'])
def updateMachine():
    """Update machine with id passed by user"""
    try:
        machineInfo = request.json['info']
        machineId = machineInfo['id']
        device = machineInfo['device']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        port = machineInfo['port']

        db.Machines.update_one({'_id':ObjectId(machineId)
            },{'$set':{'device':device,'ip':ip,'username':username,
            'password':password,'port':port}
            })
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/deleteMachine",methods=['POST'])
def deleteMachine():
    """Delete machine with id passed by user"""
    try:
        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


############# New section of tutorial using fabric

@application.route("/execute",methods=['POST'])
def execute():
    """Execute command requested by user. 

    Command defined by machineInfo
    Host_string and password need to be set
    """
    try:
        machineInfo = request.json['info']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        command = machineInfo['command']
        isRoot = machineInfo['isRoot']
        
        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK',message=resp)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))




if __name__ == "__main__":
    application.run(host='0.0.0.0')