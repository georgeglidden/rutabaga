import argparse
parser = argparse.ArgumentParser(description='LEGSNet Arguments') # collect arguments passed to file
parser.add_argument('--dataset', type=str,
                    help='Dataset to use for training.')
parser.add_argument('--model', type=str,
                    help='Model to run.')
parser.add_argument('--transform', type=str, default='scatter_cat',
                    help='Preprocessing to apply to dataset (scatter_cat is default)')
parser.add_argument('--no_cuda', action='store_true', default=False,
                    help='enables CUDA training')
parser.add_argument('--test_seed', type=int, default=4,
                    help='random seed for testing (default: 4)')
parser.add_argument('--val_seed', type=int, default=42,
                    help='random seed for validation (default: 4)')
parser.add_argument('--num_epochs', type=int, default=1000, metavar='N',
                    help='how many epochs?')
parser.add_argument('--diffusion_flexibility', type=int, default=4, metavar='N',
                    help='For LEGS Dynamo - the number of diffusion scales to be chosen each time.')
parser.add_argument('--splits', nargs='+', type=int, default = [8,1,1], help="The train-val-test split, supplied as a list of integers which sum to 10. The default is [8,1,1].")
parser.add_argument('--model_args', type=dict, default = {"epsilon": 1e-16, "num_layers": 60}, help="Additional model arguments, including epsilon and the number of layers.")
parser.add_argument('--out_file', type=str, default='out.pth',
                    help='Where to save the results')
args = parser.parse_args()
if __name__ == '__main__':
    train_model(args,args.out_file)