#!/usr/bin/env python

__author__ = "Jay Goldberg"
__copyright__ = "Copyright 2015"
__credits__ = ["Jay Goldberg"]
__license__ = "Apache 2.0"
__maintainer__ = "Jay Goldberg"
__email__ = "jaymgoldberg@gmail.com"

import sys
import json
from copy import deepcopy, copy
#from operator import itemgetter # for sorting by subkeys

class Bookmark:
    def __init__(self, proto='http', url=None, host=None, port=None, tags=[], path=None):
        self.proto = 'http'
        self.url = url
        self.tags = tags

class BookmarkParser:
    def __init__(self):
        self._json_bookmark = None
        self.bookmarks = []
        self.tagtracker = []

    def loadChildren(self, roots, pathstack=None):
        
        for item, contents in roots.iteritems():
            self.tagtracker.append(item)
            if 'children' in contents:
                self.childsort(contents)
            if isinstance(item, dict):
                if item['type'] == 'folder':
                    self.tagtracker.append(item['name'])
                    self.childsort(contents)

# three ways to sort a list based on the contents of a subkey
# for element in children:
#     print(element['type'])
# for element in sorted(children, key=lambda child: child['type'][0]):
#     print(element['type'][0])
# for element in sorted(children, key=itemgetter('type')):
#     print(element['type'])

    def childsort(self, contents):
        for entry in sorted(contents['children'], key=lambda child: child['type'][0]):
            if entry['type'] == 'folder':
                self.tagtracker.append(entry['name'])
                self.childsort(entry)
                self.tagtracker.pop()
            elif entry['type'] == 'url':
                bookmark = Bookmark(url=entry['url'], tags=self.tagtracker)
                self.bookmarks.append(deepcopy(bookmark))

    def parse(self):
        if not self._json_bookmark:
            return
        if 'roots' not in self._json_bookmark:
            return

        self.loadChildren(self._json_bookmark['roots'])

        return self.bookmarks
 
    def open_json_bookmark(self, json_filepath):
        with open(json_filepath, 'r') as jb_file:
            jb = ''.join(jb_file.readlines())
        self._json_bookmark = json.loads(jb)

if __name__ == '__main__':
    bookmarks = BookmarkParser()
    data = bookmarks.open_json_bookmark(sys.argv[1])
    bookmarklist = bookmarks.parse()

    for item in bookmarklist:
        print("%s %s" % (item.url,item.tags))
