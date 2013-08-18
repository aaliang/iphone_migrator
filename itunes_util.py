import sys
import re
import codecs
from collections import namedtuple
import csv
from types import StringType, UnicodeType

def parse_tracks(input_fs):
    '''
        Given an input file of Tab separated values, returns a generator of namedtuples containing the properties of those tracks
        
        @type input_fs: StringType or UnicodeType
        @rtype: GeneratorType
    '''
    assert isinstance(input_fs, (StringType, UnicodeType))
    assert input_fs, 'no input file specified'

    with codecs.open(input_fs, encoding='utf-16') as tsv:
        csv_reader = csv.reader(tsv, dialect="excel-tab")
        Track = namedtuple('Track', [x.replace(' ', '_').lower() for x in csv_reader.next()])
        
        return (Track(*line) for line in csv_reader)

if __name__ == '__main__':
    input_fs = sys.argv[1]
    g_tracks = parse_tracks(input_fs)