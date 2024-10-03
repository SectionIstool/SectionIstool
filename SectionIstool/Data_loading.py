<<<<<<< HEAD
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
            
            # 将字符串转化为 UTC datetime 对象
            utc_datetime = datetime.fromisoformat(utc_datetime_str)  # 直接使用包含时区信息的字符串
            
            # 将 UTC 时间转换为 UTC+8 时区
            utc_8_timezone = pytz.timezone('Asia/Shanghai')
            utc_8_datetime = utc_datetime.astimezone(utc_8_timezone)

            # 格式化为所需的字符串格式
            formatted_time = utc_8_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            return formatted_time  # 返回格式化后的时间字符串



async def get_specific_asset_size(owner, repo, release_tag, asset_name, token=None):
    # 获取Release信息的URL
    release_url = f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}'
    
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        async with session.get(release_url, headers=headers) as response:
            release_data = await response.json()
            
            # 检查资产（assets）是否存在
            if 'assets' in release_data:
                for asset in release_data['assets']:
                    if asset['name'] == asset_name:
                        return asset['size']  # 如果找到，返回大小并退出函数
            
            return None  # 如果没有找到，返回None

async def get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None):
    api_url = f'https://api.github.com/repos/{repo}/releases'
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=headers) as response:
                response.raise_for_status()  # 检查请求是否成功
                
                releases = await response.json()
                filtered_download_links = []
                existing_versions = set()  # 存储已存在的版本号

                for release in releases:
                    latest_tag = release.get('tag_name')

                    # 版本过滤逻辑
                    if (min_version and latest_tag < min_version) or (max_version and latest_tag > max_version):
                        continue
                    
                    if latest_tag in existing_versions:
                        continue
                    
                    existing_versions.add(latest_tag)
                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')  # 发布时间

                    # 构造下载链接
                    if software_name:
                        # 有指定软件名，构造具体链接
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/{software_name}.{file_extension}'
                    else:
                        # 如果没有指定软件名，默认构造使用release里面的资产
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/'

                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, f'{software_name}.{file_extension}' if software_name else '', token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"

                    # 根据当前数量生成id (倒序)
                    download_link = {
                        "id": str(limit - len(filtered_download_links)) if limit else str(len(filtered_download_links)),  # 倒序生成id
                        "name": software_true_name,
                        "author": author, 
                        "version": latest_tag,
                        "size": file_size,
                        "format": file_extension,
                        "source": source,
                        "note": "",
                        "first_release": publish_date.split('T')[0],
                        "url": download_url,
                    }

                    filtered_download_links.append(download_link)

                    if limit and len(filtered_download_links) >= limit:
                        break
                
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
                
                if filtered_download_links:
                    data_to_write = {
                        "download_links": filtered_download_links,
                        "fetch_time": utc_time
                    }
                    os.makedirs('Config/All_online', exist_ok=True)
                    with open(f'Config/All_online/{software_true_name}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_download_links

        except aiohttp.ClientResponseError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")
        except ValueError:
            raise ValueError("JSON数据解析失败")


# 更新 get_software_async 函数，添加与上面类似的逻辑
async def get_software_async(repo, software_name, software_true_name, file_extension, source, author, token=None, limit=None):
    releases_url = f'https://api.github.com/repos/{repo}/releases'
    repo_url = f'https://api.github.com/repos/{repo}'  # 获取仓库信息的URL

    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            # 发送GET请求以获取仓库信息
            async with session.get(repo_url, headers=headers) as response:
                response.raise_for_status()
                repo_info = await response.json()

                owner_avatar_url = repo_info.get('owner', {}).get('avatar_url', '') + '&s=64'  # 添加大小查询参数
                repository_description = repo_info.get('description', '')
                stars_count = repo_info.get('stargazers_count', 0)  # 获取Stars数量

            # 发送GET请求以获取发布版本
            async with session.get(releases_url, headers=headers) as response:
                response.raise_for_status()  # 检查请求是否成功，抛出异常
                
                # 解析返回的JSON数据，获取版本
                releases = await response.json()
                
                if not releases:
                    return []  # 如果没有发布版本，返回空列表
                
                filtered_software_info = []
                
                for release in releases:
                    latest_tag = release.get('tag_name')

                    if software_name:
                        # 有指定软件名，构造具体链接
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/{software_name}.{file_extension}'
                    else:
                        # 如果没有指定软件名，下载链接使用release文件
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/'

                    # 其他信息 与之前保持一致
                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')  # 发布时间
                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, f'{software_name}.{file_extension}' if software_name else '', token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"

                    software_info = {
                        "name": software_true_name,
                        "author": author, 
                        "version": latest_tag,
                        "size": file_size,
                        "format": file_extension,
                        "source": source,
                        "note": "",
                        "first_release": publish_date.split('T')[0],
                        "url": download_url,
                        "avatar_url": owner_avatar_url,
                        "description": repository_description,
                        "stars_count": stars_count
                    }

                    filtered_software_info.append(software_info)

                    if limit and len(filtered_software_info) >= limit:
                        break

                # 获取当前时间（与之前一样）
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
                
                # 写入JSON文件
                os.makedirs('Config/All_online', exist_ok=True)
                with open(f'Config/All_online/{software_true_name}_info.json', 'w', encoding='utf-8') as json_file:
                    data_to_write = {
                        "software_info": filtered_software_info,
                        "fetch_time": utc_time  # 写入从网上获取的时间
                    }
                    json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_software_info  # 返回包含该链接的列表

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")  # 处理请求失败
        except ValueError:
            raise ValueError("JSON数据解析失败")  # 处理JSON解析错误




# 读取JSON文件
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"读取JSON文件失败: {e}")


# 检查并获取数据
async def check_and_get_data(file_path, info_type, repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit):
    data = read_json_file(file_path)
    written_time_str = data.get("fetch_time")

    # 检查写入时间
    if written_time_str:
        # 将时间字符串转换为 datetime 对象
        written_time = datetime.strptime(written_time_str, '%Y-%m-%d %H:%M:%S')
        # 获取当前时间（与之前一样）
        try:
            current_time = await fetch_current_time()
        except Exception:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
        
        # 确保 current_time 为 datetime 对象
        if isinstance(current_time, str):
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

    if not written_time or written_time is None or current_time - written_time > timedelta(hours=2):
        if info_type == "software_info":
            software_async = await get_software_async(repo, software_name, software_true_name, file_extension, source, author, token, limit)  # 超过一小时或没有更新时间，返回新的软件信息
            return software_async

        elif info_type == "download_links":
            all_versions_async = await get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)  # 超过一小时或没有更新时间，返回新的下载链接
            return all_versions_async

        else:
            return []  # 处理未知的info_type


    return data.get(info_type)  # 返回已有数据或空列表


# 用户登录检测获取数据
async def filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None, info_type=None, file_path=None):
    if os.path.exists(file_path):
        try:
            return await check_and_get_data(file_path, info_type, repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

        except Exception as e:
            raise RuntimeError(f"获取数据失败: {e}")

    # 如果文件不存在，直接获取
    if info_type == "software_info":
        return await get_software_async(repo, software_name, software_true_name, file_extension, source, author, token, limit) # 超过一小时，返回新的数据

    elif info_type == "download_links":
        return await get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit) # 超过一小时，返回新的数据

    else:
        return []  # 未知的info_type


# 主函数
def get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}.json"
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit, "download_links", file_path))

def get_software_info(repo, software_name, software_true_name, file_extension, source, author, token=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}_info.json"
    min_version = None
    max_version = None
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit, "software_info", file_path))
=======
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
            
            # 将字符串转化为 UTC datetime 对象
            utc_datetime = datetime.fromisoformat(utc_datetime_str)  # 直接使用包含时区信息的字符串
            
            # 将 UTC 时间转换为 UTC+8 时区
            utc_8_timezone = pytz.timezone('Asia/Shanghai')
            utc_8_datetime = utc_datetime.astimezone(utc_8_timezone)

            # 格式化为所需的字符串格式
            formatted_time = utc_8_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            return formatted_time  # 返回格式化后的时间字符串



async def get_specific_asset_size(owner, repo, release_tag, asset_name, token=None):
    # 获取Release信息的URL
    release_url = f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}'
    
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        async with session.get(release_url, headers=headers) as response:
            release_data = await response.json()
            
            # 检查资产（assets）是否存在
            if 'assets' in release_data:
                for asset in release_data['assets']:
                    if asset['name'] == asset_name:
                        return asset['size']  # 如果找到，返回大小并退出函数
            
            return None  # 如果没有找到，返回None

async def get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None):
    api_url = f'https://api.github.com/repos/{repo}/releases'
    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=headers) as response:
                response.raise_for_status()  # 检查请求是否成功
                
                releases = await response.json()
                filtered_download_links = []
                existing_versions = set()  # 存储已存在的版本号

                for release in releases:
                    latest_tag = release.get('tag_name')

                    # 版本过滤逻辑
                    if (min_version and latest_tag < min_version) or (max_version and latest_tag > max_version):
                        continue
                    
                    if latest_tag in existing_versions:
                        continue
                    
                    existing_versions.add(latest_tag)
                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')  # 发布时间

                    # 构造下载链接
                    if software_name:
                        # 有指定软件名，构造具体链接
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/{software_name}.{file_extension}'
                    else:
                        # 如果没有指定软件名，默认构造使用release里面的资产
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/'

                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, f'{software_name}.{file_extension}' if software_name else '', token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"

                    # 根据当前数量生成id (倒序)
                    download_link = {
                        "id": str(limit - len(filtered_download_links)) if limit else str(len(filtered_download_links)),  # 倒序生成id
                        "name": software_true_name,
                        "author": author, 
                        "version": latest_tag,
                        "size": file_size,
                        "format": file_extension,
                        "source": source,
                        "note": "",
                        "first_release": publish_date.split('T')[0],
                        "url": download_url,
                    }

                    filtered_download_links.append(download_link)

                    if limit and len(filtered_download_links) >= limit:
                        break
                
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
                
                if filtered_download_links:
                    data_to_write = {
                        "download_links": filtered_download_links,
                        "fetch_time": utc_time
                    }
                    os.makedirs('Config/All_online', exist_ok=True)
                    with open(f'Config/All_online/{software_true_name}.json', 'w', encoding='utf-8') as json_file:
                        json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_download_links

        except aiohttp.ClientResponseError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")
        except ValueError:
            raise ValueError("JSON数据解析失败")


# 更新 get_software_async 函数，添加与上面类似的逻辑
async def get_software_async(repo, software_name, software_true_name, file_extension, source, author, token=None, limit=None):
    releases_url = f'https://api.github.com/repos/{repo}/releases'
    repo_url = f'https://api.github.com/repos/{repo}'  # 获取仓库信息的URL

    headers = {"Authorization": f"token {token}"} if token else {}

    async with aiohttp.ClientSession() as session:
        try:
            # 发送GET请求以获取仓库信息
            async with session.get(repo_url, headers=headers) as response:
                response.raise_for_status()
                repo_info = await response.json()

                owner_avatar_url = repo_info.get('owner', {}).get('avatar_url', '') + '&s=64'  # 添加大小查询参数
                repository_description = repo_info.get('description', '')
                stars_count = repo_info.get('stargazers_count', 0)  # 获取Stars数量

            # 发送GET请求以获取发布版本
            async with session.get(releases_url, headers=headers) as response:
                response.raise_for_status()  # 检查请求是否成功，抛出异常
                
                # 解析返回的JSON数据，获取版本
                releases = await response.json()
                
                if not releases:
                    return []  # 如果没有发布版本，返回空列表
                
                filtered_software_info = []
                
                for release in releases:
                    latest_tag = release.get('tag_name')

                    if software_name:
                        # 有指定软件名，构造具体链接
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/{software_name}.{file_extension}'
                    else:
                        # 如果没有指定软件名，下载链接使用release文件
                        download_url = f'https://mirror.ghproxy.com/https://github.com/{repo}/releases/download/{latest_tag}/'

                    # 其他信息 与之前保持一致
                    publish_date = release.get('published_at', '1970-01-01T00:00:00Z')  # 发布时间
                    file_size_bytes = await get_specific_asset_size(repo.split('/')[0], repo.split('/')[1], latest_tag, f'{software_name}.{file_extension}' if software_name else '', token)
                    file_size = convert_size(file_size_bytes) if file_size_bytes is not None else "未知大小"

                    software_info = {
                        "name": software_true_name,
                        "author": author, 
                        "version": latest_tag,
                        "size": file_size,
                        "format": file_extension,
                        "source": source,
                        "note": "",
                        "first_release": publish_date.split('T')[0],
                        "url": download_url,
                        "avatar_url": owner_avatar_url,
                        "description": repository_description,
                        "stars_count": stars_count
                    }

                    filtered_software_info.append(software_info)

                    if limit and len(filtered_software_info) >= limit:
                        break

                # 获取当前时间（与之前一样）
                try:
                    utc_time = await fetch_current_time()
                except Exception:
                    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
                
                # 写入JSON文件
                os.makedirs('Config/All_online', exist_ok=True)
                with open(f'Config/All_online/{software_true_name}_info.json', 'w', encoding='utf-8') as json_file:
                    data_to_write = {
                        "software_info": filtered_software_info,
                        "fetch_time": utc_time  # 写入从网上获取的时间
                    }
                    json.dump(data_to_write, json_file, indent=4, ensure_ascii=False)

                return filtered_software_info  # 返回包含该链接的列表

        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"发生错误:{e}")  # 处理请求失败
        except ValueError:
            raise ValueError("JSON数据解析失败")  # 处理JSON解析错误




# 读取JSON文件
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"读取JSON文件失败: {e}")


# 检查并获取数据
async def check_and_get_data(file_path, info_type, repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit):
    data = read_json_file(file_path)
    written_time_str = data.get("fetch_time")

    # 检查写入时间
    if written_time_str:
        # 将时间字符串转换为 datetime 对象
        written_time = datetime.strptime(written_time_str, '%Y-%m-%d %H:%M:%S')
        # 获取当前时间（与之前一样）
        try:
            current_time = await fetch_current_time()
        except Exception:
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # 使用本地UTC时间
        
        # 确保 current_time 为 datetime 对象
        if isinstance(current_time, str):
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')

    if not written_time or written_time is None or current_time - written_time > timedelta(hours=2):
        if info_type == "software_info":
            software_async = await get_software_async(repo, software_name, software_true_name, file_extension, source, author, token, limit)  # 超过一小时或没有更新时间，返回新的软件信息
            return software_async

        elif info_type == "download_links":
            all_versions_async = await get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)  # 超过一小时或没有更新时间，返回新的下载链接
            return all_versions_async

        else:
            return []  # 处理未知的info_type


    return data.get(info_type)  # 返回已有数据或空列表


# 用户登录检测获取数据
async def filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None, info_type=None, file_path=None):
    if os.path.exists(file_path):
        try:
            return await check_and_get_data(file_path, info_type, repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

        except Exception as e:
            raise RuntimeError(f"获取数据失败: {e}")

    # 如果文件不存在，直接获取
    if info_type == "software_info":
        return await get_software_async(repo, software_name, software_true_name, file_extension, source, author, token, limit) # 超过一小时，返回新的数据

    elif info_type == "download_links":
        return await get_all_versions_async(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit) # 超过一小时，返回新的数据

    else:
        return []  # 未知的info_type


# 主函数
def get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token=None, min_version=None, max_version=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}.json"
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit, "download_links", file_path))

def get_software_info(repo, software_name, software_true_name, file_extension, source, author, token=None, limit=None):
    file_path = f"Config/All_online/{software_true_name}_info.json"
    min_version = None
    max_version = None
    return asyncio.run(filtered_get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit, "software_info", file_path))
>>>>>>> 4fa2a7888d33a4299e04b4d0deacd959883e7656
