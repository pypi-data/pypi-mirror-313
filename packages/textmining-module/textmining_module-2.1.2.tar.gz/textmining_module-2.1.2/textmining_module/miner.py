from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split as tts, RandomizedSearchCV
from sklearn.inspection import permutation_importance
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import RandomOverSampler, SMOTEN
from imblearn.pipeline import Pipeline
from mlxtend.frequent_patterns import fpgrowth, association_rules  #  divide and conquer algorithm for frequent itemsets mining
import yake  # YAKE keywords mining algorithm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from sklearn.metrics.pairwise import pairwise_distances  # jaccard
import seaborn as sns

#===================================================================================#
#==================================Generic Helpers==================================#
#===================================================================================#
"""

:what: Generic helpers for KEM class

"""

def flatten(lambda_list):
    """
    :what: takes a list of list and flattens it into a single list.
    """
    return [item for sublist in lambda_list for item in sublist]

def removeDups(lambda_list):
    """
    :what: removes duplicates from a list
    """
    return list(frozenset(lambda_list))

def lenComplexity(msg_len, qtl_map):
    """
    :what: maps length complexity based on quartiles from qtl_map.
    """
    if msg_len < qtl_map['25%'] : return 'LC_S_'
    elif msg_len < qtl_map['75%'] : return 'LC_M_'
    else : return 'LC_L_'

def heatmap_head(distance_matrix):
    """
    :what: shows heatmap of distance_matrix (head).
    """
    sns.heatmap(distance_matrix.iloc[:10,:10], annot=True)

def str_outersectionFilter(kws_list):
  """
  :what: filters out keywords that contain other keywords from a list kws_list.
  """
  keeps = []
  for i, kw in enumerate(kws_list):
    filtered = kws_list.copy()
    del filtered[i]

    c1 = False
    if filtered:
      c1 = any(pd.Series(filtered).str.contains(kw.lower()))
    c2 = not [j for j in keeps if kws_list[j] in kw.lower()]

    if c1 and c2:
      for j in keeps:
        keeps = [j for j in keeps if kw not in kws_list[j]]
      keeps.append(i)

    if (not c1) and c2:
      keeps.append(i)

  out = kws_list

  if keeps:
    out = [kws_list[i] for i in keeps]

  return out


#===================================================================================#
#=============================Text Mining Module============================#
#===================================================================================#
"""

:what: Framework using YAKE, FPGrowth and Random Forest to extract keywords

:pub class KEM: keyword fetching wrapper with machine learning tools

:pub fun KEM.fit: fit an optimized weighted-balanced random forest (WBRF) per strata (target on F1 Score)
:pub fun KEM.findClusters: find obervations and keywords clusters per strata
:pub fun KEM.reqGlobalChunk: fetch a concatenation of all messages
:pub fun KEM.reqStratifiedChunks: fetch a concatenation of all messages, for each strata
:pub fun KEM.reqUniqueTargets: fetch unique targets list
:pub fun KEM.reqUniqueStratas: fetch unique stratas list
:pub fun KEM.reqYAKEKeywords: fetch keywords output from YAKE
:pub fun KEM.reqKeywordsByTarget: fetch keywords associated with each (strata, target)
:pub fun KEM.reqKeywordsCounters: fetch keywords counters for each (strata, target)
:pub fun KEM.reqOneHotData: fetch cleaned onehot data
:pub fun KEM.reqStratifiedOneHotData: fetch cleaned onehot data by strata
:pub fun KEM.reqDistanceMatrix: fetch Jaccard distance matrix

:issue mlxtend out of RAM: mlxtend out of RAM https://www.lieuzhenghong.com/handling_bigish_data/
:issue ROS: KNN OS techniques fail if minority class lacks observations
"""

class KEM:
    def __init__(self, data, comment_variable, target_variable, strata_variable=None, keywords_variable=None, clean_words=None,  # data
                 search_mode='micro', n=3, top=1, stop_words=None, truncation_words=None, truncation_mode='right', # YAKE
                 fpg_min_support=1E-3, keep_strongest_association=False, removeOutersection=False, # FPG
                 req_len_complexity=False, req_importance_score=False, # Random Forest
                 verbose=True, preprocessing_only=False): # class use
        """

        :what: Clean messages and find keywords at init of KEM object.

        :req param data: (pd dataframe) data to fetch keywords from
        :req param comment_variable: (str) name of the comment variable in pd dataframe
        :req param target_variable: (str) name of the target variable in pd dataframe
        :ctrl param strata_variable: (str) name of the strata variable in pd dataframe
        :ctrl param keyword_variable: (str) name of the strata variable in pd dataframe
        :ctrl param search_mode: (str) {'macro' : concatenate all rows in one chunk before extracting kws, 'micro' : search }
        :ctrl param top: (int) number of ngrams to extract
        :ctrl param stop_words: (str list) words to disregard in output of ngrams
        :ctrl param truncation_words: (str list) words where a split occur to truncate a message to the left/right - useful if french copy before/after an english message
        :ctrl param truncation_mode: (str) {'right' : remove rhs of message at truncation_word, 'left' : remove lhs of message at truncation_word}
        :ctrl param fpg_min_support: (float) minimal support for FP Growth. Try Higher value if FPG takes too long
        :ctrl param keep_strongest_association: (bool) filter One Hot Data to keep highest supported bits before fetching association
        :ctrl param req_importance_score: (bool) find importance score for all bags of relevant keywords

        :pub member progress: (widgets) html display of progress bar
        :pub member status: (bool dict) executable operations and their status
        :pvt member __data: (pd dataframe) internal copy of og data
        :pvt member __s: (str) internal access to strata_variable
        :pvt member __factor_s: (str list)
        :pvt member __x: (str) internal access to comment_variable
        :pvt member __y: (str) internal access to target_variable
        :pvt member __factor_y: (str list)
        :pvt member __mode: (str) internal access to search_mode
        :pvt member __tmode: (str) internal access to truncation_mode
        :pvt member __top: (int) internal access to top
        :pvt member __sw: (str list) internal access to stop_words
        :pvt member __tw: (str list) internal access to truncation_words
        :pvt member __req_imp: (bool) internal access to req_importance_score
        :pvt member __textChunk: (str) concatenation of every messages in data.loc[:,comment_variable]
        :pvt members __data_by_s: (pd dataframe dict) subset of data in regard to *STRATAS* keys from strata_variable
        :pvt members __textChunk_by_s: (str dict) concatenation of every messages in __data_by_s[*STRATA*].loc[:,comment_variable]

        """
        style = {'description_width': 'initial', 'bar_color': '#00AEFF'}

        self.progress = widgets.FloatProgress(
        value=0,
        min=0,
        max=100,
        bar_style='',
        style=style,
        description='Init...',)

        self.__verbose = verbose

        if self.__verbose:
          display(self.progress)

        self.progress.description = 'Init...'
        self.progress.value = 0

        # Global Init
        cols_to_keep = [col for col in [comment_variable, target_variable, strata_variable, keywords_variable] if col is not None]
        self.__data = data.copy()
        self.__s = strata_variable
        self.__z = keywords_variable
        self.__x = comment_variable
        self.__y = target_variable
        if self.__s: self.__factor_s = self.__data[self.__s].unique().tolist()
        self.__factor_y = self.__data[self.__y].unique().tolist()

        self.__mode = search_mode
        self.__tmode = truncation_mode
        self.__n = n
        self.__top = top
        self.__sw = stop_words
        if not self.__sw:
            self.__sw = []
        self.__tw = truncation_words
        if not self.__tw:
            self.__tw = []
        self.__cw = clean_words
        if not self.__cw:
            self.__cw = []
        self.__min_sup = fpg_min_support
        self.__filter = keep_strongest_association
        self.__removeOutersection = removeOutersection
        self.__req_lencomp = req_len_complexity
        self.__req_imp = req_importance_score

        self.progress.value = 50

        # Checkpoint
        self.__KEM_safetyNet()
        self.__data = data[cols_to_keep].copy()

        # Bootup Routine
        self.status = {'Cleaned stopwords' : False,
                       'Complexity table available' : False,
                       'Computed rescoring' : False,
                       'Encoded NAs to -999' : False,
                       'Global text chunk available' : False,
                       'Importance score available' : False,
                       'Jaccard proximity available' : False,
                       'KWs associated with target available' : False,
                       'Macro keywords available' : False,
                       'Manifold available' : False,
                       'Micro keywords available' : False,
                       'Search mode is macro' : True if self.__mode == 'macro' else False,
                       'Search mode is micro' : True if self.__mode == 'micro' else False,
                       'Stratified data' : True if self.__s else False,
                       'Stratified text chunk available' : False,
                       'Truncated left' : False,
                       'Truncated right' : False
        }

        self.progress.description = 'Init Done!'
        self.progress.value = 0

        self.__cleanupDaemon()
        self.__bootupDaemon()
        self.__truncationDaemon()
        self.__stratifyDaemon()
        self.__lenDaemon()

        if not preprocessing_only:
            # YAKE
            if self.__mode == 'micro':
                self.__microYAKE()
            elif self.__mode == 'macro':
                self.__macroYAKE()

            # FPGrowth
            self.__makeBoolData()
            self.__fetchTargetAssociation()

        self.progress.description = 'Done!'
        self.progress.value = 100

    """ = = = = = = = = = = = = = = = = = = = = = = = = = =
    = = = = = = = = = = USER INTERFACE = = = = = = = = = =
    = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    """

    def fit(self, k_neighbors=3, train_ratio=0.7, n_fold=5, n_round=10, optim_metric='f1_macro', n_jobs=-1, skl_verbose=0, verbose=True):
        """
        :what: UI for standard (stratified) training of Weighted-Balanced Random Forest (WBRF) with hyperparameters finetuning. Returns trained SKL pipeline (by strata)

        :ctrl param train_ratio: (float) ratio in (0, 1) for train data in train-test-split
        :ctrl param n_fold: (int) number of folds in K-Fold hyperparameter tuning
        :ctrl param n_round: (int) number of rounds (new hyperparameter candidates) for K-Fold hyperparamter tuning
        :ctrl param optim_metric: (str) skl target metric for RandomizedSearchCV
        :ctrl param n_jobs: (int) number of parallel processing workers, -1 for all workers available
        :ctrl param skl_verbose: (int) verbosity of SKL randomized search, 0 (none), (2) light, (3) heavy

        :pub member model(_by_s): trained SKL pipeline (by strata)
        """

        self.__optimizeRF(k_neighbors, train_ratio, n_fold, n_round, optim_metric, n_jobs, skl_verbose, verbose)
        if not self.__s:
          return self.model
        return self.model_by_s


    def clusterize(self, treshold=0.7):
        """
        :what: UI for standard (stratified) clustering with Average Linkage, using Jaccard similarity. Fetches and returns for both rows and columns (transpose) (by strata).

        :ctrl param treshold: (float) ratio in (0, 1) for highest difference in jaccard similarity tolerated to merge two sets in a generic cluster

        :pvt member data(_by_s): (pd dataframe (dict)) internally managed (stratified) data. This function adds a cluster attribute.
        :pvt idx_clusters(_by_s): (pd dataframe (dict)) observations clusters (by strata)
        :pvt col_clusters(_by_s): (pd dataframe (dict)) keywords clusters (by strata)
        """        
        self.__getClusters(treshold)

        if 'Cluster' in self.__data.columns.to_list():
          self.__data = self.__data.drop(['Cluster'], axis=1)
        self.__data = self.__data.join(self.__idx_clusters)

        if not self.__s:
          return self.__idx_clusters, self.__col_clusters

        for s in self.__factor_s:
          if 'Cluster' in self.__data_by_s[s].columns.to_list():
            self.__data_by_s[s] = self.__data_by_s[s].drop(['Cluster'], axis=1)
          self.__data_by_s[s] = self.__data_by_s[s].join(self.__idx_clusters_by_s[s])
        return self.__idx_clusters_by_s, self.__col_clusters_by_s


    def reqGlobalChunk(self):
        """
        :what: returns a concatenation of every message given
        """
        return self.__textChunk


    def reqStratifiedChunks(self):
        """
        :what: returns a concatenation of every message given, for each strata
        """
        return self.__textChunk_by_s.copy()


    def reqUniqueTargets(self):
        """
        :what: returns a list of unique targets
        """
        return self.__factor_y.copy()


    def reqUniqueStratas(self):
        """
        :what: returns a list of unique stratas
        """
        return self.__factor_s.copy()


    def reqYAKEKeywords(self):
        """
        :what: if micro : returns (dictionnary of) data with keywords per row (and per strata) [micro] or (dictionnary of) pd dataframe of keywords extracted (per strata) [macro]
        """
        if self.__s:
            if self.__mode == 'micro':
                return self.__data_by_s.copy()
            elif self.__mode == 'macro':
                return self.__yake_kws_by_s.copy()

        if self.__mode == 'micro':
            return self.__data.copy()
        elif self.__mode == 'macro':
            return self.__yake_kws.copy()


    def reqKeywordsByTarget(self):
        """
        :what: returns dictionnary of keywords associated to each target (for each strata)
        """
        if self.__s:
            return self.__kws_by_y_by_s
        return self.__kws_by_y


    def reqKeywordsCounters(self):
        """
        :what: returns m : cumulative keywords counters for each target
                       n : cumulative keywords counters for each strata (if strata available)
                       d : raw counters for each strata-target pair, in a summarized dataframe (if strata available)
        """
        if self.__s:
            n = {}
            d = pd.DataFrame(0, index=self.__factor_s, columns=self.__factor_y)
            for y in self.reqUniqueTargets():
                n[y] = 0
                for s in self.reqUniqueStratas():
                    n[y] += len(self.reqKeywordsByTarget()[s][y])
                    d.loc[s,y] = len(self.reqKeywordsByTarget()[s][y])

            m = {}
            for s in self.reqUniqueStratas():
                m[s] = 0
                for y in self.reqUniqueTargets():
                    m[s] += len(self.reqKeywordsByTarget()[s][y])

            return n, m, d

        n = 0
        for y in self.reqUniqueTargets():
            n += len(self.reqKeywordsByTarget()[y])
        return n, None, None

    def reqCleanedData(self):
        """
        :what: returns (dictionnary of) cleaned data (split by strata)
        """
        if not self.__s:
          return self.__data.copy()
        return self.__data_by_s.copy()

    def reqOneHotData(self):
        """
        :what: returns (dictionnary of) dummified data (split by strata)
        """
        if not self.__s:
          return self.__onehot.copy()
        return self.__onehot_by_s.copy()


    def reqSimilarityMatrix(self):
        """
        :what: returns (dictionnary of) jaccard similarity matrix (split by strata)
        """
        self.__getJaccardDistance()
        if not self.__s:
          return self.__jaccard_sim.copy()
        return self.__jaccard_sim_by_s.copy()


    """ = = = = = = = = = = = = = = = = = = = = = =
    = = = = = = = = PREPROCESSING = = = = = = = = =
    = = = = = = = = = = = = = = = = = = = = = = = =
    
    Functions that modify an internal copy of user’s data to obtain a workable data set by machine learning standards.
    """


    def __cleanupDaemon(self):
        """
        :what: cleans messages according to cleanwords dictionnary
        """
        if self.__cw:
            new_msg = []
            new_key = []
            for _, row in self.__data.iterrows():
                if isinstance(row[self.__x], str):
                    m = row[self.__x].lower()
                    m_out = ''
                    for w in m.split(' '):
                        for k in list(self.__cw.keys()):
                            if w == k:
                                w = w.replace(k, self.__cw[k])
                        w = w.replace('.', '')
                        m_out = m_out + w + ' '
                    new_msg.append(m_out[:-1])
                else:
                    new_msg.append(row[self.__x])

                if self.__z:
                    if isinstance(row[self.__z], str):
                        d = row[self.__z].lower()
                        d_out = ''
                        for w in d.split(' '):
                            for k in list(self.__cw.keys()):
                                if w == k:
                                    w = w.replace(k, self.__cw[k])
                            w = w.replace('.', '')
                            d_out = d_out + w + ' '
                        new_key.append(d_out[:-1])
                    else:
                        new_key.append(row[self.__z])

            self.__data[self.__x] = new_msg
            if self.__z:
              self.__data[self.__z] = new_key


    def __bootupDaemon(self):
        """
        :what: preprocess data for coherent format
        """
        self.progress.description = 'Bootup...'
        self.progress.value = 0

        cleaned_msg = []
        cleaned_kw = []
        for _, row in self.__data.iterrows():
            keep_msg = str()
            if isinstance(row[self.__x], str):
                keep_msg = row[self.__x].lower()
                if self.__z:
                  if isinstance(row[self.__z], str):
                    keep_msg += ' - ' + row['Key_Descriptor'].lower()

            elif (not isinstance(row[self.__x], str)) and (self.__z):
                if isinstance(row[self.__z], str):
                    keep_msg = row['Key_Descriptor'].lower()
            else:
                keep_msg = '-999'
            cleaned_msg.append(keep_msg)

            keep_kw = str()
            if self.__z:
                if isinstance(row[self.__z], str) :
                    keep_kw = row[self.__z].lower()
                else:
                    keep_kw = '-999'
                cleaned_kw.append(keep_kw)

        self.__data[self.__x] = cleaned_msg
        if self.__z:
            self.__data[self.__z] = cleaned_kw
        self.__textChunk = ' '.join(self.__data[self.__x]).lower()

        self.progress.description = 'Bootup Done!'
        self.progress.value = 100

        self.status['Encoded NAs to -999'] = True
        self.status['Global text chunk available'] = True


    def __stratifyDaemon(self):
        """
        :what: stratifies the data
        """
        self.progress.description = 'Stratification...'
        self.progress.value = 0


        self.__data['UniqueID'] = range(self.__data.shape[0])

        if self.__s:
            self.__data_by_s = {}
            self.__textChunk_by_s = {}
            for s in self.__factor_s:
                self.__data_by_s[s] = self.__data.loc[self.__data[self.__s] == s].drop([self.__s], axis=1).copy()
                self.__textChunk_by_s[s] = ' '.join(self.__data_by_s[s][self.__x]).lower()

            self.status['Stratified data'] = True
            self.status['Stratified text chunk available'] = True

        self.progress.description = 'Stratification Done!'
        self.progress.value = 100


    def __truncationDaemon(self):
        """
        :what: truncates the data
        """
        self.progress.description = 'Truncation...'
        self.progress.value = 0

        if self.__tw:
            if self.__tmode == 'right':
              self.status['Truncated right'] = True
            elif self.__tmode == 'left':
              self.status['Truncated left'] = True
            trc_msg = []
            for _, row in self.__data.iterrows():
                keep = row[self.__x].lower()
                for tw in self.__tw:
                        if self.__tmode == 'right':
                            keep, _, _ = keep.partition(tw)
                        elif self.__tmode == 'left':
                            _, _, keep = keep.partition(tw)
                trc_msg.append(keep)
            self.__data[self.__x] = trc_msg

        self.progress.description = 'Truncation Done!'
        self.progress.value = 100


    def __lenDaemon(self):
        """
        :what: find length complexity based on quartiles (for each strata). Default medium length interval : Q1-Q3
        """
        if self.__req_lencomp:
          self.__data['lenComplexity'] = self.__data[self.__x].apply(len)
          temp = self.__data[self.__data[self.__x] != '-999']
          bound = {}
          for qtl in ['25%', '75%']:
            bound[qtl] = temp['lenComplexity'].describe()[qtl]

          self.__data['lenComplexity'] = self.__data['lenComplexity'].apply(lambda x: lenComplexity(x, bound))

          if self.__s:
            for s in self.__factor_s:
              self.__data_by_s[s]['lenComplexity'] = self.__data_by_s[s][self.__x].apply(len)
              temp = self.__data_by_s[s][self.__data_by_s[s][self.__x] != '-999']
              bound = {}
              for qtl in ['25%', '75%']:
                bound[qtl] = temp['lenComplexity'].describe()[qtl]

              self.__data_by_s[s]['lenComplexity'] = self.__data_by_s[s]['lenComplexity'].apply(lambda x: lenComplexity(x, bound))


    """ = = = = = = = = = = = = = = = = = = = = = = =
    = = = = = = = = = PROCESSING = = = = = = = = = =
    = = = = = = = = = = = = = = = = = = = = = = = = =
    
    Functions that heavily use YAKE and FP-Growth algorithms to enhance data.
    """


    def __microYAKE(self):
        """
        :what: fetch and add column 'keywords_yake' to internally managed data
        """
        self.progress.description = 'YAKE...'
        self.progress.value = 0

        progress_i=1
        progress_n = 90/float(self.__data.shape[0])

        kws=[]

        for _, row in self.__data.iterrows():

            yake_extractor = yake.KeywordExtractor(n=self.__n, top=self.__top, stopwords=self.__sw)
            kw = yake_extractor.extract_keywords(row[self.__x].lower())
            if not kw:
                kws.append(['-999'])
            else:
                kw = pd.DataFrame(kw)
                kw.columns = ['keywords_yake', 'score_lower_is_better']
                kws.extend([kw['keywords_yake'].values])

            self.progress.value = progress_n*progress_i
            progress_i+=1

        self.__data['keywords_yake'] = kws.copy()

        if self.__s:
            for s in self.__factor_s:
                temp = self.__data_by_s[s].merge(self.__data[['keywords_yake', 'UniqueID']], on=['UniqueID']).sort_values(by=['UniqueID'])
                temp.index = self.__data_by_s[s].index
                self.__data_by_s[s] = temp.drop(['UniqueID'], axis=1)


        self.__data = self.__data.drop(['UniqueID'],axis=1)

        self.progress.description = 'YAKE Done!'
        self.progress.value = 100

        self.status['Cleaned stopwords'] = True
        self.status['Micro keywords available'] = True

    def __macroYAKE(self):
        """
        :what: fetch and create internally managed macro kws dataframes, in regard to stratas

        :member: __yake_kws: macro kws dataframe
        :member: __yake_kws_by_s: macro kws dict of dataframe in regard to *STRATAS* values from strata_variable
        """
        self.progress.description = 'YAKE...'
        self.progress.value = 0

        if 'UniqueID' in self.__data.columns:
          self.__data = self.__data.drop(['UniqueID'], axis=1)

        yake_extractor = yake.KeywordExtractor(n=self.__n, top=self.__top, stopwords=self.__sw)
        kws = pd.DataFrame(yake_extractor.extract_keywords(self.__textChunk))
        kws.columns = ['keywords_yake', 'score_lower_is_better']
        self.__yake_kws = kws.copy()

        if self.__s:
            progress_i=1
            progress_n = 90/float(len(self.__factor_s))
            self.__yake_kws_by_s = {}
            for s in self.__factor_s:
                if 'UniqueID' in self.__data_by_s[s].columns:
                  self.__data_by_s[s] = self.__data_by_s[s].drop(['UniqueID'], axis=1)
                yake_extractor = yake.KeywordExtractor(n=self.__n, top=self.__top, stopwords=self.__sw)
                kws = pd.DataFrame(yake_extractor.extract_keywords(self.__textChunk_by_s[s]))
                kws.columns = ['keywords_yake', 'score_lower_is_better']
                self.__yake_kws_by_s[s] = kws.copy()

                self.progress.value = progress_n*progress_i
                progress_i+=1

        self.progress.description = 'YAKE Done!'
        self.progress.value = 100

        self.status['Cleaned stopwords'] = True
        self.status['Macro keywords available'] = True

    def __makeBoolData(self):
        """
        :what: creates a boolean dataset (per strata) for basket analysis. User can specify filtering method(s).

        :pvt member data(_by_s): (pd dataframe (dict)) internally managed (stratified) data. This function updates keywords_yake attribute.
        :pvt member onehot(_by_s): (pd dataframe (dict)) internally managed (stratified) One Hot data.
        """

        self.__onehot = self.__data
        unique_kws = []

        self.progress.description = 'Dummify...'
        self.progress.value = 0

        if self.__mode == 'micro':
            progress_i = 1
            progress_n = 50/float(self.__data.shape[0])
            self.__onehot = self.__onehot.drop(['keywords_yake'], axis=1)
            for _, row in self.__data.iterrows():
                unique_kws.extend(row['keywords_yake'])

                self.progress.value = progress_n*progress_i
                progress_i+=1
        elif self.__mode == 'macro':
            unique_kws = list(self.__yake_kws['keywords_yake'])
        if self.__z:
            unique_kws.extend(list(self.__data[self.__z]))
            self.__onehot = self.__onehot.drop([self.__z], axis=1)
        unique_kws = removeDups(unique_kws)

        self.progress.value = 20

        if self.__removeOutersection:
            unique_kws = str_outersectionFilter(unique_kws)

        self.progress.value = 40

        if self.__req_lencomp:
          self.__onehot = self.__onehot.join(pd.get_dummies(self.__data[['lenComplexity']], prefix='', prefix_sep='', dtype=bool)).drop(['lenComplexity'], axis=1)

        self.__onehot = pd.concat([self.__onehot, pd.DataFrame(index=self.__onehot.index, columns=unique_kws)], axis=1)

        for kw in unique_kws:
            self.__onehot[kw] = np.where(self.__onehot[self.__x].str.contains(kw), True, False)

        self.__onehot = self.__onehot.drop([self.__x], axis=1)

        temp = self.__onehot[unique_kws]
        self.__data['keywords_yake'] = temp.dot(temp.columns + ';').str.split(';').apply(lambda x: x[:-1])

        self.progress.value = 50

        if self.__s:
            self.__onehot = self.__onehot.drop([self.__s], axis=1)

            progress_i=1
            progress_n = 40/float(len(self.__factor_s))
            self.__onehot_by_s = {}
            for s in self.__factor_s:
                unique_kws = []
                self.__onehot_by_s[s] = self.__data_by_s[s]
                if self.__mode == 'micro':
                    self.__onehot_by_s[s] = self.__data_by_s[s].drop(['keywords_yake'], axis=1)
                    for _, row in self.__data_by_s[s].iterrows():
                        unique_kws.extend(row['keywords_yake'])
                elif self.__mode == 'macro':
                    unique_kws = list(self.__yake_kws_by_s[s]['keywords_yake'])
                if self.__z:
                    unique_kws.extend(self.__data_by_s[s][self.__z])
                    self.__onehot_by_s[s] = self.__onehot_by_s[s].drop([self.__z], axis=1)

                unique_kws = removeDups(unique_kws)

                self.progress.value = 50+progress_n*(progress_i-0.6)

                if self.__removeOutersection:
                    unique_kws = str_outersectionFilter(unique_kws)

                self.progress.value = 50+progress_n*(progress_i-0.3)

                if self.__req_lencomp:
                  self.__onehot_by_s[s] = self.__onehot_by_s[s].join(pd.get_dummies(self.__data_by_s[s][['lenComplexity']], prefix='', prefix_sep='', dtype=bool)).drop(['lenComplexity'], axis=1)

                self.__onehot_by_s[s] = pd.concat([self.__onehot_by_s[s], pd.DataFrame(index=self.__onehot_by_s[s].index, columns=unique_kws)], axis=1)

                for kw in unique_kws:
                    self.__onehot_by_s[s][kw] = np.where(self.__onehot_by_s[s][self.__x].str.contains(kw), True, False)
                self.__onehot_by_s[s] = self.__onehot_by_s[s].drop([self.__x], axis=1)

                temp = self.__onehot_by_s[s][unique_kws]
                self.__data_by_s[s]['keywords_yake'] = temp.dot(temp.columns + ';').str.split(';').apply(lambda x: x[:-1])

                self.progress.value = 50+progress_n*progress_i
                progress_i+=1

        self.progress.description = 'Dummify Done!'
        self.progress.value = 100


    def __fetchTargetAssociation(self):
        """
        :what:  uses Basket Analysis to fetch strong associations between keywords and target_variable.

        :pub member bestbucket(_by_s): (pd dataframe (dict)) map of individual keywords to strongest target based on support (per strata)
        :pvt member kws_by_y(_by_s): (str list (dict)) list of keywords associated to each target (for each strata)
        """
        self.progress.description = 'FP Growth...'
        self.progress.value = 0

        mink, maxk = 1, 8

        if not self.__s:
            self.bestbucket = pd.DataFrame(self.__onehot.groupby(by=[self.__y]).sum().T.apply(lambda s: s.abs().nlargest(1).index.tolist()[0], axis=1), columns=['BestBucket']).T
            fetch_data = self.__onehot.copy()
            if self.__filter:
              for i, row in fetch_data.iterrows():
                  for kw in fetch_data.columns[1:]:
                      if (self.bestbucket.loc[:,kw].values[0] != row[self.__y]) & (row[kw] == True):
                          fetch_data.loc[i,kw] = False

            fetch_data = fetch_data.join(pd.get_dummies(self.__onehot[[self.__y]], prefix='', prefix_sep='', dtype=bool)).drop([self.__y], axis=1)

            frequent_itemsets = fpgrowth(fetch_data, min_support=self.__min_sup, use_colnames=True)
            num_itemsets = len(frequent_itemsets)  # Fix: Calculate num_itemsets

            rules = association_rules(frequent_itemsets, metric='confidence', support_only=False, min_threshold=0.5, num_itemsets=num_itemsets)  # Fix: Add num_itemsets
            rules["k"] = rules['antecedents'].apply(lambda x: len(x))
            rules = rules[(rules['k'] >= mink) & (rules['k'] <= maxk) & ((rules['zhangs_metric'] >= 0.6) | (rules['confidence'] >= 0.8))].sort_values(by=['k','zhangs_metric'], ascending=False)

            self.__kws_by_y = {}
            for y in self.__factor_y:
                rules_y = rules[rules['consequents'].astype(str).str.contains(y)].copy()
                kws_clean = pd.DataFrame(rules_y['antecedents'].apply(list))
                self.__kws_by_y[y] = removeDups(flatten(kws_clean['antecedents'].values))

        if self.__s:
            progress_i=1
            progress_n = 90/float(len(self.__factor_s))
            self.bestbucket_by_s = {}
            self.__kws_by_y_by_s = {}
            for s in self.__factor_s:
                self.bestbucket_by_s[s] = pd.DataFrame(self.__onehot_by_s[s].groupby(by=[self.__y]).sum().T.apply(lambda s: s.abs().nlargest(1).index.tolist()[0], axis=1), columns=['BestBucket']).T
                fetch_data = self.__onehot_by_s[s].copy()
                if self.__filter:
                  for i, row in fetch_data.iterrows():
                      for kw in fetch_data.columns[1:]:
                          if (self.bestbucket_by_s[s].loc[:,kw].values[0] != row[self.__y]) & (row[kw] == True):
                              fetch_data.loc[i,kw] = False

                fetch_data = fetch_data.join(pd.get_dummies(self.__onehot_by_s[s][[self.__y]], prefix='', prefix_sep='', dtype=bool)).drop([self.__y], axis=1)

                frequent_itemsets = fpgrowth(fetch_data, min_support=self.__min_sup, use_colnames=True)
                num_itemsets = len(frequent_itemsets)  # Fix: Calculate num_itemsets
                if s == 'Home':
                  self.test = frequent_itemsets

                self.progress.value = progress_n*(progress_i-0.6)

                rules = association_rules(frequent_itemsets, metric='confidence', support_only=False, min_threshold=0.5, num_itemsets=num_itemsets)  # Fix: Add num_itemsets
                rules["k"] = rules['antecedents'].apply(lambda x: len(x))
                rules = rules[(rules['k'] >= mink) & (rules['k'] <= maxk) & ((rules['zhangs_metric'] >= 0.6) | (rules['confidence'] >= 0.8))].sort_values(by=['k','zhangs_metric'], ascending=False)

                self.progress.value = progress_n*(progress_i-0.2)

                self.__kws_by_y_by_s[s] = {}
                for y in self.__factor_y:
                    rules_y = rules[rules['consequents'].astype(str).str.contains(y)].copy()
                    kws_clean = pd.DataFrame(rules_y['antecedents'].apply(list))
                    self.__kws_by_y_by_s[s][y] = removeDups(flatten(kws_clean['antecedents'].values))

                self.progress.value = progress_n*progress_i
                progress_i+=1

        self.progress.description = 'FP Growth Done!'
        self.progress.value = 100


    """ = = = = = = = = = = = = = = = = = = = = = = =
    = = = = = = = = POSTPROCESSING = = = = = = = = =
    = = = = = = = = = = = = = = = = = = = = = = = = =
    
    Student functions that execute machine learning tasks for teacher functions called by user.
    """

    def __optimizeRF(self,k_neighbors=3, train_ratio=0.7, n_fold=5, n_round=10, optim_metric='f1_macro', n_jobs=-1, skl_verbose=0, verbose=True):
        """
        :what: standard (stratified) training of Weighted-Balanced Random Forest (WBRF) with hyperparameters finetuning. Returns trained SKL pipeline (by strata)

        :ctrl param train_ratio: (float) ratio in (0, 1) for train data in train-test-split
        :ctrl param n_fold: (int) number of folds in K-Fold hyperparameter tuning
        :ctrl param n_round: (int) number of rounds (new hyperparameter candidates) for K-Fold hyperparamter tuning
        :ctrl param optim_metric: (str) skl target metric for RandomizedSearchCV
        :ctrl param n_jobs: (int) number of parallel processing workers, -1 for all workers available
        :ctrl param skl_verbose: (int) verbosity of RandomizedSearchCV, 0 (none), (2) light, (3) heavy

        :pvt member data(_by_s): (pd dataframe (dict)) internally managed (stratified) data. This function adds importance (mdi, perm, harmonic) attributes, if required.
        :pvt member yake_kws(_by_s): (pd dataframe (dict)) keywords extracted in macro mode (by strata). This function adds importance (mdi, perm, harmonic) attributes, if required.

        :pub member model(_by_s): trained SKL pipeline (by strata)
        :pub member best_hp(_by_s): (str dict (dict)) hyperparameters of trained SKL pipeline (by strata)
        :pub member train_cm(_by_s): (pd dataframe (dict)) confusion matrix of trained SKL pipeline on train set (by strata)
        :pub member test_cm(_by_s): (pd dataframe (dict)) confusion matrix of trained SKL pipeline on test set (by strata)
        :pub member train_metrics(_by_s): (pd dataframe (dict)) metrics of trained SKL pipeline on train set (by strata)
        :pub member test_metrics(_by_s): (pd dataframe (dict)) metrics of trained SKL pipeline on test set (by strata)
        :pub member mdi_importances(_by_s): (pd series (dict)) mean decrease in impurity (MDI) score of random forest (by strata), if required
        :pub member perm_importances(_by_s): (pd series (dict)) permutations score of random forest (by strata), if required
        """
        style = {'description_width': 'initial', 'bar_color': '#00AEFF'}

        fitprogress = widgets.FloatProgress(
        value=0,
        min=0,
        max=100,
        bar_style='',
        style=style,
        description='Init...',)

        if verbose:
          display(fitprogress)
        fitprogress.description = 'Fit...'
        fitprogress.value = 0

        grid = {'rf__n_estimators' : [100, 500, 1000],
                'rf__max_depth' : [20, 40, None],
                'rf__class_weight' : ['balanced', 'balanced_subsample', None],
                'rf__bootstrap' : [True, False]}

        if not self.__s:
          X_train, X_test, y_train, y_test = tts(self.__onehot.drop(self.__y, axis=1).replace({True: 1, False: 0}),
                                                 self.__onehot[self.__y],
                                                 train_size=train_ratio, random_state=42)

          pipeline = Pipeline([("smoten", SMOTEN(k_neighbors=k_neighbors, sampling_strategy='not majority')),
                               ("rf", RandomForestClassifier(n_jobs=n_jobs, random_state=42))])

          optim = RandomizedSearchCV(pipeline, param_distributions=grid,
                                     scoring=optim_metric, n_iter = n_round, cv = n_fold,
                                     verbose=skl_verbose, random_state=42, n_jobs=n_jobs)
          optim.fit(X_train, y_train)

          self.best_hp = optim.best_params_

          model = optim.best_estimator_.fit(X_train, y_train)
          self.model = [model.steps[0][1], model.steps[1][1]]

          train_pred = model.predict(X_train)
          test_pred = model.predict(X_test)

          self.train_cm = pd.DataFrame(confusion_matrix(y_train, train_pred, labels=self.__factor_y),
                                 index=self.__factor_y, columns=self.__factor_y)
          self.train_metrics = pd.DataFrame(classification_report(y_train, train_pred, output_dict=True))

          self.test_cm = pd.DataFrame(confusion_matrix(y_test, test_pred, labels=self.__factor_y),
                                 index=self.__factor_y, columns=self.__factor_y)
          self.test_metrics = pd.DataFrame(classification_report(y_test, test_pred, output_dict=True))

          if self.__req_imp:
            feature_names=list(X_train.columns)
            self.mdi_importances = pd.Series(self.model[1].feature_importances_, index=feature_names)

            scores = permutation_importance(self.model[1], X_test, y_test, n_repeats=5, random_state=1, n_jobs=n_jobs)
            self.perm_importances = pd.Series(scores.importances_mean, index=feature_names)

            def rcprcl(x):
                return 0 if x==0 else 1/x

            rf_mdi = []
            rf_perm = []
            rf_harm = []
            for _, row in self.reqYAKEKeywords().iterrows():
                mdi = sum([max(self.mdi_importances[kw], 0) for kw in row['keywords_yake']])
                perm = sum([max(self.perm_importances[kw], 0) for kw in row['keywords_yake']])
                harm = rcprcl(rcprcl(mdi) + rcprcl(perm))
                rf_mdi.append(mdi)
                rf_perm.append(perm)
                rf_harm.append(harm)

            self.__data['MDI Importance'] = rf_mdi
            self.__data['Permutations Importance'] = rf_perm
            self.__data['Harmonic Importance'] = rf_harm

            if self.__mode == 'macro':
                self.__yake_kws['MDI Importance'] = rf_mdi
                self.__yake_kws['Permutations Importance'] = rf_perm
                self.__yake_kws['Harmonic Importance'] = rf_harm

          del optim
          del model
          del pipeline

        if self.__s:
          self.train_cm_by_s = {}
          self.train_metrics_by_s = {}
          self.test_cm_by_s = {}
          self.test_metrics_by_s = {}
          self.best_hp_by_s = {}
          self.model_by_s = {}
          self.mdi_importances_by_s = {}
          self.perm_importances_by_s = {}
          progress_i=1
          progress_n = 90/float(len(self.__factor_s))
          for s in self.__factor_s:
            X_train, X_test, y_train, y_test = tts(self.__onehot_by_s[s].drop(self.__y, axis=1).replace({True: 1, False: 0}),
                                                   self.__onehot_by_s[s][self.__y], train_size=train_ratio,
                                                   random_state=42)

            pipeline = Pipeline([("smoten", SMOTEN(k_neighbors=k_neighbors, sampling_strategy='not majority')),
                                 ("rf", RandomForestClassifier(n_jobs=n_jobs, random_state=42))])

            optim = RandomizedSearchCV(pipeline, param_distributions=grid,
                                       scoring=optim_metric, n_iter = n_round, cv = n_fold,
                                       verbose=skl_verbose, random_state=42, n_jobs=n_jobs)
            optim.fit(X_train, y_train)

            fitprogress.value = progress_n*(progress_i-0.4)

            self.best_hp_by_s[s] = optim.best_params_

            model = optim.best_estimator_.fit(X_train, y_train)

            self.model_by_s[s] = [model.steps[0][1], model.steps[1][1]]

            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            self.train_cm_by_s[s] = pd.DataFrame(confusion_matrix(y_train, train_pred, labels=self.__factor_y),
                                           index=self.__factor_y, columns=self.__factor_y)
            self.train_metrics_by_s[s] = pd.DataFrame(classification_report(y_train, train_pred, output_dict=True))

            self.test_cm_by_s[s] = pd.DataFrame(confusion_matrix(y_test, test_pred, labels=self.__factor_y),
                                           index=self.__factor_y, columns=self.__factor_y)
            self.test_metrics_by_s[s] = pd.DataFrame(classification_report(y_test, test_pred, output_dict=True))

            fitprogress.value = progress_n*(progress_i-0.2)
            
            if self.__req_imp:
                feature_names=list(X_train.columns)
                self.mdi_importances_by_s[s] = pd.Series(self.model_by_s[s][1].feature_importances_, index=feature_names)

                scores = permutation_importance(self.model_by_s[s][1], X_test, y_test, n_repeats=5, random_state=1, n_jobs=n_jobs)
                self.perm_importances_by_s[s] = pd.Series(scores.importances_mean, index=feature_names)

                def rcprcl(x):
                    return 0 if x==0 else 1/x

                rf_mdi = []
                rf_perm = []
                rf_harm = []
                for _, row in self.reqYAKEKeywords()[s].iterrows():
                    mdi = sum([max(self.mdi_importances_by_s[s][kw], 0) for kw in row['keywords_yake']])
                    perm = sum([max(self.perm_importances_by_s[s][kw], 0) for kw in row['keywords_yake']])
                    harm = rcprcl(rcprcl(mdi) + rcprcl(perm))
                    rf_mdi.append(mdi)
                    rf_perm.append(perm)
                    rf_harm.append(harm)

                self.__data_by_s[s]['MDI Importance'] = rf_mdi
                self.__data_by_s[s]['Permutations Importance'] = rf_perm
                self.__data_by_s[s]['Harmonic Importance'] = rf_harm

                if self.__mode == 'macro':
                    self.__yake_kws_by_s[s]['MDI Importance'] = rf_mdi
                    self.__yake_kws_by_s[s]['Permutations Importance'] = rf_perm
                    self.__yake_kws_by_s[s]['Harmonic Importance'] = rf_harm

            fitprogress.value = progress_n*progress_i
            progress_i+=1

            del optim
            del model
            del pipeline

        fitprogress.description = 'Done!'
        fitprogress.value = 100


    def __getJaccardDistance(self):
        """
        :what: student function to calculate Jaccard similarity (by fetching Jaccard distance)

        """        
        self.__jaccard_sim = pd.DataFrame(1 - pairwise_distances(self.__onehot.iloc[:,1:].to_numpy(), metric='jaccard'),
                                          index=self.__onehot.iloc[:,1:].T.columns,
                                          columns=self.__onehot.iloc[:,1:].T.columns)

        if self.__s:
          self.__jaccard_sim_by_s = {}
          self.__heatmap_by_s = {}
          for s in self.__factor_s:
            self.__jaccard_sim_by_s[s] = pd.DataFrame(1 - pairwise_distances(self.__onehot_by_s[s].iloc[:,1:].to_numpy(), metric='jaccard'),
                                                      index=self.__onehot_by_s[s].iloc[:,1:].T.columns,
                                                      columns=self.__onehot_by_s[s].iloc[:,1:].T.columns)


    def __getClusters(self, treshold=0.7):
        """
        :what: standard (stratified) clustering with Average Linkage, using Jaccard similarity. Fetches and returns for both rows and columns (transpose) (by strata).

        :ctrl param treshold: (float) ratio in (0, 1) for highest difference in jaccard similarity tolerated to merge two sets in a generic cluster

        :pvt idx_clusters(_by_s): (pd dataframe (dict)) observations clusters (by strata)
        :pvt col_clusters(_by_s): (pd dataframe (dict)) keywords clusters (by strata)
        """

        idx_dist_matrix = linkage(self.__onehot.iloc[:,1:], method = 'average', metric = 'jaccard')
        col_dist_matrix = linkage(self.__onehot.T.iloc[1:,:], method = 'average', metric = 'jaccard')
        self.__idx_clusters = pd.DataFrame({'Cluster':fcluster(idx_dist_matrix, t=treshold, criterion='distance')}, index=self.__onehot.iloc[:,1:].index.tolist())
        self.__col_clusters = pd.DataFrame({'Cluster':fcluster(col_dist_matrix, t=treshold, criterion='distance')}, index=self.__onehot.T.iloc[1:,:].index.tolist())

        if self.__s:
          self.__idx_clusters_by_s = {}
          self.__col_clusters_by_s = {}
          for s in self.__factor_s:
            idx_dist_matrix = linkage(self.__onehot_by_s[s].iloc[:,1:], method = 'average', metric = 'jaccard')
            col_dist_matrix = linkage(self.__onehot_by_s[s].T.iloc[1:,:], method = 'average', metric = 'jaccard')
            self.__idx_clusters_by_s[s] = pd.DataFrame({'Cluster':fcluster(idx_dist_matrix, t=treshold, criterion='distance')}, index=self.__onehot_by_s[s].iloc[:,1:].index.tolist())
            self.__col_clusters_by_s[s] = pd.DataFrame({'Cluster':fcluster(col_dist_matrix, t=treshold, criterion='distance')}, index=self.__onehot_by_s[s].T.iloc[1:,:].index.tolist())


    def __KEM_safetyNet(self):
        if self.__s:
            assert self.__s in self.__data.columns, 'strata arg was given, it must be in data'
        if self.__z:
            assert self.__z in self.__data.columns, 'keywords arg was given, it must be in data'
        assert self.__y in self.__data.columns, 'target must be in data'
        assert self.__x in self.__data.columns, 'comment must be in data'
        assert self.__s != self.__y, 'strata and target must be different'
        assert self.__s != self.__x, 'strata and comment must be different'
        if self.__s or self.__z:
            assert self.__s != self.__z, 'strata and keywords must be different'
        assert self.__x != self.__y, 'comment and target must be different'
        assert self.__x != self.__z, 'comment and keywords must be different'
        assert self.__z != self.__y, 'keywords and target must be different'
        assert self.__mode == 'micro' or self.__mode == 'macro', 'search mode must be either micro or macro'
        assert type(self.__top) == int, 'top must be an integer'
        assert type(self.__sw) == list, 'stop words must be in a list'
        assert type(self.__tw) == list, 'truncation words must be in a list'
        assert self.__tmode == 'left' or self.__tmode == 'right', 'truncation mode must be either left or right'