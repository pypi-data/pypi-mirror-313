import os
import argparse
import itrm
import numpy as np

def main():
    # Parse the arguments.
    parser = argparse.ArgumentParser(
            description="Interactive terminal utilities")
    parser.add_argument("--func", "-f", type=str,
            choices=["iplot", "heat", "spy", "colors"], default="iplot",
            help="which function to use")
    parser.add_argument("--type", "-t", type=str,
            choices=[None, "txt", "csv", "bin"], default=None,
            help="file type of data file")
    parser.add_argument("--columns", "-c", type=int, default=0,
            help="number of columns in the data file")
    parser.add_argument("--xcolumns", "-x", type=int, default=1,
            help="number of columns belonging to the x axis")
    parser.add_argument("file", type=str, nargs="?", default=None,
            help="the data file to read")
    args = parser.parse_args()

    # Read in data.
    data = None
    if args.file is not None: 
        # Early exit if the file does not exist.
        if not os.path.exists(args.file):
            raise ValueError("The file does not exist.")

        # Check the extension.
        if args.type is None:
            _, extension = os.path.splitext(args.file)
            if extension.lower() == ".txt":
                args.type = "txt"
            if extension.lower() == ".csv":
                args.type = "csv"
            if extension.lower() == ".bin":
                args.type = "bin"

        # Read the data.
        if args.type == "bin":
            data_raw = np.fromfile(args.file)
            if args.columns == 0:
                args.columns = itrm.likely_columns(data_raw)
            data = data_raw.reshape((-1, args.columns)).T
        elif args.type == "csv":
            data = np.loadtxt(args.file, delimiter=",").T
        elif args.type == "txt":
            data = np.loadtxt(args.file, delimiter=None).T
    
    # Process the appropriate function.
    if (args.func == "iplot") and (data is not None):
        if (data.ndim > 1) and (data.shape[0] > 1):
            if args.xcolumns >= 1:
                itrm.iplot(data[:args.xcolumns], data[args.xcolumns:])
            else:
                itrm.iplot(data)
        else:
            itrm.iplot(data.flatten())
    elif (args.func == "heat") and (data is not None):
        itrm.heat(data)
    elif (args.func == "spy") and (data is not None):
        itrm.spy(data)
    elif args.func == "colors":
        itrm.colors()

if __name__ == "__main__":
    main()
