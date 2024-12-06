# -*- coding: utf-8 -*-
import hashlib
import os.path
import re
from datetime import datetime

from pytz import timezone
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session

from easymaker.api.api_sender import ApiSender
from easymaker.common import constants, exceptions


class ObjectStorage:
    DUPLICATE_CHECK_FILE_SIZE = 100 * 1024 * 1024  # 100MB 이상이면 기존에 업로드 된 동일한 파일이 있는지 확인
    MULTIPART_UPLOAD_FILE_SIZE_THRESHOLD = 2 * 1024 * 1024 * 1024  # 2GB 이상이면 분할 업로드 (2,147,483,647bytes 이상에서 OverflowError 발생해서 5G->2G로 변경)
    MULTIPART_UPLOAD_CHUNK_SIZE = 500 * 1024 * 1024  # 500MB 분할 업로드 파일당 크기
    MAX_OBJECT_LIST_COUNT = 10000

    def __init__(self, easymaker_region=None, username=None, password=None):
        self.token_expires = None
        self.api_sender = None

        if easymaker_region:
            self.region = easymaker_region
        elif os.environ.get("EM_REGION"):
            self.region = os.environ.get("EM_REGION")
        else:
            self.region = constants.DEFAULT_REGION
        self.username = username
        self.password = password

        self.session = Session()
        self.session.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1)))

    def _get_token(self, tenant_id=None):
        if tenant_id:
            self.tenant_id = tenant_id

        if self.token_expires is not None:
            if os.environ.get("EM_TOKEN"):
                self.now = datetime.now(timezone("Asia/Seoul"))
            else:
                self.now = datetime.utcnow()
            time_diff = self.token_expires - self.now
            if time_diff.total_seconds() > 600:
                return

        self.api_sender = ApiSender(self.region, os.environ.get("EM_APPKEY"), os.environ.get("EM_SECRET_KEY"))
        response = self.api_sender.get_objectstorage_token(tenant_id=self.tenant_id, username=self.username, password=self.password)
        try:
            self.token = response["access"]["token"]
        except KeyError:
            print(response)

        self.token_id = self.token["id"]

        if os.environ.get("EM_TOKEN"):
            self.token_expires = datetime.strptime(self.token["expires"], "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            self.token_expires = datetime.strptime(self.token["expires"], "%Y-%m-%dT%H:%M:%SZ")

    def _get_request_header(self):
        self._get_token(self.tenant_id)
        return {"X-Auth-Token": self.token_id}

    def _get_object_list(self, container_url, req_header, object_path, maker=None):
        response = self.session.get(container_url, headers=req_header, params={"prefix": object_path, "marker": maker})

        if response.status_code != 200 and response.status_code != 204:
            raise exceptions.EasyMakerError(response)

        return response.text.split("\n")[:-1]

    def _get_object_file_size(self, container_url, req_header, object_path):
        response = self.session.head(f"{container_url}/{object_path}", headers=req_header)

        if response.status_code != 200 and response.status_code != 204:
            raise exceptions.EasyMakerError(response)

        return response.headers["content-length"]

    def get_object_size(self, easymaker_obs_uri):
        """
        Args:
            easymaker_obs_uri : easymaker obs uri (obs://{object_storage_endpoint}/{container_name}/{path})
        """
        object_size_total = 0
        object_list, object_size = self._get_object_size(easymaker_obs_uri)
        object_size_total += object_size
        # 최대 10000건 조회 가능, 더 많은 경우 마지막 object부터 다시 조회 : https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/api-guide/#_17
        while len(object_list) == self.MAX_OBJECT_LIST_COUNT:
            object_list, object_size = self._get_object_size(easymaker_obs_uri, object_list[-1])
            object_size_total += object_size

        return object_size_total

    def _get_object_size(self, easymaker_obs_uri, marker=None):
        _, _, container_url, tenant_id, _, object_prefix = parse_obs_uri(easymaker_obs_uri)
        self._get_token(tenant_id)

        file_object_list = []
        object_size_total = 0
        object_list = self._get_object_list(container_url, self._get_request_header(), object_prefix, marker)
        for obj in object_list:
            if (object_prefix.endswith("/") == False) and (obj == object_prefix):  # target object is file
                object_size_total += int(self._get_object_file_size(container_url, self._get_request_header(), object_prefix))
                return object_size_total

            if object_prefix.endswith("/") == False:
                object_prefix = "".join([object_prefix, "/"])

            if (obj.startswith(object_prefix) or object_prefix == "/") and not obj.endswith("/"):
                file_object_list.append(obj)

        for file_object in file_object_list:
            object_size_total += int(self._get_object_file_size(container_url, self._get_request_header(), file_object))

        return object_list, object_size_total

    def upload(self, easymaker_obs_uri, local_path):
        """
        Args:
            easymaker_obs_uri : easymaker obs directory uri (obs://{object_storage_endpoint}/{container_name}/{path})
            local_path : upload local path (file or directory)
        """
        obs_full_url, _, _, tenant_id, _, _ = parse_obs_uri(easymaker_obs_uri)
        self._get_token(tenant_id)

        if os.path.isfile(local_path):
            upload_url = os.path.join(obs_full_url, os.path.basename(local_path))
            try:
                self._upload_file(upload_url, local_path)
            except FileNotFoundError as e:
                print(f"File not found: {e}")
                return
            except Exception as e:
                print(f"Error uploading file: {e}")
                return
        elif os.path.isdir(local_path):
            file_path_list = []
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    file_path_list.append(os.path.join(root, file))

            for upload_file_path in file_path_list:
                upload_url = os.path.join(obs_full_url, os.path.relpath(upload_file_path, os.path.abspath(local_path)))
                try:
                    self._upload_file(upload_url, upload_file_path)
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                    continue
                except Exception as e:
                    print(f"Error uploading file: {e}")
                    continue
        else:
            print(f"Path not found: {local_path}")

    def _calc_file_md5_hash(self, file_path):
        f = open(file_path, "rb")
        data = f.read()
        hash = hashlib.md5(data).hexdigest()
        return hash

    def _is_duplicate_file(self, request_url, local_file_path):
        file_size = os.path.getsize(local_file_path)

        if file_size < self.DUPLICATE_CHECK_FILE_SIZE:  # 크기 큰 파일만 동일 파일 존재 여부 확인
            return False

        self._get_token(self.tenant_id)
        req_header = self._get_request_header()

        response = self.session.head(request_url, headers=req_header)
        if response.status_code != 200:
            return False

        if response.headers["content-length"] == str(file_size):
            # 멀티파트 오브젝트의 ETag는 각 파트 오브젝트의 ETag 값을 이진 데이터로 변환하고 순서대로 연결해(concatenate) MD5 해시한 값이라 분할 업로드한 대용량 파일에서는 비교 불가
            if response.headers["etag"] == self._calc_file_md5_hash(local_file_path):
                return True

        return False

    def _upload_file(self, upload_url, upload_file_path):
        """
        Upload files under 5G
        Args:
            easymaker_obs_uri : obs object path (file)
            upload_file_path : upload local path (file)
        """
        if self._is_duplicate_file(upload_url, upload_file_path):
            return

        if os.path.getsize(upload_file_path) >= self.MULTIPART_UPLOAD_FILE_SIZE_THRESHOLD:
            return self._upload_large_file(upload_url, upload_file_path)

        req_header = self._get_request_header()
        with open(upload_file_path, "rb") as f:
            return self.session.put(upload_url, headers=req_header, data=f.read())

    def _upload_large_file(self, upload_url, upload_file_path):
        """
        Objects with a capacity exceeding 2 GB are uploaded in segments of 2 GB or less.
        """
        req_header = self._get_request_header()

        with open(upload_file_path, "rb") as f:
            chunk_index = 1
            chunk_size = self.MULTIPART_UPLOAD_CHUNK_SIZE
            total_bytes_read = 0
            obj_size = os.path.getsize(upload_file_path)

            while total_bytes_read < obj_size:
                remained_bytes = obj_size - total_bytes_read
                if remained_bytes < chunk_size:
                    chunk_size = remained_bytes

                request_url = "%s/%03d" % (upload_url, chunk_index)
                self.session.put(request_url, headers=req_header, data=f.read(chunk_size))
                total_bytes_read += chunk_size
                f.seek(total_bytes_read)
                chunk_index += 1

        # create manifest
        req_header = self._get_request_header()
        # X-Object-Manifest : AUTH_*****/ 뒷부분 경로
        uri_element_list = upload_url.split("/")
        for idx, val in enumerate(uri_element_list):
            if val.startswith("AUTH_"):
                object_manifest = "/".join(uri_element_list[idx + 1 :])
        req_header["X-Object-Manifest"] = object_manifest
        return self.session.put(upload_url, headers=req_header)

    def download(self, easymaker_obs_uri, download_dir_path):
        """
        Args:
            easymaker_obs_uri : easymaker obs uri (obs://{object_storage_endpoint}/{container_name}/{path})
            download_dir_path : download local path (directory)
        """
        object_list = self._download(easymaker_obs_uri, download_dir_path)
        # 최대 10000건 조회 가능, 더 많은 경우 마지막 object부터 다시 조회 : https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/api-guide/#_17
        while len(object_list) == self.MAX_OBJECT_LIST_COUNT:
            object_list = self._download(easymaker_obs_uri, download_dir_path, object_list[-1])

    def _download(self, easymaker_obs_uri, download_dir_path, maker=None):
        obs_full_url, _, container_url, tenant_id, _, object_prefix = parse_obs_uri(easymaker_obs_uri)
        self._get_token(tenant_id)

        file_object_list = []
        object_list = self._get_object_list(container_url, self._get_request_header(), object_prefix, maker)
        for obj in object_list:
            if (object_prefix.endswith("/") == False) and (obj == object_prefix):  # target object is file
                download_file_path = os.path.join(download_dir_path, os.path.basename(object_prefix))
                # object : depth1/file1
                # download_file_path => download_dir_path + /file1
                self._download_file(container_url, object_prefix, download_file_path)
                return object_list

            if object_prefix.endswith("/") == False:
                object_prefix = "".join([object_prefix, "/"])

            if (obj.startswith(object_prefix) or object_prefix == "/") and not obj.endswith("/"):
                file_object_list.append(obj)

        for file_object in file_object_list:
            if object_prefix == "/":
                download_file_path = os.path.join(download_dir_path, file_object)
            else:
                download_file_path = os.path.join(download_dir_path, os.path.relpath(file_object, object_prefix))
            # object : deps1/deps2, file_object : deps1/deps2/deps3/file1
            # download_file_path => download_dir_path + /deps3/file1
            self._download_file(container_url, file_object, download_file_path)

        return object_list

    def _download_file(self, container_url, file_object, download_file_path):
        """
        Args:
            container_url : obs container url (https://{object_storage_endpoint}/{container_name})
            file_object : obs object path (file)
            download_file_path : download local path (file)
        """
        request_url = os.path.join(container_url, file_object)
        req_header = self._get_request_header()
        response = self.session.get(request_url, headers=req_header)

        if response.status_code != 200:
            raise exceptions.EasyMakerError(f"Object storage download fail {response.json()}")
        download_file_dir = os.path.dirname(download_file_path)
        if os.path.isfile(download_file_dir):
            raise exceptions.EasyMakerError(f"{download_file_dir} already exists as file. Please check if there is a file and a folder with the same names in object storage.")

        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as f:
            f.write(response.content)

    def find_object_list(self, easymaker_obs_uri, file_extension=None):
        _, _, container_url, tenant_id, _, object_prefix = parse_obs_uri(easymaker_obs_uri)
        self._get_token(tenant_id)
        object_list = self._get_object_list(container_url, self._get_request_header(), object_prefix)

        if not file_extension:
            return object_list

        find_object_list = []
        for object in object_list:
            if object.endswith(file_extension):
                find_object_list.append(object)

        return find_object_list

    def delete(self, easymaker_obs_uri, file_extension=None):
        _, _, container_url, tenant_id, _, object_prefix = parse_obs_uri(easymaker_obs_uri)
        self._get_token(tenant_id)

        file_object_list = []
        object_list = self.find_object_list(easymaker_obs_uri, file_extension)
        for obj in object_list:
            if (object_prefix.endswith("/") == False) and (obj == object_prefix):  # target object is file
                request_url = os.path.join(container_url, object_prefix)
                return self._delete_file(request_url)

            if object_prefix.endswith("/") == False:
                object_prefix = "".join([object_prefix, "/"])

            if (obj.startswith(object_prefix) or object_prefix == "/") and not obj.endswith("/"):
                file_object_list.append(obj)

        for file_object in file_object_list:
            request_url = os.path.join(container_url, file_object)
            self._delete_file(request_url)

    def _delete_file(self, request_url):
        print(f"Delete Object : {request_url}")
        response = self.session.delete(request_url, headers=self._get_request_header())
        if response.status_code != 200 and response.status_code != 204 and response.status_code != 404:
            raise exceptions.EasyMakerError(response)

        return response


def parse_obs_uri(easymaker_obs_uri):
    obs_full_url, number_of_subs_made = re.subn("^(obs)://(.+)$", r"https://\2", easymaker_obs_uri)
    obs_uri_pattern = re.compile("^(?P<container_url>https://(?P<obs_host>[^/]+)/(?P<version>[^/]+)/AUTH_(?P<tenant_id>[^/]+)/(?P<container_name>[^/]+))/?(?P<object_prefix>.*)$")
    match = obs_uri_pattern.match(obs_full_url)

    if number_of_subs_made != 1 or match is None:
        raise exceptions.EasyMakerError(f"Object storage uri parse fail. Invalid uri {easymaker_obs_uri}")

    return obs_full_url, match.group("obs_host"), match.group("container_url"), match.group("tenant_id"), match.group("container_name"), match.group("object_prefix")


def download(easymaker_obs_uri, download_dir_path, easymaker_region=None, username=None, password=None):
    """
    Args:
        easymaker_obs_uri (str): easymaker obs uri (obs://{object_storage_endpoint}/{container_name}/{path})
        download_dir_path (str): download local path (directory)
        easymaker_region (str): NHN Cloud object storage Region
        username (str): NHN Cloud object storage username
        password (str): NHN Cloud object storage password
    """
    object_storage = ObjectStorage(easymaker_region=easymaker_region, username=username, password=password)
    object_storage.download(easymaker_obs_uri, download_dir_path)


def upload(easymaker_obs_uri, local_path, easymaker_region=None, username=None, password=None):
    """
    Args:
        easymaker_obs_uri (str): easymaker obs directory uri (obs://{object_storage_endpoint}/{container_name}/{path})
        local_path (str): upload local path (file or directory)
        easymaker_region (str): NHN Cloud object storage Region
        username (str): NHN Cloud object storage username
        password (str): NHN Cloud object storage password
    """
    object_storage = ObjectStorage(easymaker_region=easymaker_region, username=username, password=password)
    object_storage.upload(easymaker_obs_uri, local_path)


def delete(easymaker_obs_uri, file_extension=None, easymaker_region=None, username=None, password=None):
    """
    Args:
        easymaker_obs_uri (str): easymaker obs directory uri (obs://{object_storage_endpoint}/{container_name}/{path})
        file_extension (str): Target file extension
        easymaker_region (str): NHN Cloud object storage Region
        username (str): NHN Cloud object storage username
        password (str): NHN Cloud object storage password
    """
    object_storage = ObjectStorage(easymaker_region=easymaker_region, username=username, password=password)
    object_storage.delete(easymaker_obs_uri, file_extension)


def find_object_list(easymaker_obs_uri, file_extension=None, easymaker_region=None, username=None, password=None):
    """
    Args:
        easymaker_obs_uri (str): easymaker obs directory uri (obs://{object_storage_endpoint}/{container_name}/{path})
        file_extension (str): Target file extension
        easymaker_region (str): NHN Cloud object storage Region
        username (str): NHN Cloud object storage username
        password (str): NHN Cloud object storage password
    """
    object_storage = ObjectStorage(easymaker_region=easymaker_region, username=username, password=password)
    return object_storage.find_object_list(easymaker_obs_uri, file_extension)


def get_object_size(easymaker_obs_uri, easymaker_region=None, username=None, password=None):
    """
    Args:
        easymaker_obs_uri (str): easymaker obs directory uri (obs://{object_storage_endpoint}/{container_name}/{path})
        easymaker_region (str): NHN Cloud object storage Region
        username (str): NHN Cloud object storage username
        password (str): NHN Cloud object storage password
    """
    object_storage = ObjectStorage(easymaker_region=easymaker_region, username=username, password=password)
    return object_storage.get_object_size(easymaker_obs_uri)
