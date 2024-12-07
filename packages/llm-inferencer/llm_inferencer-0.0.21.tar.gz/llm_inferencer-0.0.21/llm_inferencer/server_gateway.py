import argparse
import os
import sys
import requests

import importlib.util
import shutil
import multiprocessing
from wayne_utils import get_ROOT_PATH, load_data, save_data

_ROOT_PATH = get_ROOT_PATH( 1, __file__)
# sys.path.insert( 0, _ROOT_PATH)

from .local.reader.vllm_predict import vLLMPredict
from .local.server.single_model_server import start_single_model_server
from .remote.api_predict import OpenAIPredict
'''
from local.reader.vllm_predict import vLLMPredict
from local.server.single_model_server import start_single_model_server
from remote.api_predict import OpenAIPredict
'''
def get_interval_pair( prompt, part_id, part_num ):
    total_len = len(prompt)
    part_len = total_len // part_num
    index_list = []
    for i in range(part_num):
        index_list.append( part_len*i )
    index_list.append( total_len)
    # 获取所有分部的range左右区间，并根据part_id获取自身要处理的数据集的左右区间
    split_list = []
    for i in range(part_num):
        index_pair = []
        left = index_list[i]
        right = index_list[i+1]
        split_list.append((left, right))
    index_pair = split_list[part_id]
    return index_pair

def get_gpu_list( gpu_list_str, must=True ):
    if gpu_list_str != None:
        return list(map(int, gpu_list_str.split(',')))
    else:
        if must:
            print( "GPU必需，但未指定GPU，默认为0号")
            return [0]
        else:
            print( "GPU非必需，未指定GPU，默认为CPU推理")
            return 'cpu'

def merge_predict( gpu_list, file_output_path ):
    ret = []
    for i in gpu_list:
        part_data = load_data( os.path.join( file_output_path, f"{str(i)}.pickle"), "pickle")
        ret.extend( part_data )
    save_data( ret, os.path.join(file_output_path, "predict_list.pickle") )

class Inferencer():
    def __init__(self, kwargs):
        # Inference config
        self.inference_config = kwargs
        # Model config
        model_config_path = os.path.join(_ROOT_PATH, "model_list.yaml")
        self.model_config = load_data( model_config_path, "yaml")
        # Check intermediate results path
        self.temp_path = os.path.join( _ROOT_PATH, "temp")
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        "Inference config"
        self.gpu_list = get_gpu_list( kwargs["gpu_list"], must=True )               # GPU list: Used in both local and remote, for GPUs and temp file merge
        if "prompt_list_from_path" in kwargs and kwargs["prompt_list_from_path"] != None:
            self.prompts = load_data( kwargs["prompt_list_from_path"], "pickle" )
            self.sample_little = kwargs["sample_little"]
            if kwargs["sample_little"] !=None and isinstance( self.sample_little, int):
                print(f"进行小样本推理：{ self.sample_little }")
                self.prompts = self.prompts[ : self.sample_little ]
            self.merge_path = os.path.join( self.temp_path, "predict_list.pickle" )
            self.predict_list_to_path = kwargs["predict_list_to_path"]

        self.flask_server_list_url = []
        # 启动
        self.start_service()
    
    def parallel( self, inference_config, inferencer):
        "Multi-processor"
        part_num = len( self.gpu_list )
        processes = []
        for part_id, gpu_id in enumerate( self.gpu_list ):
            index_pair = get_interval_pair( self.prompts, part_id, part_num )
            sub_prompt_list = self.prompts[index_pair[0]: index_pair[1] ]
            inference_config["gpu_id"] = gpu_id
            inference_config["prompt_list"] = sub_prompt_list
            p = multiprocessing.Process(target=inferencer, kwargs=inference_config )
            processes.append(p)
            p.start()  # 启动子进程
        # 等待所有子进程完成
        for p in processes:
            p.join()
        merge_predict( self.gpu_list, self.temp_path )
        shutil.copy( self.merge_path, self.predict_list_to_path) 
        print("Model inference finished！")

    ######################################################本地运行：server or reader###########################################################
    def get_local_model_path(self):
        if self.inference_config["local_or_remote"] == "remote":
            raise Exception( "Remote mode need no model path")
        model_name = self.inference_config["model_name"]
        if model_name not in self.model_config["local"]:
            raise Exception( f"Local model {model_name} not in list")
        return self.model_config["local"][model_name]
    
    def run_servers_on_multiple_gpus( self, inference_config, gpu_list):
        """
        启动多个 Flask 服务器，每个服务器运行在不同的 GPU 上
        """
        processes = []
        self.flask_server_list_url = []
        for gpu_id in gpu_list:
            # 在每个 GPU 上启动一个服务器
            inference_config["gpu_id"] = gpu_id
            p = multiprocessing.Process(target=start_single_model_server, args=(inference_config,))
            p.start()
            processes.append(p)
            self.flask_server_list_url.append( f"http://127.0.0.1:{5001+gpu_id}/api/v1/llm/predict")
        print( f"There are {len(self.flask_server_list_url)} available. Now you can request using self.request( prompt, index:int )->list")
        """join会阻塞
        for p in processes:
            p.join()
        """

    def request( self, prompt, index:int)->list:
        "简化Flask请求"
        if index > len(self.flask_server_list_url):
            raise Exception( f"Index error, available flask urls are {self.flask_server_list_url}.")
        SERVER_URL = self.flask_server_list_url[index]
        data = {
            "prompt": prompt,
        }
        response = requests.post(SERVER_URL, json=data)
        return response.json()['result']

    def local_inference( self ):
        "Inference with local model"
        local_model_path = self.get_local_model_path()
        local_engine = self.inference_config["local_engine"]            # LLM engine and lib check
        engine_config = None
        if local_engine != None:
            if importlib.util.find_spec( local_engine ) is None:
                print(f"Engine {local_engine} not exists, run without any engine")
            else:
                engine_config = self.model_config[ "engine_config" ][local_engine]
                print(f"Engine{local_engine} exists, run with vllm")
        # 准备推理
        inference_config = {
            "model_path": local_model_path,
            "file_output_path": self.temp_path,
            "engine_config" : engine_config if engine_config else None
        }
        if self.inference_config["server_or_reader"] == "reader":
            "Read file and run model"
            self.parallel( inference_config, vLLMPredict)
        elif self.inference_config["server_or_reader"] == "server":
            "Start a server and return the api"
            self.run_servers_on_multiple_gpus( inference_config, self.gpu_list )

    ######################################################远程运行：server or reader###########################################################
    def remote_inference( self ):
        inference_config = {
            'API': self.model_config["remote"][ self.inference_config["apikey_name"] ],
            "model": self.inference_config["model_name"],
            "file_output_path": self.temp_path,
        }
        if self.inference_config["server_or_reader"] == "reader":
            "Read file and run model"
            self.parallel( inference_config, OpenAIPredict)
        elif self.inference_config["server_or_reader"] == "server":
            raise Exception("API server not available yet")
    
    def start_service(self):
        if self.inference_config["local_or_remote"] == "local":
            self.local_inference()
        elif self.inference_config["local_or_remote"] == "remote":
            self.remote_inference()
    
def main():
    parser = argparse.ArgumentParser(description="Run script with external arguments")
    parser.add_argument('--local_or_remote', type=str, required=True, help='local model or api')
    parser.add_argument('--server_or_reader', type=str, required=True, help='start a server or read file and batch processing')
    parser.add_argument('--prompt_list_from_path', type=str, required=False, help='提示词路径')
    parser.add_argument('--predict_list_to_path', type=str, required=False, help='预测输出路径')
    parser.add_argument('--model_name', type=str, required=True, help='模型路径')
    parser.add_argument('--gpu_list', type=str, required=False, help='可用GPU列表，非空表示本地，否则用远程')
    parser.add_argument('--sample_little', type=str, required=False, help='小样本情况')
    parser.add_argument('--local_engine', type=str, required=False, help='本地模型使用的推理引擎，可以为vllm, ollama等')
    parser.add_argument('--apikey_name', type=str, required=False, help='远程模型的apikey的名称')
    args = parser.parse_args()
    # 获取参数值
    local_or_remote = args.local_or_remote
    server_or_reader = args.server_or_reader
    prompt_list_from_path = args.prompt_list_from_path if args.prompt_list_from_path else None
    predict_list_to_path = args.predict_list_to_path if args.predict_list_to_path else None
    model_name = args.model_name
    gpu_list = args.gpu_list if args.gpu_list else None
    sample_little = args.sample_little if args.sample_little else None
    local_engine = args.local_engine if args.local_engine else None
    apikey_name = args.apikey_name if args.apikey_name else None

    kwargs = {}
    kwargs["local_or_remote"] = local_or_remote
    kwargs["server_or_reader"] = server_or_reader
    kwargs["model_name"] = model_name
    kwargs["gpu_list"] = gpu_list
    kwargs["local_engine"] = local_engine
    kwargs["apikey_name"] = apikey_name
    if prompt_list_from_path != None:
        kwargs["prompt_list_from_path"] = prompt_list_from_path
        kwargs["predict_list_to_path"] = predict_list_to_path
        kwargs["sample_little"] = sample_little
    inferencer = Inferencer( kwargs )

if __name__=="__main__":
    local_or_remote = "local"
    server_or_reader = "reader"
    model_name = "ChatGLM3-6B"
    gpu_list = "0,1,2,5"
    prompt_list_from_path = "/home/jiangpeiwen2/jiangpeiwen2/TKGT/test/LiveSum/v1/prompt_list_only.pickle"
    predict_list_to_path = "/home/jiangpeiwen2/jiangpeiwen2/TKGT/test/LiveSum/v1/predict_list_only.pickle"
    '''prompt_list_from_path = None
    predict_list_to_path = None'''
    sample_little = 6
    local_engine = "vllm"   # "vllm"
    apikey_name = "NL2GQL"
    
    kwargs = {}
    kwargs["local_or_remote"] = local_or_remote
    kwargs["server_or_reader"] = server_or_reader
    kwargs["model_name"] = model_name
    kwargs["gpu_list"] = gpu_list
    kwargs["local_engine"] = local_engine
    kwargs["apikey_name"] = apikey_name
    if prompt_list_from_path != None:
        kwargs["prompt_list_from_path"] = prompt_list_from_path
        kwargs["predict_list_to_path"] = predict_list_to_path
        kwargs["sample_little"] = sample_little

    inferencer = Inferencer( kwargs )
