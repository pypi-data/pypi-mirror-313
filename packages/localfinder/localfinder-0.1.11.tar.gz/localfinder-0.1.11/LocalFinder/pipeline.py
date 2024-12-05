# File: pipeline.py

import os
import json
import argparse
import pandas as pd
from LocalFinder.commands.bin import main as bin_tracks_main
from LocalFinder.commands.calc import main as calc_corr_main
from LocalFinder.commands.findreg import main as find_regions_main
from LocalFinder.utils import check_external_tools

def run_pipeline(args):
    # Ensure required external tools are available
    check_external_tools()

    # Step 1: Bin the tracks
    bin_output_dir = os.path.join(args.output_dir, 'binned_tracks')
    bin_args = argparse.Namespace(
        input_files=args.input_files,
        output_dir=bin_output_dir,
        bin_size=args.bin_size,
        chrom_sizes=args.chrom_sizes,
        chroms=args.chroms
    )
    bin_tracks_main(bin_args)

    # Step 2: Calculate correlation and enrichment
    binned_files = [
        os.path.join(bin_output_dir, os.path.basename(f).replace('.bam', f'.binSize{args.bin_size}.bedgraph')
                                   .replace('.sam', f'.binSize{args.bin_size}.bedgraph')
                                   .replace('.bedgraph', f'.binSize{args.bin_size}.bedgraph')
                                   .replace('.bigwig', f'.binSize{args.bin_size}.bedgraph')
                                   .replace('.bw', f'.binSize{args.bin_size}.bedgraph'))
        for f in args.input_files
    ]

    # Ensure that exactly two binned files are present
    if len(binned_files) < 2:
        print("Error: At least two binned files are required for correlation and enrichment calculation.")
        sys.exit(1)

    calc_output_dir = os.path.join(args.output_dir, 'correlation_enrichment')
    calc_args = argparse.Namespace(
        track1=binned_files[0],
        track2=binned_files[1],
        output_dir=calc_output_dir,
        method=args.method,
        method_params=json.dumps(args.method_params),  # Convert dict to JSON string
        bin_num=args.bin_num,
        step=args.step,
        chroms=args.chroms
    )
    calc_corr_main(calc_args)

    # Step 3: Find significantly different regions
    find_output_dir = os.path.join(args.output_dir, 'significant_regions')
    find_args = argparse.Namespace(
        track_E=os.path.join(calc_output_dir, 'track_ES.bedgraph'),
        track_C=os.path.join(calc_output_dir, 'track_locCor.bedgraph'),
        output_dir=find_output_dir,
        min_regionSize=args.min_regionSize,
        E_upPercentile=args.E_upPercentile,
        E_lowPercentile=args.E_lowPercentile,
        C_upPercentile=args.C_upPercentile,
        C_lowPercentile=args.C_lowPercentile,
        chroms=args.chroms
    )
    find_regions_main(find_args)

    print("Pipeline completed successfully.")
