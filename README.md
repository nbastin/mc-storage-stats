Small library and command line tool for offline analysis of the contents of containers in a set of minecraft chunks, intended for tracking storage system inventories over time.

# Getting Started

Clone this repository and install it in a Python 3.6 (or later) environment:

```
git clone https://github.com/nbastin/mc-storage-stats.git
cd mc-storage-stats/
pip install .
```

You will also need a file that lists the chunks (in their regions) that you want to analyze.  This is currently only specified in the format that MCASelector uses for selection exports:

```
0;-1;0;-1
0;-1;3;-7
0;-1;3;-6
0;-1;1;-7
```

The first two fields are the region, and the second two are the chunk.

# Usage

The command-line tool `storage-totals` will take your region data directory and the list of chunk selections, and output total counts for each distinct item it finds in a container in JSON or CSV format.  Shulkers within other containers are also searched.

```
usage: storage-totals [-h] [--output-type OTYPE] [--outfile OUTFILE]
                      regiondir chunk_export

positional arguments:
  regiondir            Path to directory containing region files
  chunk_export         Path to MCASelector chunk selection export

optional arguments:
  -h, --help           show this help message and exit
  --output-type OTYPE  Type of output data (JSON and CSV currently supported)
  --outfile OUTFILE    Name of output file (minus extension).
```

# Notes

Potions are written out in the format ```<id>(<effect_id>)```:

```minecraft:potion(minecraft:long_fire_resistance)```

This format may change in the future to something less ugly.

