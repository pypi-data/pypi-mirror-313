import os
import logging
import tempfile
import requests
from tqdm import tqdm
from functools import partial
from argparse import ArgumentParser
from requests.adapters import Retry
from concurrent.futures import ThreadPoolExecutor


FILE_DOWNLOAD_RETRY_TIMES = 5
FILE_DOWNLOAD_TIMEOUT = 60 * 5
FILE_DOWNLOAD_CHUNK_SIZE = 4096
LOCAL_DIR = os.path.join(os.path.expanduser('~'), '.cubeai_model_cache')
if not os.path.exists(LOCAL_DIR):
    os.mkdir(LOCAL_DIR)


def get_model_path(file_name):
    return os.path.join(LOCAL_DIR, file_name)


def download_file(url, file_dir, file_name):
    filepath = os.path.join(file_dir, file_name)
    if os.path.exists(filepath):
        logging.critical(f'File {filepath} already exist!')
        return

    temp_file_manager = partial(tempfile.NamedTemporaryFile, mode='wb', dir=file_dir, delete=False)
    get_headers = {}
    with temp_file_manager() as temp_file:
        logging.critical('downloading %s to %s', url, temp_file.name)
        # retry sleep 0.5s, 1s, 2s, 4s
        retry = Retry(total=FILE_DOWNLOAD_RETRY_TIMES, backoff_factor=1)
        while True:
            try:
                downloaded_size = temp_file.tell()
                get_headers['Range'] = 'bytes=%d-' % downloaded_size
                r = requests.get(url, stream=True, headers=get_headers, timeout=FILE_DOWNLOAD_TIMEOUT)
                r.raise_for_status()
                content_length = r.headers.get('Content-Length')
                total = int(content_length) if content_length is not None else None
                progress = tqdm(
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    total=total,
                    initial=downloaded_size,
                    desc='Downloading',
                )
                for chunk in r.iter_content(chunk_size=FILE_DOWNLOAD_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        progress.update(len(chunk))
                        temp_file.write(chunk)
                progress.close()
                break
            except (Exception) as e:  # no matter what happen, we will retry.
                retry = retry.increment('GET', url, error=e)
                retry.sleep()

    logging.critical('storing %s in cache at %s', url, file_dir)
    downloaded_length = os.path.getsize(temp_file.name)
    if total != downloaded_length:
        msg = 'File %s download incomplete, content_length: %s but the \
                    file downloaded length: %s, please download again' % (
            file_name, total, downloaded_length)
        logging.error(msg)
        filepath = filepath + '.incomplete'

    os.replace(temp_file.name, filepath)
    return filepath


def download_file_parallel(url, file_dir, file_name, parallels=4):
    filepath = os.path.join(file_dir, file_name)
    if os.path.exists(filepath):
        logging.critical(f'File {filepath} already exist!')
        return

    r = requests.get(url, stream=True, timeout=FILE_DOWNLOAD_TIMEOUT)
    r.raise_for_status()
    content_length = r.headers.get('Content-Length')
    file_size = int(content_length) if content_length is not None else None

    temp_file_manager = partial(tempfile.NamedTemporaryFile, mode='wb', dir=file_dir, delete=False)
    with temp_file_manager() as temp_file:
        logging.critical('downloading %s to %s', url, temp_file.name)
        progress = tqdm(
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            total=file_size,
            initial=0,
            desc='Downloading',
        )
        PART_SIZE = 100 * 1024 * 1012  # every part is 100M
        tasks = []
        end = -1
        for idx in range(int(file_size / PART_SIZE)):
            start = idx * PART_SIZE
            end = (idx + 1) * PART_SIZE - 1
            tasks.append((progress, start, end, url, temp_file.name))
        if end + 1 < file_size:
            tasks.append((progress, end + 1, file_size - 1, url, temp_file.name))
        with ThreadPoolExecutor(
                max_workers=parallels,
                thread_name_prefix='download') as executor:
            list(executor.map(download_part, tasks))

        progress.close()

    os.replace(temp_file.name, filepath)
    return filepath


def download_part(params):
    # unpack parameters
    progress, start, end, url, file_name = params
    get_headers = {}
    get_headers['Range'] = 'bytes=%s-%s' % (start, end)
    with open(file_name, 'rb+') as f:
        f.seek(start)
        r = requests.get(
            url,
            stream=True,
            headers=get_headers,
            timeout=FILE_DOWNLOAD_TIMEOUT)
        for chunk in r.iter_content(chunk_size=FILE_DOWNLOAD_CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                progress.update(len(chunk))


def download_file_cmd():
    parser = ArgumentParser()
    parser.add_argument('--url', default=None, help='待下载文件URL')
    parser.add_argument('--file-dir', default=None, help='下载后保存至该文件夹')
    parser.add_argument('--file-name', default=None, help='下载后保存至该文件名')
    args = parser.parse_args()

    if args.url is None or args.file_dir is None or args.file_name is None:
        parser.print_usage()
        return

    download_file(url=args.url, file_dir=args.file_dir, file_name=args.file_name)


def download_file_parallel_cmd():
    parser = ArgumentParser()
    parser.add_argument('--url', default=None, help='待下载文件URL')
    parser.add_argument('--file-dir', default=None, help='下载后保存至该文件夹')
    parser.add_argument('--file-name', default=None, help='下载后保存至该文件名')
    args = parser.parse_args()

    if args.url is None or args.file_dir is None or args.file_name is None:
        parser.print_usage()
        return

    download_file_parallel(url=args.url, file_dir=args.file_dir, file_name=args.file_name)


def download_model_cmd():
    parser = ArgumentParser()
    parser.add_argument('--url', default=None, help='待下载文件URL')
    parser.add_argument('--file-name', default=None, help='下载后保存至该文件名')
    args = parser.parse_args()

    if args.url is None or args.file_name is None:
        parser.print_usage()
        return

    download_file(url=args.url, file_dir=LOCAL_DIR, file_name=args.file_name)


def download_model_parallel_cmd():
    parser = ArgumentParser()
    parser.add_argument('--url', default=None, help='待下载文件URL')
    parser.add_argument('--file-name', default=None, help='下载后保存至该文件名')
    args = parser.parse_args()

    if args.url is None or args.file_name is None:
        parser.print_usage()
        return

    download_file_parallel(url=args.url, file_dir=LOCAL_DIR, file_name=args.file_name)


