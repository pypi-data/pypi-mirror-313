import oss2
import logging
import os
import time

from echobox.tool import byte
from echobox.tool import file


class AliyunOss:

    def __init__(self, app, oss_config, dry_run=False):
        self.logger = app.logger

        aliyun_stupid_loggers = ['oss2', 'ask_queue.py', 'http.py', 'select_response.py', 'auth.py', 'utils.py',
                                 'xml_utils.py', 'resumable.py', 'api.py']
        for logger in aliyun_stupid_loggers:
            logging.getLogger(logger).setLevel(logging.CRITICAL)

        auth = oss2.Auth(oss_config['access_key_id'], oss_config['access_key_secret'])
        self.bucket = oss2.Bucket(auth, 'http://%s' % (oss_config['endpoint']), oss_config['bucket'])
        self.dry_run = dry_run

    def check_file_exist_with_md5(self, filepath, oss_path):
        etag = ''
        try:
            result = self.bucket.head_object(oss_path)
            etag = result.etag
        except Exception as e:
            pass
        md5_file = file.md5_file(filepath)
        if etag and md5_file and etag.lower() == md5_file.lower():
            return True
        else:
            return False

    def upload_if_not_exist(self, filepath, oss_path):
        if not os.path.isfile(filepath):
            self.logger.error('upload_if_not_exist: %s => %s, file not exist', filepath, oss_path)
            return
        if self.check_file_exist_with_md5(filepath, oss_path):
            self.logger.info('upload: %s => %s, already exist', filepath, oss_path)
            return
        self.logger.debug('upload_if_not_exist: %s => %s', filepath, oss_path)
        self.upload(filepath, oss_path)

    def upload(self, filepath, oss_path):
        self.logger.info('prepare upload: %s(%s) => %s', filepath, byte.size_readable(bytes=os.path.getsize(filepath)), oss_path)
        if not self.dry_run:
            start = time.time()
            self.bucket.put_object_from_file(oss_path, filepath)
            self.logger.info('upload: %s => %s, took: %ss', filepath, oss_path, time.time() - start)

    def download(self, oss_path, filepath):
        self.logger.info('download: %s => %s', oss_path, filepath)
        file.ensure_dir_for_file(filepath)
        if not self.dry_run:
            start = time.time()
            self.bucket.get_object_to_file(oss_path, filepath)
            self.logger.info('download: %s => %s, took: %ss', oss_path, filepath, time.time() - start)
        else:
            self.logger.info('download: %s => %s', oss_path, filepath)

    def download_if_not_exist(self, oss_path, filepath):
        if self.check_file_exist_with_md5(filepath, oss_path):
            self.logger.info('download: %s => %s, already exist', oss_path, filepath)
            return
        self.logger.debug('download_if_not_exist: %s => %s', oss_path, filepath)
        self.download(oss_path, filepath)

    def download_dir_if_not_exist(self, oss_prefix=None, local_dir='/tmp'):
        if oss_prefix and not oss_prefix.endswith('/'):
            oss_prefix = oss_prefix + '/'

        for obj in oss2.ObjectIterator(self.bucket, prefix=oss_prefix, delimiter='/'):
            name = obj.key[len(oss_prefix):] if oss_prefix else obj.key
            obj_local_path = os.path.join(local_dir, name)

            if obj.is_prefix():
                self.download_dir_if_not_exist(obj.key, obj_local_path)
            else:
                obj_local_path = os.path.join(local_dir, name)
                self.download_if_not_exist(obj.key, obj_local_path)
