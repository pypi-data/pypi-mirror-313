# (C) Quantum Computing Inc., 2024.
import numpy as np
import networkx as nx
from .base import NodeModel


class MaxKCutModel(NodeModel):

    def __init__(self, G : nx.Graph, k : int):
        super(MaxKCutModel, self).__init__(G)
        self.k = k
        self.lhs = None
        self.rhs = None
        self._objective = None
        self._J = None
        self._C = None

    def decode(self, solution: np.ndarray) -> np.ndarray:
        """ Override the default decoding to use a the max cut metric to determine a solution """

        # only one partition per node can be selected
        # rather than the same cutoff per node, use the max value per partition
        decoded_solution = np.zeros_like(solution, dtype=np.int32)
        k = self.k
        for i, u in enumerate(self.variables):
            idx = slice(k*i, k*(i+1))
            spins = solution[idx]
            mx = np.max(spins)
            for j in range(k):
                if spins[j] == mx:
                    decoded_solution[k*i+j] = 1
                    break
        return decoded_solution
    
    def partition(self, solution):
        """ Return a dictionary with the partition number of each node """
        k = self.k
        n = len(self.variables)
        partition_num = {}
        for i, u in enumerate(self.variables):
            for j in range(k):
                if solution[i*k+j] == 1:
                    partition_num[u] = j+1
        return partition_num
    
    def getCutSize(self, partition):
        cut_size = 0
        for u, v in self.G.edges:
            if partition[u]!=partition[v]:
                cut_size += 1
        return cut_size

    def _build_objective(self):
        
        node_map = self.variables
        G = self.G
        m = len(G.nodes)
        n = self.k * m
        # construct the quadratic portion of the objective
        # the linear portion is 0
        objective = np.zeros((n, n), dtype=np.float32)
        # increment the joint variable terms indicating the nodes are in different sets
        pairs = [(i, j) for i in range(self.k) for j in range(self.k) if i!=j]
        for u, v in G.edges:
            i = node_map.index(u)
            j = node_map.index(v)
            ibase = i * self.k
            jbase = j * self.k
            for incr1, incr2 in pairs:
                idx1 = ibase + incr1
                idx2 = jbase + incr2
                objective[idx1, idx2] += -1
        self._objective = (np.zeros((n, 1)), objective)

    def _build_constraints(self):

        node_map = self.variables
        G = self.G
        m = len(G.nodes)
        n = self.k * m

        # build the constraints
        A = np.zeros((m, n))
        b = np.ones((m,))
        for u in G.nodes:
            i = node_map.index(u)
            ibase = i * self.k
            A[i, ibase:ibase+self.k] = 1
        self.lhs = A
        self.rhs = b

    def build(self, multiplier=None):
        """ Create the constraints and objective and Hamiltonian """

        # there are k * m variables in this problem where m is the number of nodes in the graph
        node_map = self.variables
        G = self.G
        m = len(G.nodes)
        n = self.k * m
        self.upper_bound = np.ones((n,))
        
        self._build_objective()
        if multiplier is None:
            multiplier = np.max(np.abs(self._objective[1]))
        self._build_constraints()

        self._C, self._J = self.buildH(multiplier)
        self.sum_constraint = m

    def buildH(self, multiplier):
        """ Combine the objective and penalties using the multiplier """

        objC, objJ = self.objective
        lhs, rhs = self.constraints
        Pq = lhs.T@lhs
        Pl = -2 * rhs.T@lhs
        offset = rhs.T@rhs
        n = self.n
        J = np.zeros((n, n), np.float32)
        C = np.zeros([n, 1], np.float32)
        C += objC
        J[:,:] += objJ
        C += multiplier * Pl.reshape((n, 1))
        J[:,:] += multiplier * Pq
        return C, J

    @property
    def constraints(self):
        """ Return LHS, RHS in numpy matrix format """
        if self.rhs is None:
            self.build()
        return self.lhs, self.rhs

    @property
    def objective(self):
        """ Return the quadratic objective as NxN+1 matrix """

        if self._objective is None:
            self.build()
        return self._objective

    @property
    def H(self):
        """ Return the Hamiltonian as parts C, J """

        if self._C is None:
            self.build()
        return self._C, self._J
    
class WeightedMaxKCutModel(MaxKCutModel):

    def __init__(self, G: nx.Graph, k: int, weight_label : str = "weight"):
        super().__init__(G, k)

        self.weight_label = weight_label
    
    def _build_objective(self):
        
        node_map = self.variables
        G = self.G
        m = len(G.nodes)
        n = self.k * m
        # construct the quadratic portion of the objective
        # the linear portion is 0
        objective = np.zeros((n, n), dtype=np.float32)
        # increment the joint variable terms indicating the nodes are in different sets
        pairs = [(i, j) for i in range(self.k) for j in range(self.k) if i!=j]
        for u, v in G.edges:
            i = node_map.index(u)
            j = node_map.index(v)
            ibase = i * self.k
            jbase = j * self.k
            for incr1, incr2 in pairs:
                idx1 = ibase + incr1
                idx2 = jbase + incr2
                objective[idx1, idx2] += G[u][v][self.weight_label]
        self._objective = (np.zeros((n, 1)), objective)

    def getCutSize(self, partition):
        cut_size = 0
        for u, v in self.G.edges:
            if partition[u]!=partition[v]:
                cut_size += self.G[u][v][self.weight_label]
        return cut_size
