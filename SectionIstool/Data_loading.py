import aiohttp
import asyncio
import math
import json
import os
import pytz
from datetime import datetime, timedelta

# 辅助函数：将字节转换为带有单位的大小
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

async def fetch_current_time(token=None):
    """从网络获取当前时间并转换为UTC+8时区"""
    api_url = "http://worldtimeapi.org/api/timezone/Asia/Shanghai"  
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers) as response:
            response.raise_for_status()  # 检查请求是否成功
            data = await response.json()
            
            # 获取原始 UTC 时间字符串
            utc_datetime_str = data['utc_datetime']
            utc_datetime = datetime.fromisoformat(utc_datetime_str)
            utc_8_timezone = pytz.timezone('Asia/Shanghai')
            utc_8_datetime = utc_datetime.astimezone(utc_8_timezone)
            formatted_time = utc_8_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            return formatted_time

async def get_specific_asset_size(owner, repo, release_tag, token=None):
    release_url = f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}'
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        async with session.get(release_url, headers=headers) as response:
            release_data = await response.json()
            
            if 'assets' in release_data:
                for asset in release_data['assets']:
                    return asset['size']
            
            return None

async def get_specific_asset_url(owner, repo, release_tag, token=None):
    release_url = f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}'
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        async with session.get(release_url, headers=headers) as response:
            release_data = await response.json()
            
            if 'assets' in release_data:
                for asset in release_data['assets']:
                    return asset['browser_download_url']
            
            return None

async def get_all_versions_async(repo, software_name, software_true_name, file_extension, author, source_first=None, source_second=None, token=None, min_version=None, max_version=None, limit=None):
    api_url = f'https://api.github.com/repos/{repo}/releases'
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=headers) as response:
                response.raise_for_status()
                releases = await response.json()
                filtered_download_links = []
                existing_versions = set()

                for release in releases:
                    latest_tag = release.get('tag_name')

                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"
                    download_url_temp = await get_specific_asset_url(repo.split('/')[0], repo.split('/')[1], latest_tag, token) 

                    # 确保 update_body 在使用之前被定义
                    update_body = ''
                    if (min_version and latest_tag < min_version) or (max_version and latest_tag > max_version):
                        continue
                    
                    if latest_tag in existing_versions:
                        continue
                    
                    existing_versions.add(latest_tag)
                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')

                    # 确定软件名称
                    if software_true_name:
                        software_display_name = software_true_name
                    elif software_name:
                        software_display_name = software_name
                    else:
                        print("警告: 软件名称和真实名称都为空")
                        continue

                    if source_first == '1':
                        download_url_first = download_url_temp if download_url_temp else None

                        link_first = {
                            "id": str(limit - len(filtered_download_links)) if limit else str(len(filtered_download_links) + 1),  # 倒序生成id
                            "name": software_display_name,
                            "author": author,
                            "version": latest_tag,
                            "size": file_size,
                            "format": file_extension,
                            "source": "github",
                            "note": update_body,
                            "first_release": publish_date.split('T')[0],
                            "url": download_url_first,
                        }
                        filtered_download_links.append(link_first)

                    if source_second == '2':
                        download_url_second = ('https://ghp.ci/' + download_url_temp) if download_url_temp else None
                        
                        link_second = {
                            "id": str(limit - len(filtered_download_links)) if limit else str(len(filtered_download_links) + 1),  # 倒序生成id
                            "name": software_display_name,
                            "author": author,
                            "version": latest_tag,
                            "size": file_size,
                            "format": file_extension,
                            "source": "github(镜像源)",
                            "note": update_body,
                            "first_release": publish_date.split('T')[0],
                            "url": download_url_second,
}
                        # 确保不重复添加
                        if link_second not in filtered_download_links:
                            filtered_download_links.append(link_second)

                    if limit and len(filtered_download_links) >= limit:
                        break

                # 更新获取的 UTC 时间
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                if filtered_download_links:
                    os.makedirs('Config/All_online', exist_ok=True)
                    data_to_write = {
                        "download_links": filtered_download_links,
                        "fetch_time": utc_time
                    }
                    with open(f'Config/All_online/{software_display_name}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_download_links

        except aiohttp.ClientResponseError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")
        except ValueError:
            raise ValueError("JSON数据解析失败")



async def get_software_async(repo, software_name, software_true_name, file_extension, author, source_first=None, source_second=None, token=None, limit=None):
    releases_url = f'https://api.github.com/repos/{repo}/releases'
    repo_url = f'https://api.github.com/repos/{repo}'
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(repo_url, headers=headers) as response:
                response.raise_for_status()
                repo_info = await response.json()

                owner_avatar_url = repo_info.get('owner', {}).get('avatar_url', '') + '&s=64'
                repository_description = repo_info.get('description', '')
                stars_count = repo_info.get('stargazers_count', 0)

            async with session.get(releases_url, headers=headers) as response:
                response.raise_for_status()
                releases = await response.json()

                if not releases:
                    return []

                filtered_software_info = []
                
                for release in releases:
                    latest_tag = release.get('tag_name')

                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"
                    download_url_temp = await get_specific_asset_url(repo.split('/')[0], repo.split('/')[1], latest_tag, token) 

                    # 确定软件名称
                    if software_true_name:
                        software_display_name = software_true_name
                    elif software_name:
                        software_display_name = software_name
                    else:
                        print("警告: 软件名称和真实名称都为空")
                        continue  # 跳过这次迭代

                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')
                    update_body = release.get('body', '')  # 获取更新内容

                    # 处理下载链接
                    if source_first == '1':
                        download_url_first = download_url_temp if download_url_temp else None
                        software_info_first = {
                            "name": software_display_name,
                            "author": author, 
                            "version": latest_tag,
                            "size": file_size,
                            "format": file_extension,
                            "source": "github",
                            "note": update_body,
                            "first_release": publish_date.split('T')[0],
                            "url": download_url_first,
                            "avatar_url": owner_avatar_url,
                            "description": repository_description,
                            "stars_count": stars_count
                        }
                        filtered_software_info.append(software_info_first)

                    if source_second == '2':
                        download_url_second = ('https://ghp.ci/' + download_url_temp) if download_url_temp else None
                        software_info_second = {
                            "name": software_display_name,
                            "author": author, 
                            "version": latest_tag,
                            "size": file_size,
                            "format": file_extension,
                            "source": "github(镜像源)",
                            "note": update_body,
                            "first_release": publish_date.split('T')[0],
                            "url": download_url_second,
                            "avatar_url": owner_avatar_url,
                            "description": repository_description,
                            "stars_count": stars_count
                        }

                        # 确保不重复添加
                        if software_info_second not in filtered_software_info:
                            filtered_software_info.append(software_info_second)

                    if limit and len(filtered_software_info) >= limit:
                        break

                # 更新获取的 UTC 时间
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                # 写入JSON文件
                if filtered_software_info:
                    os.makedirs('Config/All_online', exist_ok=True)
                    data_to_write = {
                        "software_info": filtered_software_info,
                        "fetch_time": utc_time
                    }
                    with open(f'Config/All_online/{software_display_name}_info.json', 'w', encoding='utf-8') as json_file:
                        json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_software_info

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")
        except ValueError:
            raise ValueError("JSON数据解析失败")



def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"读取JSON文件失败: {e}")

async def check_and_get_data(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit, info_type, file_path):
    data = read_json_file(file_path)
    written_time_str = data.get("fetch_time")

    if written_time_str:
        written_time = datetime.strptime(written_time_str, '%Y-%m-%d %H:%M:%S')
        try:
            current_time = await fetch_current_time()
        except Exception:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        if isinstance(current_time, str):
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

    if not written_time or written_time is None or current_time - written_time > timedelta(hours=2):
        if info_type == "software_info":
            software_async = await get_software_async(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, limit)
            return software_async

        elif info_type == "download_links":
            all_versions_async = await get_all_versions_async(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit)
            return all_versions_async

        else:
            return []

    return data.get(info_type)

async def filtered_get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token=None, min_version=None, max_version=None, limit=None, info_type=None, file_path=None):
    if os.path.exists(file_path):
        try:
            return await check_and_get_data(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit, info_type, file_path)
        except Exception as e:
            raise RuntimeError(f"获取数据失败: {e}")

    if info_type == "software_info":
        return await get_software_async(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, limit)

    elif info_type == "download_links":
        return await get_all_versions_async(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit) 

    else:
        return []

def get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first=None, source_second=None, token=None, min_version=None, max_version=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}.json"
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit, "download_links", file_path))

def get_software_info(repo, software_name, software_true_name, file_extension, author, source_first=None, source_second=None, token=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}_info.json"
    min_version = None
    max_version = None
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit, "software_info", file_path))

def get_update_info(repo, software_name, software_true_name, file_extension, author, source_first=None, source_second=None, token=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}_info.json"
    min_version = None
    max_version = None
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, token, min_version, max_version, limit, "software_info", file_path))

