import logging
from sys import path
import requests
import hashlib
import os
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor,as_completed
import base64
import time
from Crypto.Cipher import AES
import datetime

from PIL import Image
from moviepy import VideoFileClip

from os.path import join, dirname, abspath, basename, exists
from typing import Optional, Dict, Any, List
from os import makedirs
from .types import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnkerAutoTrainSDK:
    def __init__(self, url="https://dataloop.anker-in.com"):
        self.url = url
        self.logger = logging.getLogger(__name__)

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()

    def _get_file_meta(self, file_path: str) -> FileMeta:
        """获取文件的宽度和高度，如果是视频，还返回时长"""
        try:
            # Try to open the file as an image
            with Image.open(file_path) as img:
                width, height = img.size
                resolution = Resolution(width=width, height=height)
                return FileMeta(resolution=resolution, tokenLength=0, duration=0)
        except IOError:
            # If it fails, try to open the file as a video
            try:
                with VideoFileClip(file_path) as video:
                    width, height = video.size
                    duration = int(video.duration)  # Convert duration to int
                    resolution = Resolution(width=width, height=height)
                    return FileMeta(resolution=resolution, tokenLength=0, duration=duration)
            except Exception as e:
                # If it fails, return a default FileMeta and log the error
                print(f"Error reading file {file_path}: {e}")
                return None

    def _query_origin_data(self, query_data: dict) -> dict:
        try:
            url = f"{self.url}/query_origin_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_data)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while querying origin data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")

    def _summarize_and_download(self, dataset_name: str, dataset_version: str) -> SummaryAndDownloadDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/summarize_and_download"
            headers = { 'accept': 'application/json', 'Content-Type': 'application/json' }
            dataset_list = [{"datasetName": dataset_name, "datasetVersion": dataset_version}]
            dataset_info = {"dataset": dataset_list}
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return SummaryAndDownloadDataSetResponse(
                url=response.get("url", ""),
                bucket=response.get("bucketName", ""),
                object_name=response.get("objectName", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while summarizing and downloading dataset: {e}")

    def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        # get upload url
        try:
            url = f"{self.url}/get_upload_url"
            file_name = basename(file_path)
            response = requests.post(url, params={"directory": directory, "file_name": file_name})
            response.raise_for_status()  # Check for HTTP errors
            response = response.json()
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            print(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
        except Exception as e:
            print(f"An error occurred while getting upload URL: {e}")
            raise Exception(f"An error occurred while getting upload URL: {e}")

        # upload file by url
        try:
            upload_url = response.get("url")  # Get the upload URL from the response
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # Calculate the file's MD5
            file_meta = self._get_file_meta(file_path)  # Get the file's metadata
            # Then put to this path
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # Check for HTTP errors
                return UploadFileResponse(
                    url=upload_url,
                    bucket=response.get("bucket", ""),
                    storage_id=response.get("storage_id", ""),
                    object_name=response.get("object_name", ""),
                    uid=file_md5,
                    meta=file_meta
                )
        except requests.exceptions.RequestException as e:
            detail = None
            if res is not None:
                try:
                    detail = res.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading file: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")

    # def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
    #     try:
    #         url = f"{self.url}/get_upload_url"
    #         file_name = basename(file_path)
    #         response = requests.post(url, params={"directory": directory, "file_name": file_name})
    #         response.raise_for_status()  # 检查HTTP错误
    #         response = response.json()
    #     except requests.exceptions.RequestException as e:
    #         if response is None:
    #             raise Exception(f"HTTP error occurred while getting upload URL: {e}")
    #         detail = response.json().get("detail")
    #         raise Exception(f"HTTP error occurred while getting upload URL: {detail}")
    #     except ValueError as e:
    #         raise Exception(f"Error parsing JSON response: {e}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while getting upload URL: {e}")

    #     try:
    #         upload_url = response.get("url")  # 从响应中获取上传URL
    #         if not upload_url:
    #             raise Exception("No upload URL found in the response.")
    #         file_md5 = self._calculate_md5(file_path)  # 计算文件的MD5
    #         # 然后put到这个路径
    #         with open(file_path, "rb") as f:
    #             res = requests.put(upload_url, data=f)
    #             res.raise_for_status()  # 检查HTTP错误
    #             return UploadFileResponse(
    #                 url=upload_url,
    #                 bucket=response.get("bucket", ""),
    #                 storage_id=response.get("storage_id", ""),
    #                 object_name=response.get("object_name", ""),
    #                 uid=file_md5
    #             )
    #     except requests.exceptions.RequestException as e:
    #         if res is None:
    #             raise Exception(f"HTTP error occurred while uploading file: {e}")
    #         detail = res.json().get("detail")
    #         raise Exception(f"HTTP error occurred while uploading file: {detail}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while uploading file: {e}")

    def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/upload_raw_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            print(f"upload raw_data: {raw_data}")
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response_json = response.json()
            if response_json.get("raw_data_id") is None:
                print(f"Failed to upload raw data: {response_json.get('detail', 'No detail provided')}")
            return UploadRawDataResponse(
                raw_data_id=response_json.get("raw_data_id", "")
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading raw data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")

    # def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
    #     try:
    #         url = f"{self.url}/upload_raw_data"
    #         headers = {
    #             'accept': 'application/json',
    #             'Content-Type': 'application/json'
    #         }  # 设置请求头
    #         response = requests.post(url, headers=headers, json=raw_data)
    #         response.raise_for_status()  # 检查HTTP错误
    #         response = response.json()
    #         return UploadRawDataResponse(
    #             raw_data_id=response.get("raw_data_id", "")
    #         )
    #     except requests.exceptions.RequestException as e:
    #         if response is None:
    #             raise Exception(f"HTTP error occurred while uploading raw data: {e}")
    #         detail = response.json().get("detail")
    #         raise Exception(f"HTTP error occurred while uploading raw data: {detail}")
    #     except ValueError as e:
    #         raise Exception(f"Error parsing JSON response: {e}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while uploading raw data: {e}")

    def upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadFileWithInfoResponse:
        try:
            # 上传文件
            upload_file_response = self.upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name, "storageId": upload_file_response.storage_id, "bucket": upload_file_response.bucket}

            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "medium"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0 if raw_data.get('meta') is not None else 1

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            upload_info_response = self.upload_raw_data(raw_data)
            # print(f"Raw data uploaded with file: {raw_data}")
            return UploadFileWithInfoResponse(
                url=upload_file_response.url,
                bucket=upload_file_response.bucket,
                storage_id=upload_file_response.storage_id,
                object_name=upload_file_response.object_name,
                uid=upload_file_response.uid,
                raw_data_id=upload_info_response.raw_data_id,
                meta=upload_file_response.meta
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if e.response is not None:
                try:
                    detail = e.response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading data with info: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {str(e)}")

    def upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse: 
        try:
            url = f"{self.url}/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadAnnotationDataResponse( 
                annotation_data_id=response.get("id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while uploading annotated data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")

    def download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while getting download URL: {detail}")
            else:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        try:
            download_url = response.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while downloading file: {detail}")
            else:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")

    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self._query_origin_data(query_origin_data)

            if not origin_data:  # 检查origin_data是否为空
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:  # 检查records是否为空
                raise Exception("No origin data found for the given UID.")

            record = records[0]  # 获取第一个记录
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return self.download_file_by_storage(storage_id, bucket, object_name, directory)  # 调用原始下载方法
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

    def create_dataset(self, dataset_info: dict) -> CreateDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/version"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 棃查HTTP错误
            response = response.json()
            return CreateDataSetResponse(
                dataset_id=response.get("dataset_version_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while creating dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while creating dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while creating dataset: {e}")

    def link_dataset(self, annotation_id_list: list, dataset_id: str) -> dict:
        try:
            # 去除annotation_id_list中的重复元素
            unique_annotation_id_list = list(set(annotation_id_list))

            url = f"{self.url}/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            dataset_info = {
                "annotationIds": unique_annotation_id_list,
                "annotationVersionId": dataset_id
            }
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while linking dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while linking dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking dataset: {e}")

    def download_dataset(self, dataset_name: str, dataset_version: str, directory: str) -> str:
        try:
            download_response = self._summarize_and_download(dataset_name, dataset_version)

            download_url = download_response.url  # 从响应中获取下载URL
            download_object_name = download_response.object_name
            if not download_url:
                raise Exception("No download URL found in the download_dataset.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, download_object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while downloading dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while downloading dataset: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading dataset: {e}")

    def batch_download_annotation4human(
        self, req: dict, file_path="./data.json", thread_nums: int = 4
    ) -> str:
        """创建数据集

        Args:
            req (dict): 请求参数
            file_path (str): 输出文件路径
            thread_nums (int, optional): 线程数量. Defaults to 4.

        Returns:
            str: 处理结果
        """
        logger = self.logger
        logger.info("开始处理数据集创建请求...")

        param = CreateDatasetRequest.model_validate(req)
        multi_query_data = []

        # 处理多标签查询
        if param.mutipleLabelQuery:
            for i in param.mutipleLabelQuery:
                query_data = param.model_dump()
                if i.get("label"):
                    query_data["labelQuery"] = {
                        "label": i.get("label", ""),
                    }
                multi_query_data.append(query_data)

        query_data = param.model_dump()
        multi_query_data = [query_data] if len(multi_query_data) == 0 else multi_query_data

        # 查询总数
        logger.info("开始查询标注数据总数...")
        label_count = 0
        for i in tqdm(multi_query_data, desc="查询数据总数"):
            try:
                data = requests.post(f"{self.url}/data/annotation/query", json=i)
                data.raise_for_status()
                data = data.json()
                if data["total"] > 0:
                    i["total_count"] = int(data["total"])
                    label_count += int(data["total"])
            except Exception as e:
                logger.error(f"查询总数失败: {str(e)}")
                continue

        logger.info(f"找到总计 {label_count} 条标注数据")

        # 分页查询数据
        page_size = 1000
        annotation_data = []

        def fetch_page_data(args):
            query, page = args
            current_query = query.copy()  # 创建查询参数的副本
            current_query["limit"] = page_size
            current_query["skip"] = (page - 1) * page_size
            try:
                data = requests.post(
                    f"{self.url}/data/annotation/query_no_total", json=current_query
                )
                data.raise_for_status()
                return data.json()["records"]
            except Exception as e:
                logger.error(f"获取页面 {page} 数据失败: {str(e)}")
                return []

        logger.info("开始分页获取标注数据...")
        all_page_args = []

        # 收集所有查询的分页参数
        for query in multi_query_data:
            if "total_count" in query:
                total_pages = (query["total_count"] + page_size - 1) // page_size
                page_args = [(query, page) for page in range(1, total_pages + 1)]
                all_page_args.extend(page_args)

        # 使用线程池并行处理所有页面
        with ThreadPoolExecutor(max_workers=thread_nums) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_page_data, all_page_args),
                    total=len(all_page_args),
                    desc="获取标注数据",
                )
            )
            for result in results:
                if result:
                    annotation_data.extend(result)

        logger.info(f"成功获取 {len(annotation_data)} 条标注数据")

        # 获取原始数据ID
        raw_data_ids = list(
            set(
                item["dataId"][0]
                for item in annotation_data
                if item.get("dataId") and len(item["dataId"]) > 0
            )
        )

        def fetch_raw_data_batch(id_batch):
            """批量获取原始数据
            
            Args:
            id_batch (list): UID列表
            """
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    data = requests.post(
                    f"{self.url}/batch_query_origin_data", json={"uids": id_batch}
                    )
                    data.raise_for_status()
                    return data.json()["records"]
                except Exception as e:
                    logger.error(f"批量获取原始数据失败: {str(e)}, UIDs: {id_batch[:5]}... 尝试次数: {attempt + 1}")
                    if attempt == max_retries - 1:  
                        return []

        logger.info(f"开始获取原始数据，共 {len(raw_data_ids)} 条...")
        raw_data = []
        # 将ID列表分割成批次
        id_batches = [
            raw_data_ids[i:i + page_size] 
            for i in range(0, len(raw_data_ids), page_size)
        ]
        with ThreadPoolExecutor(max_workers=thread_nums * 10) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_raw_data_batch, id_batches),
                    total=len(id_batches),
                    desc="获取原始数据",
                )
            )
            # 展平结果列表
            for batch_result in results:
                if batch_result:
                    raw_data.extend(batch_result)

        logger.info(f"成功获取 {len(raw_data)} 条原始数据")

        # 保存数据到文件
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"originalData": raw_data, "annotationData": annotation_data},
                    f,
                    ensure_ascii=False,
                )
            logger.info(f"数据已保存到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存数据到文件失败: {str(e)}")

        logger.info("数据集创建完成!")
        return raw_data

    def get_download_url(self, storage_id: str, bucket: str, object_name: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return response.get("url", "")
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while getting download URL: {detail}")
            else:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")
    
    
    def _get_basic_auth_token(self, username: str, password: str) -> str:
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return token

    def get_raw_data_summary(self, username: str, password: str,  bg: str, startDate: str, endDate: str, projectId: Optional[List[str]] = None) -> dict:
        try:
            url = f"{self.url}/report/generateReport"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f"Basic {self._get_basic_auth_token(username, password)}"  # Add the Basic Authorization header
            }
            query = {
                "bg": bg,
                "startDate": startDate,
                "endDate": endDate
            } if projectId is None else {
                "bg": bg,
                "startDate": startDate,
                "endDate": endDate,
                "projectId": projectId
            }
            response = requests.post(url, headers=headers, json=query)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return response
        except requests.exceptions.RequestException as e:
            detail = None
            if e.response is not None:
                try:
                    detail = e.response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while getting raw data summary: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting raw data summary: {e}")

    def get_raw_data_statistics(self, username: str, password: str, bg: str, date: str, task: str) -> GetRawDataResponse:
        try:
            response = self.get_raw_data_summary(username, password, bg, date, date)
        except Exception as e:
            raise Exception(f"Failed to get raw data summary: {e}")

        if isinstance(response, list) and len(response) > 0:
            response = response[0]  # Access the first dictionary in the list

        num_videos = response.get("numVideos") if response.get("numVideos") else 0
        num_images = response.get("numImages") if response.get("numImages") else 0
        num_device = response.get("numDevice") if response.get("numDevice") else 0
        num_labels = response.get("numLabels") if response.get("numLabels") else 0
        num_hardcase = response.get("numHardcase") if response.get("numHardcase") else 0
        task_hardcase = 0

        if bg == 'ap':
            details = response.get("details", {})
            all_details = details.get("all", [])

            for item in all_details:
                if item.get("label") == task:
                    task_hardcase = item.get("numHardcase", 0)
                    break

        elif bg == 'zx':
            details = response.get("details", {})
            for project_id, types in details.items():
                for type in types:
                    if type.get("label") == task:
                        task_hardcase += type.get("numHardcase", 0)

        return GetRawDataResponse(
            num_video=num_videos,
            num_image=num_images,
            num_device = num_device,
            num_label = num_labels,
            num_hardcase = num_hardcase,
            task_hardcase = task_hardcase
        )

    def download_raw_data4human(
        self, file_path="./data.json", dist_path="./data", thread_num=4
    ):
        """
        多线程下载原始数据文件

        Args:
            file_path (str): JSON文件路径
            dist_path (str): 下载文件保存目录
            thread_num (int): 线程数量
        """
        logging.info(f"开始下载数据，源文件：{file_path}")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise Exception(f"找不到源文件: {file_path}")

        # 创建目标目录
        abs_path = os.path.abspath(dist_path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
            logging.info(f"创建目标目录: {abs_path}")

        # 读取JSON文件
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"读取JSON文件失败: {str(e)}")
            raise

        # 获取原始数据
        raw_data = data.get("originalData", [])
        total_files = len(raw_data)
        logging.info(f"共找到 {total_files} 个文件待下载")

        if total_files == 0:
            logging.warning("没有找到需要下载的文件")
            return

        # 定义下载任务
        def download_task(item):
            try:
                storage = item.get("storage", {})
                storage_id = storage.get("storageId")
                bucket = storage.get("bucket")
                object_name = storage.get("objectName")
                target_path = os.path.join(abs_path, object_name)

                self.download_file_by_storage(storage_id, bucket, object_name, target_path)
                return True
            except Exception as e:
                logging.error(f"下载文件失败 {object_name}: {str(e)}")
                return False

        # 使用线程池进行并发下载
        success_count = 0
        with ThreadPoolExecutor(max_workers=thread_num) as executor:
            # 使用tqdm显示进度
            results = list(
                tqdm(
                    executor.map(download_task, raw_data),
                    total=total_files,
                    desc="下载进度",
                )
            )

            success_count = sum(1 for x in results if x)

        # 打印下载结果统计
        logging.info(f"下载完成: 成功 {success_count}/{total_files}")
        if success_count < total_files:
            logging.warning(f"有 {total_files - success_count} 个文件下载失败")

        return

    def get_datasets_statistics(self, dataset_ids: List[str], thread_nums=4) -> Dict[str, LabelStatsResponse]:
        """
        批量获取多个数据集的统计信息

        Args:
            dataset_ids: 数据集ID列表
            thread_nums: 线程数量 默认是4
        Returns:
            Dict[str, LabelStatsResponse]: 数据集ID到统计信息的映射
        """
        results = {}

        def process_single_dataset(dataset_id: str) -> tuple[str, LabelStatsResponse]:
            """处理单个数据集的统计信息"""
            try:
                logging.info(f"开始处理数据集 {dataset_id}")

                # 获取标签统计信息
                url = f"{self.url}/data/annotation/version/label_stats"
                response = requests.post(url, json={"datasetId": dataset_id}, auth=("AIDC", "AIDC_PASSWORD"))
                response.raise_for_status()
                response = response.json()
                label_stats = LabelStatsResponse.model_validate(response)

                # 计算百分比
                for label in label_stats.labelStats:
                    label.percent = round(label.count / label_stats.totalCount, 4)

                # 获取数据集图片信息
                url = f"{self.url}/data/annotation/version/{dataset_id}"
                response = requests.get(url)
                response.raise_for_status()
                dataIds = response.json()["dataIds"]

                # 批量查询图片信息
                def query_batch(id_batch):
                    url = f"{self.url}/data/annotation/query_batch"
                    response = requests.post(url, json={"annotationIds": id_batch})
                    response.raise_for_status()
                    return response.json()["records"]

                # 将数据分批
                batch_size = 1000
                batches = [dataIds[i:i + batch_size] for i in range(0, len(dataIds), batch_size)]

                data = []
                with ThreadPoolExecutor(max_workers=thread_nums) as executor:
                    futures = {executor.submit(query_batch, batch): batch for batch in batches}
                    with tqdm(total=len(batches),
                              desc=f"数据集 {dataset_id} 批量查询进度",
                              leave=False) as pbar:
                        for future in as_completed(futures):
                            try:
                                batch_data = future.result()
                                data.extend(batch_data)
                                pbar.update(1)
                            except Exception as e:
                                logging.error(f"数据集 {dataset_id} 处理批次时出错: {e}")

                # 统计图片数量
                label_stats.totalDataCount = len(set(data))
                logging.info(f"数据集 {dataset_id} 统计完成! 总数据量: {label_stats.totalDataCount}")

                return dataset_id, label_stats

            except requests.exceptions.RequestException as e:
                error_msg = f"数据集 {dataset_id} 获取统计信息时发生HTTP错误: {str(e)}"
                logging.error(error_msg)
                return dataset_id, None
            except Exception as e:
                error_msg = f"数据集 {dataset_id} 处理时发生错误: {str(e)}"
                logging.error(error_msg)
                return dataset_id, None

        try:
            # 使用线程池处理多个数据集
            with ThreadPoolExecutor(max_workers=thread_nums) as executor:
                # 创建总进度条
                futures = {executor.submit(process_single_dataset, dataset_id): dataset_id
                           for dataset_id in dataset_ids}

                with tqdm(total=len(dataset_ids),
                          desc="总体处理进度",
                          position=0) as pbar:
                    for future in as_completed(futures):
                        dataset_id, stats = future.result()
                        if stats is not None:
                            results[dataset_id] = stats
                        pbar.update(1)

            # 输出统计摘要
            logging.info("\n=== 处理完成统计 ===")
            logging.info(f"成功处理数据集数量: {len(results)}")
            logging.info(f"失败数据集数量: {len(dataset_ids) - len(results)}")
            if len(dataset_ids) - len(results) > 0:
                failed_ids = set(dataset_ids) - set(results.keys())
                logging.info(f"处理失败的数据集ID: {failed_ids}")
            logging.info("=== 统计摘要结束 ===")
            # 打印结果
            for dataset_id, stats in results.items():
                logging.info(f"数据集 {dataset_id} 名称 {stats.datasetName} 总图片数量 {stats.totalDataCount} 总标签数 {stats.totalCount}")
                for label in stats.labelStats:
                    logging.info(f"标签 {label.label} 数量 {label.count} 占比 {label.percent}")
            return results

        except Exception as e:
            error_msg = f"批量处理数据集时发生错误: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

class EncryptionUtil:

    @staticmethod
    def encryption(src, key_word):
        # Generate key
        key_bytes = key_word.encode('utf-8')
        key = key_bytes[:16]  # AES-128 requires a 16-byte key

        # Generate IV
        iv = key_bytes[:16]  # IV should also be 16 bytes

        # Create cipher
        cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)

        # Encrypt
        encrypted_bytes = cipher.encrypt(src.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')


class AnkerAutoTrainModelSDK:
    def __init__(self, url: str = 'https://aidc-us.anker-in.com', username: str = None, password_base64: str = None, token_expiry_duration: int = 11*60*60):
        """初始化 AnkerAutoTrainModelSDK 类，设置基础 URL、会话和认证信息"""
        self.url = url.rstrip('/')  # 确保基URL没有尾部斜杠
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.username = username
        self.password_base64 = password_base64
        self.token = None
        self.token_expiry = 0  # Token 过期时间戳
        self.token_expiry_duration = token_expiry_duration  # Token 有效期（秒）
    
        # 初始化时获取 Token
        self.get_token()
    
    def get_token(self):
        """从 AIDC 接口获取认证 Token 并缓存"""
        # 检查缓存的 Token 是否有效
        current_time = time.time()
        if self.token and current_time < self.token_expiry:
            # Token 仍然有效
            print("使用缓存的Token。")
            return self.token
    
        # 如果没有 Token 或 Token 已过期，重新获取
        auth_url = f"{self.url}/api/auth/oauth2/token"
        print(f"请求获取 Token 的接口: {auth_url}")
    
        # 解码 Base64 编码的密码
        password = base64.b64decode(self.password_base64).decode('utf-8')
        key_word = "AIDC_SECRET_KEYS"
        # 加密密码
        encrypted_password = EncryptionUtil.encryption(password, key_word)
    
        params = {
            'username': self.username,
            'password': encrypted_password,
            'grant_type': 'password',
            'scope': 'server'
        }
        headers = {
            'Authorization': 'Basic YXBwOmFwcA==',
            'Cookie': 'Path=/'
        }
    
        print(f"获取 Token 的请求参数: {params}")
        print(f"获取 Token 的请求头: {headers}")
    
        try:
            response = requests.post(auth_url, headers=headers, params=params)
            response.raise_for_status()
            response_data = response.json()
            print(f"获取 Token 的响应: {json.dumps(response_data, indent=4)}")
    
            # 提取 access_token
            self.token = response_data.get('data', {}).get('access_token')
    
            if self.token:
                # 设置 Token 的过期时间
                self.token_expiry = current_time + self.token_expiry_duration
                # 在会话头中添加 Token
                self.session.headers.update({'Authorization': f"Bearer {self.token}"})
                print("Token 已成功获取并添加到请求头中。")
                return self.token
            else:
                print("响应中未找到 Access Token。")
                return None
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在获取 Token 时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在获取 Token 时: {req_err}")
            return None
        except Exception as e:
            print(f"获取 Token 时发生未知错误: {e}")
            return None


    def calculate_md5(self, file_path):
        """计算文件的 Base64 编码的 MD5 值"""
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        # 返回 Base64 编码的 MD5 值
        return base64.b64encode(md5_hash.digest()).decode('utf-8')

    def get_url(
        self, 
        model_name: str, 
        model_version_name: str, 
        path: str, 
        url_type: str, 
        interface: str = '/api/model/internal/getUploadUrl'
    ) -> Optional[str]:
        """获取上传或下载文件的 URL"""
        # 在请求前确保 Token 有效
        self.get_token()

        url_interface = f"{self.url}{interface}"
        print(f"请求 URL 的接口: {url_interface}")

        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name,
            "type": url_type,
            "path": path
        }
        print(f"获取 URL 的请求体: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url_interface, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"获取 URL 的响应: {json.dumps(response_data, indent=4)}")

            if response_data.get('ok'):
                url = response_data.get('data')
                if url:
                    return url
                else:
                    print("响应中未包含 URL。")
                    return None
            else:
                print(f"获取 URL 失败: {json.dumps(response_data, indent=4)}")
                return None
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在获取 URL 时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在获取 URL 时: {req_err}")
            return None
        except Exception as e:
            print(f"获取 URL 时发生未知错误: {e}")
            return None

    def _upload_file(self, upload_url: str, file_path: str) -> bool:
        """Upload a file to the specified URL, adding MD5 in the header

        :param upload_url: URL to upload to
        :param file_path: Local file path
        :return: True if upload is successful, else False
        """
        print(f"Starting to upload file to: {upload_url}")
        try:
            md5_value = self.calculate_md5(file_path)
            with open(file_path, 'rb') as file:
                headers = {
                    'Content-Type': 'application/octet-stream',
                    'Content-MD5': md5_value
                }
                response = requests.put(upload_url, data=file, headers=headers)
                response.raise_for_status()
                print(f"File successfully uploaded to {upload_url}")
                return True
        except FileNotFoundError:
            print(f"File not found at path: {file_path}")
            return False
        except requests.HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else 'Unknown'
            print(f"HTTP error occurred while uploading file: {http_err} - Status code: {status_code}")
            return False
        except requests.RequestException as req_err:
            print(f"Request exception occurred while uploading file: {req_err}")
            return False
        except Exception as e:
            print(f"An unknown error occurred while uploading file: {e}")
            return False

    def _upload_one_file(self, model_name: str, model_version_name: str, file_path: str) -> Optional[str]:
        """Upload a single file and return the upload URL

        :param model_name: Model name
        :param model_version_name: Model version name
        :param file_path: File path
        :return: Upload URL or None
        """
        upload_url = self.get_url(
            model_name=model_name, 
            model_version_name=model_version_name, 
            path=file_path, 
            url_type="upload"
        )
        if upload_url:
            success = self._upload_file(upload_url, file_path)
            if success:
                print(f"File uploaded successfully. Upload URL: {upload_url}")
                return upload_url
            else:
                print("File upload failed.")
                return None
        else:
            print("Failed to get upload URL, cannot upload file.")
            return None

    def upload_model_file(self, model_name: str, model_version_name: str, file_path: str) -> Dict[str, Any]:
        """
        Upload model file and return a dictionary containing the upload URL.

        :param model_name: Model name
        :param model_version_name: Model version name
        :param file_path: File path
        :return: Dictionary { "model_name:model_version_name": upload_data }
        """
        upload_data = self._upload_one_file(model_name, model_version_name, file_path)
        key = f"{model_name}:{model_version_name}"
        result = {key: upload_data}
        if upload_data:
            print(f"Upload result: {json.dumps(result, indent=4)}")
        else:
            print(f"Upload failed, model: {key}")
        return result

    def download_model_file(self, model_name: str, model_version_name: str, file_path: str, save_to: str) -> bool:
        """
        Get the download link for a model file and download the file locally

        :param model_name: Model name
        :param model_version_name: Model version name
        :param file_path: File path on server
        :param save_to: Local save path
        :return: Download result (success or failure)
        """
        url = f"{self.url}/api/model/internal/getUploadUrl"
        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name,
            "type": "download",
            "path": file_path
        }

        print(f"Interface to request download URL: {url}")
        print(f"Request body to get download URL: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"Response for getting download URL: {json.dumps(response_data, indent=4)}")

            if response_data.get("code") == 0 and response_data.get("ok"):
                download_url = response_data["data"]
                print(f"Download URL obtained: {download_url}")

                file_response = requests.get(download_url, stream=True)
                if file_response.status_code == 200:
                    with open(save_to, "wb") as file:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                    print(f"File successfully downloaded and saved to {save_to}")
                    return True
                else:
                    print(f"Failed to download file from URL: {download_url} - Status code: {file_response.status_code}")
                    return False
            else:
                print(f"Error: {json.dumps(response_data.get('msg', 'Unknown error'), indent=4)}")
                return False

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while downloading model file: {http_err}")
            return False
        except requests.RequestException as req_err:
            print(f"Request exception occurred while downloading model file: {req_err}")
            return False
        except Exception as e:
            print(f"An unknown error occurred while downloading model file: {e}")
            return False

    def download_file(self, url: str, local_path: str) -> bool:
        """
        Download a file from a specified URL and save it to a local path

        :param url: URL address of the file
        :param local_path: Local path to save the file
        :return: Whether the download was successful
        """
        print(f"Starting to download file from URL: {url}")
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                print(f"File successfully downloaded to {local_path}")
                return True
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"Request error occurred while downloading file: {e}")
            return False
        except Exception as e:
            print(f"An unknown error occurred while downloading file: {e}")
            return False

    def get_model_version_files(self, model_name: str, model_version_name: str) -> Optional[list]:
        """
        Get all file information under a model version

        :param model_name: Model name
        :param model_version_name: Model version name
        :return: List of file information or error message
        """
        url = f"{self.url}/api/model/internal/getDirectory"
        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name
        }

        print(f"Interface to request model version file info: {url}")
        print(f"Request body to get model version file info: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"Response for getting model version file info: {json.dumps(response_data, indent=4)}")

            if response_data.get("code") == 0 and response_data.get("ok"):
                files = response_data["data"]["records"]
                print(f"Total files found: {len(files)}")
                for file in files:
                    print(f"Name: {file['name']}, Size: {file['size']}, Last Modified: {file['lastModified']}")
                return files
            else:
                print(f"Error: {json.dumps(response_data.get('msg', 'Unknown error'), indent=4)}")
                return None

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while getting model version file info: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"Request exception occurred while getting model version file info: {req_err}")
            return None
        except Exception as e:
            print(f"An unknown error occurred while getting model version file info: {e}")
            return None

    def add_model_to_db(
        self, 
        bg: str, 
        owner: str, 
        model_name: str, 
        model_version_name: str, 
        tar_md5: str, 
        onnx_md5: str, 
        rknn_md5: str, 
        model_arc: str, 
        region: str,
        model_id: str = None,
        test_result: Optional[list] = None, 
        test_set_ids: Optional[list] = None, 
        train_set_ids: Optional[list] = None, 
        quant_set_ids: Optional[list] = None, 
        params: Optional[Any] = None, 
        show: Optional[Any] = None, 
        task_type: str = 'detection', 
        desc: Optional[Any] = None, 
        code_id: Optional[Any] = None, 
        docker_image_id: Optional[Any] = None, 
        frame_type: str = 'pytorch', 
        model_format: str = 'onnx', 
        model_type: str = '目标检测'
    ) -> Optional[Dict[str, Any]]:
        """Add model information to the database

        :param bg: Background info
        :param owner: Owner
        :param model_name: Model name
        :param model_version_name: Model version name
        :param tar_md5: MD5 of tar file
        :param onnx_md5: MD5 of onnx file
        :param rknn_md5: MD5 of rknn file
        :param model_arc: Model architecture
        :param region: Region
        :param test_result: Test results
        :param test_set_ids: List of test set IDs
        :param train_set_ids: List of train set IDs
        :param quant_set_ids: List of quantization set IDs
        :param params: Parameters
        :param show: Show info
        :param task_type: Task type
        :param desc: Description
        :param code_id: Code ID
        :param docker_image_id: Docker image ID
        :param frame_type: Framework type
        :param model_format: Model format
        :param model_type: Model type
        :return: JSON response from upload, or None if not uploaded
        """
        url = f"{self.url}/api/model/internal/version"

        payload = {
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name,
            "region": region,
            "taskType": task_type,
            "modelArc": model_arc,
            "params": params,
            "testResult": test_result,
            "show": show,
            "trainSetIds": train_set_ids,
            "testSetIds": test_set_ids,
            "quantSetIds": quant_set_ids,
            "codeId": code_id,
            "dockerImageId": docker_image_id,
            "modelFile": {
                "tar": tar_md5,
                "onnx": onnx_md5,
                "rknn": rknn_md5
            },
            "modelDescription": desc,
            "modelType": model_type,
            "frameType": frame_type,
            "modelFormat": model_format
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        print(f"Request body to add model to database: {json.dumps(payload, indent=4)}")
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"Response for adding model to database: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while adding model to database: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"Request exception occurred while adding model to database: {req_err}")
            return None
        except Exception as e:
            print(f"An unknown error occurred while adding model to database: {e}")
            return None

    def get_model_list(
        self, 
        model_name: Optional[str] = None, 
        model_version_name: Optional[str] = None, 
        bg: Optional[str] = None, 
        owner: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get model list

        :param model_name: Model name
        :param model_version_name: Model version name
        :param bg: Background info
        :param owner: Owner
        :return: JSON data of model list or error message
        """
        url = f"{self.url}/api/model/internal/version/list"
        payload = { 
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        print(f"Interface to request model list: {url}")
        print(f"Request body to get model list: {json.dumps(payload, indent=4)}")
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"Response for getting model list: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while getting model list: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"Request exception occurred while getting model list: {req_err}")
            return None
        except Exception as e:
            print(f"An unknown error occurred while getting model list: {e}")
            return None

    def get_model_id(self, model_name: str, model_version_name: str) -> Optional[str]:
        """Get the ID of a model version

        :param model_name: Model name
        :param model_version_name: Model version name
        :return: Model version ID or None
        """
        model_list = self.get_model_list(model_name, model_version_name)
        if model_list and model_list.get('code') == 0 and model_list.get('data'):
            return model_list.get('data')[0].get('modelVersionId')
        else:
            print(f"Model ID not found: {model_name} - {model_version_name}")
            return None

    def add_board_result_to_db(
        self, 
        model_name: str, 
        model_version_name: str, 
        board_result: list, 
        chip: str, 
        test_set_ids: list, 
        input_h: int, 
        input_w: int, 
        infer_time: float, 
        memory: int, 
        flash: int, 
        project: str, 
        projectId: str, 
        modelPath: str, 
        boardTestVersion: str, 
        testResultPath: str, 
        bad_case_ids: list,
        model_id: str = None,
        quant_algo: str = "normal", 
        quant_method: str = "channel"
    ) -> Optional[Dict[str, Any]]:
        """
        Upload board test results to the database

        :param model_name: Model name
        :param model_version_name: Model version name
        :param board_result: Board test results
        :param chip: Chip info
        :param model_id: Model ID, default None
        :param project: Project name
        :param quant_algo: Quantization algorithm, default "normal"
        :param quant_method: Quantization method, default "channel"
        :param test_set_ids: List of test set IDs
        :param input_h: Input height
        :param input_w: Input width
        :param infer_time: Inference time
        :param memory: Memory usage
        :param flash: Flash size
        :param projectId: Project ID
        :param modelPath: Model path
        :param boardTestVersion: Board test version
        :param testResultPath: Test result path
        :param bad_case_ids: List of bad case IDs
        :return: JSON response from upload, or None if not uploaded
        """
        if model_id is None:
            model_id = self.get_model_id(model_name, model_version_name)
            if model_id is None:
                print(f"Model ID not found: {model_name} - {model_version_name}. Skipping board result upload.")
                return None

        url = f"{self.url}/api/model/internal/versionTest"
        
        payload = {
            "modelVersionId": model_id,
            "projectId": projectId,
            "projectName": project,
            "chipName": chip,
            "modelPath": modelPath,
            "boardTestVersion": boardTestVersion,
            "quantAlgo": quant_algo,
            "quantMethod": quant_method,
            "testResultBoard": board_result,
            "testResultPath": testResultPath,
            "testSetIds": test_set_ids,
            "badCaseIds": bad_case_ids,
            "inputH": input_h,
            "inputW": input_w,
            "inferTime": infer_time,
            "memory": memory,
            "flash": flash
        }

        payload = {k: v for k, v in payload.items() if v is not None}
        
        print(f"Request body to upload board test results: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()
            print(f"Response for uploading board test results: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while uploading board test results: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"Request exception occurred while uploading board test results: {req_err}")
            return None
        except Exception as e:
            print(f"An unknown error occurred while uploading board test results: {e}")
            return None


class ai_tools:
    def __init__(self):
        """
        初始化 BadCaseDetector 类。
        所有必要的参数通过设置方法进行配置。
        """
        self.class_names = {}
        self.thresholds = {}
        self.badcase_positive_file_path = ""
        self.badcase_false_positive_file_path = ""
        self.val_file_path = ""
        self.positive_dataset_paths = []
        self.negative_dataset_paths = []
        
    def _compute_iou(self, rec1, rec2):
        """
        计算两个矩形框的 IoU
        :param rec1: (x1, y1, x2, y2)
        :param rec2: (x1, y1, x2, y2)
        :return: IoU 值
        """
        # 计算每个矩形的面积
        S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

        # 计算交集
        left_line = max(rec1[0], rec2[0])
        right_line = min(rec1[2], rec2[2])
        top_line = max(rec1[1], rec2[1])
        bottom_line = min(rec1[3], rec2[3])

        if left_line >= right_line or top_line >= bottom_line:
            return 0
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            union = S_rec1 + S_rec2 - intersect
            return intersect / union

    def is_badcase(self, predicted_labels, groundtruth_labels, class_names, thresholds, iou_threshold=0.5, is_positive=True):
        """
        判断一个标签文件是否为坏案例。

        参数：
        - predicted_labels: 模型预测的标签列表，每个标签格式为 [cls, conf, x1, y1, x2, y2]
        - groundtruth_labels: 真实标签列表，每个标签格式为 [cls, x1, y1, x2, y2]
        - class_names: 类别名称字典，键为类别索引，值为类别名称
        - thresholds: 阈值字典，键为类别名称，值为对应的阈值
        - iou_threshold: IoU 阈值，默认值为 0.5
        - is_positive: 布尔变量，判断是否为正检测（True）还是误检测（False）
        
        返回：
        - bool: 如果是坏案例返回 True，否则返回 False
        """
        if is_positive:
            # 正检测需要比较预测与真实标签
            matched = False
            for gt in groundtruth_labels:
                gt_cls = gt[0]
                gt_class_name = class_names.get(gt_cls, "")
                gt_conf_thres = thresholds.get(gt_class_name, 0)
                gt_box = gt[2:]  # [x1, y1, x2, y2]

                for pred in predicted_labels:
                    pred_cls, pred_conf, pred_box = pred[0], pred[1], pred[2:]
                    if pred_cls != gt_cls or pred_conf < gt_conf_thres:
                        continue
                    iou = self._compute_iou(gt_box, pred_box)
                    if iou > iou_threshold:
                        matched = True
                        break
            return not matched  # 如果没有匹配到，则为坏案例
        else:
            # 误检测只需要检查是否有假阳性
            for pred in predicted_labels:
                pred_cls, pred_conf, _ = pred
                class_name = class_names.get(pred_cls, "")
                conf_thres = thresholds.get(class_name, 0)
                if pred_conf > conf_thres:
                    return True  # 存在假阳性
            return False
