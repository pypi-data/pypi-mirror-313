# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

'Reconstruct logs from AWS CloudWatch.'
from lagoon.binary import bash, date
from lagoon.program import partial
import argparse, json

logs = bash._ic[partial]('aws logs "$@"', 'logs') # TODO: Do not use interactive mode.
tskey = 'lastIngestionTime'

def _shorten(line, radius = 250):
    if len(line) <= 2 * radius:
        return line
    sep = '...'
    return line[:radius - len(sep)] + sep + line[-radius:]

def streamnames(group, starttime):
    streams = json.loads(logs.describe_log_streams('--log-group-name', group))['logStreams']
    streams.sort(key = lambda s: -s.get(tskey, 0)) # Freshest first.
    def g():
        for s in streams:
            if s.get(tskey, 0) < starttime:
                break
            yield s['logStreamName']
    names = list(g())
    names.reverse()
    return names

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-trunc', action='store_true')
    parser.add_argument('--ago', default='1 hour')
    parser.add_argument('group')
    config = parser.parse_args()
    shorten = (lambda x: x) if config.no_trunc else _shorten
    for stream in streamnames(config.group, int(date('-d', f"{config.ago} ago", '+%s000'))):
        token = []
        while True:
            page = json.loads(logs.get_log_events.__start_from_head('--log-group-name', config.group, '--log-stream-name', stream, *token))
            for m in (e['message'] for e in page['events']):
                if m and '\n' == m[0]:
                    print('$ ', end = '')
                    m = m[1:]
                for i, l in enumerate(m.split('\r')):
                    if i:
                        print()
                        print('> ', end = '')
                    print(shorten(l), end = '')
            t = page['nextForwardToken']
            if token and t == token[1]: # Looks like first page can never be final page.
                break
            token = ['--next-token', t]

if '__main__' == __name__:
    main()
