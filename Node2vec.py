import networkx as nx
import random
from gensim.models import Word2Vec

class Node2Vec(object):
    """Perform node2vec (Deepwalk) on an undirected networkx MultiGraph with edge attributes. 
 
    Parameters
    ----------
    graph : networkx.MultiGraph
    walk_length : (default 100)
    N_iterations : (default 1)
    
    Methods: 
    get_walks
    word2vec
    
    Attributes
    ----------
    get_walks()
    word2vec()
    """
    
    def __init__(self,graph,walk_length=100,N_iterations=1):
        self.graph = graph
        self.walks=[]
        self.wl=walk_length
        self.N_iter=N_iterations
        self.N_walks=0
        
    def get_walks(self):
        """Generate collection of graph walks: one for each node (= starting point) 
        sampled by an (unbiased) random walk over the networkx MultiGraph.
        """
        start = time.time()
        g_iter=nx.nodes_iter(self.graph)
        for u in g_iter:
            self.N_walks=self.N_walks+len(self.graph[u].keys())
        self.N_walks=self.N_walks*self.N_iter
                
        self.walks=[[] for i in range(self.N_walks)]
        count=0#row index for self.walks
        g_iter=nx.nodes_iter(self.graph)
        for u in g_iter:
            N_neighbor=len(self.graph[u].keys())
            for i in range(self.N_iter):
                for k in range(N_neighbor):
                    if count%10000==0:
                        print(count,'/',self.N_walks,' ',time.time() - start)
                    self._graph_walk(count,u)
                    count+=1
                  

    def _graph_walk(self,idx,u):
        """Generates walks (sentences) sampled by an (unbiased) random walk over the networkx MultiGraph:
        node and edge names for the sentences.
        
        Parameters
        ----------
        idx : index of walk in self.walks that will form corpus for word2vec
        u : starting node
        """
        self.walks[idx]=['NA' for i in range(self.wl)]
        self.walks[idx][0]=u
        for i in range(1,self.wl):
            self.walks[idx][i]=random.choice(list(self.graph[u].keys() ) )
            u=self.walks[idx][i]       
            
    
    def word2vec(self,sg=1,size=10,window=3, min_count=1, negative=5, workers=4,sample=0):
        """source: https://radimrehurek.com/gensim/models/word2vec.html
        Parameters
        ----------
        sentences (iterable of iterables) : The sentences iterable can be simply a list of lists of tokens, 
            but for larger corpora, consider an iterable that streams the sentences directly from disk/network.
        sg (int {1, 0}) – Defines the training algorithm. If 1, skip-gram is employed; otherwise, CBOW is used.
        size (int) : Dimensionality of the feature vectors.
        window (int) : (aka context size) maximum distance between the current and predicted word within a sentence.
        min_count (int) : Ignores all words with total frequency lower than this.
        negative (int) : If > 0, negative sampling will be used, the int for negative specifies how many 
            “noise words” should be drawn (usually between 5-20). If set to 0, no negative sampling is used.
        workers (int) : Use these many worker threads to train the model (=faster training with multicore machines).
        sample (float) : The threshold for configuring which higher-frequency words are randomly downsampled,
        useful range is (0, 1e-5). parameter t in eq 5 Mikolov et al. Without edge labels: set to 0.
        """
        self.model = Word2Vec(sentences=self.walks,sg=sg,size=size,window=window, 
                              min_count=min_count,negative=negative, workers=workers,sample=sample) 
        
        
