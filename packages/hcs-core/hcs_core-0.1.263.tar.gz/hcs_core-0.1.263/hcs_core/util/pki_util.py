"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import os
import subprocess
from typing import List
from OpenSSL import crypto
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


def base64_encode(text: str) -> str:
    return base64.b64encode(text.encode("ascii")).decode("ascii")


def base64_decode(encoded: str) -> str:
    return base64.b64decode(encoded.encode("ascii")).decode("ascii")


def decode_x509_pem(x509_cert_pem: str) -> x509.Certificate:
    x509_cert_pem = x509_cert_pem.strip()
    return x509.load_pem_x509_certificate(x509_cert_pem.encode("ascii"), default_backend())


def get_x509_subject(cert: x509.Certificate) -> dict:
    subject = {}
    for n in cert.subject:
        subject[n.oid._name] = n.value
    return subject


def split_cert_chain_pem(cert_chain_pem: str) -> list:
    cert_chain_pem = cert_chain_pem.strip()

    cert_chain_pem = cert_chain_pem.replace("TRUSTED CERTIFICATE", "CERTIFICATE")

    # Separators:
    # -----BEGIN CERTIFICATE-----
    # -----END CERTIFICATE-----
    # -----BEGIN TRUSTED CERTIFICATE-----
    # -----END TRUSTED CERTIFICATE-----

    dash = "-----"
    separator = dash + "\n" + dash
    parts = cert_chain_pem.split(separator)

    for i in range(len(parts)):
        if i > 0:
            parts[i] = dash + parts[i]
        if i < len(parts) - 1:
            parts[i] = parts[i] + dash
    return parts


def cert_chain_pem_to_certs(cert_chain_pem: str) -> List[x509.Certificate]:
    pems = split_cert_chain_pem(cert_chain_pem)
    return list(map(decode_x509_pem, pems))


def check_cert_equals(cert1: x509.Certificate, cert2: x509.Certificate) -> bool:
    subject1 = get_x509_subject(cert1)
    subject2 = get_x509_subject(cert2)
    if subject1 != subject2:
        print("Different subject:")
        print(subject1)
        print(subject2)
        return False
    if cert1.serial_number != cert2.serial_number:
        print("Different serial_number:")
        print(cert1.serial_number)
        print(cert2.serial_number)
        return False

    fingerprint1 = fingerprint_sha256(cert1)
    fingerprint2 = fingerprint_sha256(cert2)
    if fingerprint1 != fingerprint2:
        print("Different fingerprint:")
        print(fingerprint1)
        print(fingerprint2)
        return False
    if cert1.signature != cert2.signature:
        print("Different signature")
        return False
    return True


def fingerprint_sha256(cert) -> str:
    return bytearray(cert.fingerprint(hashes.SHA256())).hex()


def validate_cert_chain_pem_using_openssl(chain_pems: list):
    with open("temp_leaf.pem", "w") as f:
        f.write(chain_pems[0])
    with open("temp_chain.pem", "w") as f:
        for pem in chain_pems[1:]:
            f.write(pem)
            f.write("\n")
    cmd = "openssl verify -verbose -CAfile temp_chain.pem temp_leaf.pem"

    subprocess.run(cmd, shell=True, check=True, capture_output=False)

    os.unlink("temp_leaf.pem")
    os.unlink("temp_chain.pem")


# Generate pkey
def generate_key(type=crypto.TYPE_RSA, bits: int = 4096):
    key = crypto.PKey()
    key.generate_key(type, bits)
    return key


def _ascii(text: str) -> bytes:
    return text.encode("ascii")


def generate_CSR(nodename, sans=[], key_length: int = 2048):
    C = "US"
    ST = "California"
    L = "Palo Alto"
    O = "VMware, Inc."
    OU = "EUC"

    ss = []
    for i in sans:
        ss.append("DNS: %s" % i)
    ss = ", ".join(ss)

    req = crypto.X509Req()
    req.get_subject().CN = nodename
    req.get_subject().countryName = C
    req.get_subject().stateOrProvinceName = ST
    req.get_subject().localityName = L
    req.get_subject().organizationName = O
    req.get_subject().organizationalUnitName = OU
    # Add in extensions
    base_constraints = [
        crypto.X509Extension(_ascii("keyUsage"), False, _ascii("Digital Signature, Non Repudiation, Key Encipherment")),
        crypto.X509Extension(_ascii("basicConstraints"), False, _ascii("CA:FALSE")),
    ]
    x509_extensions = base_constraints
    # If there are SAN entries, append the base_constraints to include them.
    if ss:
        san_constraint = crypto.X509Extension("subjectAltName", False, ss)
        x509_extensions.append(san_constraint)
    req.add_extensions(x509_extensions)
    # Utilizes generateKey function to kick off key generation.
    key = generate_key(crypto.TYPE_RSA, key_length)
    req.set_pubkey(key)
    req.sign(key, "sha256")
    csr_pem = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode("ascii")
    private_key_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("ascii")
    return csr_pem, private_key_pem
