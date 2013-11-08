import sys
import re
import codecs
import collections
import csv
from library_parser.XMLLibraryParser import XMLLibraryParser
from library_parser.HashPathParser import HashPathParser
from UnicodeTools import UnicodeReader
from types import StringType, UnicodeType

def parse_tracks_from_export_list(input_fs):
    """
        Given an input file of Tab separated values, returns a generator of namedtuples containing the properties of 
        those tracks
        
        @type input_fs: StringType or UnicodeType
        @param input_fs: path of the Music.txt file generated from iPhone/iPod
        @rtype: GeneratorType
    """
    assert isinstance(input_fs, (StringType, UnicodeType))
    assert input_fs, 'no input file specified'

    f = open(input_fs, 'r+')
    csv_reader = UnicodeReader(f, dialect=csv.excel_tab, encoding="utf-16")
    Track = collections.namedtuple('Track', [x.replace(' ', '_') for x in csv_reader.next()])
    return (x for x in [Track(*line) for line in csv_reader])

# The bottleneck is this function, it will depend on how big the library.xml file is
def library_map(input_fs):
    """
        @type input_fs: StringType or UnicodeType
        @param input_fs: path of the "iTunes Music Library.xml" file
    """
    assert isinstance(input_fs, (StringType, UnicodeType))
    assert input_fs, 'no input file specified'

    return HashPathParser(input_fs).dictionary

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: python itunes_util.py {device_track_file} {itunes_library_file}'
    else:
        device_track_list = sys.argv[1]
        itunes_music_library = sys.argv[2]
    
    
        print 'loading itunes music library xml file...'
        lib_map = library_map(itunes_music_library)
    
        print 'parsing device track list file...'
        g_tracks = parse_tracks_from_export_list(device_track_list)
    
        print 'writing to playlist output.m3u...'
    
        not_found = 0
        target = open('output.m3u', 'w')
        for i, track in enumerate(g_tracks):
            hash_string = HashPathParser.construct_hash_key_from_namedtuple(track)
            try:
                print >> target, lib_map[hash_string]
            except KeyError:
                not_found += 1
                print 'could not find track: %s' % hash_string
                pass
    
        print 'done! %s/%s tracks not found' % (not_found, i + 1)
        target.close()
