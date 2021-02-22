"""
A very small script which generates roots of the discriminants of the characteristic polynomial of the Q recursion matrix, which are said to have a mysterious affinity with the roots of the Q polynomials.
"""
import pandas as pd

class DiscriminantGenerator():
    def __init__(self, Q_dict, out_file = "disc.csv"):
        self.verbose = True
        self.out_file = out_file
        self.disc_dict = { }
        vertices = list(Q_dict.columns)[1:]  # the first entry is always "Unnamed = 0". We skip this.
        # convert the list of strings into a list of lists
        vertices = [[int(a) for a in gamma[1:-1].split(',')] for gamma in vertices]  # vertices p/q
        print(vertices)
        for v in vertices:
            # discriminant is Q(gamma)^2 + 4*dQ(gamma)
            Q_gamma = Q_dict[self.array_to_str(v)].to_list()
            Q_gamma_2 = self.poly_multiply(Q_gamma, Q_gamma)
            dQ_gamma = [(-1) ** v[0] * 4] + [0] * (v[1])
            disc = self.array_subtract(Q_gamma_2, dQ_gamma)
            self.disc_dict[self.array_to_str(v)] = self.trim_zeros(disc)# PART III: The polynomials have now been generated. All that remains is to cache them safely in the heart of a live volcano, i.e. a csv file, or not, if you're calling it directly
        if out_file:
            self.save_to_csv()
            print(f"Success! Generated {len(self.disc_dict.keys())} Q discriminant polynomials.")
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
        for i in self.disc_dict.values():
            if len(i) > max_len: max_len = len(i)
        # now cycle through the keys and update each value
        for key in self.disc_dict.keys():
            self.disc_dict[key] = [0]*(max_len - len(self.disc_dict[key])) + self.disc_dict[key]
        # finally, create DF and save
        df = pd.DataFrame(self.disc_dict)
        df.to_csv(self.out_file)
if __name__ == "__main__":
    Q_list = pd.read_csv("data/q_to_denom_30.csv")
    pg = DiscriminantGenerator(Q_list, out_file=f'data/discriminants_to_denom_30.csv')