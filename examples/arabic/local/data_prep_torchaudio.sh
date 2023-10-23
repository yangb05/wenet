#!/bin/bash

# Copyright 2014  Vassil Panayotov
#           2014  Johns Hopkins University (author: Daniel Povey)
# Apache 2.0

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <src-dir> <dst-dir>"
  echo "e.g.: $0 /export/a15/vpanayotov/data/LibriSpeech/dev-clean data/dev-clean"
  exit 1
fi

src=$1
dst=$2
# all utterances are FLAC compressed
# if ! which flac >&/dev/null; then
#    echo "Please install 'flac' on ALL worker nodes!"
#    exit 1
# fi

mkdir -p $dst || exit 1

[ ! -d $src ] && echo "$0: no such directory $src" && exit 1
dataset=$(basename $src)
wav_scp=$dst/wav.scp; [[ -f "$wav_scp" ]] && rm $wav_scp
trans=$dst/text; [[ -f "$trans" ]] && rm $trans

for reader_dir in $(find -L $src -mindepth 1 -maxdepth 1 -type d | sort); do
  reader=$(basename $reader_dir)
  # if ! [ $reader -eq $reader ]; then  # not integer.
  #   echo "$0: unexpected subdirectory name $reader"
  #   exit 1
  # fi

  for chapter_dir in $(find -L $reader_dir/ -mindepth 1 -maxdepth 1 -type d | sort); do
    chapter=$(basename $chapter_dir)
    # if ! [ "$chapter" -eq "$chapter" ]; then
    #   echo "$0: unexpected chapter-subdirectory name $chapter"
    #   exit 1
    # fi
    find -L $chapter_dir/ -iname "*.wav" | sort | xargs -I% basename % .wav | \
      awk -v "dir=$chapter_dir" -v "d=$dataset" -v "r=$reader" -v "c=$chapter" '{printf "%s_%s_%s_%s %s/%s.wav\n", d, r, c, $0, dir, $0}' >>$wav_scp|| exit 1
    
    find -L $chapter_dir/ -iname "*.opus" | sort | xargs -I% basename % .opus | \
      awk -v "dir=$chapter_dir" -v "d=$dataset" -v "r=$reader" -v "c=$chapter" '{printf "%s_%s_%s_%s %s/%s.opus\n", d, r, c, $0, dir, $0}' >>$wav_scp|| exit 1
    
    find -L $chapter_dir/ -iname "*.txt" | sort | \
      while read file_name; do
        basename=$(basename $file_name)
        key="${basename%.*}"
        content=`cat $file_name`
        echo "${dataset}_${reader}_${chapter}_${key} $content" >> $trans
      done
  done
done

echo "$0: successfully prepared data in $dst"

exit 0
