#!/usr/bin/env python
import os
import tarfile
import requests

MATHJAX_PATH = "_static/javascript/MathJax-3.0.5"
MATHJAX_URL = "http://www.silx.org/pub/nabu/static/MathJax-3.0.5.tar.lzma"


def download_file(file_url, target_file_path):
    print("Downloading %s" % file_url)
    rep = requests.get(file_url)
    with open(target_file_path, "wb") as f:
        f.write(rep.content)


def uncompress_file(compressed_file_path, target_directory):
    print("Uncompressing %s into %s" % (compressed_file_path, target_directory))
    with tarfile.open(compressed_file_path) as f:
        f.extractall(path=target_directory)


def main():
    doc_path = os.path.dirname(os.path.realpath(__file__))
    mathjax_path = os.path.join(doc_path, MATHJAX_PATH)
    if os.path.isdir(mathjax_path):
        return
    mathjax_comp_file = mathjax_path + ".tar.lzma"
    download_file(MATHJAX_URL, mathjax_comp_file)
    uncompress_file(mathjax_comp_file, os.path.dirname(mathjax_path))


if __name__ == "__main__":
    main()
