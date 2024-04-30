from pathlib import Path 
import pandas as pd 

pathlikeObject = str | Path 

def get_files(path: pathlikeObject) -> pd.DataFrame:
    if isinstance(path, str):
        path = Path(path).resolve() 
    
    if not path.exists(): 
        raise FileNotFoundError()
    
    data = list(map(get_infos, [f for f in path.iterdir()]))
    df = pd.DataFrame(data, columns=['path', 'filename', 'filetype', 'size'])
    df.set_index('path', inplace=True)
    
    return df


def get_infos(path: Path) -> list: 
    v_files = [f for f in path.iterdir() if f.suffix.lower() in ['.ser', '.avi']]
    if len(v_files) != 1: 
        return []
    v_file = v_files[0]
    str_path = str(v_file)
    filename = v_file.name 
    filetype = v_file.suffix
    size = round(v_file.stat().st_size /1e9, 2)
    return [str_path, filename, filetype, size]

if __name__ == '__main__': 
    path = Path(__file__).parents[1].joinpath('temp')
    df = get_files(path)
    print(df.head())