"""
This module generates all Q polynomials Q(m/n) for n <= supplied max.
"""
import numpy as np
import pandas as pd
import time
class PolynomialGenerator():
    def __init__(self, out_file = "q.csv", max_integer=1, max_denominator=10):
        self.verbose = False
        self.out_file = out_file
        self.max_integer = max_integer
        self.max_denominator = max_denominator
        self.level_list = np.array([[0,1],[1,1]]) # the current level of the Farey graph is stored here for immediate computation of the next level. p/q is stored as [p,q]. We exclude 1/0 because it's only needed in the first stage
        self.q_dict = { # this is the great big fancy dictionary holding the keys to the q polynomials
            '[0,1]' : np.array([0]), # polynomials are represented as lists of the coefficients, in inverse order: [c_n ... c_2, c_1]
            '[1,1]' : np.array([1]), # we use numpy arrays because you can add them to each other and multiply them by integers. It's all very nice.
            '[1,0]' : np.array([1]),
            }
        # PART I: We have 0/1 and 1/1 -- but the user may specify some maximum integer larger than 1/1. This next bit computes those.
        max_in_level = 1
        while max_in_level < self.max_integer: # as long as the largest numerator (with denom of 1) is less than max_integer
            alpha = np.array([max_in_level - 1, 1])
            gamma = np.array([1,0])
            self.level_list = np.vstack([self.level_list,self.Q_new(alpha, gamma)])
            max_in_level += 1
        self.print(f"The initial levels listed are {self.level_list}")
        # PART II: With the initial levels fresh in hand, we enter the forest of recursion.
        # A brief description of the strategy behooves us:
        # Between each point now established in `levels`, we shall build two staircases, the first going leftward, the second rightward. Each of those stairs will then become the set of levels for a future iteration.
        start_time = time.time()
        while len(self.level_list) > 0: # as long as there are levels higher than the max denominator, continue building staircases.
            new_levels = []
            self.print("========= New Level =========")
            for mom, dad in zip(self.level_list[:-1], self.level_list[1:]): # iterate through parents
                self.print(f"Currently on parents {mom} and {dad}")
                if max([mom,dad], key=lambda x:x[1])[1] >= max_denominator:
                    pass
                elif self.array_to_str(mom - dad) in self.q_dict: # if this pair is part of a previous downward staircase
                    downstairs = self.staircase(mom,dad)
                    upstairs = self.staircase(downstairs[1],mom) # start with the midpoint
                    new_levels.extend(upstairs[::-1])  # flipped to put smallest first, and with the parent chopped off.
                    new_levels.extend(downstairs[2:])  # to skip the repeated middle element present in both
                else:
                    upstairs = self.staircase(dad, mom)
                    downstairs = self.staircase(upstairs[1], dad)
                    new_levels.extend(upstairs[1:][::-1]) # flipped to put smallest first, and with the parent chopped off.
                    new_levels.extend(downstairs[1:])# to skip the repeated middle element present in both
                self.print(f"upstairs: {upstairs} downstairs {downstairs}. new_levels {self.decimalize(new_levels)}")
            self.print(f"after going down all the stairs, we have new_levels {new_levels} ")
            self.level_list = np.array(new_levels)
        stop_time = time.time()
        # PART III: The polynomials have now been generated. All that remains is to cache them safely in the heart of a live volcano, i.e. a csv file, or not, if you're calling it directly
        if out_file:
            self.save_to_csv()
            print(f"Success! Generated {len(self.q_dict.keys())} Q polynomials in {stop_time - start_time} seconds.")

    def staircase(self, mom, dad):
        # takes parents, sends one down a staircase of "children" towards the other --  walking "down the triangle" from mom towards dad.
        # self.print(f"building staircase from {mom} to {dad}")
        stairs = [mom]
        while stairs[-1][1] < self.max_denominator:
            grandma = stairs[-1] - dad
            child = self.Q_new(grandma,dad)
            stairs.append(child)
        return stairs


    def Q_new(self, alpha, gamma):
        """To find a new, unseen q polynomial. Automatically adds the resulting polynomial to Q_dict and returns the coordinate p/q """
        # Q(alpha +2 gamma) = (-1)^p x^q Q(alpha)
        self.print(f"Finding new polynomial from alpha {alpha} and gamma {gamma}")
        p_q = alpha+gamma*2
        first_term = np.concatenate(((-1)**(p_q[0]+1) * self.Q(alpha),np.zeros(p_q[1], dtype=int)))
        second_term = self.poly_multiply(self.Q(alpha+gamma), self.Q(gamma))
        # self.print(f"For {p_q}, We have first term {first_term} and second term {second_term}")
        result = self.poly_add(first_term,second_term)
        # add the polynomial, and the fraction, to the relevant internal lists.
        self.q_dict[self.array_to_str(p_q)] = np.trim_zeros(result, trim='f')
        # self.level_list = np.vstack([self.level_list, p_q])
        return p_q
    def poly_multiply(self, a, b):
        # find out which polynomial is shorter and prepend zeros to the front
        largest_length = np.max([len(a),len(b)])
        new_a = np.concatenate([np.zeros(largest_length-len(a), dtype=int),a])
        new_b = np.concatenate([np.zeros(largest_length-len(b), dtype=int),b])
        # polynomial multiplication is equivalent to taking the outer product of these polynomial vectors and summing along the "inverse" diagonals
        outer = np.outer(new_a,new_b)[:,::-1]
        diagonal_sums = [outer.trace(offset=-o) for o in range(-len(outer)-1,len(outer))]
        return np.array(diagonal_sums)

    def poly_add(self, a, b):
        largest_length = np.max([len(a), len(b)])
        new_a = np.concatenate([np.zeros(largest_length - len(a), dtype=int), a])
        new_b = np.concatenate([np.zeros(largest_length - len(b), dtype=int), b])
        return new_a + new_b
    def Q(self,x):
        return self.q_dict[self.array_to_str(x)]
    def print(self, data):
        if self.verbose:
            print(data)
    def array_to_str(self,array):
        # these are all of length 2, thank god.
        return f"[{array[0]},{array[1]}]"
    def decimalize(self, array_of_pqs):
        outs = []
        for pq in array_of_pqs:
            if pq[1] == 0:
                outs.append('inf')
            else:
                outs.append(pq[0]/pq[1])
        return outs
    def save_to_csv(self):
        # save the q_dict to a csv file with pandas
        # to do this, we'll need to convert each numpy array to the same length by prepending zeros.
        max_len = 1
        for i in self.q_dict.values():
            if len(i) > max_len: max_len = len(i)
        # now cycle through the keys and update each value
        for key in self.q_dict.keys():
            self.q_dict[key] = np.concatenate([np.zeros(max_len - len(self.q_dict[key]), dtype=int), self.q_dict[key]])
        # finally, create DF and save
        df = pd.DataFrame(self.q_dict)
        df.to_csv(self.out_file)
if __name__ == "__main__":
    pg = PolynomialGenerator(max_integer=1, max_denominator=100, out_file='data/q_to_denom_100.csv')
