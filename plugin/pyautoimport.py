import sys
import subprocess
from collections import Counter


class Reporter:
    def __init__(self):
        self.names = set()

    def flake(self, msg):
        from pyflakes.messages import UndefinedName

        if isinstance(msg, UndefinedName):
            self.names.add(msg.message_args[0])


def get_undefined_names(path):
    from pyflakes.api import checkPath

    reporter = Reporter()
    checkPath(path, reporter)
    return reporter.names


def get_import(name):
    call = subprocess.run(
        ['git', 'grep', '-h', f'import\( [^ ]\+ as\)\? {name}$'],
        stdout=subprocess.PIPE,
        encoding='utf-8',
    )
    matches = Counter(call.stdout.splitlines())
    best = matches.most_common(1)
    if best:
        return best[0][0]


def get_imports(path):
    names = get_undefined_names(path)
    lines = [get_import(name) for name in names]
    return sorted(line for line in lines if line)


if __name__ == '__main__':
    for line in get_imports(sys.argv[1]):
        print(line)
