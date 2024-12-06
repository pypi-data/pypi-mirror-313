#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""github api操作
@author: deng
@file: github
@time: 2023/12/7 15:34 
"""
import os
import re
import json
import logging
import requests
from .git import parser_git_url
from .my_http import format_output


logger = logging.getLogger("DengUtils")

DOMAIN = os.environ["GITHUB_CI_API_URL"].strip(" /")
ACCESS_TOKEN = os.environ["GITHUB_CI_TOKEN"]

auth_header = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}

session = requests.Session()
session.headers.update(auth_header)


def checkout_response(response: requests.Response, level="debug"):
    """检查请求响应"""
    if response.status_code == 403 or response.status_code == 401:
        format_output(response, "error", depth=3)
        raise ValueError("权限认证失败，请检查！")

    if response.status_code >= 400:
        format_output(response, "error", depth=3)
    else:
        if level:
            format_output(response, level=level, depth=3)
        if response.status_code == 204:
            return ""
        else:
            return response.json()


def release_exists(
    *, owner: str, repo: str, name: str, tag_name: str, target: str
) -> dict:
    """判断release是否已经存在"""
    _release_list = get_releases(owner=owner, repo=repo)
    for _release in _release_list:
        if (
            _release["name"] == name
            and _release["tag_name"] == tag_name
            and _release["target_commitish"] == target
        ):
            logger.info(f"release已经存在：{owner}/{repo}:{name}")
            return _release
    logger.info(f"release不存在：{owner}/{repo}:{name}")
    return {}


def get_releases(*, owner: str, repo: str, page=1, per_page=100):
    """获取release列表"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/releases"
    params = {"page": page, "per_page": per_page}
    _res = session.get(_url, params=params)
    return checkout_response(_res)


def get_release_by_id(*, owner: str, repo: str, release_id: int):
    """获取release详情"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/releases/{release_id}"
    _res = session.get(_url)
    return checkout_response(_res, level="debug")


def create_release(*, owner: str, repo: str, payload: dict) -> dict:
    """创建release"""
    # 先判断相应的release是否已经存在
    _release = release_exists(
        owner=owner,
        repo=repo,
        name=payload["name"],
        tag_name=payload["tag_name"],
        target=payload["target_commitish"],
    )
    if _release:
        return _release

    # 不存在时创建
    _url = f"{DOMAIN}/repos/{owner}/{repo}/releases"
    logger.info(
        f"【{owner}/{repo}】库发布版本，参数：{json.dumps(payload, ensure_ascii=False, indent=4)}"
    )
    _res = session.post(_url, json=payload)
    return checkout_response(_res, level="info")


def batch_delete_release(release_list: list):
    """批量删除release"""
    for _release in release_list:
        _res = session.delete(_release["url"])
        if _res.status_code == 204:
            logger.info(f"删除成功：{_release['url']}")
        elif _res.status_code == 404:
            logger.warning(f"记录不存在：{_release['url']}")
        else:
            format_output(_res)
            logger.error(f"删除失败：{_release['url']}")


def delete_release(*, owner: str, repo: str, release_id: int):
    """删除release"""
    release_obj = get_release_by_id(owner=owner, repo=repo, release_id=release_id)
    if not release_obj:
        raise ValueError(f"release不存在：{owner}/{repo}:{release_id}")
    assert release_obj["id"] == release_id
    # assert release_obj["prerelease"] is True, "非预发布状态，不能删除"
    assert release_obj["name"].startswith("temp_"), "release名字校验不通过，只有以temp_开头的才能删除"
    logger.info(f"可删除性校验通过，开始删除release: {release_obj['name']}")
    _url = f"{DOMAIN}/repos/{owner}/{repo}/releases/{release_id}"
    _res = session.delete(_url)
    return checkout_response(_res, level="info")


def is_checkout(*, owner: str, repo: str, target: str):
    """提供的branch/tag/commitId是否存在"""
    # gitea中允许branch与tag重名，必须区分优先级
    # tag优先级最高
    _res_tag = get_tags(owner=owner, repo=repo)
    if _res_tag:
        for _tag in _res_tag:
            if _tag["name"] == target:
                return _tag

    # branch优先级第二
    _res_branch = tetrieve_branch(owner=owner, repo=repo, branch=target)
    if _res_branch:
        return _res_branch

    # commit 优先级最低
    _res_commit = get_commit_default(owner=owner, repo=repo, sha=target)
    if _res_commit:
        return _res_commit

    logger.warning(f"在{owner}/{repo}的tag/branch/commit中找不到目标：{target}")
    return None


def is_checkout_by_obj(repos: dict, target: str):
    """提供的branch/tag/commitId是否存在"""
    # target预处理，target中可能带有前缀
    if ":" in target:
        _type, target = target.split(":", 1)
    else:
        _type = None

    # gitea中允许branch与tag重名，必须区分优先级
    # tag优先级最高
    owner, repo = parser_git_url(repos["repo_url"])
    _res_tag = get_tags(owner=owner, repo=repo)
    if _res_tag:
        for _tag in _res_tag:
            if _tag["name"] == target:
                repos["branch"] = f"TAG:{target}"
                return True, owner, repo, target, repos

    # branch优先级第二
    _res_branch = tetrieve_branch(owner=owner, repo=repo, branch=target)
    if _res_branch:
        repos["branch"] = f"BRANCH:{target}"
        return True, owner, repo, target, repos

    # commit 优先级最低
    _res_commit = get_commit_default(owner=owner, repo=repo, sha=target)
    if _res_commit:
        repos["branch"] = f"COMMIT:{target}"
        return True, owner, repo, target, repos

    logger.error(f"在{owner}/{repo}的tag/branch/commit中找不到目标：{target}")
    repos["branch"] = None
    return False, owner, repo, target, repos


def list_branch(*, owner: str, repo: str, page: int = 1, per_page: int = 100):
    """分支列表"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/branches"
    params = {"page": page, "per_page": per_page}
    _res = session.get(_url, params=params)
    return checkout_response(_res, level="debug")


def tetrieve_branch(*, owner: str, repo: str, branch: str):
    """检索特定分支"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/branches/{branch}"
    _res = session.get(_url)
    return checkout_response(_res, level="debug")


def get_tags(*, owner: str, repo: str):
    """获取库中tag标签列表"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/tags"
    _res = session.get(_url)
    return checkout_response(_res)


def get_commit_default(*, owner: str, repo: str, sha: str):
    """获取commit详情"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}/git/commits/{sha}"
    _res = session.get(_url)
    return checkout_response(_res, level="debug")


def repo_list(*, owner: str, page: int = 1, per_page: int = 100):
    """获取库列表"""
    _url = f"{DOMAIN}/orgs/{owner}/repos"
    params = {"page": page, "per_page": per_page}
    _res = session.get(_url, params=params)
    return checkout_response(_res, level="debug")


def repo_detail(*, owner: str, repo: str):
    """获取库列表"""
    _url = f"{DOMAIN}/repos/{owner}/{repo}"
    _res = session.get(_url)
    return checkout_response(_res, level="debug")
