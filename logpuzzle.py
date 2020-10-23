#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # Define regex patterns for searching file for urls
    puzzle_regex = re.compile(r'(\S+puzzle\S+)')
    char_regex = re.compile(r'(\S+puzzle/p-)(\w{4})-(\w{4})')
    # initialize urls list
    urls = []
    # open file to be read/searched
    with open(filename, 'r') as f:
        # set server string variable
        server_regex = re.compile(r'(_)(\S+)')
        server_match = re.search(server_regex, filename)
        server = 'http://' + server_match.group(2)
        # search file line-by-line
        for line in f:
            # check each line against each regex pattern
            puzzle_match = re.search(puzzle_regex, line)
            char_match = re.search(char_regex, line)
            # handle matching of "letters-moreletters" pattern
            if char_match:
                # define sort key pattern for urls
                sort_key = char_match.group(3)
                # append sort key to beginning of url
                full_url = sort_key + server + puzzle_match.group(1)
                # create key-sortable url list
                if full_url not in urls:
                    urls.append(full_url)
            # use default criteria for url list creation
            elif puzzle_match:
                pattern = puzzle_match.group(1)
                full_url = server + pattern
                if full_url not in urls:
                    urls.append(full_url)
    # sort and return list of urls
    urls.sort()
    return urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # define count variable for image filenames
    count = 0
    # create and switch to destination dir
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        os.chdir(dest_dir)
    # simply switch to dir if it already exists
    else:
        os.chdir(dest_dir)
    # checks first letter of first url list item for key character
    if img_urls[0][0] == 'b':
        urls = []
        # strips key pattern from each url
        for url in img_urls:
            url = url[4:]
            urls.append(url)
        # Downloads each image via url and assigns filename
        for img in urls:
            print(f'Downloading image {count}...')
            urllib.request.urlretrieve(img, f'img{count}.jpg')
            count += 1
        # creates html file with stacked image tags to display in browser
        with open('index.html', 'w') as f:
            f.write('<html>\n<body>\n')
            for num in range(count):
                f.write(f'<img src =img{num}.jpg>')
            f.write('\n</body>\n</html>\n')
    # same behavior as above minus key stripping from urls
    else:
        for url in img_urls:
            print(f'Downloading image {count}...')
            urllib.request.urlretrieve(url, f'img{count}.jpg')
            count += 1

        with open('index.html', 'w') as f:
            f.write('<html>\n<body>\n')
            for num in range(count):
                f.write(f'<img src =img{num}.jpg>')
            f.write('\n</body>\n</html>\n')


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
