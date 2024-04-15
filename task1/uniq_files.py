#!/usr/bin/python3

import os
import argparse

def get_uniq_fn(dirs, symlinks):
    """
    Returns a list of unique filenames which entries in all the input directory list.
    Args:
        dirs (list): list od directory names (paths)
        symlinks (bool): if True includes symbol links into result as well
    Return:
        list: list of filenames
    """
    uniq_fn = set()
    for dir in dirs:
        if not os.path.exists(dir):
            print(f"Error: Path {dir} does not exist.")
            continue
        if not os.access(dir, os.R_OK):
            print(f"Error: Permission denied to access {dir}.")
            continue
        with os.scandir(dir) as entries:
            for entry in entries:
                if entry.is_file() or (symlinks and entry.is_symlink):
                    uniq_fn.add(entry.name)
    return list(uniq_fn)

if __name__ == "__main__":

    # Parsing command line arguments:
    # > script.py [-l] dir1, dir2, ..., dirN
    # -l: if present it includes symbol links as well
    # dir1, dir2, ..., dirN: list of directori names
    parser = argparse.ArgumentParser(description="Get unique filenames from directories.", 
                                     usage="[-l] dir1 dir2 ... dirN")
    parser.add_argument("directories", nargs="+", 
                        help="List of directories to search for files")
    parser.add_argument("-l", "--include-symlinks", action="store_true", 
                        help="Include symbolic links in the result")
    args = parser.parse_args()

    uniq_fn = get_uniq_fn(args.directories, args.include_symlinks)
    for file in sorted(uniq_fn):
        print(file)