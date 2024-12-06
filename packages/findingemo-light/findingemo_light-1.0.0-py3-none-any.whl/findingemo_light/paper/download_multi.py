"""

.. codeauthor:: Laurent Mertens <laurent.mertens@kuleuven.be>
"""
import os
import json

from urllib import request

import requests
from termcolor import cprint

from findingemo_light.config import Config


def _download_img(url: str, file_path: str, b_test=True):
    """

    :param url: url to the image to be downloaded
    :param file_path: full path, including filename, where the image will be downloaded to
    :param b_test: if True, don't download the image, just test the URL
    :return:
    """
    req = request.Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    res = request.urlopen(req, timeout=10)

    if not b_test:
        # Create output directory, if it does not already exist
        file_dir = os.path.dirname(file_path)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        # Download image
        with open(file_path, 'wb') as fout:
            fout.write(res.read())


def _query_waybackmachine(url: str, file_path: str, b_test):
    """
    Check if the URL is archived at WayBackMachine.

    :param url: the url to query WayBackMachine for
    :param file_path: full path, including filename, where the image will be downloaded to
    :return: False if no archived URL could be found, else the most recent archived URL
    """
    payload = {
        'url': url
    }
    archive_query_url = 'https://archive.org/wayback/available'
    response = requests.post(archive_query_url, data=payload, timeout=10, verify=True)

    try:
        archived_results = json.loads(response.content)
        archived_results = archived_results['results'][0]['archived_snapshots']
    except json.decoder.JSONDecodeError:
        return -1

    if archived_results:
        archived_url = archived_results['closest']['url']
        try:
            # Convert URL to direct link to image; thanks to Sihang Chen for catching this
            idx = archived_url.find(url)
            # Check for mismatch between "http" and "https" that can happen sometimes
            if idx < 0 and url.startswith('http://'):
                idx = archived_url.find(url.replace('http://', 'https://'))
            archived_url = archived_url[:idx - 1] + "if_" + archived_url[idx - 1:]
            _download_img(url=archived_url, file_path=file_path, b_test=b_test)
            cprint("\nImage downloaded through WayBackMachine!", color='red', force_color=True)
            return 1
        except Exception as e:
            cprint("\nFound a match through WayBackMachine, but could not download.", color='cyan', force_color=True)
            cprint(f"Error: {e}", color='cyan', force_color=True)
            return -1
    else:
        return 0

def download_data(target_dir: str):
    """
    Convenience method for the PyPi package version of the repo.

    :param target_dir: path to the folder to which the downloaded images will be written
    :return:
    """
    # Download again if file already exists?
    b_re_download = False
    # Path to the dataset_urls_merged.txt file
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(abs_dir, '..', 'data', 'dataset_urls_exploded.json')

    # Local parent folder where the images will be downloaded; will be created if it does not yet exist.
    parent_folder = target_dir

    not_found = set()

    json_data = json.load(open(url_file, 'r'))
    b_test = False

    downloaded_imgs = set()
    for img_idx, img_data in enumerate(json_data):
        rel_path = img_data['rel_path']
        img_url = img_data['url']
        url_idx = img_data['idx_url']

        img_path = os.path.join(parent_folder, *rel_path.split('/'))

        # Image was already successfully downloaded, move on
        if rel_path in downloaded_imgs or (not b_re_download and os.path.exists(img_path)):
            if not rel_path in downloaded_imgs:
                cprint(f"Image [{rel_path}] already exists, skipping...", color='yellow', force_color=True)
                downloaded_imgs.add(rel_path)
            continue

        print(f"\rTrying URL {url_idx}...", end='', flush=True)

        # Download URL
        try:
            _download_img(url=img_url, file_path=img_path, b_test=b_test)
            downloaded_imgs.add(rel_path)
            print(f"Downloaded: [{img_url}]")
            if rel_path in not_found:
                not_found.remove(rel_path)

        except Exception as e:
            cprint(f'\nCould not download image: {rel_path}\nURL: {img_url}', color='cyan', force_color=True)
            cprint(f"Error: {e}", color='cyan', force_color=True)
            cprint("Trying WayBackMachine...", end='', flush=True, color='cyan', force_color=True)
            wayback_hit = _query_waybackmachine(img_url, img_path, b_test=b_test)
            if wayback_hit < 1:
                not_found.add(rel_path)
                if wayback_hit == 0:
                    cprint(" no potatoes.", color='cyan', force_color=True)
            else:
                downloaded_imgs.add(rel_path)
                if rel_path in not_found:
                    not_found.remove(rel_path)

        print(f"\nDownloaded {len(downloaded_imgs)} images. Not found: {len(not_found)}")

    print("\nDone!")
    print("Here is a list of images that were not found:")
    for img_path in not_found:
        print(img_path)


if __name__ == '__main__':
    # Download again if file already exists?
    b_re_download = False
    # Path to the dataset_urls_merged.txt file
    url_file = os.path.join(Config.DIR_DATA, 'dataset_urls_exploded.json')

    # Local parent folder where the images will be downloaded; will be created if it does not yet exist.
    parent_folder = Config.DIR_IMAGES

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Just because an image does not download automatically does
    # not mean it is no longer available.
    # You can always try clicking on the links to see if they open
    # in your browser.
    # In case of HTTP 404's, Waybackmachine sometimes brings
    # solace.
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    not_found = set()

    json_data = json.load(open(url_file, 'r'))
    # If b_test is set to True, the script will just check whether the URLs are alive,
    # without downloading the images.
    b_test = False

    downloaded_imgs = set()
    for img_idx, img_data in enumerate(json_data):
        rel_path = img_data['rel_path']
        img_url = img_data['url']
        url_idx = img_data['idx_url']

        img_path = os.path.join(parent_folder, *rel_path.split('/'))

        # Image was already successfully downloaded, move on
        if rel_path in downloaded_imgs or (not b_re_download and os.path.exists(img_path)):
            if not rel_path in downloaded_imgs:
                cprint(f"Image [{rel_path}] already exists, skipping...", color='yellow', force_color=True)
                downloaded_imgs.add(rel_path)
            continue

        print(f"\rTrying URL {url_idx}...", end='', flush=True)

        # Download URL
        try:
            _download_img(url=img_url, file_path=img_path, b_test=b_test)
            downloaded_imgs.add(rel_path)
            print(f"Downloaded: [{img_url}]")
            if rel_path in not_found:
                not_found.remove(rel_path)

        except Exception as e:
            cprint(f'\nCould not download image: {rel_path}\nURL: {img_url}', color='cyan', force_color=True)
            cprint(f"Error: {e}", color='cyan', force_color=True)
            cprint("Trying WayBackMachine...", end='', flush=True, color='cyan', force_color=True)
            wayback_hit = _query_waybackmachine(img_url, img_path, b_test=b_test)
            if wayback_hit < 1:
                not_found.add(rel_path)
                if wayback_hit == 0:
                    cprint(" no potatoes.", color='cyan', force_color=True)
            else:
                downloaded_imgs.add(rel_path)
                if rel_path in not_found:
                    not_found.remove(rel_path)

        print(f"\nDownloaded {len(downloaded_imgs)} images. Not found: {len(not_found)}")

    print("\nDone!")
    print("Here is a list of images that were not found:")
    for img_path in not_found:
        print(img_path)
