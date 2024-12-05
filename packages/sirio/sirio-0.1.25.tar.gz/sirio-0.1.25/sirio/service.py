from typing import Union
from datetime import datetime
from sirio.business_object import BusinessObject
import requests
import contextlib
import json

from sirio.exceptions import SirioBoServiceNotRetriableException, SirioBoServiceRetriableException, SirioBoServiceTimeoutException


class SirioService():

    _get_bo_ep: str = '' 
    _complete_task_ep: str = ''
    _error_task_ep: str = ''
    

    def __init__(self, 
                 get_bo_ep: str = None, 
                 complete_task_ep: str = None,
                 error_task_ep: str = None, 
                 host_sirio_ep: str = None) -> None:

        """
        SirioCommService Class

        This class is responsible for all the communication to and from Sirio 

        Args:
            get_bo_ep (str): the URL of the endpoint to get a BO, given a businesskey. Alternatively, use only host_sirio_ep
            complete_task_ep (str): the URL of the endpoint to complete a task, given a businesskey and a valid BO. Alternatively, use only host_sirio_ep
            error_task_ep (str): the URL of the endpoint to error a task, given a businesskey and a valid BO. Alternatively, use only host_sirio_ep
            host_sirio_ep (str): the URL of the host for all endpoints. Alternatively, use: get_bo_ep, complete_task_ep and error_task_ep
        """
        if host_sirio_ep is not None:
            self._get_bo_ep = '{host}/sirio/enginebackend/businessobjects/{businessKey}?domain={domain}&taskId={taskId}'.replace('{host}',host_sirio_ep)
            self._complete_task_ep = '{host}/sirio/enginebackend/processes/domains/{domain}/tasks/{taskId}'.replace('{host}',host_sirio_ep)
            self._error_task_ep = '{host}/sirio/enginebackend/processes/domains/{domain}/tasks/{taskId}'.replace('{host}',host_sirio_ep) #Da sistemare quando il servizio sarà disponibile
        else:
            self._get_bo_ep = get_bo_ep
            self._complete_task_ep = complete_task_ep
            self._error_task_ep = error_task_ep


    def retrieveBo(self, businesskey: str, domain: str, taskId: str):
        
        try:
            response = requests.get(
                self._get_bo_ep.replace('{businessKey}', businesskey).replace('{domain}',domain).replace('{taskId}', taskId))
            
            # Check if something went wrong
            response.raise_for_status()
            
            # Get and return the Business Object
            bo = BusinessObject(businessKey=businesskey)
            bo.businessObject = response.json()
            bo.description = bo.businessObject['description']
            bo.subject = bo.businessObject['subject']
            bo.owner = bo.businessObject['owner']
            bo.priority = bo.businessObject['priority']
            bo.internalBusinessKey = bo.businessObject['internalBusinessKey']

            return bo

        except requests.exceptions.Timeout as ex:
            # This is retryable, but we *DON'T* want a retry policy executed in the lambda, to avoid 
            # nasty interaction between SQS visibility_windows and the lambda_timeout setting. 
            # If something goes wrong, the same message could be processed more than once, and 
            # who knows what could happen...
            raise SirioBoServiceTimeoutException(f"Timeout retrieving BO with BusinessKey {businesskey}")
        except requests.HTTPError as ex:
            # In these case we verify that the error is 404. In this case we want not to retry the 
            status_code = ex.response.status_code

            if status_code in [404, 501, 503]:
                raise SirioBoServiceNotRetriableException(f"BO with BusinessKey {businesskey} does not exists. Status {status_code}")

            raise SirioBoServiceRetriableException(f"Error retriving BO with BusinessKey {businesskey}. Status {status_code}")
        except Exception as ex:
            raise SirioBoServiceRetriableException(f"Generic error retriving BO with BusinessKey {businesskey}. Exc -> {ex}")



    def completeTask(self, bo: BusinessObject, domain: str, taskId: str, priority=None, owner=None):
        with contextlib.ExitStack() as stack:
            if len(bo.objects) > 0:
                if 'objects' not in bo.jsonComplete:
                    bo.jsonComplete['objects'] = []
                
                for index, obj in enumerate(bo.objects):
                    if obj.multipartMode:
                        jsonObj = {
                            "id" : obj.id,
                            "extension" : obj.extension,
                            "name" : obj.name,
                            "key" : obj.key,
                            "base64" : obj.base64,
                            "partIndex":index,
                            "params" : obj.params
                        }
                        bo.objects[index].file = stack.enter_context(open(obj.fileName, 'rb'))
                    else:
                            jsonObj = {
                            "id" : obj.id,
                            "extension" : obj.extension,
                            "name" : obj.name,
                            "key" : obj.key,
                            "base64" : obj.base64,
                            "params" : obj.parmas
                        }
                            #'dto': (json, 'application/json')
                    bo.jsonComplete['objects'].append(jsonObj)
            #json_file = stack.enter_context(tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8'))
            #json.dump(json_string, json_file, ensure_ascii=False, indent=4)
            #json_file.flush() 
            dto = bo.jsonComplete
            files = []
            payload = ('dto',(None, json.dumps(dto), 'application/json'))
            files.append(payload)
            for index, obj in enumerate(bo.objects):
                if obj.multipartMode:
                    files.append(('files',('{}.{}'.format(obj.name,obj.extension), obj.file, obj.contentType)))
            try:
                responseComplete = requests.post(self._complete_task_ep.replace('{domain}', domain).replace('{taskId}', taskId), files=files)

                # Check if something went wrong. We intercept all 
                # the issues in the response            
                responseComplete.raise_for_status()

                return True


            except requests.exceptions.Timeout as ex:
                # This is retryable, but we *DON'T* want a retry policy executed in the lambda, to avoid 
                # nasty interaction between SQS visibility_windows and the lambda_timeout setting. 
                # If something goes wrong, the same message could be processed more than once, and 
                # who knows what could happen...
                raise SirioBoServiceTimeoutException(f"Timeout persisting BO with BusinessKey {bo.businessKey}")
            except requests.HTTPError as ex:
                # In these case we verify that the error is 404. In this case we want not to retry the 
                status_code = ex.response.status_code

                if status_code in [404, 501, 503]:
                    raise SirioBoServiceNotRetriableException(f"Error persisting BO with BusinessKey {bo.businessKey}. Status {status_code}")

                raise SirioBoServiceRetriableException(f"Error persisting BO with BusinessKey {bo.businessKey}. Status {status_code}")
            except Exception as ex:
                raise SirioBoServiceRetriableException(f"Generic error persisting BO with BusinessKey {bo.businessKey}. Exc -> {ex}")
            
       