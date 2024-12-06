from compextAI.api.api import APIClient

class ThreadExecutionParam:
    thread_execution_param_id: str
    name: str
    environment: str
    model: str
    temperature: float
    timeout: int
    max_tokens: int
    max_completion_tokens: int
    top_p: float
    max_output_tokens: int
    response_format: any
    system_prompt: str

    def __init__(self, thread_execution_param_id:str, name:str, environment:str, model:str, temperature:float, timeout:int, max_tokens:int=None, max_completion_tokens:int=None, top_p:float=None, max_output_tokens:int=None, response_format:any=None, system_prompt:str=None):
        self.thread_execution_param_id = thread_execution_param_id
        self.name = name
        self.environment = environment
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.max_completion_tokens = max_completion_tokens
        self.top_p = top_p
        self.max_output_tokens = max_output_tokens
        self.response_format = response_format
        self.system_prompt = system_prompt

    def __str__(self):
        return f"ThreadExecutionParam(thread_execution_param_id={self.thread_execution_param_id}, name={self.name}, environment={self.environment}, model={self.model}, temperature={self.temperature}, timeout={self.timeout}, max_tokens={self.max_tokens}, max_completion_tokens={self.max_completion_tokens}, top_p={self.top_p}, max_output_tokens={self.max_output_tokens}, response_format={self.response_format}, system_prompt={self.system_prompt})"

def get_thread_execution_param_object_from_dict(data:dict) -> ThreadExecutionParam:
    return ThreadExecutionParam(data["identifier"], data["name"], data["environment"], data["model"], data["temperature"], data["timeout"], data["max_tokens"], data["max_completion_tokens"], data["top_p"], data["max_output_tokens"], data["response_format"], data["system_prompt"])

def list(client:APIClient, project_name:str) -> list[ThreadExecutionParam]:
    response = client.get(f"/execparams/fetchall/{project_name}")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to list thread execution parameters, status code: {status_code}, response: {data}")
    
    return [get_thread_execution_param_object_from_dict(param) for param in data]

def retrieve(client:APIClient, name:str, environment:str, project_name:str) -> ThreadExecutionParam:
    response = client.post(f"/execparams/fetch", data={"name": name, "environment": environment, "project_name": project_name})

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to retrieve thread execution parameter, status code: {status_code}, response: {data}")
    
    return get_thread_execution_param_object_from_dict(data)


def create(client:APIClient, name:str, environment:str, project_name:str, template_id:str) -> ThreadExecutionParam:
    response = client.post(f"/execparams/create", data={"name": name, "environment": environment, "project_name": project_name, "template_id": template_id})

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to create thread execution parameter, status code: {status_code}, response: {data}")
    
    return get_thread_execution_param_object_from_dict(data)

def update(client:APIClient, name:str, environment:str, templateID:str) -> ThreadExecutionParam:
    response = client.post(f"/execparams/update", data={"name": name, "environment": environment, "template_id": templateID})

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to update thread execution parameter, status code: {status_code}, response: {data}")
    
    return get_thread_execution_param_object_from_dict(data)

def delete(client:APIClient, name:str, environment:str, project_name:str) -> bool:
    response = client.post(f"/execparams/delete", data={"name": name, "environment": environment, "project_name": project_name})

    return response["status"] == 204
