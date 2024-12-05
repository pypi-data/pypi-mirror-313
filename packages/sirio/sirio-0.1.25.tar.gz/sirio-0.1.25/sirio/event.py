import json
from typing import List

class ObjEvent:
    taskId = ''
    taskPriority = ''
    taskName = ''
    processId = ''
    domain = ''
    businessKey = ''
    owner = ''
    internalBusinessKey = ''
    def __init__(self):
        self.files = []

def getObjEvent(event) -> List[ObjEvent]: 
    objReturn = []
    myList = list(event['Records'])
    for elem in myList:
        objEvent = ObjEvent()
        objMsg = json.loads(elem["body"])

        objEvent.taskId = objMsg["taskId"]
        objEvent.taskPriority = objMsg["taskPriority"]
        objEvent.taskName = objMsg["taskName"]
        objEvent.processId = objMsg["processId"]
        objEvent.domain = objMsg["domain"]
        objEvent.businessKey = objMsg["businessKey"]
        processVariables = objMsg["processVariables"]
        #objEvent.owner = processVariables["owner"]
        objEvent.internalBusinessKey = processVariables["internalBusinessKey"]
        objReturn.append(objEvent)

    return objReturn