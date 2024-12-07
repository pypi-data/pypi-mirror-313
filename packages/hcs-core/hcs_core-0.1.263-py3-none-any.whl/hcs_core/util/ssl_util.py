import ssl
import hashlib
import socket
from urllib.parse import urlparse


def get_cert_thumbprints(url, verify_cert: bool = False):
    # Parse the URL to extract the hostname and port
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port or 443  # Use port 443 if no port is specified

    # Create a context with default settings and system's certificates
    context = ssl.create_default_context()
    if not verify_cert:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    # Connect to the server
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            # Get the DER-encoded certificate
            der_cert = sslsock.getpeercert(binary_form=True)
            # Compute the SHA256 and SHA1 fingerprints
            sha256_fingerprint = hashlib.sha256(der_cert).hexdigest().upper()
            sha1_fingerprint = hashlib.sha1(der_cert).hexdigest().upper()
            return {"SHA256": sha256_fingerprint, "SHA1": sha1_fingerprint}


if __name__ == "__main__":
    url = "https://pod30-vc1.pod30.hcs.steslabs.net"
    ret = get_cert_thumbprints(url)
    print(ret)
