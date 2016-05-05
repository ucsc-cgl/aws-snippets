#!/usr/bin/env python2.7

import sys, os, re, getopt
import argparse
import textwrap
import hashlib
import base64
import os
import subprocess

def build_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description = textwrap.dedent('''\
           Download encrypted file from S3 using curl and header injection

           '''), 
        epilog = textwrap.dedent('''\
           Example of use: 
           s3_encrypted_download.py -m master.key -u https://s3-us-west-2.amazonaws.com/projects-encrypted/fastq.tar -o decrypted.tar
           '''))
    parser.add_argument('-m', '--masterkey', required=True, help='file containing master key')
    parser.add_argument('-u', '--url', required=True, help='url location')
    parser.add_argument('-o', '--outfile', required=True, help='output file')
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    return parser

def download_encrypted_file(key_path, url, file_path):
    """
    Downloads encrypted files from S3 via header injection

    input_args: dict    Input dictionary defined in main()
    name: str           Symbolic name associated with file
    """
    with open(key_path, 'r') as f:
        key = f.read()
    if len(key) != 32:
        raise RuntimeError('Invalid Key! Must be 32 bytes: {}'.format(key))

    key = generate_unique_key(key_path, url)

    encoded_key = base64.b64encode(key)
    encoded_key_md5 = base64.b64encode(hashlib.md5(key).digest())
    h1 = 'x-amz-server-side-encryption-customer-algorithm:AES256'
    h2 = 'x-amz-server-side-encryption-customer-key:{}'.format(encoded_key)
    h3 = 'x-amz-server-side-encryption-customer-key-md5:{}'.format(encoded_key_md5)
    print
    #print ' '.join(['curl', '-fs', '--retry', '5', '-H', h1, '-H', h2, '-H', h3, url, '-o', file_path])
    print ' '.join(['curl', '--retry', '5', '-H', h1, '-H', h2, '-H', h3, url, '-o', file_path])
    print
    try:
        subprocess.check_call(['curl', '--retry', '5', '-H', h1, '-H', h2, '-H', h3, url, '-o', file_path])
    except OSError:
        raise RuntimeError('Failed to find "curl". Install via "apt-get install curl"')
    assert os.path.exists(file_path)

def generate_unique_key(master_key_path, url):
    """
    master_key_path: str    Path to the BD2K Master Key (for S3 Encryption)
    url: str                S3 URL (e.g. https://s3-us-west-2.amazonaws.com/bucket/file.txt)

    Returns: str            32-byte unique key generated for that URL
    """
    with open(master_key_path, 'r') as f:
        master_key = f.read()
    assert len(master_key) == 32, 'Invalid Key! Must be 32 characters. ' \
                                  'Key: {}, Length: {}'.format(master_key, len(master_key))
    new_key = hashlib.sha256(master_key + url).digest()
    assert len(new_key) == 32, 'New key is invalid and is not 32 characters: {}'.format(new_key)
    return new_key


# Main
# Run program
parser = build_parser()
args = parser.parse_args()

download_encrypted_file(args.masterkey, args.url, args.outfile) 

