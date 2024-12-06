from pathlib import Path
from fnmatch import fnmatch
from typing import Generator
from dataclasses import dataclass
from collections import defaultdict

import pdb

#TODO: update ignore to support ignoring directory patterns in addition to file patterns
def tree_gen(dir_path: Path, prefix: str = '', *, max_depth: int, max_similar: int, ignore: list[str] = []) -> Generator[str, None, None]:
    """
    A recursive generator, given a directory Path object, will yield a visual tree structure line by line

    Args:
    - dir_path (Path): path to the directory to be traversed
    - prefix (str, optional): spaces ' ' and branches '|' to be added to each line
    - max_depth (int): the maximum depth to traverse. Set to negative for infinite depth
    - max_similar (int): the maximum number of similar files to display before eliding them
    - ignore (list[str], optional): list of file patterns to ignore

    Yields:
    - str: a line of the visual tree structure
    """

    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '


    # heuristics to keep track of so we can elide when there are too many files of some pattern
    elide_heuristics: dict[Path, list[Pattern]] = defaultdict(list)

    paths = sorted(dir_path.iterdir(), key=lambda p: (not p.is_file(), p.name))  # sort files and directories
    contents = [p for p in paths if not any(fnmatch(p.name, pattern) for pattern in ignore)]
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        last_was_elided = False
        if max_depth == 0 and path.is_dir():
            yield prefix + pointer + path.name + '/ ...'
            continue

        # handle printing a file or eliding it if there were too many similar matches already
        if path.is_file():
            if (match:=check_for_matches(path, elide_heuristics[path.parent])):
                # increment the match count for this pattern
                update_pattern(match, path)

                # check if we should print or elide
                if match._count >= max_similar:
                    # draw the elision if we haven't yet
                    if not match._elided:
                        yield prefix + tee + path.name
                        yield prefix + pointer + '...'
                        match._elided = True
                        last_was_elided = pointer != last
                    else:
                        last_was_elided = True
                else:
                    yield prefix + pointer + path.name
            else:
                # if it's a new file, make a new pattern
                pattern = make_pattern(path)
                elide_heuristics[path.parent].append(pattern)
                yield prefix + pointer + path.name

        if path.is_dir():  # extend the prefix and recurse:
            yield prefix + pointer + path.name + '/'
            extension = branch if pointer == tee else space # i.e. space because last, └── , above so no more |
            yield from tree_gen(path, prefix=prefix+extension, ignore=ignore, max_depth=max_depth-1, max_similar=max_similar)

    if len(contents) > 0 and last_was_elided:
        yield prefix + last + '...'


def tree(dir_path: Path, ignore: list[str] = [], max_depth: int = -1, max_similar: int = 25) -> str:
    """
    Generate a string representation of the tree structure of a directory

    Args:
    - dir_path (Path): path to the directory to be traversed
    - ignore (list[str], optional): list of file patterns to ignore
    - max_depth (int, optional): the maximum depth to traverse. Set to negative for infinite depth

    Returns:
    - str: a string representation of the tree structure of the directory
    """
    return '\n'.join((
        str(dir_path) + '/',  # include the root directory
        *tree_gen(dir_path, ignore=ignore, max_depth=max_depth, max_similar=max_similar))
    )

#TODO: this would be better if it compared distributions
class CharacterClass(set[str]):
    def diff(self, other) -> float:
        """determine how different two character classes are. returns a number between 0 and 1 (0 = identical, 1 = completely different)"""
        return len(self - other) / len(self | other)
        
    def __repr__(self):
        return f"CharacterClass({super().__repr__()})"


@dataclass
class Pattern:
    charclass: CharacterClass
    length: int
    extension: str|None
    _count: int = 1 # how many paths matched this pattern
    _elided: bool = False # whether this pattern has been elided already

def match_score(path: Path, pattern:Pattern) -> float: 
    """determine how well a path matches a pattern"""
    name = path.stem
    ext = path.suffix

    # no match at all if the extension is wrong
    if ext != pattern.extension:
        return 0.0
    
    # calculate the proportion of characters that match
    char_score =  1 - pattern.charclass.diff(set(name))
    len_score = 1 - abs(len(name) - pattern.length) / max(len(name), pattern.length)

    return char_score * len_score

def check_for_matches(path: Path, patterns: list[Pattern], threshold=0.5) -> Pattern|None:
    """check if a path matches any of the given patterns"""
    scores = []
    for pattern in patterns:
        score = match_score(path, pattern)
        scores.append(score)
        if score >= threshold:
            return pattern
    return None

def make_pattern(path: Path) -> Pattern:
    """create a pattern from a path"""
    name = path.stem
    ext = path.suffix
    charclass = CharacterClass(set(name))
    return Pattern(charclass, len(name), ext)

def update_pattern(pattern: Pattern, path: Path) -> None:
    """modify the pattern (mainly the character class) based on a new path, and update the count"""
    assert path.suffix == pattern.extension, f"Extension mismatch: {path.suffix} != {pattern.extension}. Cannot update pattern unless path matchs pattern. Got {path=}, {pattern=}"
    name = path.stem
    charclass = CharacterClass(set(name))
    pattern.charclass |= charclass
    pattern.length = ((pattern.length*pattern._count) + len(name)) / (pattern._count + 1) # exponential moving average of lengths in this pattern
    pattern._count += 1




if __name__ == "__main__":
    # simple test case
    # target_dir = Path('tests/runs/20241022_140505/test_case[GDC_processed_2]')
    target_dir = Path('.') # whatever directory you want to test
    print(tree(target_dir))
