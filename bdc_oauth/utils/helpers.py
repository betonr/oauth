import locale
import threading, webbrowser
import os, binascii
import base64
import hashlib
import subprocess

def open_brower(url, time=1):
    """
    open new brower
    Args:
        url: url to open in brower
        time: time delay to open brower
    """
    threading.Timer(time, lambda: webbrowser.open(url)).start()


def random_string(size=16):
    """
    generate random string
    Args:
        size: string size
    """
    return (binascii.hexlify(os.urandom(size))).decode('ascii')


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def key_id_encode(the_bytes):
    source = base64.b32encode(the_bytes).decode('utf-8')
    result = []
    for i in range(0, len(source), 4):
        start = i
        end = start+4
        result.append(source[start:end])
    return ":".join(result)


def kid_from_crypto_key(private_key_path, key_type='EC'):
    algorithm = hashlib.sha256()
    if key_type == 'EC':
        der, msg = run_command(['openssl', 'ec', '-in', private_key_path,
                                '-pubout', '-outform', 'DER'])

    elif key_type == 'RSA':
        der, msg = run_command(['openssl', 'rsa', '-in', private_key_path,
                                '-pubout', '-outform', 'DER'])

    else:
        raise Exception("Key type not supported")

    if not der:
        raise Exception(msg)

    algorithm.update(der)
    return key_id_encode(algorithm.digest()[:30])
