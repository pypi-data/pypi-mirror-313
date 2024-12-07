"""
"""
from openai import OpenAI
from wayne_utils import load_data, save_data
import os
import sys
from tqdm import tqdm

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

def single_chat( prompt, client, model):
    completion = client.chat.completions.create(
        model= model,  # "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def OpenAIPredict( **configs ):
    part_id = configs['gpu_id']
    prompt_list = configs["prompt_list"]
    model = configs["model"]
    client = OpenAI(
        api_key = configs['API']['api_key'],
        base_url = configs['API']['base_url'],
    )
    if model not in configs['API']['model_list']:
        raise Exception( f"模型不支持{model}")
    part_result = []
    print(f"No.{ part_id } LLM API Inderence start!")
    for i in tqdm(range(len( prompt_list )), dynamic_ncols=True, file=sys.stdout, desc=f"第{part_id}部分："):
        "分类讨论prompt情况：都变成单个执行"
        if isinstance( prompt_list[i], str):                       # 如果是字符串列表，直接推理
            outputs = single_chat( prompt_list[i], client, model)
            part_result.append( outputs )
        elif isinstance( prompt_list[i], list): 
            sub_total = []
            for j in range( len(prompt_list[i]) ):
                outputs = single_chat( prompt_list[i][j], client, model)
                sub_total.append( outputs )
            part_result.append( sub_total )
    # 保存列表
    save_data( part_result, os.path.join( configs["file_output_path"], f"{str(part_id)}.pickle") )


if __name__ == "__main__":
    configs = {
        'API':{
            'api_key': 'sk-t4Mv9tJa0ftMCcKqKMAlqJmq3x5Da83Pk4U4Jq2M98C57GZG', 
            'base_url': "https://api.pro365.top/v1",
            'model_list': [
                'gpt-3.5-turbo', 'gpt-3.5-turbo-1106', 'gpt-4', 'gpt-4-0125-preview', 'gpt-4-turbo', 'gpt-4o', 'gpt-4o-2024-08-06', 'claude-2', 'claude-3-5-sonnet', 'llama-3-70b'
            ],
        },
        'gpu_id': 0,
        "prompt_list": load_data( "/home/jiangpeiwen2/jiangpeiwen2/TKGT/test/CPL/v1/prompt_lists.pickle", "pickle" )[:2],
        "model": "gpt-4",
        "file_output_path": "/home/jiangpeiwen2/jiangpeiwen2/test/pickle"

    }
    OpenAIPredict( configs )
    