import urllib.request
import zlib


def reverse_dict(d):
    return {v: k for k, v in d.items()}


def download_txt_url(path_to_file, url):
    with urllib.request.urlopen(url) as stream:
        with open(path_to_file, 'wb') as outfile:
            for line in stream:
                outfile.write(line)


def stream_gzip_decompress(stream):
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            yield rv
