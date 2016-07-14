import urllib.request
import zlib


def reverse_dict(d):
    return {v: k for k, v in d.items()}


def download_txt_url(path_to_file, url):
    with urllib.request.urlopen(url) as stream:
        CHUNK = 2 ** 14
        with open(path_to_file, 'wb') as outfile:
            while True:
                chunk = stream.read(CHUNK)
                if not chunk:
                    break
                outfile.write(chunk)


def stream_gzip_decompress(stream):
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            yield rv


def line_bytestream_gzip(in_fh):
    leftovers = b''
    for chunk in stream_gzip_decompress(in_fh):
        chunk = leftovers + chunk
        if chunk.endswith(b'\n'):
            for line in chunk.rstrip(b'\n').split(b'\n'):
                yield line
            leftovers = b''
        else:
            lines = chunk.split(b'\n')
            while len(lines) > 1:
                yield lines.pop(0)
            leftovers = lines.pop()
    if leftovers:
        yield leftovers


# Given a string, and start and end string, return the sandwiched string within the the original string
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
