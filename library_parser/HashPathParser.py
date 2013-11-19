# Date created 8/18/2013
# @author aliang

# TODO: Improve XMLLibraryParser

import re
from collections import defaultdict
from library_parser.XMLLibraryParser import XMLLibraryParser
from HTMLParser import HTMLParser


class HashPathParser(XMLLibraryParser):
   '''
     Subclass of XMLLibraryParser https://github.com/liamks/pyitunes,
     typed to fit my needs.

     This eschews the existence of lxml, lxml, SAX, and DOM version of xml parse and just
     parses the text raw. Since liamks already wrote the annoying regex stuff, (and I trust
     that it works), I just jacked his methods and instead of hashing by track id I hash
     by name, artist, album, and size.

     I'm not sure why Apple decided to build their xml schema for this the way that they do,
     but since it's constructed that way, I think parsing this way is almost as clean as 
     using the xml parsing classes
   '''

   HASH_KEYS = ('Name', 'Artist', 'Album')
   '''
      The properties that will be used to construct to hash
   '''

   VALUE_KEY = 'Location'
   # this is the only value we have a vested interest in

   KEYS_WE_CARE_ABOUT = HASH_KEYS + (VALUE_KEY,)
   '''
       All relevant keys
   '''

   hp = HTMLParser()
   unescape = HTMLParser.unescape
      # jacking the unescape method from here

   @staticmethod
   def construct_hash_key_from_dict(key_parts):  # @NoSelf
     '''
        Gives the hash used 
     
        @type key_parts: DictType
        @precondition set(HashPathParser.HASH_KEYS) == set(key_parts.keys())
        @rtype: UnicodeType
     '''
     return " ".join("(%s:%s)" % (x, key_parts[x]) for x in HashPathParser.HASH_KEYS)

   # this was kind of overkill to make this method. at least it's relatively centralized here
   @staticmethod
   def construct_hash_key_from_namedtuple(key_parts):
      return " ".join("(%s:%s)" % (x, getattr(key_parts, x)) for x in HashPathParser.HASH_KEYS)


   def __init__(self, xmlLibrary):
      f = open(xmlLibrary)
      s = f.read()
      # this constructor uses a generator instead of a list for lines, doesn't need to be a list
      lines = (x for x in s.split("\n"))
      self.dictionary = self.parser(lines)


   def parser(self, lines):
      '''
         Given a generator of lines (which presumably are of an XML file), this will return a generator
         of Dictionaries where each is keyed by the values in L{<self.KEYS_WE_CARE_ABOUT>}

         @type lines: GeneratorType
         @postcondition: isinstance(x, DictType) for x in return
      '''
      dicts = 0
      songs = {}
      inSong = False
      for line in lines:
         if re.match('(\s)*<dict>', line):
            dicts += 1
         elif re.match('(\s)*</dict>', line):
            dicts -= 1
            inSong = False

            # I don't think there is a high likelihood of hash collisions (or key), not the end of the world if there are
            songkey = self.construct_hash_key_from_dict(temp)
            songs[songkey] = temp[self.VALUE_KEY]

         elif dicts > 2 and re.match('(\s)*<key>(.*?)</key>', line):
            key, restOfLine = self.keyAndRestOfLine(line)
            if key in self.KEYS_WE_CARE_ABOUT:
               # update the dictionary, also a hack to unescape xml character
               temp.update({key: self.unescape(self.hp, self.getValue(restOfLine))})

         elif dicts == 2 and re.match('(\s)*<key>(.*?)</key>', line):
            inSong = True
            # it's possible that there are null values for the HASH_KEYS defined above. default to empty string in that case
            temp = defaultdict(lambda: '')

         elif len(songs) > 0 and dicts < 2:
            return songs
      return songs
