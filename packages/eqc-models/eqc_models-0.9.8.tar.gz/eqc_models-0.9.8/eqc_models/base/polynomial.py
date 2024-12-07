# (C) Quantum Computing Inc., 2024.
from typing import Tuple, Union, List
import numpy as np
from eqc_models.base.base import EqcModel
from eqc_models.base.operators import Polynomial
from eqc_models.base.constraints import ConstraintsMixIn

class PolynomialMixin:
    """This class provides an instance method and property that
    manage polynomial models.
    """

    @property
    def H(self) -> Tuple[np.ndarray, np.ndarray]:
        """ 
        Hamiltonian specified as a polynomial : coefficients, indices 
        
        indices are of the format [0, idx-1, ..., idx-d] which must be non-decreasing
        and each idx-j is a 1-based index of the variable which is a power in the 
        term. For a polynomial where the highest degree is 3 and specifying a term 
        such as x_1x_2, the index array is [0, 1, 2]. Another example, x_1^2x_2 is
        [1, 1, 2].

        """
        return self.coefficients, self.indices
    
    @H.setter
    def H(self, value : Tuple[np.ndarray, np.ndarray]):
        """ Set H directly as coefficients, indices """

        coefficients, indices = value
        self.coefficients = coefficients
        self.indices = indices

    @property
    def sparse(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.H
    
    def evaluate(self, solution : np.ndarray) -> float:
        """ 
        Evaluate polynomial at solution 
        
        :solution: 1-d numpy array with the same length as the number of variables

        returns a floating point value

        """

        value = self.polynomial.evaluate(np.array(solution))

        return value
    
    @property
    def dynamic_range(self) -> float:
        """
        Dynamic range is a measure in decibels of the ratio of the largest
        magnitude coefficient in a problem to the smallest non-zero magnitude
        coefficient. 

        The possible range of values are all greater than or equal to 0. The
        calculation is performed by finding the lowest non-zero of the 
        absolute value of all the coefficients, which could be empty. In that
        case, the dynamic range is undefined, so an exception is raised. If
        it is positive, then the maximum of the absolute values is divided
        by the lowest. The base-10 logarithm of that value is taken and mul-
        tiplied by 10. This is the dynamic range.

        Returns
        ----------
        
        float
        
        """
        H = self.H
        coefficients = np.array(H[0])
        try:
            lowest = np.min(np.abs(coefficients[coefficients!=0]))
        except IndexError:
            raise ValueError("Dynamic range of a Hamiltonian of all 0 is undefined")
        highest  = np.max(np.abs(coefficients))
        return 10*np.log10(highest / lowest)
        
class PolynomialModel(PolynomialMixin, EqcModel):
    """
    Polynomial model base class.

    Parameters
    ------------
    coefficients: An array of polynomial coeffients.
    indices: An array of polynomial indices.

    Examples
    ------------

    >>> coeffs = np.array([1, 2, 3])
    >>> indices = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1]])
    >>> from eqc_models.base.polynomial import PolynomialModel        
    >>> polynomial = PolynomialModel(coeffs, indices)
    >>> solution = np.array([1, 1, 1])
    >>> value = polynomial.evaluate(solution)
    >>> int(value)
    6
    >>> polynomial.H # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    (array([1, 2, 3]), array([[0, 0, 1],
       [0, 1, 1],
       [1, 1, 1]]))    
    """

    def __init__(self, coefficients : Union[List, np.ndarray], indices : Union[List, np.ndarray]) -> None:
        self.coefficients = coefficients
        self.indices = indices

    @property
    def polynomial(self) -> Polynomial:
        coefficients, indices = self.H
        return Polynomial(coefficients=coefficients, indices=indices)
    
class ConstrainedPolynomialModel(ConstraintsMixIn, PolynomialModel):
    """
    Constrained Polynomial model base class.

    Parameters
    ------------
    coefficients: An array of polynomial coeffients.
    indices: An array of polynomial indices.
    lhs: Left hand side of the linear constraints.
    rhs: Right hand side of the linear constraints.

    """

    def __init__(self, coefficients : Union[List, np.ndarray], indices : Union[List, np.ndarray],
                 lhs : np.ndarray, rhs: np.ndarray):
        self.coefficients = np.array(coefficients)
        self.indices = np.array(indices).astype(np.int64)
        self.max_order = self.indices.shape[1]
        self.lhs = lhs
        self.rhs = rhs

    @property
    def penalties(self):
        """ 
        Penalty terms specified as a polynomial: coefficients, indices 
        
        indices are of the format [0, idx-1, ..., idx-d] which must be non-decreasing
        and each idx-j is a 1-based index of the variable which is a power in the 
        term. For a polynomial where the highest degree is 3 and specifying a term 
        such as x_1x_2, the index array is [0, 1, 2]. Another example, x_1^2x_2 is
        [1, 1, 2].

        Only linear equality constraints are supported. Translate Ax=b into 
        penalties using the superclass.
        """

        indices = []
        coefficients = []
        def lpad(index):
            missing = self.max_order - len(index)
            if missing > 0:
                index = (0,) * missing + index
            assert len(index) > 0
            return np.array(index)
        Pl, Pq = super(ConstrainedPolynomialModel, self).penalties
        for i in range(Pl.shape[0]):
            if Pl[i] != 0:
                indices.append(lpad((0, i+1)))
                coefficients.append(Pl[i])
            for j in range(i, Pq.shape[1]):
                if Pq[i, j] != 0:
                    indices.append(lpad((i+1, j+1)))
                    value = Pq[i, j]
                    if i!=j:
                        value += Pq[j, i]
                    coefficients.append(value)
        return coefficients, indices
    
    def evaluatePenalties(self, solution : np.ndarray, include_offset=False) -> float:
        """
        Take the polynomial form of the penalties from the penalties property
        and evaluate the solution. The offset can be included by passing a True
        value to the `include_offset` keyword argument.

        Parameters
        -----------

        solution : np.ndarray
            Solution to evaluate for a penalty value
        include_offset : bool
            Optional argument indicating whether or not to include the offset value.

        Returns
        ---------

        Penalty value : float

        Examples 
        ---------

        >>> coeff = np.array([-1.0, -1.0])
        >>> indices = np.array([(0, 1), (0, 2)])
        >>> lhs = np.array([[1.0, 1.0]])
        >>> rhs = np.array([1.0])
        >>> model = ConstrainedPolynomialModel(coeff, indices, lhs, rhs)
        >>> sol = np.array([1.0, 1.0])
        >>> lhs@sol - rhs
        array([1.])
        >>> model.evaluatePenalties(sol)+model.offset
        1.0
        >>> model.evaluatePenalties(sol)
        0.0
        >>> model.evaluatePenalties(sol, include_offset=True)
        1.0
        
        """

# get the coefficients and indices for the penalty polynomial
# use the Polynomial operator to evaluate the solution
        coefficients, indices = self.penalties
        solution = np.array(solution, dtype=np.float64)
        polynomial = Polynomial(coefficients, indices)
        if include_offset:
            value = self.offset
        else:
            value = 0
        value += polynomial.evaluate(solution)
        return value
        
    def evaluateObjective(self, solution : np.ndarray) -> float:
        """
        Take the polynomial coeff and indices from constructor and evalute the 
        solution with it.

        Parameters
        -----------

        solution : np.ndarray
            Soluttion to evaluate the objective value

        Returns
        --------

        objective value : float

        """
        coefficients = self.coefficients
        indices = self.indices
        solution = np.array(solution, dtype=np.float64)
        polynomial = Polynomial(coefficients, indices)
        return polynomial.evaluate(solution)

    @property
    def H(self) -> Tuple[np.ndarray, np.ndarray]:
        """ Provide the sparse format for the Hamiltonian """

        p_coeff, p_indices = self.penalties
        coefficients, indices = self.coefficients, self.indices
        terms = {}
        alpha = self.alpha
        for index, coeff in zip(p_indices, p_coeff):
            index = tuple(index)
            assert len(index) > 1
            if index not in terms:
                terms[index] = alpha * coeff
            else:
                terms[index] += alpha * coeff
        for index, coeff in zip(indices, coefficients):
            index = tuple(index)
            if index not in terms:
                terms[index] = coeff
            else:
                terms[index] += coeff
        indices = [index for index in terms.keys()]
        indices.sort()
        coefficients = [terms[tuple(index)] for index in indices]
        return coefficients, indices
