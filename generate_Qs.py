"""
This module generates all Q polynomials Q(m/n) for n <= supplied max.
"""
import pandas as pd
import time
class PolynomialGenerator():
    def __init__(self, out_file = "q.csv", max_integer=1, max_denominator=10):
        self.verbose = True
        self.out_file = out_file
        self.max_integer = max_integer
        self.max_denominator = max_denominator
        self.level_list = [[0,1],[1,1]] # the current level of the Farey graph is stored here for immediate computation of the next level. p/q is stored as [p,q]. We exclude 1/0 because it's only needed in the first stage
        self.q_dict = { # this is the great big fancy dictionary holding the keys to the q polynomials
            '[0,1]' : [1], # polynomials are represented as lists of the coefficients, in inverse order: [c_n ... c_2, c_1]
            '[1,1]' : [1], # numpy can't handle our larger coefficients, so we handle all of the coefficients as python integers (which have unlimited precision) ~~we use numpy arrays because you can add them to each other and multiply them by integers. It's all very nice.~~
            '[1,0]' : [0],
            }
        # PART I: We have 0/1 and 1/1 -- but the user may specify some maximum integer larger than 1/1. This next bit computes those.
        max_in_level = 1
        while max_in_level < self.max_integer: # as long as the largest numerator (with denom of 1) is less than max_integer
            alpha = [max_in_level - 1, 1]
            gamma = [1,0]
            self.level_list = self.level_list.append(self.Q_new(alpha, gamma))
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
                elif self.array_to_str(self.array_subtract(mom, dad)) in self.q_dict: # if this pair is part of a previous downward staircase
                    downstairs = self.staircase(mom,dad)
                    upstairs = self.staircase(downstairs[1],mom) # start with the midpoint
                    new_levels.extend(upstairs[::-1])  # flipped to put smallest first, and with the parent chopped off.
                    new_levels.extend(downstairs[2:])  # to skip the repeated middle element present in both
                else:
                    upstairs = self.staircase(dad, mom)
                    downstairs = self.staircase(upstairs[1], dad)
                    new_levels.extend(upstairs[1:][::-1]) # flipped to put smallest first, and with the parent chopped off.
                    new_levels.extend(downstairs[1:])# to skip the repeated middle element present in both
                # self.print(f"upstairs: {upstairs} downstairs {downstairs}. new_levels {self.decimalize(new_levels)}")
            self.print(f"after going down all the stairs, we have new_levels {new_levels} ")
            self.level_list = new_levels
        stop_time = time.time()
        # PART III: The polynomials have now been generated. All that remains is to cache them safely in the heart of a live volcano, i.e. a csv file, or not, if you're calling it directly
        if out_file:
            self.save_to_csv()
            print(f"Success! Generated {len(self.q_dict.keys())} Q polynomials in {stop_time - start_time} seconds.")

    def staircase(self, mom, dad):
        # takes parents, sends one down a staircase of "children" towards the other --  walking "down the triangle" from mom towards dad.
        self.print(f"building staircase from {mom} to {dad}")
        stairs = [mom]
        while stairs[-1][1] < self.max_denominator:
            grandma = self.array_subtract(stairs[-1], dad)
            child = self.Q_new(grandma,dad)
            stairs.append(child)
            print(child)
        return stairs

    def Q_new(self, alpha, gamma):
        """To find a new, unseen q polynomial. Automatically adds the resulting polynomial to Q_dict and returns the coordinate p/q """
        # Q(alpha +2 gamma) = -dQ(gamma) Q (alpha) + ... =-(-1)^gamma[0] x^gamma[1] * Q(alpha) + ...
        p_q = self.array_add(alpha, self.multiply_by_constant(gamma, 2))
        self.print(f"Finding new polynomial {p_q} from alpha {alpha} and gamma {gamma}")
        # first_term = np.concatenate(((-1)**(gamma[0]+1) * self.Q(alpha),np.zeros(gamma[1], dtype=int)))
        first_term = self.multiply_by_constant(self.Q(alpha),(-1)**(gamma[0]+1)) + [0]*gamma[1]
        second_term = self.poly_multiply(self.Q(self.array_add(alpha,gamma)), self.Q(gamma))
        self.print(f"For {p_q}, We have first term {first_term} and second term {second_term}")
        result = self.array_add(first_term,second_term)
        self.print(f"For {p_q}, We have result {self.trim_zeros(result)}")
        # add the polynomial, and the fraction, to the relevant internal lists.
        self.q_dict[self.array_to_str(p_q)] = self.trim_zeros(result)
        # if self.array_to_str(p_q) == self.array_to_str([1, 97]): # use this to track down parentage
        #     self.print(f"Finding new polynomial {p_q} from alpha {alpha} and gamma {gamma}")
        #     self.print(f"For {p_q}, We have first term {first_term} and second term {second_term}")
        #     self.print(f"For {p_q}, We have result {np.trim_zeros(result, trim='f')}")
        #     a = first_term
        #     b = second_term
        #     largest_length = max(len(a), len(b))
        #     print("largest length", largest_length)
        #     new_a = [0]*(largest_length - len(a)) + a
        #     new_b = np.concatenate([np.zeros(largest_length - len(b), dtype=int), b])
        #     print("new a ", new_a, "new b ", new_b)
        #     for i in range(largest_length):
        #         print(i, new_a[i] + new_b[i], '=', new_a[i],'+', new_b[i])
        #     print(type(new_a[0]))
        # self.level_list = np.vstack([self.level_list, p_q])
        return p_q
    def trim_zeros(self, array):
        # cuts off leading zeros
        i = 0
        sum = array[i]
        while sum == 0:
            i += 1
            sum += abs(array[i])
        return array[i:]

    def multiply_by_constant(self, array, c):
        return [ a*c for a in array]
    def poly_multiply(self, a, b):
        # find out which polynomial is shorter and prepend zeros to the front
        # largest_length = max(len(a),len(b))
        # new_a = [0]*(largest_length-len(a)) + a
        # new_b = [0] * (largest_length - len(b)) + b
        # new_a = np.concatenate([np.zeros(largest_length-len(a), dtype=int),a])
        # new_b = np.concatenate([np.zeros(largest_length-len(b), dtype=int),b])
        # Nifty python implementation from Hugh Bothwell
        res = [0] * (len(a) + len(b) - 1)
        for o1, i1 in enumerate(a):
            for o2, i2 in enumerate(b):
                res[o1 + o2] += i1 * i2
        # polynomial multiplication is equivalent to taking the outer product of these polynomial vectors and summing along the "inverse" diagonals
        # outer = np.outer(new_a,new_b)[:,::-1]
        # diagonal_sums = [outer.trace(offset=-o) for o in range(-len(outer)-1,len(outer))]
        return res

    def array_add(self, a, b):
        largest_length = max(len(a),len(b))
        new_a = [0]*(largest_length - len(a)) + a
        new_b = [0]*(largest_length - len(b)) + b
        added = [new_a[i] + new_b[i] for i in range(largest_length)]
        # largest_length = np.max([len(a), len(b)])
        # new_a = np.concatenate([np.zeros(largest_length - len(a), dtype=int), a])
        # new_b = np.concatenate([np.zeros(largest_length - len(b), dtype=int), b])
        # return new_a + new_b
        return added
    def array_subtract(self, a, b):
        largest_length = max(len(a),len(b))
        new_a = [0]*(largest_length - len(a)) + a
        new_b = [0]*(largest_length - len(b)) + b
        added = [new_a[i] - new_b[i] for i in range(largest_length)]
        # largest_length = np.max([len(a), len(b)])
        # new_a = np.concatenate([np.zeros(largest_length - len(a), dtype=int), a])
        # new_b = np.concatenate([np.zeros(largest_length - len(b), dtype=int), b])
        # return new_a + new_b
        return added
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
            self.q_dict[key] = [0]*(max_len - len(self.q_dict[key])) + self.q_dict[key]
        # finally, create DF and save
        df = pd.DataFrame(self.q_dict)
        df.to_csv(self.out_file)
if __name__ == "__main__":
    max_denom = 100
    pg = PolynomialGenerator(max_integer=1, max_denominator=max_denom, out_file=f'data/q_to_denom_{max_denom}.csv')