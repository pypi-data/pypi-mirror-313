## Imports
import numpy as np
import seaborn as sns
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from blobBgone.utils import Helper
import matplotlib.patches as mpatches
from sklearn.decomposition import PCA

# typehinting
from typing import List, Tuple

## Collection of small quick evaluation methods
class eval(object):
    @staticmethod
    def plot_feature_correlation_heatmaps(blob_features:np.ndarray, 
                                          track_features:np.ndarray, 
                                          feature_keywords:List[str]
                                          )->Tuple[plt.Figure, plt.Axes]:
        
        """Plot the correlation matrices of the blob and track features as heatmaps.

        Args:
            blob_features (np.ndarray): Row-stacked blob features. Shape: (n_blobs, n_features)
            track_features (np.ndarray): Row-stacked track features. Shape: (n_tracks, n_features)
            feature_keywords (list): Sequence of included features. The length has to match the number of features.

        Returns:
            plt.figure, plt.ax: Figure and axis objects of the two heatmaps.
        """
        
        assert blob_features.shape[1] == track_features.shape[1] == len(feature_keywords), 'Number of features does not match the number of feature keywords.'
        
        ## Set up the figure
        fig, axs = plt.subplots(1,2, figsize = (28,10), dpi = 300)
        axs[0].set_title('Blob Feature Correlation Matrix', fontweight = 'bold', fontsize = 18)
        axs[1].set_title('Track Feature Correlation Matrix', fontweight = 'bold', fontsize = 18)

        ## Calculate the correlation matrices
        corr_blob = DataFrame(blob_features, columns = feature_keywords).corr()
        corr_track = DataFrame(track_features, columns = feature_keywords).corr()

        ## Find the min and max values for the colorbar
        v_min = min(*corr_blob.min(), *corr_track.min())
        v_max = max(*corr_blob.max(), *corr_track.max())

        ## Plot the correlation matrices as heatmaps
        hm1 = sns.heatmap(corr_blob, 
                    cmap="RdBu", annot=True, ax = axs[0], linewidths=0.5, linecolor='black', vmin=v_min, vmax=v_max, annot_kws={"size": 14, 'weight': 'bold'})
        hm2 = sns.heatmap(corr_track, 
                    cmap="RdBu", annot=True, ax = axs[1], linewidths=0.5, linecolor='black', vmin=v_min, vmax=v_max, annot_kws={"size": 14, 'weight': 'bold'})


        ## Adjust axis fontsize
        for ax in axs:
            for tick_x, tick_y in zip(ax.xaxis.get_major_ticks(), ax.yaxis.get_major_ticks()):
                tick_x.label.set_fontsize(14) 
                tick_y.label.set_fontsize(14)
                tick_x.label.set_fontweight('bold') 
                tick_y.label.set_fontweight('bold') 
                tick_y.label.set_rotation(45)

        ## Adjust Colorbar fontsize
        hm1.cb = hm1.collections[0].colorbar
        for t in hm1.cb.ax.get_yticklabels():
            t.set_fontsize(16)
            t.set_fontweight('bold')

        hm2.cb = hm2.collections[0].colorbar
        for t in hm2.cb.ax.get_yticklabels():
            t.set_fontsize(16)
            t.set_fontweight('bold')
        
        return fig, axs

    @staticmethod
    def plot_feature_correlation_clustermap(features:np.ndarray, 
                                            feature_keywords:List[str], 
                                            title:str = 'Correlation Clustermap'
                                            )->plt.Figure:
        
        """Plot a clustermap of the correlation matrix of the features. This includes a dendrogram to show the clustering of the features.

        Args:
            features (np.ndarray): Row-stacked features. Shape: (n_samples, n_features)
            feature_keywords (list): Sequence of included features. The length has to match the number of features.
            title (str, optional): Title given to the general figure. Defaults to 'Correlation Clustermap'.

        Returns:
            plt.figure: Figure object of the clustermap.
        """
        
        assert features.shape[1] == len(feature_keywords), 'Number of features does not match the number of feature keywords.'
        
        ## Calculate the correlation matrices
        corr_blob = DataFrame(features, columns = feature_keywords).corr()
        
        ## Plot the correlation matrices as heatmaps
        cm1 = sns.clustermap(corr_blob,
                            method = 'complete',
                            cmap   = 'RdBu', 
                            annot  = True, 
                            linewidths=0.75, linecolor='black',
                            dendrogram_ratio=0.15, tree_kws={'linewidth': 5},
                            annot_kws={"size": 16, 'weight': 'bold'})

        cm1.ax_heatmap.set_yticklabels(cm1.ax_heatmap.get_yticklabels(), rotation = -45, fontsize = 16, fontweight = 'bold')
        cm1.ax_heatmap.set_xticklabels(cm1.ax_heatmap.get_xticklabels(), rotation = 0, fontsize = 16, fontweight = 'bold')
            
        cb = cm1.ax_heatmap.collections[0].colorbar
        for t in cb.ax.get_yticklabels():
            t.set_fontsize(16)
            t.set_fontweight('bold')
        
        if title:
            plt.title(title, fontweight = 'bold', fontsize = 18, loc="left", pad=25)
        
        return cm1
            
    @staticmethod
    def plot_feature_distributions(features1:np.ndarray, 
                                   features2:np.ndarray, 
                                   feature_keywords:List, 
                                   title:str = 'Feature Distribution'
                                   )->Tuple[plt.Figure, plt.Axes]:
        
        """Plot a comparison of the feature distributions of two feature sets.

        Args:
            features1 (np.ndarray): Feature set 1. Shape: (n_samples, n_features)
            features2 (np.ndarray): Feature set 2. Shape: (n_samples, n_features)
            feature_keywords (list): Sequence of included features. The length has to match the number of features.
            title (str, optional): Title given to the general figure. Defaults to 'Feature Distribution'.

        Returns:
            plt.figure, plt.ax: The figure and axis objects of the histograms.
        """
        
        assert features1.shape[1] == features2.shape[1] == len(feature_keywords), 'Number of features does not match the number of feature keywords.'
        
        plt.style.use('default')
        font = {'family' : 'DejaVu Sans',
                'weight' : 'bold',
                'size'   : 14}
        plt.rc('font', **font)

        # blobs
        fig, axs = plt.subplots(1, 5, figsize = (25, 5), dpi = 150)

        for i, desc in enumerate(feature_keywords):
            axs[i].hist(features1[:,i], alpha = 0.5, bins = 25, label = 'Blob', color = 'blue')
            axs[i].hist(features2[:,i], alpha = 0.5, bins = 25, label = 'Track', color = 'red')
            axs[i].set_title(desc, fontsize = 14, fontweight = 'bold')
            axs[i].legend()

        fig.suptitle(title, fontsize = 16, fontweight = 'bold')
        axs[0].set_ylabel('Counts [a.u.]', fontsize = 14, fontweight = 'bold')
        
        return fig, axs
        
    @staticmethod
    def plot_PCA(features:np.ndarray, 
                 labels:np.ndarray, 
                 feature_keywords:List, 
                 include_eigenvectors:bool = False, 
                 absolute:bool = False
                 )->Tuple[plt.Figure, plt.Axes]:
        
        """Plot the PCA of the features and optionally, the respective Eigenvectors.

        Args:
            features (np.ndarray): Row-stacked features. Shape: (n_samples, n_features)
            feature_keywords (list): Sequence of included features. The length has to match the number of features.
            include_eigenvectors (bool, optional): Whether to include the Eigenvectors. Defaults to False.
            absolute (bool, optional): Whether to plot the absolute values of the Eigenvectors. Defaults to False.

        Returns:
            plt.figure, plt.ax: The figure and axis objects of the PCA plot.
        """
        
        assert features.shape[1] == len(feature_keywords), 'Number of features does not match the number of feature keywords.'

        ## Formatting ##
        plt.style.use('default')
        font = {'family' : 'DejaVu Sans',
                'weight' : 'bold',
                'size'   : 10}
        plt.rc('font', **font)
        
        def _calculate_PCA_eigenvectors(pca:PCA, 
                                        absolute:bool = True
                                        )->Tuple[np.ndarray, np.ndarray]:
            
            ## A Function to calculate the eigenvectors of the PCA for a list of features and return both eigenvectors and explained variance ratios
            
            pca.fit_transform(features)

            if absolute:
                return abs(pca.components_), pca.explained_variance_ratio_.round(2)
            else:
                return pca.components_, pca.explained_variance_ratio_.round(2)
            
        def _plot_PCA_eigenvectors(pca:PCA, 
                                   feature_keywords:List[str], 
                                   absolute:bool = True, 
                                   ax = None
                                   )->Tuple[plt.Figure, plt.Axes]:
            
            PCA_components, PCA_ratios = _calculate_PCA_eigenvectors(pca=pca, absolute = absolute)
            PCA_components_dict = {'PCA_comp':(PCA_components, PCA_ratios)}

            temp_df = DataFrame.from_dict(PCA_components_dict['PCA_comp'][0])
            temp_df.columns = feature_keywords
            temp_df.index = [f"PC{i+1} - EVR: {PCA_components_dict['PCA_comp'][1][i]:.2f}" for i in range(2)]
            temp_df = temp_df.T
            
            temp_df.T.plot(kind = 'bar', ylim = (-1,1), ax=ax)
            
            if absolute:
                ax.set_ylim(0,1)   
                plt.legend(loc = 'upper left', fontsize = 10, ncols = 2)  
            else:
                plt.legend(loc = 'lower right', fontsize = 10, ncols = 2)  
                plt.hlines(0,-1,5, color = 'k', linestyle = '--')

            plt.setp(ax.get_xticklabels(), rotation=0) 

        pca = PCA(n_components=2)
        trans= pca.fit_transform(features)
        
        cluster_1_mean = np.array([np.mean(trans[labels == 0], axis = 0)[0], np.mean(trans[labels == 0], axis = 0)[1]])
        cluster_2_mean = np.array([np.mean(trans[labels == 1], axis = 0)[0], np.mean(trans[labels == 1], axis = 0)[1]])
        P1,P2 = Helper.generate_perpendicular_vector(cluster_1_mean, cluster_2_mean, scale = 1.5, direction = 'center')
        if include_eigenvectors:
            fig, axs = plt.subplots(1,2, figsize=(12,5), dpi = 100)
            axs[1].set_title('Eigenvectors for\nPCA 1&2', fontsize = 14, fontweight = 'bold') 
            if absolute:
                axs[1].set_title('Absolute Eigenvectors for\nPCA 1&2', fontsize = 14, fontweight = 'bold')
            _plot_PCA_eigenvectors( pca=pca,
                                    feature_keywords=feature_keywords, 
                                    absolute=absolute, 
                                    ax = axs[1]) 
        else:
            fig, axs = plt.subplots(1,1, figsize=(6,5), dpi = 150)
            axs = [axs]
        axs[0].scatter(trans[:,0][labels == 0], trans[:,1][labels == 0], c = 'blue', s = 14)
        axs[0].scatter(trans[:,0][labels == 1], trans[:,1][labels == 1], c = 'red', s = 14)
        axs[0].scatter(cluster_1_mean[0], cluster_1_mean[1], c = 'black', s = 350, marker = '2', label = 'Center of Mass')
        axs[0].scatter(cluster_2_mean[0], cluster_2_mean[1], c = 'black', s = 350, marker = '2')
        axs[0].plot([cluster_1_mean[0], cluster_2_mean[0]], [cluster_1_mean[1], cluster_2_mean[1]], '--', c = 'black', linewidth = 1.25)
        axs[0].plot([P1.x, P2.x], [P1.y,P2.y], '-', c = 'magenta', linewidth = 2)
        axs[0].scatter([P1.x], [P1.y], c = 'magenta', s = 75, marker = 'v')
        axs[0].scatter([P2.x], [P2.y], c = 'magenta', s = 75, marker = '^')

        axs[0].set_xlabel('PC1 [a.u.]', fontsize = 14, fontweight = 'bold')
        axs[0].set_ylabel('PC2 [a.u.]', fontsize = 14, fontweight = 'bold')
        axs[0].set_title('Feature PCA', fontsize = 14, fontweight = 'bold')

        red_patch = mpatches.Patch(color='red', label='Freely Diffusing Markers')
        blue_patch = mpatches.Patch(color='blue', label='Blob Markers')
        Division = mlines.Line2D([P1.x, P2.x], [P1.y,P2.y],  linestyle = '-',c = 'magenta', label = 'Cluster Division')
        CoM =  axs[0].scatter(cluster_1_mean[0], cluster_1_mean[1], c = 'black', s = 250, marker = '2', label = 'Center of Mass')

        axs[0].legend(handles=[red_patch, blue_patch, Division, CoM], fontsize = 9, loc = 'upper left', ncol= 2)
              
        return fig, axs