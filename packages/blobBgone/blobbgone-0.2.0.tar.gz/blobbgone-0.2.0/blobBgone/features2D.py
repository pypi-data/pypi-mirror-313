from blobBgone.features import features
from dataclasses import dataclass

@dataclass
class features2D(features):
    ## Distances
    MAX_DIST: float
    
    ## Areas
    CV_AREA: float

    ## Ratios
    SPHE: float
    ELLI: float
    CV_DENSITY: float