from wayne_utils import load_data, save_data, get_ROOT_PATH
import os

_ROOT_PATH = get_ROOT_PATH( 1, __file__)

class Register():
    def __init__(self):
        self.model_list_path = os.path.join( _ROOT_PATH, "model_list.yaml")
        self.model_list_empty = {
            "local": {},
            "remote": {},
            "engine_config":{
                "vllm":{
                    "temperature": 0,
                    "top_p": 1,
                    "gpu_memory_utilization": 0.7,
                    "seed": 32,
                    "use_beam_search": True,
                    "best_of": 2,
                }
            }
            
        }
    
    def empty_list( self ):
        "Copy empty list to model_list"
        save_data( self.model_list_empty, self.model_list_path )
    
    def list_models( self ):
        "List all register"
        if not os.path.exists( self.model_list_path ):
            self.empty_list( )
        model_list = load_data( self.model_list_path, "yaml")
        print(model_list)

    def add_local_model( self, model_name, model_path):
        "Add a model path to dict"
        model_list = load_data( self.model_list_path, "yaml")
        if model_name in model_list["local"]:
            raise Exception( f"""Model name {model_name} already exist, path {model_list["local"][model_name]}.
                  If you want to modify the path, please use the function 'modify_local_model.'
            """)
        else:
            if not os.path.exists( model_path ):
                raise Exception( f"Path {model_path} not exists, please check your input.")
            model_list["local"][model_name] = model_path
            save_data( model_list, self.model_list_path )

    def modify_local_model( self, model_name, model_path):
        "Modify a model path to dict"
        model_list = load_data( self.model_list_path, "yaml")
        if not os.path.exists( model_path ):
            raise Exception( f"Path {model_path} not exists, please check your input.")
        if model_name not in model_list["local"]:
            print( f"""Model name {model_name} not exist, now add it to dict.'
            """)
        model_list["local"][model_name] = model_path
        save_data( model_list, self.model_list_path )
    
    def add_remote_model( self, api_name, api_key, base_url, model_list = None ):
        "Add a api config to dict"
        config = load_data( self.model_list_path, "yaml")
        if api_name in config["remote"]:
            raise Exception( f"""API name {api_name} already exist, conifg {config["remote"][api_name]}.
                  If you want to modify the path, please use the function 'modify_local_model.'
            """)
        else:
            config["remote"][api_name] = {
                "api_key": api_key,
                "base_url": base_url,
                "model_list": model_list if model_list else []
            }
            save_data( config, self.model_list_path )

    def modify_remote_model( self, api_name, api_key = None, 
                            replace_model_list = None, add_model_list = None, remove_model_list = None):
        "Modify a api config to dict"
        model_list = load_data( self.model_list_path, "yaml")
        if api_name not in model_list["remote"]:
            raise Exception( f"""Api name {api_name} not exist, please add it to dict.'
            """)
        if api_key != None:
            model_list["remote"]["api_key"] = api_key
        if replace_model_list != None:
            model_list["remote"]["model_list"] = replace_model_list
        else:
            model_list = model_list["remote"]["model_list"]
            if add_model_list != None:
                model_list.extend( add_model_list )
            if remove_model_list != None:
                for model in remove_model_list:
                    model_list.remove( model )
            model_list["remote"]["model_list"] = model_list
        save_data( model_list, self.model_list_path )

if __name__=="__main__":
    reg = Register()
    reg.empty_list()
            
