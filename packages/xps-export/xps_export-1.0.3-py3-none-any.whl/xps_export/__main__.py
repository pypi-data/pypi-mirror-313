import os
import argparse
from xps_export import xpsexport

def main():
    """
    Command-line interface for the file parser using argparse.
    """
    parser = argparse.ArgumentParser(
        description="Utility for parsing files to XML.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_file",nargs="?", default=None, help="Path to the output file.")
    parser.add_argument("--skip-plots", action="store_true",
                        help="Generate plots.")
    parser.add_argument("--skip-csv", action="store_true",
                        help="Generate CSV files.")

    args = parser.parse_args()

    # Validate input file
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        return

    if args.output_file is None:
        args.output_file = os.path.splitext(args.input_file)[0]

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"When utilizing xps-export, please cite it using the following DOI: 10.5281/zenodo.14269021\nExporting data from {args.input_file} to {args.output_file}.zip");    

    xpsexport.parse_file_to_xml(args.input_file, args.output_file,
                      not(args.skip_plots), not(args.skip_csv))

    print(f"Export finished.");    


if __name__ == "__main__":
    main()
    
