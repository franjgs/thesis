#! /usr/bin/env python

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from lib.util import get_comments_data

def main(infile, outfile):
    """read from infile, write to outfile"""
    print "Reading from %s..." % infile
    labels, timestamps, comments = get_comments_data(infile)
    print "Parsing..."
    vec = TfidfVectorizer(
        ngram_range = (1, 2),
        strip_accents = None,
        charset_error = "ignore",
        stop_words = None,
        min_df = 2
    )
    vec.fit(comments)
    print "Processing and writing to %s..." % outfile
    f = open(outfile, 'w')
    counter = 0
    comments = vec.transform(comments)
    rows, cols = comments.get_shape()
    for row in xrange(0, rows):
        if counter % 100 == 0:
            print counter
        buf, indices = list(), comments[row].indices.tolist()
        indices.sort()
        buf.append(str(float(labels[row])))
        for col in indices:
            buf.append("%d:%.3f" % (col, comments[row, col]))
        buf.append("\n")
        f.write(" ".join(buf))
        counter = counter + 1
    f.close()
    print "Done!"

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python %s <infile> <outfile>" % sys.argv[0]
    else:
        infile, outfile = sys.argv[1], sys.argv[2]
        main(infile, outfile)
