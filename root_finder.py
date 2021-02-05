"""
Given a csv file, RootFinder finds the roots of polynomials.
It's designed to operate in a transient state, loading discovered roots into a csv file in batches to as to avoid overloading memory.
"""
import mpmath
import pandas as pd
import numpy as np
from tqdm import tqdm, trange
from csv import writer
class RootFinder():
    def __init__(self, input_file=None, input_data=None, precision=100, maxsteps=100, batch_size=100):
        """
        Initializes the rootfinder. Supply
        :param input_file: The path to a csv file containing polynomials of Q roots. Default: None.
        :param input_data: Alternatively, pandas dataframe containing the polynomials. Default: None.
        :param precision: The floating point precision for the root calculations. Default 100.
        :param batch_size: number of polynomials to process before offloading results.
        """
        mpmath.mp.dps = precision
        self.pols = input_data
        self.maxsteps = maxsteps
        self.roots_list = pd.DataFrame(columns=['real','imaginary','p/q','error'])
        self.batch_size = batch_size
        if input_file:
            self.pols = pd.read_csv(input_file)
        else:
            if input_data is None:
                print("You need to specify either input_file or pass a dataframe as input_data")
                raise Exception
            self.pols = input_data
    def generate_roots(self, polly):
        """
        Given a polynomial, cleans it up (removes leading zeros), and generates roots.
        Returns roots as list of tuples
        """
        polly = np.trim_zeros(polly)
        # print(polly)
        if len(polly)<2: # no roots!
            return [], None
        roots, error = mpmath.polyroots(polly, error=True, maxsteps=self.maxsteps)
        return roots, error

    def generate_to(self, output_file):
        """
        Goes through the inputted polynomials, feeds them to generate_roots, and saves in increments to avoid overloading memory.
        :return:
        """
        roots_list = pd.DataFrame(columns=['real', 'imaginary', 'q', 'error'])
        for i in trange(len(self.pols.columns)-1):
            key = self.pols.columns[i+1] # ignore the "unnamed = 0" string.
            q = key.strip('][').split(',')[1]
            polly = self.pols[key].to_numpy()
            roots, error = self.generate_roots(polly)
            # print(roots)
            for root in roots:
                # print(roots_list)
                roots_list = roots_list.append({'real':str(root.real),
                                   'imaginary':str(root.imag),
                                   'q':str(q),
                                   'error':str(error)
                                   }, ignore_index=True)
            if i % self.batch_size == 0:  # every batch_size iterations, save progress.
                # print("save triggered!")
                if i == 0:
                    roots_list.to_csv(output_file) # create the file, if this is the first run.
                else: # otherwise, append to the file and delete the existing roots from memory.
                    # print("before deleting",roots_list)
                    roots_list.to_csv(output_file, mode='a')
                    del roots_list
                    roots_list = pd.DataFrame(columns=['real', 'imaginary', 'q', 'error'])
        roots_list.to_csv(output_file, mode='a')
        print(roots_list)


if __name__=='__main__':
    rf = RootFinder(input_file='data/q_to_denom_50.csv', precision=50, maxsteps=1000)
    rf.generate_to('data/roots_50.csv')