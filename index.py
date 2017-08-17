"""
Flask Module for evaluating Quil Programs on the QVM.
"""

import re
import struct
import time
import numpy as np

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import jsonify
from flask_cors import CORS

import pyquil.forest as forest
from pyquil.gates import *


APP = Flask(__name__)
CORS(APP) # only needed for development mode

@APP.route("/")
def index():
    """Load the web app's HTML

    Returns:
        str: String representation of the web app HTML
    """
    return render_template('index.html')


@APP.route("/measure", methods=['POST'])
def measure():
    """Return the wave function and classical bit measurement of a Quil Program

    Returns:
        json: Response (wave function, classical measurement, status_code) for the front end
    """
    qvm = forest.Connection()
    quil_str = fmt_quil_str(request.form.get('quil_string'))
    classical_addrs = extract_classical_addrs(quil_str)

    res = get_wf_mem(qvm, quil_str, classical_addrs)

    # save properly formed quil strings to local filesystem
    if res['status_code'] == 200:
        quil_filename = 'your_quil_files/%s.quil' % time.time()
        with open(quil_filename, 'w') as quilfile:
            quilfile.write(quil_str)

    return make_response(jsonify(res))


def fmt_quil_str(raw_str):
    """Format a raw Quil program string
    Args:
        raw_str (str): Quil program typed in by user.

    Returns:
        str: The Quil program with leading/trailing whitespace trimmed.
    """
    raw_quil_str = str(raw_str)
    raw_quil_str_arr = raw_quil_str.split('\n')

    trimmed_quil_str_arr = [qs.strip() for qs in raw_quil_str_arr]
    trimmed_quil_str = '\n'.join([x for x in trimmed_quil_str_arr])

    return trimmed_quil_str


def extract_classical_addrs(quil_string):
    """Format a raw Quil program string
    Args:
        raw_str (str): Quil program typed in by user.

    Returns:
        list: Classical addresess from the Quil program
    """
    classical_bits = re.findall(r"\[(\d)\]", quil_string)
    return [int(b) for b in classical_bits]

def get_wf_mem(qvm, quil_string, classical_addrs):
    """
    Format a raw Quil program string

    Args:
        raw_str (str): Quil program typed in by user.

    Returns:
        str: The Quil program with leading/trailing whitespace trimmed.
    """
    payload = {
        "type": "wavefunction",
        "quil-instructions": quil_string,
        "trials": 1,
        "addresses": classical_addrs
    }

    try:
        res = qvm.post_json(payload)
        [wf, mem] = recover_complexes(res.content, classical_addrs)
        print wf
        wf = repr(list(wf))
        mem = repr(mem)
        print "wavefunction:", wf
        print "classical memory:", mem

        return {'status_code': res.status_code, 'wf': wf, 'mem': mem}
    except Exception as e:
        return {'status_code': e.response.status_code, 'wf': e.message, 'mem': e.message}


def recover_complexes(coef_string, classical_addrs):
    """
    Parse the wave function and classical memory from a binary object.
    Borrowed from forest.py.

    Args:
        coef_string (str): Binary representation of wave function and classical memory
        classical_addrs (list): classical addresses

    Returns:
        tuple: The string representation of wave function and classical memory
    """
    num_octets = len(coef_string)
    num_addresses = len(classical_addrs)
    num_memory_octets = forest._round_to_next_multiple(num_addresses, 8) / 8
    num_wavefunction_octets = num_octets - num_memory_octets

    # Parse the classical memory
    mem = []
    for i in xrange(num_memory_octets):
        octet = struct.unpack('B', coef_string[i])[0]
        mem.extend(forest._octet_bits(octet))

    mem = mem[0:num_addresses]

    # Parse the wavefunction
    wf = np.zeros(num_wavefunction_octets / forest.OCTETS_PER_COMPLEX_DOUBLE, dtype=np.cfloat)
    for i, p in enumerate(xrange(num_memory_octets, num_octets, forest.OCTETS_PER_COMPLEX_DOUBLE)):
        re_be = coef_string[p: p + forest.OCTETS_PER_DOUBLE_FLOAT]
        im_be = coef_string[p + forest.OCTETS_PER_DOUBLE_FLOAT: p + forest.OCTETS_PER_COMPLEX_DOUBLE]
        re = struct.unpack('>d', re_be)[0]
        im = struct.unpack('>d', im_be)[0]
        wf[i] = complex(re, im)

    return wf, mem


if __name__ == "__main__":
    APP.run()
