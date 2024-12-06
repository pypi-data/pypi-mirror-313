#! /usr/bin/env python3

import sys
from pyliftover import LiftOver
import gzip

### Some config parameter
sourceVersion='hg19'
targetVersion='hg38'

infile = None
outfile = None

if __name__=="__main__":
    vcf_processor.tools.parse_args.parse_args()

    vcf_lines = []
    lo = LiftOver('hg19', 'hg38')

    file = infile
    if infile.name.endswith('.gz'):
        file = gzip.open(infile.name, 'rt')


    for line in file:
        if line.startswith('#'):
            if line.startswith('##reference'):
                print('##reference='+targetVersion, file=outfile)
                continue
            print(line.strip(), file=outfile)
            continue
        fields = line.split('\t')
        chr,pos, refBase, altBase = fields[0], fields[1], fields[3], fields[4]
        loc = lo.convert_coordinate(chr, int(pos))
        if loc is None:
            print('could not lift over location, it does not exist in the target version =>{}'.format(line.strip()), file=sys.stderr)
            continue
        if len(loc) != 1:
            print('could not lift over position because there are {} positions in the target =>{}'.format(len(loc), line.strip()), file=sys.stderr)
            continue
        fields[1] = str(loc[0][1])
        print("\t".join(fields).strip(), file=outfile)