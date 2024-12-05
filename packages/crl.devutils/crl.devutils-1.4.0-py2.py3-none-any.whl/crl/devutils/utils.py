import random
import string


__copyright__ = 'Copyright (C) 2019, Nokia'


def get_randomstring(length):
    return ''.join(random.SystemRandom().choice(
        string.ascii_lowercase) for _ in range(length))


def execfile(filename, namespace):
    with open(filename) as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, namespace)
