#!/bin/bash

# create dirs and files
mkdir -p ./my_dir_{1,2}
touch ./my_dir_1/file{1..3}.txt
touch ./my_dir_2/file{2,4}.txt

# test sym links
ln -s ./my_dir1/file1.txt ./my_dir_2/file_ln.txt
