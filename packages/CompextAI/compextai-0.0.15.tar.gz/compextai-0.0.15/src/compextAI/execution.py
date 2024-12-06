from compextAI.api.api import APIClient
from compextAI.messages import Message
from compextAI.threads import ThreadExecutionResponse

class ThreadExecutionStatus:
    status: str

    def __init__(self, status:str):
        self.status = status

def get_thread_execution_status(client:APIClient, thread_execution_id:str) -> str:
    response = client.get(f"/threadexec/{thread_execution_id}/status")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution status, status code: {status_code}, response: {data}")
    
    return ThreadExecutionStatus(data["status"])

def get_thread_execution_response(client:APIClient, thread_execution_id:str) -> dict:
    response = client.get(f"/threadexec/{thread_execution_id}/response")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution response, status code: {status_code}, response: {data}")
    
    return data


class ExecuteMessagesResponse:
    thread_execution_id: str

    def __init__(self, thread_execution_id:str):
        self.thread_execution_id = thread_execution_id

def execute_messages(client:APIClient, thread_execution_param_id:str, messages:list[Message],system_prompt:str="", append_assistant_response:bool=True, metadata:dict={}) -> ThreadExecutionResponse:
    thread_id = "compext_thread_null"
    response = client.post(f"/thread/{thread_id}/execute", data={
            "thread_execution_param_id": thread_execution_param_id,
            "append_assistant_response": append_assistant_response,
            "thread_execution_system_prompt": system_prompt,
            "messages": [message.to_dict() for message in messages],
            "metadata": metadata
        })

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to execute thread, status code: {status_code}, response: {data}")
        
    return ExecuteMessagesResponse(data["identifier"])
