"""
Finds duplicate files in multiple directories
"""

from collections import defaultdict
from functools import lru_cache
from glob import iglob
from hashlib import md5
from os import getcwd
from os.path import isfile, getsize, join
from sys import argv
from typing import List, Set, DefaultDict


@lru_cache(maxsize=None)
def filehash(filename: str) -> bytes:
    hashobj = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashobj.update(chunk)
    return hashobj.digest()


def find_duplicates(directories: List[str]) -> List[List[str]]:
    files_by_size = defaultdict(set)  # type: DefaultDict[int, Set[str]]
    duplicates_by_hash = defaultdict(set)  # type: DefaultDict[bytes, Set[str]]
    for directory in directories:
        for path in iglob(join(directory, '**', '*.*')):
            if isfile(path):
                size = getsize(path)
                if size in files_by_size:
                    h = filehash(path)
                    for other in files_by_size[size]:
                        if filehash(other) == h:
                            duplicates_by_hash[h].add(path)
                            duplicates_by_hash[h].add(other)
                            break
                files_by_size[size].add(path)

    return list(map(sorted, duplicates_by_hash.values()))


if __name__ == '__main__':
    if len(argv) > 1:
        directories = argv[1:]
    else:
        directories = [getcwd()]

    print('Searching for duplicate files in ', directories)

    for bucket in find_duplicates(directories):
        for f in bucket:
            print(f)
        print()
