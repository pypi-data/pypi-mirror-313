import os
import pathlib
import shutil
import tempfile
from gitignore_parser import rule_from_pattern, handle_negation
from .path import normal_path, new_empty_path
from .operation import read_lines, merge_move, remove_path, write_file, list_dir


class FileHitChecker:
    def __init__(self, src_dir, *ignore_file_list, lines=None):
        self.src_dir = normal_path(src_dir)
        rules = []
        for ignore_file in ignore_file_list:
            full_path = normal_path(os.path.join(src_dir, ignore_file))
            rules.extend(self.trans_lines(read_lines(full_path, skip_empty=True, default=''), full_path))
        if lines:
            rules.extend(self.trans_lines(lines))
        self.rules = rules
        self.negation = self.calc_negation(rules)

    @staticmethod
    def calc_negation(rules):
        return any(r.negation for r in rules)

    @staticmethod
    def match(full_path, rules, negation):
        if negation:
            return handle_negation(full_path, rules)
        else:
            return any(r.match(full_path) for r in rules)

    def trans_lines(self, lines=None, source=''):
        all_rules = []
        for index, line in enumerate(lines, 1):
            rule = rule_from_pattern(line, base_path=self.src_dir, source=(source, index))
            if rule:
                all_rules.append(rule)
        return all_rules

    def new_match(self, lines=None):
        if lines:
            rules = self.trans_lines(lines)
            all_rules = [*self.rules, *rules]
            negation = self.calc_negation(rules) or self.negation
        else:
            all_rules = self.rules
            negation = self.negation
        return lambda x: self.match(x, all_rules, negation)

    @staticmethod
    def _expand_base_path(base_path):
        """
        expand the user directory and make absolute, but dont resolve symlinks
        """
        # Convert base_path to a string if it's a PathLike object
        base_path_str = os.fspath(base_path)
        path_base_dir = pathlib.Path(os.path.abspath(os.path.expanduser(base_path_str)))
        return path_base_dir

    def shutil_ignore(self, base_dir, file_names, match, reverse=False):
        """
        Ignore function for shutil.copy_tree
        """
        path_base_dir = self._expand_base_path(base_path=base_dir)
        ignore_files = set()
        for file in file_names:
            hit = match(str(path_base_dir / file))
            if reverse:
                hit = not hit
            if hit:
                ignore_files.add(file)
        return ignore_files

    def is_hit(self, path):
        path = normal_path(path)
        return self.match(path, self.rules, self.negation)

    def walk(self, func, lines=None):
        def wrapper(path):
            for fn in os.listdir(path):
                fp = os.path.join(path, fn)
                func(fp, match(fp), fp[len(self.src_dir) + 1:])
                if os.path.isdir(fp):
                    wrapper(fp)

        match = self.new_match(lines)
        if os.path.exists(self.src_dir):
            wrapper(self.src_dir)

    def merge_dir(self, dest, lines=None, reverse=False):
        dp = new_empty_path(dest)
        self.write_dir(dp, lines, reverse)
        merge_move(dest, dp)
        remove_path(dp)

    def write_dir(self, dest=None, lines=None, reverse=False):
        if dest is None:
            dest = tempfile.mkdtemp()
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        match = self.new_match(lines)
        shutil.copytree(self.src_dir, dest, ignore=lambda x, y: self.shutil_ignore(x, y, match, reverse))
        return dest


def copy_recurse_ignore(src, dest=None, ignores=None):
    def walk(root):
        for ignore in ignores:
            if os.path.isfile(os.path.join(root, ignore)):
                FileHitChecker(root, ignore).write_dir(
                    dest + root[len(src):],
                    lines={'.git'} if ignore == '.gitignore' else None
                )
                break
        else:
            for pa in list_dir(root):
                if os.path.isdir(pa):
                    walk(pa)
                else:
                    write_file(dest + pa[len(src):], c=pa)

    if not dest:
        dest = tempfile.mkdtemp()
    walk(src)
    return dest
