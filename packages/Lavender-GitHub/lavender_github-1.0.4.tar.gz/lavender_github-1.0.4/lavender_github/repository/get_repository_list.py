import requests


def get_public_repo_list(username):
    page = 1
    per_page = 100
    list = []
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    while True:
        params = {"per_page": per_page, "page": page}
        res = requests.get(url, headers=headers, params=params).json()
        list += res
        if len(res) < per_page:
            break
        else:
            page += 1
    return list


def get_private_repo_list(username, token):
    page = 1
    per_page = 30
    list = []
    url = f"https://api.github.com/user/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    while True:
        params = {"per_page": per_page, "page": page, "type": "private"}
        res = requests.get(url, headers=headers, params=params).json()
        list += res
        if len(res) < per_page:
            break
        else:
            page += 1
    return list


def get_starred_repo_list(username, token):
    page = 1
    per_page = 100
    list = []
    url = f"https://api.github.com/users/{username}/starred"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    while True:
        params = {"per_page": per_page, "page": page}
        res = requests.get(url, headers=headers, params=params).json()
        list += res
        if len(res) < per_page:
            break
        else:
            page += 1
    return list
