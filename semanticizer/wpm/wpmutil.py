# Copyright 2012-2013, University of Amsterdam. This program is free software:
# you can redistribute it and/or modify it under the terms of the GNU Lesser
# General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unicodedata

dump_filenames = {
    'translations': 'translations.csv',
    'stats': 'stats.csv',
    'labels': 'label.csv',
    'pages': 'page.csv',
    'inlinks': 'pageLinkIn.csv',
    'outlinks': 'pageLinkOut.csv'
}


def normalize(raw, dash=True, accents=True, lower=True):
    """Replaces hyphens with spaces, removes accents, lower cases and
    strips the input text.

    All steps, except for the strip(), can be disabled with the
    optional arguments.
    """
    text = raw
    if dash:
        text = text.replace('-', ' ')
    if accents:
        text = remove_accents(text)
    if lower:
        text = text.lower()
    text = text.strip()
    return text if len(text) else raw


def remove_accents(input_str):
    """Replaces accented characters in the input with their
    non-accented counterpart."""
    if isinstance(input_str, str):
        input_unicode = input_str.decode(errors="ignore")
    else:
        input_unicode = input_str
    nkfd_form = unicodedata.normalize('NFKD', input_unicode)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def check_dump_path(path):
    """
    Checks whether a path exists and raises an error if it doesn't.

    @param path: The pathname to check
    @raise IOError: If the path doesn't exist or isn't readbale
    """
    import os
    pathlist = [os.path.normpath(path) + os.sep,
                os.path.normpath(os.path.abspath(path)) + os.sep]
    for fullpath in pathlist:
        print "Checking " + fullpath
        if os.path.exists(fullpath):
            for _, filename in dump_filenames.iteritems():
                if os.path.isfile(fullpath + filename) == True:
                    print "Found " + fullpath + filename
                else:
                    raise IOError("Cannot find " + fullpath + filename)
            return fullpath
        else:
            print fullpath + " doesn't exist"
    raise IOError("Cannot find " + path)
