#!/bin/bash

# Copyright   2014  Johns Hopkins University (author: Daniel Povey)
# Apache 2.0

remove_archive=false

if [ "$1" == --remove-archive ]; then
  remove_archive=true
  shift
fi

if [ $# -ne 2 ]; then
  echo "Usage: $0 [--remove-archive] <data-base> <url-base>"
  echo "e.g.: $0 /export/a15/vpanayotov/data www.openslr.org/resources/11"
  echo "With --remove-archive it will remove the archive after successfully un-tarring it."
  exit 1
fi

data=$1
url=$2

if [ ! -d "$data" ]; then
  echo "$0: no such directory $data"
  exit 1
fi

if [ -z "$url" ]; then
  echo "$0: empty URL base."
  exit 1
fi

if [ -d $data/masc ]; then
  echo "$0: data was already successfully extracted, nothing to do."
  exit 0
fi


# sizes of the archive files in bytes.  This is some older versions.
# sizes_old="371012589 347390293 379743611 361838298 6420417880 23082659865 30626749128"
# sizes_new is the archive file sizes of the final release.  Some of these sizes are of
# things we probably won't download.
# sizes_new="337926286 314305928 695964615 297279345 87960560420 33373768 346663984 328757843 6387309499 23049477885 30593501606"

if [ -f $data/masc.tar.gz ]; then
  # size=$(/bin/ls -l $data/$part.tar.gz | awk '{print $5}')
  # size_ok=false
  # for s in $sizes_old $sizes_new; do if [ $s == $size ]; then size_ok=true; fi; done
  # if ! $size_ok; then
  #   echo "$0: removing existing file $data/$part.tar.gz because its size in bytes $size"
  #   echo "does not equal the size of one of the archives."
  #   rm $data/$part.tar.gz
  # else
  echo "$data/masc.tar.gz exists and appears to be complete."
fi

if [ ! -f $data/masc.tar.gz ]; then
  if ! which wget >/dev/null; then
    echo "$0: wget is not installed."
    exit 1
  fi
  echo "$0: downloading data from $url.  This may take some time, please be patient."

  if ! wget -P $data --no-check-certificate $url; then
    echo "$0: error executing wget $url"
    exit 1
  fi
fi

if ! tar -C $data/masc -xvzf $data/masc.tar.gz; then
  echo "$0: error un-tarring archive $data/masc.tar.gz"
  exit 1
fi

# touch $data/untar/$part/.complete

echo "$0: Successfully downloaded and un-tarred $data/masc.tar.gz"

if $remove_archive; then
  echo "$0: removing $data/masc.tar.gz file since --remove-archive option was supplied."
  rm $data/masc.tar.gz
fi
