import requests


def get_deployment_list(token, owner, repo, per_page=100, _page=1):
    """
    Get all deployments of a repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/deployments"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    deployments_list = []
    while True:
        params = {"per_page": per_page, "page": _page}
        res = requests.get(url, headers=headers, params=params).json()
        deployments_list += res
        if len(res) < per_page:
            break
        else:
            _page += 1
    return deployments_list
