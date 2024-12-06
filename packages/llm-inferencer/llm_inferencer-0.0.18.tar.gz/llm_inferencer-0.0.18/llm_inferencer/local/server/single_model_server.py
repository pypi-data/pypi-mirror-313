"""
Flask是同步框架，所以在接口消息收发上异步比较困难
"""

import os
import sys
from flask import Flask, request, jsonify, Blueprint
from vllm import LLM, SamplingParams



# 初始化 Flask 应用
app = Flask(__name__)
llm_blueprint = Blueprint('single_llm_server', __name__, url_prefix='/api/v1/llm')


# 模型和推理函数
llm, sampling_params = None, None

def load_model( engine_config,  model_path ):
    global llm, sampling_params
    sampling_params = SamplingParams( temperature=engine_config["temperature"],
                                    top_p=engine_config["top_p"], 
                                    use_beam_search=engine_config["use_beam_search"],
                                    best_of=engine_config["best_of"])
    llm = LLM(
        model=model_path,
        trust_remote_code=True,
        dtype='float16',
        gpu_memory_utilization=engine_config["gpu_memory_utilization"],
        seed = engine_config["seed"],
    )


@llm_blueprint.route('/predict', methods=['POST'])
def predict():
    """
    接收推理请求并进行推理
    """
    if llm is None:
        return jsonify({"error": "Model not loaded yet"}), 500
    
    # 获取请求的推理输入数据
    data = request.get_json()
    prompt = data.get('prompt')
    if prompt == "<STOP>":
        func = request.environ.get('werkzeug.server.shutdown')      # 只能用于开发模式debug=True，生成模式直接手动退出即可
        if func:
            func()  # 优雅地关闭服务器
        return jsonify({"result": "服务器正在关闭..."}), 200
        # return jsonify({"result": "Quit"})
        
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    outputs = llm.generate(prompt, sampling_params, use_tqdm=False)   # 将输入提示添加到vLLM引擎的等待队列中，并执行vLLM发动机以生成高吞吐量的输出。输出以RequestOutput对象列表的形式返回，其中包括所有输出令牌。
    ret = []
    for output in outputs:
        ret.append( output.outputs[0].text )
    return jsonify({"result": ret})

def start_single_model_server( inference_config ):
    """
    启动单个 Flask 服务器，负责一个模型
    """
    app.register_blueprint(llm_blueprint)
    gpu_id = inference_config["gpu_id"]
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)  # 设置CUDA设备
    engine_config = inference_config[ "engine_config" ]
    model_path = inference_config[ "model_path" ]
    load_model( engine_config,  model_path )
    app.run(host="0.0.0.0", port=5000 + gpu_id+1)


if __name__ == '__main__':
    engine_config = {
        "temperature" : 0,
        "top_p" : 1,
        "use_beam_search": True,
        "best_of": 2,
        "gpu_memory_utilization": 0.7,
        "seed": 24
    }
    inference_config = {
        "model_path": "/home/jiangpeiwen2/jiangpeiwen2/workspace/LLMs/ChatGLM3-6B/ZhipuAI/chatglm3-6b",
        "gpu_id": 0,
        "engine_config" : engine_config
    }
    start_single_model_server( inference_config )
