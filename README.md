# aws-snippets
Small scripts to interact with AWS

### list_s3_bucket.py
Get a listing of all files in an S3 bucket. You must have a `~/.boto` and `s3am` installed

### s3_encrypted_download.py
Download one file from S3 and decrypt. You must have a master key file and `curl` installed

**Note**: To download unencrypted files, get the URL (from the Properties) and use `wget`:

``
wget --no-check-certificate https://s3-us-west-2.amazonaws.com/varscan-hg19-input/centromeres.bed
``
