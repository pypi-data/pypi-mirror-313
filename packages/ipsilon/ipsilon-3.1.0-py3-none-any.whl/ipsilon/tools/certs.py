# Copyright (C) 2014 Ipsilon project Contributors, for license see COPYING

from subprocess import Popen
import os


class Certificate(object):

    def __init__(self, path=None):
        self.subject = None
        self.key = None
        self.cert = None
        if path:
            self.path = path
        else:
            self.path = os.getcwd()

    def generate(self, prefix, subject):
        self.key = os.path.join(self.path, '%s.key' % prefix)
        self.cert = os.path.join(self.path, '%s.pem' % prefix)
        self.subject = '/CN=%s' % subject
        command = ['openssl',
                   'req', '-x509', '-batch', '-days', '1825', '-text',
                   '-newkey', 'rsa:2048', '-nodes', '-subj', self.subject,
                   '-keyout', self.key, '-out', self.cert]
        proc = Popen(command)
        proc.wait()

    def import_cert(self, certfile, keyfile):
        self.cert = certfile
        self.key = keyfile

    def get_cert(self):
        if not self.cert:
            raise ValueError('Certificate unavailable')
        with open(self.cert, 'r', encoding='utf-8') as f:
            cert = f.readlines()

        # Find the beginning of the certificate
        # This helps if the admin pointed us to a certificate that includes
        # the OpenSSL textual representation (openssl x509 -text)
        begin = cert.index('-----BEGIN CERTIFICATE-----\n')
        cert = cert[begin:]

        # poor man stripping of BEGIN/END lines
        if cert[0] == '-----BEGIN CERTIFICATE-----\n':
            cert = cert[1:]
        if cert[-1] == '-----END CERTIFICATE-----\n':
            cert = cert[:-1]

        return " ".join(cert)
