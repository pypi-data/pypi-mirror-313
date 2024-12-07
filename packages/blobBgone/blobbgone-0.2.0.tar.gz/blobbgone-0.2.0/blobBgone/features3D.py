from blobBgone.features import features
from dataclasses import dataclass

@dataclass
class features3D(features):
    ## Distances
    MAX_DIST: float
    
    ## Volumes
    CV_VOL: float
    
    ## Ratios
    ELLI: float
    SPHE: float
    CV_DENSITY: float