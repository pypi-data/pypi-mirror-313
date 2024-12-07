"""
数据接口定义：
输入prompt_list: List[List]，外部的List长度决定循环次数以及多卡各自的循环次数，内部的List长度是batch_size。
输出predict_list: List[List]，n张卡就有n个部分

函数接口定义：6个参数
model_path          模型路径
gpu_id              使用的GPU id
prompt_list         分割好的提示词列表
file_output_path：  Predict输出结果路径
engine_config       推理引擎（如vllm）的配置

"""

import pickle
from tqdm import tqdm
from vllm import LLM, SamplingParams
import os
import sys
from wayne_utils import save_data



def split_inner_list( prompt ):
    # aaa = [i for i in range(99)]
    inner_list = []
    interval = []
    for j in range( 0, len(prompt)+1, 10):
        interval.append(j)
    if len(prompt)%10 != 0:
        interval.append(len(prompt))
    for j in range(len(interval)-1):
        inner_list.append( prompt[ interval[j]: interval[j+1] ])
    return inner_list

def load_model( engine_config,  model_path ):
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
    return sampling_params, llm


def vLLMPredict( **configs ):
    # 加载Prompt，检查本地路径
    os.environ["CUDA_VISIBLE_DEVICES"] = str( configs["gpu_id"] )
    prompt_list = configs["prompt_list"]
    # 加载模型，在对应GPU上启动vllm引擎（在bash脚本中由环境变量指定GPU）
    engine_config = configs["engine_config"]
    sampling_params, llm = load_model( engine_config,  configs["model_path"] )
    print(f"No.{ configs['gpu_id'] } LLM Inderence start!")
    # 开始批处理
    part_result = []
    for i in tqdm(range(len( prompt_list )), dynamic_ncols=True, file=sys.stdout, desc=f"第{configs['gpu_id']}部分："):
        "分类讨论prompt情况"
        if not isinstance( prompt_list[i], list):                   # 如果不是嵌套列表，加两层
            inner_list = [[ prompt_list[i] ]]
        elif len(prompt_list[i])>10:                                # 如果是嵌套列表且长度>10，分开
            inner_list = split_inner_list( prompt_list[i] )
            print( f"长度过长，分为{len(inner_list)}个长度为10的sub batch")
        else:                                                       # 如果是嵌套列表且长度<=10，加一层
            inner_list = [ prompt_list[i] ]
        # 推理：[ [ prompt1, 2, 3], []]
        sub_total = []
        for j in range( len(inner_list) ):
            outputs = llm.generate(inner_list[j], sampling_params, use_tqdm=False)   # 将输入提示添加到vLLM引擎的等待队列中，并执行vLLM发动机以生成高吞吐量的输出。输出以RequestOutput对象列表的形式返回，其中包括所有输出令牌。
            ret = []
            for output in outputs:
                ret.append( output.outputs[0].text )
            sub_total.extend( ret )
        part_result.append( sub_total )
    # 保存列表
    save_data( part_result, os.path.join( configs["file_output_path"], f"{str(configs['gpu_id'])}.pickle") )