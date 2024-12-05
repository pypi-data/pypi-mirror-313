import os
import getpass
import subprocess
import fnmatch
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


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.modelers_cache')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


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


def download_model(model_id, threads=8, parallels=1, include=None, exclude=None, download_subdir='yes'):
    clone_url = 'https://modelers.cn/{}.git'
    file_url = 'https://modelers.cn/api/v1/file/{}/main/media/{}'

    if model_id.find('/') < 1:
        print('model_id格式不对！')
        return None

    model_dir = os.path.join(CACHE_DIR, model_id)
    if os.path.exists(model_dir):
        print('模型 {} 已存在！'.format(model_id))
        return model_dir

    # install aria2 and git
    username = getpass.getuser()
    cmd_prefix = '' if username == 'root' else 'sudo '
    status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt update')
    if status != 0:
        print('apt update 失败！')

    status, _ = subprocess.getstatusoutput('command -v aria2c')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y aria2')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y aria2')
            if status != 0:
                print('安装 aria2 失败！')
                return None

    status, _ = subprocess.getstatusoutput('command -v git')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y git')
            if status != 0:
                print('安装 git 失败！')
                return None

    status, _ = subprocess.getstatusoutput('command -v git-lfs')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git-lfs')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y git-lfs')
            if status != 0:
                print('安装 git-lfs 失败！')
                return None

    cwd = os.getcwd()
    model_owner, model_name = model_id.split('/')
    owner_dir = os.path.join(CACHE_DIR, model_owner)
    if not os.path.exists(owner_dir):
        os.mkdir(owner_dir)
    os.chdir(owner_dir)

    # Clone模型代码（不下载长文件）
    url = clone_url.format(model_id)
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'
    status, _ = subprocess.getstatusoutput('git clone ' + url)
    if status != 0:
        print('克隆 {} 失败！'.format(url))
        os.chdir(cwd)
        return None

    # 找出所有长文件
    os.chdir(model_dir)
    status, output = subprocess.getstatusoutput('git lfs ls-files')
    output = output.split('\n')
    ls_files = []
    for line in output:
        file = line.split(' ')[2]
        ls_files.append(file)
        os.system('truncate -s 0 ' + file)

    # 下载所有长文件
    for file in ls_files:
        if download_subdir != 'yes':
            if file.find('/') >= 0:
                continue

        url = file_url.format(model_id, file)
        file_dir = subprocess.getoutput('dirname ' + file)
        file_name = subprocess.getoutput('basename ' + file)

        if include is not None:
            match = False
            for pattern in include:
                if not fnmatch.fnmatch(file_name, pattern):
                    match = True
                    os.system('rm ' + file)
                    break
            if match:
                continue

        if exclude is not None:
            match = False
            for pattern in exclude:
                if fnmatch.fnmatch(file_name, pattern):
                    match = True
                    os.system('rm ' + file)
                    break
            if match:
                continue

        os.system('mkdir -p ' + file_dir)
        status = os.system('aria2c -x {} -s {} -k 1M -c {} -d {} -o {}'.format(threads, threads, url, file_dir, file_name))
        if status != 0:
            os.system('rm ' + file)
            if parallels > 1:
                download_file_parallel(url, file_dir, file_name, parallels=parallels)
            else:
                download_file(url, file_dir, file_name)

    os.chdir(cwd)
    return os.path.join(CACHE_DIR, model_id)


def download_model_cmd():
    parser = ArgumentParser()
    parser.add_argument('model_id', default=None, help='Modelers model ID, like: model_owner/model_name')
    parser.add_argument('--threads', default=8, type=int, help='Number of download threads for aria2c')
    parser.add_argument('--parallels', default=1, type=int, help='Number of download threads for requests')
    parser.add_argument('--include', default=None,
                        help='The patterns to only download these filenames, seperated with ","')
    parser.add_argument('--exclude', default=None,
                        help='The patterns to match against filenames for exclusion, seperated with ","')
    parser.add_argument('--download-subdir', default='yes', help='Download sub-dir')
    args = parser.parse_args()

    if args.model_id is None:
        parser.print_usage()
        return

    include = None if args.include is None else args.include.split(',')
    exclude = None if args.exclude is None else args.exclude.split(',')
    download_model(model_id=args.model_id, threads=args.threads, parallels=args.parallels, include=include, exclude=exclude,
                   download_subdir=args.download_subdir)


if __name__ == '__main__':
    download_model('jeffding/llama-68m-openmind')
