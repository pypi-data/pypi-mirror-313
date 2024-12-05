# File: commands/find_significantly_different_regions.py

import os
from LocalFinder.utils import find_significantly_different_regions

def main(args):
    track_E = args.track_E
    track_C = args.track_C
    output_dir = args.output_dir
    min_regionSize = args.min_regionSize
    E_upPercentile = args.E_upPercentile
    E_lowPercentile = args.E_lowPercentile
    C_upPercentile= args.C_upPercentile
    C_lowPercentile = args.C_lowPercentile
    chroms = args.chroms

    os.makedirs(output_dir, exist_ok=True)

    find_significantly_different_regions(
        track_enrichment_file=track_E,
        track_correlation_file=track_C ,
        output_dir=output_dir,
        min_regionSize=min_regionSize,
        enrichment_high_percentile=E_upPercentile,
        enrichment_low_percentile=E_lowPercentile,
        corr_high_percentile=C_upPercentile,
        corr_low_percentile=C_lowPercentile,
        chroms=chroms
    )
