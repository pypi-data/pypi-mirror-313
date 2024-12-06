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

'Delete spam emails.'
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from email import message_from_bytes
from itertools import islice
from unidecode import unidecode
import logging, re

log = logging.getLogger(__name__)
number = re.compile(b'[0-9]+')
oddfrom = re.compile('[A-Z0-9]+')
fixup = re.compile(b'^\xc2\xb2sender: ', re.MULTILINE)

def _headerstr(header):
    if isinstance(header, str) or header is None:
        return header
    (text, charset), = header._chunks
    assert 'unknown-8bit' == charset
    parts = re.split(r'([\udc00-\udcff]+)', text)
    def g():
        yield parts[0]
        for q, p in zip(islice(parts, 1, None, 2), islice(parts, 2, None, 2)):
            yield bytes(ord(x) & 0xff for x in q).decode('utf-8')
            yield p
    return ''.join(g())

def _toplain(text):
    return unidecode(text, errors = 'preserve')

class Regex:

    def __init__(self, config):
        self.max_non_ascii = float(getattr(config.max, 'non-ascii'))
        self.max_odd_from = float(getattr(config.max.odd, 'from'))
        self.froms = list(map(re.compile, config.regex.froms))
        self.subjects = list(map(re.compile, config.regex.subjects))

    def delete(self, From, Subject):
        if From is not None and sum(map(len, oddfrom.findall(From))) / len(From) > self.max_odd_from:
            log.debug('From has too many odd chars.')
            return True
        if From is not None and Subject is not None:
            both = From + Subject
            if sum(1 for c in both if ord(c) > 0x7f) / len(both) > self.max_non_ascii:
                log.debug('Too many non-ascii chars.')
                return True
        if From is not None:
            plain = _toplain(From)
            for fromre in self.froms:
                if fromre.search(plain) is not None:
                    log.debug("From match: %s", fromre)
                    return True
        if Subject is not None:
            plain = _toplain(Subject)
            for subjectre in self.subjects:
                if subjectre.search(plain) is not None:
                    log.debug("Subject match: %s", subjectre)
                    return True

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'spamtrash.arid', encoding = 'utf-8')
    parser = ArgumentParser()
    parser.add_argument('--cron', action = 'store_true')
    parser.add_argument('-v', action = 'store_true')
    parser.parse_args(namespace = config.cli)
    logging.getLogger().setLevel(logging.DEBUG if config.verbose else logging.INFO)
    regex = Regex(config)
    with config.imap(config.host) as imap:
        with config.password as password:
            imap.login(config.user, password)
        imap.select(config.mailbox)
        ok, (ids,) = imap.search(None, 'ALL')
        assert 'OK' == ok
        message_set = ','.join(id.decode() for id in ids.split())
        if not message_set:
            log.info('No spam!')
            return
        ok, v = imap.fetch(message_set, '(BODY.PEEK[])')
        assert 'OK' == ok
        deleteids = []
        for (info, msgbytes), x in zip(islice(v, 0, None, 2), islice(v, 1, None, 2)):
            if x not in {b')', rb' FLAGS (\Seen))'}:
                raise Exception(x)
            id = number.match(info).group().decode()
            msgbytes = fixup.sub(b'Sender: ', msgbytes)
            msg = {k: _headerstr(msg[k]) for msg in [message_from_bytes(msgbytes)] for k in ['From', 'Subject']}
            if regex.delete(**msg):
                log.info("Delete %s: %s", id, msg)
                deleteids.append(number.match(info).group().decode())
            else:
                log.info("Ignore %s: %s", id, msg)
        if deleteids:
            log.info("Delete %s emails.", len(deleteids))
            imap.store(','.join(deleteids), '+X-GM-LABELS', r'\Trash')
        else:
            log.info('Nothing to delete.')

if '__main__' == __name__:
    main()
