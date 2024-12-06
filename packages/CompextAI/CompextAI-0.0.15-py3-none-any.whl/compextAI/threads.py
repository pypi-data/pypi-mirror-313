from compextAI.api.api import APIClient

class ThreadExecutionResponse:
    thread_execution_id: str
    thread_id: str

    def __init__(self, thread_execution_id:str, thread_id:str):
        self.thread_execution_id = thread_execution_id
        self.thread_id = thread_id

class Thread:
    thread_id: str
    title: str
    metadata: dict

    def __init__(self, thread_id:str, title:str, metadata:dict):
        self.thread_id = thread_id
        self.title = title
        self.metadata = metadata

    def __str__(self):
        return f"Thread(thread_id={self.thread_id}, title={self.title}, metadata={self.metadata})"
    
    def execute(self, client:APIClient, thread_exec_param_id: str, system_prompt:str="", append_assistant_response:bool=True, metadata:dict={}) -> ThreadExecutionResponse:
        response = client.post(f"/thread/{self.thread_id}/execute", data={
            "thread_execution_param_id": thread_exec_param_id,
            "append_assistant_response": append_assistant_response,
            "thread_execution_system_prompt": system_prompt,
            "metadata": metadata
        })

        status_code: int = response["status"]
        data: dict = response["data"]
        
        if status_code != 200:
            raise Exception(f"Failed to execute thread, status code: {status_code}, response: {data}")
        
        return ThreadExecutionResponse(data["identifier"], self.thread_id)


def get_thread_object_from_dict(data:dict) -> Thread:
    return Thread(data["identifier"], data["title"], data["metadata"])

def list(client:APIClient, project_name:str) -> list[Thread]:
    response = client.get(f"/thread/all/{project_name}")
    
    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to list threads, status code: {status_code}, response: {data}")
    
    threads = [get_thread_object_from_dict(thread) for thread in data]
    
    return threads

def retrieve(client:APIClient, thread_id:str) -> Thread:
    response = client.get(f"/thread/{thread_id}")
    
    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to retrieve thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def create(client:APIClient,project_name:str, title:str=None, metadata:dict={}) -> Thread:
    response = client.post(f"/thread", data={"project_name": project_name, "title": title, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to create thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def update(client:APIClient, thread_id:str, title:str=None, metadata:dict={}) -> Thread:
    response = client.put(f"/thread/{thread_id}", data={"title": title, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to update thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def delete(client:APIClient, thread_id:str) -> bool:
    response = client.delete(f"/thread/{thread_id}")
    return response["status"] == 204
