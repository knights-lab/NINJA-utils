import urllib.request


def reverse_dict(d):
    return {v: k for k, v in d.items()}


def download_txt_url(path_to_file, url):
    with urllib.request.urlopen(url) as stream:
        with open(path_to_file, 'wb') as outfile:
            for line in stream:
                outfile.write(line)
