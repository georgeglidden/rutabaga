"""
This module generates all Q polynomials Q(m/n) for n <= supplied max.
"""
import numpy as np
class PolynomialGenerator():
    def __init__(self, filename = "q.polys", max_integer=1, max_denominator=100):
        self.verbose = True
        self.max_integer = max_integer
        self.max_denominator = max_denominator
        self.level_list = np.array([[0,1],[1,0]]) # the current level of the Farey graph is stored here for immediate computation of the next level. p/q is stored as [p,q]. We exclude 1/0 because it's only needed in the first stage
        self.q_dict = { # this is the great big fancy dictionary holding the keys to the q polynomials
            '[0 1]' : np.array([0]), # polynomials are represented as lists of the coefficients, in inverse order: [c_n ... c_2, c_1]
            '[1 1]' : np.array([1]), # we use numpy arrays because you can add them to each other and multiply them by integers. It's all very nice.
            '[1 0]' : np.array([1])
        }
        # PART I: We have 0/1 and 1/1 -- but the user may specify some maximum integer larger than 1/1. This next bit computes those.
        max_in_level = 1
        while max_in_level < self.max_integer: # as long as the largest numerator (with denom of 1) is less than max_integer
            alpha = np.array([max_in_level - 1, 1])
            gamma = np.array([1,0])
            self.Q_new(alpha, gamma)
            max_in_level += 1
        self.print(f"The initial levels listed are {self.level_list}")
    #
    # def generate(self):


    def Q_new(self, alpha, gamma):
        """To find a new, unseen q polynomial. Automatically adds the resulting polynomial to Q_dict and to the current level_list """
        # Q(alpha +2 gamma) = (-1)^p x^q Q(alpha)
        self.print(f"Finding new polynomial from alpha {alpha} and gamma {gamma}")
        p_q = alpha+gamma*2
        first_term = np.concatenate(((-1)**(p_q[0]+1) * self.Q(alpha),np.zeros(p_q[1], dtype=int)))
        second_term = self.poly_multiply(self.Q(alpha+gamma), self.Q(gamma))
        self.print(f"We have first term {first_term} and second term {second_term}")
        result = self.poly_add(first_term,second_term)
        # add the polynomial, and the fraction, to the relevant internal lists.
        self.q_dict[str(p_q)] = result
        self.level_list = np.vstack([self.level_list, p_q])
        return p_q
    def poly_multiply(self, a, b):
        # find out which polynomial is shorter and prepend zeros to the front
        largest_length = np.max([len(a),len(b)])
        new_a = np.concatenate([np.zeros(largest_length-len(a), dtype=int),a])
        new_b = np.concatenate([np.zeros(largest_length-len(b), dtype=int),b])
        # polynomial multiplication is equivalent to taking the outer product of these polynomial vectors and summing along the "inverse" diagonals
        outer = np.outer(new_a,new_b)[:,::-1]
        diagonal_sums = [outer.trace(offset=o) for o in -range()]
    def poly_add(self, a, b):
        largest_length = np.max([len(a), len(b)])
        new_a = np.concatenate([np.zeros(largest_length - len(a), dtype=int), a])
        new_b = np.concatenate([np.zeros(largest_length - len(b), dtype=int), b])
        return new_a + new_b
    def Q(self,x):
        return self.q_dict[str(x)]
    def print(self, data):
        if self.verbose:
            print(data)


pg = PolynomialGenerator(max_integer=5)
print(pg.q_dict)
