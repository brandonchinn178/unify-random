from __future__ import print_function

from utils import Program
from fractions import gcd
from math import sqrt, ceil
import itertools

PRIME_BITS = 8
MAX_PRIME = 2 ** PRIME_BITS

def is_prime(x):
    if x == 1:
        return False

    i = 2
    bound = sqrt(x)
    while i < bound:
        if x % i == 0:
            return False
        i += 1

    return True

def natural_to_integer(x):
    """
    Convert given natural number to a signed integer, mapping
    0 -> 0
    1 -> -1
    2 -> 1
    3 -> -2
    4 -> 2
    ...
    """
    if x % 2 == 0:
        return x / 2
    else:
        return - x / 2

def modular_inverse(a, m):
    """
    Return the modular inverse of a mod m. Uses the extended Euclidean algorithm.
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    tmp_m = m
    tmp_a = a
    s = 0
    t = 1
    while tmp_m != 0:
        quotient = tmp_a / tmp_m
        tmp_a, tmp_m = tmp_m, tmp_a - quotient * tmp_m
        t, s = s, t - quotient * s

    return t % m

class RSAKeyGenerator(Program):
    """
    A program that generates a random RSA key pair.
    """
    DESCRIPTION = 'Generate a random RSA key pair'

    def __init__(self):
        super(RSAKeyGenerator, self).__init__()

    def _get_parser(self):
        parser = super(RSAKeyGenerator, self)._get_parser()
        parser.add_argument('-o', '--output', help='Name of output file, e.g. foo to generate foo.pub and foo.priv', default='tmp')
        parser.add_argument('-v', '--verbose', action='store_true')
        return parser

    def generate(self):
        p, q = self.get_random_int(0, MAX_PRIME, 2)

        self.output('Finding p...')
        p = self.get_closest_prime(p)

        self.output('Finding q...')
        q = self.get_closest_prime(q)

        self.output('Calculating totient...')
        n = p * q
        totient = (p - 1) * (q - 1)

        self.output('Setting e...')
        # setting e makes for efficient encryption
        e = 65537
        if gcd(e, totient) != 1 or e > totient:
            for i in range(3, totient):
                if gcd(i, totient) == 1:
                    e = i
                    break

        self.output('Calculating d...')
        d = modular_inverse(e, totient)

        self.output('Saving...')
        self.save('output/%s.pub' % self.args.output, '%d,%d' % (e,n))
        self.save('output/%s.priv' % self.args.output, d)

        self.output('Done.')

    def get_closest_prime(self, x):
        """
        Get the closest value to x that is prime
        """
        deltas = itertools.imap(natural_to_integer, itertools.count())
        neighbors = itertools.imap(lambda i: x + i % MAX_PRIME, deltas)
        filtered = itertools.ifilter(is_prime, neighbors)
        return filtered.next()

    def save(self, filename, val):
        with open(filename, 'w') as f:
            f.write(bytes(val))

    def output(self, message, newline=True):
        if self.args.verbose:
            end = '\n' if newline else ''
            print(message, end=end)

if __name__ == '__main__':
    RSAKeyGenerator().generate()
