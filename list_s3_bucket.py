#!/usr/bin/env python2.7

import sys
import argparse
from boto.s3.connection import S3Connection

parser = argparse.ArgumentParser(description = 'List contents of a bucket in your S3', 
	epilog='Example of use: list_s3_bucket.py cgl-driver-projects')
parser.add_argument('bucket', nargs = '?')	# get first argument as string

# NOTE: To use this you must have (pip) installed s3am and a ~/.boto file with your AWS credentials
# Also note that this code can not print s3 subdirectories (cgl-driver-projects/ckcc) because
# they are all in the same bucket (and not truly directories). Grep is your friend.

args = parser.parse_args()
s3=S3Connection()
try:
    b=s3.get_bucket(args.bucket)
except: 
    print 'Cannot get a listing of bucket "{}"'.format(args.bucket)
    sys.exit(1)

mylist=list(b.list())
for i in mylist:
	print i.name
