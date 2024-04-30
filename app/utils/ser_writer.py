from pathlib import Path 

class Writer: 
    def __init__(self, buffer):
        self.buffer = buffer 
        
    def write(self, filename: str | Path, overwrite=False): 
        
        if isinstance(filename, str): 
            filename = Path(filename)
        
        if not filename.parent.exists(): 
            raise FileNotFoundError() 
        
        if filename.exists(): 
            if not overwrite: 
                raise FileExistsError() 
            
        with filename.open('wb') as fp: 
            fp.write(self.buffer)
            