'''
Visualization function
'''

import random
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.cluster import KMeans


class MetricsPlot():
    """Class to compare metrics for different value parameter"""

    def __init__(self, data, start_param, stop_param, step_param):
        """
        Parameters
        ----------
        data: pd.Dataframe
            Data to plot
        start_param : int
            Start number dynamic parameter
        stop_param : int
            Stop number dynamic parameter
        step_param : int
            Step number dynamic parameter
        silhouette_scores : list (default)
            Default list for metrics
        calinski_harabasz_scores : list (default)
            Default list for metrics
        davies_bouldin_scores : list (default)
            Default list for metrics
        """

        self.silhouette_scores = []
        self.calinski_harabasz_scores = []
        self.davies_bouldin_scores = []
        self.start_param = start_param
        self.stop_param = stop_param
        self.step_param = step_param
        self.data = data

    def model(self, name_model, params):
        return name_model(**params)

    def calculate_metrics(
            self,
            name_model,
            name_dynamic_param,
            name_const_param=None,
            value_const_param = None
            ):
        """Calculate clustering and add results to list of metrics

        Parameters
        ----------
        name_model : 
            This parameter doesn't have to be string. 
            For example it have to be like HDBSCAN not 'HDBSCAN'.
        name_dynamic_param: str
            Name of dynamic parameter
        
        WARNING: The following arguments must be specified at once
        name_const_param: str, optional
            Name of constant parameter
        value_const_param: int, optional
            Value of constant parameter
        """

        self.name_dynamic = name_dynamic_param
        for dynamic_param in range(self.start_param, self.stop_param, self.step_param):
            if name_const_param:
                params = {name_dynamic_param:dynamic_param, name_const_param:value_const_param}
            else:
                params = {name_dynamic_param:dynamic_param}

            hdbscan = self.model(name_model, params)
            results = hdbscan.fit_predict(self.data)
            self.silhouette_scores.append(silhouette_score(self.data, results))
            self.calinski_harabasz_scores.append(calinski_harabasz_score(self.data, results))
            self.davies_bouldin_scores.append(davies_bouldin_score(self.data, results))

    def plot(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,5))
        ax1.plot(
            range(self.start_param, self.stop_param, self.step_param),
            self.silhouette_scores,
            'bx-')
        ax1.set_title('Silhouette Score Method')
        ax1.set_xlabel(f'{self.name_dynamic}')
        ax1.set_ylabel('Silhouette Scores')

        ax2.plot(
            range(self.start_param, self.stop_param, self.step_param),
            self.calinski_harabasz_scores,
            'rx-')
        ax2.set_title('Calinski harabasz Score Method')
        ax2.set_xlabel(f'{self.name_dynamic}')
        ax2.set_ylabel('Calinski harabasz Scores')

        ax3.plot(
            range(self.start_param, self.stop_param, self.step_param),
            self.davies_bouldin_scores,
            'gx-')
        ax3.set_title('Davies bouldin Score Method')
        ax3.set_xlabel(f'{self.name_dynamic}')
        ax3.set_ylabel('Davies bouldi Scores')

        plt.xticks(range(self.start_param, self.stop_param, self.step_param))
        plt.tight_layout()
        plt.show()


class Radar(object):
    def __init__(self, figure, title, labels, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.9, 0.9]

        self.n = len(title)
        self.angles = np.arange(0, 360, 360.0/self.n)

        self.axes = [
            figure.add_axes(
                rect,
                projection='polar',
                label='axes%d' % i) for i in range(self.n)]
        self.ax = self.axes[0]
        self.ax.set_thetagrids(
            self.angles,
            labels=title,
            fontsize=10,
            backgroundcolor="white",
            zorder=999
            )
        self.ax.set_yticklabels([])

        for ax in self.axes[1:]:
            ax.xaxis.set_visible(False)
            ax.set_yticklabels([])
            ax.set_zorder(-99)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.spines['polar'].set_color('black')
            ax.spines['polar'].set_zorder(-99)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)
        kw['label'] = '_noLabel'
        self.ax.fill(angle, values,*args,**kw)


def cluster_characteristics(data):
    """Function require standardized data with column clusters"""

    cluster_colors = [
        '#C630FC',
        '#b4d2b1',
        '#568f8b',
        '#1d4a60',
        '#cd7e59',
        '#ddb247',
        '#d15252',
        '#3832a8',
        '#4de307'
        ]

    df_result_std_mean = pd.concat(
        [pd.DataFrame(data.mean().drop('clusters'), columns=['mean']),
        data.groupby('clusters').mean().T], axis=1
        )

    df_result_std_dev_rel = df_result_std_mean.apply(
        lambda x: round((x-x['mean'])/x['mean'],2)*100, axis = 1)
    df_result_std_dev_rel.drop(columns=['mean'], inplace=True)
    df_result_std_mean.drop(columns=['mean'], inplace=True)

    fig = plt.figure(figsize=(15, 15))
    radar = Radar(fig, data.drop('clusters', axis=1).columns, np.unique(data['clusters']))

    for k in range(data['clusters'].unique().min(), data['clusters'].unique().max()+1):
        cluster_data = df_result_std_mean[k].values.tolist()
        radar.plot(
            cluster_data,
            '-',
            lw=2,
            color=cluster_colors[k],
            alpha=0.7,
            label='cluster {}'.format(k)
            )

    radar.ax.legend()
    radar.ax.set_title("Cluster characteristics: Feature means per cluster", size=22, pad=60)
    plt.show()


def comparison_density(data, column_name, value_add=0.01, multiplication=1):

    print(f'------------------------------------------------ {column_name}, multiplication = {multiplication} ------------------------------')
    data = data[column_name]*multiplication
    min_data = data.min()
    min_non_zero = data[data>0].min()

    # default log
    log = np.log(data+value_add)

    if abs(data.skew())> abs(log.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {log.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(log, ax=ax2).set(title=f'default add log transformation - value {value_add}')
        plt.show()

    # sqrt
    sqrt = np.sqrt(data)
    if abs(data.skew())> abs(sqrt.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {sqrt.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(sqrt, ax=ax2).set(title='sqrt transformation')
        plt.show()

    # extensive log
    ext_log = data.apply(lambda x: np.log(x - (min_data - 1)))

    if abs(data.skew())> abs(ext_log.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {ext_log.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(ext_log, ax=ax2).set(
            title='extensive log transformation: log(x) - (data.min - 1)')
        plt.show()

    # boxcox with value > 0
    posdata = data[data > 0]
    bcdata, lam = stats.boxcox(posdata)
    boxcox = np.empty_like(data)
    boxcox[data > 0] = bcdata
    boxcox[data == 0] = -1/lam

    if abs(data.skew())> abs(pd.Series(boxcox).skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {pd.Series(boxcox).skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(boxcox, ax=ax2).set(title='Boxcox with value > 0')
        plt.show()

    # 'neglog' transformation
    negleg = data.apply(lambda x: np.sign(x) * np.log(abs(x)+1))

    if abs(data.skew())> abs(negleg.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {negleg.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(negleg, ax=ax2).set(title='neglog transformation')
        plt.show()

    # inverse hyperbolic sine transformation
    arcsin = np.arcsinh(data)

    if abs(data.skew())> abs(arcsin.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {arcsin.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(arcsin, ax=ax2).set(title='inverse hyperbolic sine transformation')
        plt.show()

    # log + x/2, where x is min non zero value
    log_non = np.log(data+(min_non_zero/2))

    if abs(data.skew())> abs(log_non.skew()):
        print('\n')
        print(f'Raw data: {data.skew()}, transformed data: {log_non.skew()}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        sns.kdeplot(data, ax=ax1).set(title='Skewed Data')
        sns.kdeplot(log_non, ax=ax2).set(title='log transformation - value x/2')
        plt.show()


def feature_distribution_box(data, n_columns=2):
    """Fuction requires raw data with column clusters 
    
    Parameters
        ----------
        data : pd.dataframe
            Raw data (excluding id_client) from BQ with column 'clusters'. 
        n_columns: int
            Number of columns to display
    """
    if 'id_client' in data.columns:
        data.drop('id_client', axis=1, inplace=True)

    cluster_colors = []
    for column in range(0, data['clusters'].nunique()):
        r = lambda: random.randint(0,255)
        cluster_colors.append('#%02X%02X%02X' % (r(),r(),r()))
    features = data.drop('clusters', axis=1).columns
    ncols = n_columns
    nrows = len(features) // ncols + (len(features) % ncols > 0)
    fig = plt.figure(figsize=(15,40))

    for n, feature in enumerate(features):
        ax = plt.subplot(nrows, ncols, n + 1)
        box = data[[feature, 'clusters']].boxplot(
            by='clusters',ax=ax,return_type='both',patch_artist = True)

        for row_key, (ax,row) in box.iteritems():
            ax.set_xlabel('cluster')
            ax.set_title(feature,fontweight="bold")
            for i,box in enumerate(row['boxes']):
                box.set_facecolor(cluster_colors[i])

    fig.suptitle('Feature distributions per cluster', fontsize=18, y=1)
    plt.tight_layout()
    plt.show()


def elbow_visualisation(data):

    fig, ax = plt.subplots()

    visualizer = KElbowVisualizer(KMeans(), k=(2,30),ax=ax)
    visualizer.fit(data)

    ax.set_xticks(range(2,7))
    visualizer.show()
    plt.show()


def describe_clusters_metrics(data, transpose=False):
    """Function to present metrics for clusters.
    
    Parameters
        ----------
        data : pd.dataframe
            Data with column 'clusters'. 
        transpose: Bool
            Choice of type of table location
            
    """
    if 'id_client' in data.columns:
        data.drop('id_client', axis=1, inplace=True)
    if transpose:
        return data.groupby('clusters').agg(
            ['mean', 'median', 'std', 'min', 'max']).T.style.background_gradient(
                cmap='copper', axis=1)
    return data.groupby('clusters').agg(
        ['mean', 'median', 'std', 'min', 'max']).style.background_gradient(
            cmap='copper')
