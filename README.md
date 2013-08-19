iphone_migrator
===============
Requirements
  - Python 2.6
  - Windows/OSX + iTunes

NOT DONE YET.

pairs the iphone with a different library than the original, remembering what is currently on the phone

While the use case of this is probably extremely infrequent, this was a simple solution when I needed to sync my iphone
with a different computer that had windows on it, and being able to "keep" my music library on my iphone without
jailbreaking, or going through the library manually and figuring out which songs, albums, and artists that I wanted to
keep.

This assumes that whatever songs on the iphone also exist on the computer library. I.e. you have copies of the files
on both systems.

Thanksfully (and conveniently) this does not require jailbreaking the phone. All you have to do are the following steps:

1) plug in phone to iTunes, go to 'On This Phone'
2) Right click "Music' and select 'Export'
3) Export the file to some location
4) run iphone_migrator.py with the input file that you exported. This will create a m3u playlist containing references
to the files that exist already on the host computer
5) You should now be able to sync
