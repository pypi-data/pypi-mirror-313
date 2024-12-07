from pprint import pformat
import numpy as np

from typing import List, Any


class features():
    
    def __unpack(self, 
                 data:List[Any]
                 )->List[np.ndarray]:
        
        col = []
        for feature in data:
            if isinstance(feature, np.ndarray):
                col+=[*feature]
            else:
                col.append(feature)
        return col
    
    def to_array(self):
        return np.array(self.__unpack(self.__dict__.values()))
    
    def to_dict(self):
        return {**self.__dict__}

    def __len__(self):
        i = len(self.__annotations__)
        for value in self.__dict__.values():
            if isinstance(value, np.ndarray):
                if np.all(value) != None:
                    continue
            else:
                if value != None:
                    continue
            i -= 1
        return i
    
    def __getitem__(self,key:str):
        return self.__dict__[key]
    
    def __repr__(self):
        return pformat(self.__dict__)