import sys
import re
import codecs
from collections import namedtuple
from library_parser.XMLLibraryParser import XMLLibraryParser
from library_parser.HashPathParser import HashPathParser
# from itunes_library_parser import ItunesXMLParser
import csv
from types import StringType, UnicodeType

def parse_tracks_from_export_list(input_fs):
    '''
        Given an input file of Tab separated values, returns a generator of namedtuples containing the properties of those tracks
        
        @type input_fs: StringType or UnicodeType
        @param input_fs: path of the Music.txt file generated from iPhone/iPod
        @rtype: GeneratorType
    '''
    assert isinstance(input_fs, (StringType, UnicodeType))
    assert input_fs, 'no input file specified'

    with codecs.open(input_fs, encoding='utf-16') as tsv:
        csv_reader = csv.reader(tsv, dialect="excel-tab")
        Track = namedtuple('Track', [x.replace(' ', '_') for x in csv_reader.next()])
        
        return (x for x in [Track(*line) for line in csv_reader])

def library_map(input_fs):
    '''
        @type input_fs: StringType or UnicodeType
        @param input_fs: path of the "iTunes Music Library.xml" file
    '''
    assert isinstance(input_fs, (StringType, UnicodeType))
    assert input_fs, 'no input file specified'

    return HashPathParser(input_fs).dictionary

# TODO move either this chunk below, or the ones above to separate file
if __name__ == '__main__':
    device_track_list = sys.argv[1]
    itunes_music_library = sys.argv[2]

    print 'loading itunes music library xml file...'
    lib_map = library_map(itunes_music_library)

    print 'parsing device track list file...'
    g_tracks = parse_tracks_from_export_list(device_track_list)

    target = open('output.m3u', 'w')

    print 'writing to playlist output.m3u...'

    not_found = 0
    for i, track in enumerate(g_tracks):
        hash_string = HashPathParser.construct_hash_key_from_namedtuple(track)
        try:
            print >> target, lib_map[hash_string]
        except KeyError:
            not_found += 1
            print 'could not find track: %s' % hash_string

    print 'done! %s/%s tracks not found' % (not_found, i + 1)
    target.close()
    print 'done'
