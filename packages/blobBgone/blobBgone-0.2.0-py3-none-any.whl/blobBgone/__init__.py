import os
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from blobBgone.featureHandler import featureHandler
from blobBgone.features2D import features2D
from blobBgone.features3D import features3D
from blobBgone.eval import eval

# Set the number of threads to 1 
# this is a hacky fix for a currently known issue with the 
# KMeans algorithm implemented in scikit-learn.
# This will be removed as soon as the issue is resolved.
os.environ['OMP_NUM_THREADS'] = '1'

# dynamic tqdm
from IPython import get_ipython
try:
    ipy_str = str(type(get_ipython()))
    if 'zmqshell' in ipy_str:
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm
except:
    from tqdm import tqdm

## Class definition of BlobBGone ##

class blobBgone(object):
    __verbose:bool
    __regularization:str
    __custom_weights:dict
    
    __task_list:list
    __blob_IDs:list
    __free_IDs:list
    __blobs:list
    __free:list
    
    ## Initialization ##
    def __init__(self, task_list:list, 
                 verbose:bool = True) -> None:
        self.__verbose = verbose
        self.__task_list = task_list
        self.__regularization = "standardize"
        
        self.__custom_weights = None
        self.__blob_IDs = None
        self.__free_IDs = None
        self.__blobs = None
        self.__free = None
        
        self.__post_init__()
    
    ## Execute after initialization ##
    def __post_init__(self):
        self.__sort_by_ID()
        self.__spinup_weights(dimension = self.__task_list[0].dimension)
        
    ## Properties ##
    @property
    def verbose(self):
        return self.__verbose
    @verbose.setter
    def verbose(self, verbose:bool):
        self.__verbose = verbose
        return print("Verbosity has been set to {}.".format(verbose))
    
    @property
    def regularization(self):
        return self.__regularization
    @regularization.setter
    def regularization(self, regularization:str):
        try:
            assert regularization in ['standardize', 'normalize', 'force_raw']
        except AssertionError as error:
            print(error)
            print("The regularization method must be in ['standardize', 'normalize', 'force_raw'].")
            
        self.__regularization = regularization
        return print("Regularization method has been set to {}".format(regularization))
    
    @property
    def task_list(self):
        return self.__task_list
    @task_list.setter
    def task_list(self, task_list:list):
        self.__task_list = task_list
        return print("Task list has been updated.")
    
    @property
    def blobs(self):
        try:
            assert self.__blobs is not None, "Blob cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")
        return self.__blobs
    @blobs.setter
    def blobs(self, *args, **kwargs):
        return print("blobs attribute is read-only.")
    
    @property
    def free(self):
        try:
            assert self.__free is not None, "Free cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")
        return self.__free
    @free.setter
    def free(self, *args, **kwargs):
        return print("free attribute is read-only.")
    
    @property
    def blob_IDs(self):
        try:
            assert self.__blob_IDs is not None, "Blob cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")
        return self.__blob_IDs
    @blob_IDs.setter
    def blob_IDs(self, *args, **kwargs):
        return print("blob_IDs attribute is read-only.")
    
    @property
    def free_IDs(self):
        try:
            assert self.__free_IDs is not None, "Free cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")
        return self.__free_IDs
    @free_IDs.setter
    def free_IDs(self, *args, **kwargs):
        return print("free_IDs attribute is read-only.")
        
    ## Class Methods ##
    @classmethod
    def from_npy(cls, path:str = None, key:str = "*",
                 verbose:bool = True) -> None:
        
        files = featureHandler.grab_files(path = path, key = key, dtype=".npy")
        if verbose:
            print(f"Found {len(files)} files in the '{files[0].split(os.sep)[-2]}' directory.")
            
        task_list = [featureHandler.from_npy(path = file, verbose = False) for file in files]
        if verbose:
            print(f"{len(task_list)} tasks have been created.")
        
        return cls(task_list = task_list, verbose = verbose)
    
    @classmethod
    def from_pointCloud(cls, pointClouds:dict, 
                        verbose:bool = True) -> None:
        
        task_list = [featureHandler.from_pointCloud(pointCloud = value, id = key,  verbose = False) for key,value in pointClouds.items()]
        if verbose:
            print(f"{len(task_list)} tasks have been created.")
        
        return cls(task_list = task_list, verbose = verbose)
    
    ## Main Function ##
    def run(self):

        # Extracting Features
        features = self.__extract_features()
        
        # Regularize the features
        features = self.__regularize_features(features=features)
 
        # Grab weights
        features = self.__apply_custom_weights(features)

        # Cluster the features
        if self.__verbose:
            print("\nClustering...")
            
        clustering_FH  = KMeans(
            n_clusters = 2,
            init = 'k-means++',
            n_init = 'auto',
            max_iter = 300,
            verbose = 0,
            random_state = None,
            )
        fit_predict_FH = clustering_FH.fit_predict(features)
        
        cluster_1 = [self.task_list[i] for i in range(len(self.task_list)) if fit_predict_FH[i] == 0]
        cluster_2 = [self.task_list[i] for i in range(len(self.task_list)) if fit_predict_FH[i] == 1]
        comb = [cluster_1, cluster_2]
        
        ## Evaluate Blobbness ##
        if self.__verbose:
            print("\nBlob-score is being calculated...\n")
        c1_blobbness = np.mean([task.features.SPHE/task.features.MAX_DIST for task in cluster_1])
        c2_blobbness = np.mean([task.features.SPHE/task.features.MAX_DIST for task in cluster_2])
        
        if self.__verbose:
            print("Cluster 1 Blob-score: {:.2f}".format(c1_blobbness))
            print("Cluster 2 Blob-score: {:.2f}".format(c2_blobbness))
            print("Blob-score ratio: 1 : {:.2f}".format(max([c1_blobbness, c2_blobbness])/min([c1_blobbness, c2_blobbness])))
            print(
                "Silhouette Coefficient: %0.3f"
                % metrics.silhouette_score(features, fit_predict_FH, metric="euclidean")
            )
            
            print("\nCluster {} has been estimated to be the blob cluster.".format(np.argmax([c1_blobbness, c2_blobbness])+1))

        self.__blobs = [task for task in comb[np.argmax([c1_blobbness, c2_blobbness])]]
        self.__free =  [task for task in comb[np.argmin([c1_blobbness, c2_blobbness])]]
        self.__blob_IDs = [task.ID for task in comb[np.argmax([c1_blobbness, c2_blobbness])]]
        self.__free_IDs =  [task.ID for task in comb[np.argmin([c1_blobbness, c2_blobbness])]]
        if self.__verbose:
            print("\nBlob-B-Gone has finished running.\n\nGet the results with the 'blobs' and 'free' attributes\nor via the 'blob_IDs' and 'free_IDs' attributes.")
        return
    
    ## Evaluation ##
    def plot_PCA(self, include_eigenvectors:bool = True, absolute:bool = False):
        combined_features, labels = self.__construct_labels_silent()
        return eval.plot_PCA(features = self.__apply_custom_weights_silent(self.__regularize_features_silent(combined_features)), 
                             labels = labels, 
                             feature_keywords = list(self.__task_list[0].features.__dict__.keys()), 
                             include_eigenvectors=include_eigenvectors,
                             absolute = absolute)
    
    ## Advanced User Only ##
    @property
    def custom_weights(self):
        return self.__custom_weights
    @custom_weights.setter
    def custom_weights(self, custom_weights:dict):
        try:
            assert isinstance(custom_weights, dict), "custom_weights must be a dictionary."
            assert set(custom_weights.keys()) == set(self.__custom_weights.keys()), "custom_weights must have the same keys as the features."
        except AssertionError as error:
            print(error)
            return print("Default weights will be used.")
        self.__custom_weights = custom_weights
    
    ## Helper Functions ##
    def __sort_by_ID(self):
        self.__task_list = sorted(self.__task_list, key=lambda x: x.ID)
        if self.__verbose:
            print("Task list has been sorted by ID.")
        return
    
    def __spinup_weights(self, dimension:int):
        if dimension == 2:
            self.__custom_weights = {key:1 for key in features2D.__annotations__.keys()}
            return
        if dimension == 3:
            self.__custom_weights = {key:1 for key in features3D.__annotations__.keys()}
            return 
        
    def __extract_features(self):
        if self.__verbose:
            print("\nExtracting features...")
        # Extract features
        features = []
        task:featureHandler
        with tqdm(total = len(self.task_list), desc = "Extracting features") as pbar:
            for task in self.task_list:
                task.extract()
                features.append(task.to_array())
                pbar.update(1)
            pbar.close()
        return features
    
    def __regularize_features(self, features:np.ndarray):
        if self.__verbose:
            print("\nRegularizing features...")
        features = featureHandler.regularize_output(features, method = self.__regularization)
        assert np.all(np.isfinite(features)), "NaN values still present in features."
        return features
    
    def __apply_custom_weights(self, features:np.ndarray):
        weights = np.array([self.__custom_weights[feature] for feature in list(self.__task_list[0].features.__dict__.keys())])
        print(weights)
        if np.all(weights == 1):
            if self.__verbose:
                print("\nNo custom weights have been applied.")
            return features
        if self.__verbose:
            print("\nCustom weights have been applied.")
        return features*weights
    
    def __construct_labels(self):
        try:
            assert self.__blobs is not None, "Blob cluster not yet extracted."
            assert self.__free is not None, "Free cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")

        if self.__verbose:
            print("\nCollecting features...")
        combined_features = np.concatenate(([task.to_array() for task in self.__blobs], 
                                            [task.to_array() for task in self.__free]))
        if self.__verbose:
            print("\nConstructing labels...")
        labels = np.concatenate((np.zeros(len(self.__blobs)), np.ones(len(self.__free))))
        return combined_features, labels
    
#%% silent functions
    def __construct_labels_silent(self):
        try:
            assert self.__blobs is not None, "Blob cluster not yet extracted."
            assert self.__free is not None, "Free cluster not yet extracted."
        except AssertionError as error:
            print(error)
            return print("Please call the 'run' method first.")

        combined_features = np.concatenate(([task.to_array() for task in self.__blobs], 
                                            [task.to_array() for task in self.__free]))

        labels = np.concatenate((np.zeros(len(self.__blobs)), np.ones(len(self.__free))))
        return combined_features, labels
    
    def __regularize_features_silent(self, features:np.ndarray):
        features = featureHandler.regularize_output(features, method = self.__regularization)
        assert np.all(np.isfinite(features)), "NaN values still present in features."
        return features
    
    def __apply_custom_weights_silent(self, features:np.ndarray):
        weights = np.array([self.__custom_weights[feature] for feature in list(self.__task_list[0].features.__dict__.keys())])
        if np.all(weights == 1):
            return features
        return features*weights
        
    