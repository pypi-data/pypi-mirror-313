import socket
from contextlib import contextmanager
from functools import lru_cache

from lxml import etree

import sastadev.conf
from sastadev.alpinoparsing import escape_alpino_input, isempty


class AlpinoSentenceParser:
    ''' Assumes a Alpino server is running on provided host:port,
    with assume_input_is_tokenized=off '''
    @contextmanager
    def connection(self):
        try:
            s = socket.create_connection((sastadev.conf.settings.ALPINO_HOST, sastadev.conf.settings.ALPINO_PORT))
            yield s
            s.close()
        except socket.error:
            raise

    def parse_sentence(self, sentence: str, buffer_size=8096) -> str:
        sentence = escape_alpino_input(sentence)
        with self.connection() as s:
            sentence += '\n\n'   # flag end of file
            s.sendall(sentence.encode('utf-8'))
            xml = b''
            while True:
                chunk = s.recv(buffer_size)
                if not chunk:
                    break
                xml += chunk
            return xml.decode('utf-8')


@lru_cache(maxsize=128)
def parse(sentence):
    ''' Wrapper for use in sastadev'''
    if isempty(sentence):
        return None
    alp = AlpinoSentenceParser()
    xml = alp.parse_sentence(sentence)
    return etree.fromstring(bytes(xml, encoding='utf-8'))
