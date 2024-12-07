## Imports
import os
import glob
import ntpath
import warnings
import numpy as np

import scipy.spatial as spatial
import matplotlib.pyplot as plt
from functools import cached_property

from blobBgone.features import features
from blobBgone.features2D import features2D
from blobBgone.features3D import features3D

try:
    from blobBgone.utils import pyDialogue as pD
except:
    warnings.warn("pyDialogue could not be imported. This could be due to a conflict with tkinter. Falling back to manual mode.")

class featureHandler():
    def __init__(self, pointCloud:np.ndarray, id:int, verbose:bool = True) -> None:
        
        ## Meta Setup
        self.__verbose:bool = verbose
        self.__id:int = id
        self.__dimension:int = pointCloud.shape[1]
        
        self.__pointCloud:np.ndarray = pointCloud
        if self.__verbose:
            print(f"Dimension has been set to {self.__dimension}")
                    
        self.__features:features = None
        
        
    # Meta properties
    @property
    def verbose(self):
        return self.__verbose
    @verbose.setter
    def verbose(self, verbosity:bool):
        self.__verbose = verbosity
        if verbosity:
            print(f"Verbose mode set to {verbosity}")
    
    @property
    def ID(self):
        return self.__id
    @ID.setter
    def ID(self, new_id:int):
        self.__id = new_id
    
    @property
    def dimension(self):
        return self.__dimension
    @dimension.setter
    def dimension(self, *args):
        raise AttributeError("Dimension is a read-only property")
    
    ## Quantitative properties
    @property
    def pointCloud(self):
        return self.__pointCloud
    @pointCloud.setter
    def pointCloud(self, pointCloud:np.ndarray):
        try:
            assert isinstance(pointCloud, np.ndarray), "pointCloud must be a numpy array"
            if self.__dimension != pointCloud.shape[1]:
                self.__dimension = pointCloud.shape[1]
                if self.__verbose:
                    print(f"Dimension changed to {self.__dimension}")
            
            self.__pointCloud = pointCloud
        except AssertionError as e:
            print(e)
        finally:
            if self.__verbose:
                print("point cloud has been updated.")
                
    @property
    def features(self):
        return self.__features
    @features.setter
    def features(self, features:features):
        try:
            assert isinstance(features, features), "features must be an instance of features"
            self.__features = features
        except AssertionError as e:
            print(e)
        finally:
            if self.__verbose:
                print("features have been updated.")
                                
    ## Classmethods
    # Please note, that we currently only support .npy files as input as tey are commonly found and other methods can be implemented rapidly when needed.
    @classmethod
    def from_npy(cls, path:str = None, verbose:bool = True):
        def __path_leaf(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)
        
        if path == None:
            try:
                path = pD.askFILE()
            except:
                path = input("Please enter the path to the point cloud: ")
                
        assert os.path.exists(path), "Path does not exist"
        assert path.endswith(".npy"), "Path must be a .npy file"
        
        pointCloud = np.load(path)
        
        try:
            assert pointCloud.shape[1] in [2,3], "pointCloud must be two or three dimensional"
            
            if verbose:
                print(f"Dimension has been set to {pointCloud.shape[1]}")
            
            return cls(pointCloud = pointCloud, 
                   id = int(__path_leaf(path).split('-',1)[1][:-4]),
                   verbose = verbose)
        except:
            raise Exception("pointCloud must be of shape (n,2) or (n,3)")
        
    @classmethod
    def from_pointCloud(cls, pointCloud:np.ndarray, id:int, verbose:bool = True):
        try:
            assert isinstance(pointCloud, np.ndarray), "Point Cloud must be a numpy array"
            assert pointCloud.shape[1] in [2,3], "pointCloud must be two or three dimensional"
            
            if verbose:
                print(f"Dimension has been set to {pointCloud.shape[1]}")
            
            return cls(pointCloud = pointCloud, 
                   id = id,
                   verbose = verbose)
        except AssertionError as e:
            print(e)
        except:
            raise Exception("pointCloud must be of shape (n,2) or (n,3)")

    ## Staticmethods
    @staticmethod
    def grab_files(path:str = None, key:str = "*", dtype:str = ".npy"):
        if path == None:
            try:
                path = pD.askDIR()
            except:
                path = input("Please enter the path to the point clouds: ")
                
        assert os.path.exists(path), "Path does not exist"
        assert os.path.isdir(path), "Path must be a directory"
        
        return np.array(glob.glob(os.path.join(path, f"{key}{dtype}")))
    
    @staticmethod
    def regularize_output(features:list, method:str)->np.ndarray:
        features = np.vstack(features).astype(np.float32)

        def __standardize_features(stand_feature:np.ndarray)->np.ndarray:
            mean = np.mean(stand_feature, axis=0)
            std = np.std(stand_feature, axis=0)
            zero_std_mask = std == 0
            if zero_std_mask.any():
                std[zero_std_mask] = 1.0
            return (stand_feature - mean) / std
        
        def __normalize_features(norm_features:np.ndarray)->np.ndarray:
            max = np.max(norm_features, axis=0)
            zero_max_mask = max == 0
            if zero_max_mask.any():
                max[zero_max_mask] = 1.0
            return norm_features / max
        
        ## Clean up NaN values ##
        # should you encounter NaN values, you can either substitute them with a value of your choice or cut them out.
        # However, you should first check where they come from. You might have to fix some bugs.
        def __clean_nan(features:np.ndarray, nan=0.0)->np.ndarray:
            return np.nan_to_num(features, nan=0.0)
        def __check_nan(features:np.ndarray)->np.ndarray:
            if np.isnan(np.sum(features)):
                print("Warning: NaN values detected. Replacing with 0.0")
                return __clean_nan(features)
            return features
        
        if method == "standardize":
            return __check_nan(__standardize_features(__normalize_features(features)))
        
        elif method == "normalize":
            return __check_nan(__normalize_features(features))
    
        elif method == 'force_raw':
            print("Warning: Raw features are not recommended for clustering. Please use 'normalize' or 'standardize' instead.")
            return __check_nan(features)
        else:
            return print("Error: Method not recognized. Please use one of the following: 'standardize' or 'force_raw'")
    
    ## Visualisation
    def overview(self):
        plt.style.use("dark_background")
        
        font = {'family' : 'DejaVu Sans',
                'weight' : 'normal',
                'size'   : 12}

        plt.rc('font', **font)
        
        if self.__dimension == 2:
            return self.__visualize2D()
        elif self.__dimension == 3:
            return self.__visualize3D()
    
    def __visualize2D(self):
        fig, axs = plt.subplots(1,1, figsize = (5,5), dpi = 100)
        plt.title(f"Point Cloud #{self.__id}", fontsize = 10)
        axs.scatter(*zip(*self.__pointCloud), s = 0.5, c = "deeppink")
        axs.plot(*zip(*np.vstack([*self.__pointCloud[spatial.ConvexHull(self.__pointCloud).vertices], self.__pointCloud[spatial.ConvexHull(self.__pointCloud).vertices][0]])), '->', label = "Convex Hull", c = "dodgerblue")
        axs.scatter(*np.mean(self.__pointCloud, axis = 0), c = "lawngreen", s = 5, label = 'Center of Mass')
        
        axs.set_aspect("equal")
        axs.set_xlabel("x [m]")
        axs.set_ylabel("y [m]")
        
        axs.legend(loc = 'upper right', fontsize = 8, fancybox = True, framealpha = 0.5)
        plt.show()
    
    def __visualize3D(self):
        fig, axs = plt.subplots(1,1, figsize = (5,5), dpi = 100, subplot_kw={'projection': '3d'})
        plt.title(f"Point Cloud #{self.__id}", fontsize = 10)
        axs.scatter(*zip(*self.__pointCloud), s = 0.5, c = "deeppink")
        axs.scatter(*zip(*np.vstack([*self.__pointCloud[spatial.ConvexHull(self.__pointCloud).vertices], self.__pointCloud[spatial.ConvexHull(self.__pointCloud).vertices][0]])), '->', label = "Convex Hull", c = "dodgerblue")
        axs.scatter(*np.mean(self.__pointCloud, axis = 0), c = "lawngreen", s = 5, label = 'Center of Mass')
        
        axs.set_xlabel("x [m]")
        axs.set_ylabel("y [m]")
        axs.set_zlabel("z [m]")
        
        axs.legend(loc = 'upper right', fontsize = 8, fancybox = True, framealpha = 0.5)
        plt.show()
    
    # Feature Extraction Main
    def extract(self):
        if self.__dimension == 2:
            self.__extract2D()
        elif self.__dimension == 3:
            self.__extract3D()
    
    def __extract2D(self):
        try:
            assert self.__dimension == 2, "pointCloud must be two-dimensional for 2D feature extraction"
            self.__features = features2D(
                MAX_DIST = self.get_MAX_DIST,
                CV_AREA = self.get_CV_AREA,
                ELLI = self.get_ELLI,
                SPHE = self.get_SPHE,
                CV_DENSITY = self.get_CV_DENSITY,
                )
        except:
            warnings.warn("pointCloud must be 2D. No features were generated.", UserWarning)
        finally: 
            if self.__verbose:
                if self.__features != None:
                    print("The following 2D features have been extracted:\n", self.__features)
                else:
                    print("No features were extracted.")
        
    def __extract3D(self):
        try:
            assert self.__dimension == 3, "pointCloud must be three-dimensional for 3D feature extraction"
            self.__features = features3D(
                MAX_DIST = self.get_MAX_DIST,
                CV_VOL = self.get_CV_VOL,
                ELLI = self.get_ELLI,
                SPHE = self.get_SPHE,
                CV_DENSITY = self.get_CV_DENSITY,
                )
        except:
            warnings.warn("pointCloud must be 3D. No features were generated.", UserWarning)
        finally: 
            if self.__verbose:
                if self.__features != None:
                    print("The following 3D features have been extracted:\n", self.__features)
                else:
                    print("No features were extracted.")
    
    # Feature Extractiors
    @cached_property
    def __get_average_distance_2_center_in_PC(self)-> float:
        CenterOfMass = np.mean(self.__pointCloud, axis=0)
        return np.mean(np.linalg.norm(self.__pointCloud-CenterOfMass, axis=1))
    
    @cached_property
    def get_MAX_DIST(self)->float:
        """Burte Force

        Args:
            points (np.ndarray): Point cloud (x,y,z) of a convex hull

        Returns:
            ids: ids of points with largest distance
            max_dist: maximum distance of set
        """
        id_x:int
        id_y:int
        
        div = [self.__pointCloud-self.__pointCloud[i] for i in range(self.__pointCloud.shape[0])]
        div = [(np.linalg.norm(div[i],axis=1) ) for i in range(div.__len__())]
        id_y = np.argmax([np.max(div[i]) for i in range(div.__len__())])
        id_x = np.argmax(div[id_y])
        
        return div[id_y][id_x]
    
    @cached_property
    def get_CV_VOL(self)->float:
        assert self.__dimension == 3, "Convex Hull Volume is only defined for 3D point clouds"
        return spatial.ConvexHull(self.__pointCloud).volume #Volume of the convex hull when input dimension > 2.
    
    @cached_property
    def get_CV_AREA(self)->float:
        assert self.__dimension == 2, "Convex Hull Area is only defined for 2D point clouds"
        return spatial.ConvexHull(self.__pointCloud).volume #When input points are 2-dimensional, this is the area of the convex hull.

    @cached_property
    def get_SPHE(self)->float: # sphericality mean sphere/vol
        if self.__dimension == 3:
            return self.get_CV_VOL/self.__get_AVR_SPHERE_VOL()
        elif self.__dimension == 2:
            return self.get_CV_AREA/self.__get_AVR_CIRC_AREA()
        
    @cached_property
    def get_ELLI(self)->float: # ellipticality ellip (max, mean dist)/vol
        if self.__dimension == 3:
            return self.get_CV_VOL/self.__get_ellipse_volume()
        elif self.__dimension == 2:
            return self.get_CV_AREA/self.__get_ellipse_area()

    @cached_property
    def get_CV_DENSITY(self)->float: # convex density
        if self.__dimension == 3:
            return self.__pointCloud.shape[0]/self.get_CV_VOL
        elif self.__dimension == 2:
            return self.__pointCloud.shape[0]/self.get_CV_AREA
        
        
    ## Feature Extraction Helpers
    def __get_AVR_SPHERE_VOL(self)->float:
        avr = self.__get_average_distance_2_center_in_PC
        return  4/3 * np.pi * np.power(avr,3)
        
    def __get_AVR_CIRC_AREA(self)->float:
        avr = self.__get_average_distance_2_center_in_PC
        return np.pi * np.power(avr,2)
    
    def __get_ellipse_area(self):
        return np.pi * self.get_MAX_DIST * self.__get_average_distance_2_center_in_PC
    
    def __get_ellipse_volume(self):
        return 4/3 * np.pi * self.get_MAX_DIST * np.power(self.__get_average_distance_2_center_in_PC, 2)
    
    ## MISC & Magic Methods
    def to_array(self):
        return self.__features.to_array()
    
    def to_dict(self):
        return self.__features.to_dict()
    
    def __repr__(self) -> str:
        print(f"Feature Handler (ID = {self.ID}, dimension = {self.dimension}, length = {self.pointCloud.shape[0]})")
        try:
            print(f"\nFeatures in place.\n - {self.__features}")
        except:
            print("\nFeatures not yet set up. Please, call featureHandler.extract() to generate features.")
        finally:
            return " \n      -------------------------------------- \n\n - To get an array of features call featureHandler.to_array()\n - To get a dict of features call featureHandler.to_dict()"