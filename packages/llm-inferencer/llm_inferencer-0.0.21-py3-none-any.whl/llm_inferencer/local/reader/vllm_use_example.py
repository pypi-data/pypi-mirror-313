from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
llm = LLM(
    model= model_path ,
    trust_remote_code=True,
    dtype='float16',
    gpu_memory_utilization=0.9,
    seed = 42,
    max_model_len=4096
)
sampling_params = SamplingParams( temperature=0,
                                top_p=1, 
                                use_beam_search=True,
                                best_of=2,
                                stop=["<|im_end|>", "<|endoftext|>", "<|im_start|>"]
                                )

query = "你是谁?"
messages = [
                 {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
outputs = llm.generate([text ],sampling_params)
generated_text = outputs[0].outputs[0].text
print(generated_text)




from llama_index.llms.vllm import Vllm          # vllm 0.4.0+cu118
llm = Vllm(
    model = model_path,
    trust_remote_code=True,
    dtype='float16',
    max_new_tokens=200,
    temperature=0,
    vllm_kwargs={ 
        "gpu_memory_utilization": 0.9 ,
        "swap_space": 1,
        "max_model_len": 4096,
        "seed": 42},
)

respones = llm.complete( ["你好", "今天天气怎么样"] ).text