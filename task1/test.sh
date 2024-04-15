#!/bin/bash -xe

set -xe

### bash command find, files only:
find my_dir_1 my_dir_2 -type f -exec basename  {} \; | sort -u

### bash command find, files only. Negative scenario:
find my_dir_1 my_dir_2 mydir3 /root -type f -exec basename  {} \; | sort -u

### bash command ls and grep, files only:
ls -al my_dir_1 my_dir_2 | grep '^-' | grep -oE '[[:alnum:]_.-]+?[\.[:alnum:]_-]+?$' | sort -u

### python script, files only:
./uniq_files.py my_dir_1 my_dir_2

### python script, files only. Negative scenario:
./uniq_files.py my_dir_1 my_dir_2 /root mydir3

