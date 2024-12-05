# File: commands/bin_tracks.py

import os
from LocalFinder.utils import process_and_bin_file, check_external_tools

def main(args):
    input_files = args.input_files
    output_dir = args.output_dir
    bin_size = args.bin_size
    chrom_sizes = args.chrom_sizes
    chroms = args.chroms

    # Ensure required external tools are available
    check_external_tools()

    os.makedirs(output_dir, exist_ok=True)

    for input_file in input_files:
        print(f"Processing {input_file}...")
        # Determine output file name
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, base_name)
        output_file = output_file.replace('.bam', f'.binSize{bin_size}.bedgraph') \
                                 .replace('.sam', f'.binSize{bin_size}.bedgraph') \
                                 .replace('.bedgraph', f'.binSize{bin_size}.bedgraph') \
                                 .replace('.bigwig', f'.binSize{bin_size}.bedgraph') \
                                 .replace('.bw', f'.binSize{bin_size}.bedgraph')

        process_and_bin_file(
            input_file=input_file,
            output_file=output_file,
            bin_size=bin_size,
            chrom_sizes=chrom_sizes,
            chroms=chroms
        )
        print(f"Binned file saved to {output_file}")
