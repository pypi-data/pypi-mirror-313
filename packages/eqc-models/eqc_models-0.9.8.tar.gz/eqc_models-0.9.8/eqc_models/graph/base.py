# (C) Quantum Computing Inc., 2024.
from typing import List, Set
import networkx as nx
from ..base import QuadraticModel

class GraphModel(QuadraticModel):
    """ """
    def __init__(self, G : nx.Graph):
        self.G = G
        self.linear_objective, self.quad_objective = self.costFunction()

class NodeModel(GraphModel):
    """ 
    Base class for a model where the decision variables correspond to
    the graph nodes. 
    
    """

    @property
    def variables(self) -> List[str]:
        """ Provide a variable name to index lookup; order enforced by sorting the list before returning """
        names = [node for node in self.G.nodes]
        names.sort()
        return names

    def costFunction(self):
        """ 
        Parameters
        -------------
        
        None
        
        Returns
        --------------
        
        :C: linear operator (vector array of coefficients) for cost function
        :J: quadratic operator (N by N matrix array of coefficients ) for cost function
        
        """
        raise NotImplementedError("NodeModel does not implement costFunction")
    
    def modularity(self, partition : Set[Set]) -> float:
        """ Calculate modularity from a partition (set of communities) """
        
        return nx.community.modularity(self.G, partition)

class TwoPartitionModel(NodeModel):
    """ 
    Base class for a generic graph paritioning model. Override the
    cost function and evaluation methods to implement a two-partition
    algorithm.
    
    """

class EdgeModel(GraphModel):
    """ Create a model where the variables are edge-based """

    @property
    def variables(self) -> List[str]:
        """ Provide a variable name to index lookup; order enforced by sorting the list before returning """
        names = [f"({u},{v})" for u, v in self.G.edges]
        names.sort()
        return names
