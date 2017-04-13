"""
Module that abstracts retrieving random numbers from random.org.

Guidelines: (https://www.random.org/clients)
1. No multiple simultaneous requests
2. Retrieve as many numbers at once as possible
3. Long timeout value
4. Examine remaining quota
5. Supply email address in User-Agent field
"""

import argparse, requests, random

def _api_request(endpoint, **parameters):
    params = '&'.join([
        '%s=%s' % (key, val)
        for key, val in parameters.items()
    ])
    r = requests.get(
        'https://www.random.org/%s/?%s' % (endpoint, params),
        headers={
            'User-Agent': 'brandonchinn178@gmail.com',
        },
        timeout=60
    )
    if r.status_code != 200:
        raise Exception('Request returned a %d status code' % r.status_code)
    return r.content

class Program(object):
    """
    A class that wraps a program that uses the random.org API. If --debug/-d is
    specified on the command-line, uses the Python random module instead, to
    conserve bits in the random.org API.
    """
    DESCRIPTION = ''

    def __init__(self, debug=False):
        parser = self._get_parser()
        self.args = parser.parse_args()

        if self.args.debug is None:
            self.args.debug = debug

    def _get_parser(self):
        """
        Return a parser to parse command line arguments
        """
        parser = argparse.ArgumentParser(description=self.DESCRIPTION)
        parser.add_argument('-d', '--debug', action='store_true')
        return parser

    def get_random_int(self, min, max, num=1):
        """
        Get random integers from random.org.

        @param min -- Smallest value allowed for each integer
        @param max -- Largest value allowed for each integer
        @param num -- Number of integers to get from the server
        """
        # maximum number of numbers that can be retrieved at once
        if num > 1e4:
            ints = []
            while num > 1e4:
                ints.extend(self.get_random_int(min, max, 1e4))
                num -= 1e4
            ints.extend(self.get_random_int(min, max, num))
            return ints

        if self.args.debug:
            if num == 1:
                return random.randint(min, max)
            else:
                diff = max - min + 1
                return [
                    int(random.random() * diff) + min
                    for _ in range(num)
                ]
        else:
            response = _api_request(
                'integers',
                num=num,
                min=min,
                max=max,
                col=1,
                base=10,
                format='plain',
                rnd='new',
            )
            if num == 1:
                return int(response)
            else:
                return [int(x) for x in response.splitlines()]
