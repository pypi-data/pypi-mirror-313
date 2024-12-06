#!/usr/bin/env python3

import numpy as np
from PIL import Image
from numba import jit, prange

def average_entropy(filename, stereo=False):
    im = Image.open(filename)

    if stereo:
        im = im.convert("RGB")
        r, g, b = im.split()

        return (_average_entropy(np.asarray(r, dtype=np.float64)),
                _average_entropy(np.asarray(g, dtype=np.float64)))

    else:
        im = im.convert("L")
        return _average_entropy(np.asarray(im, dtype=np.float64))

@jit(nopython=True, parallel=True, nogil=True)
def _average_entropy(im):
    num_freqs = im.shape[1]
    num_spectra = im.shape[0]
    im = im ** 2 # to account for sqrt scaling

    entropies = np.zeros(num_spectra)
    for row_idx in prange(num_spectra):
        psd = (im[row_idx] ** 2) / num_freqs

        pdf = psd
        if np.sum(psd) != 0:
            pdf /= np.sum(psd)

        entropy = 0
        for p in pdf:
            if p != 0:
                entropy -= p * np.log(p)

        entropies[row_idx] = entropy
        
    return sum(entropies) / len(entropies)



