import requests


def _get_deployment_list(token, owner, repo, per_page=100, _page=1):
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


def delete_deployment(token, owner, repo, deployment_id):
    """
    Delete a deployment.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/deployments/{deployment_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    res = requests.delete(url, headers=headers)
    return res.status_code


def delete_all_deployments(token, owner, repo):
    """
    Delete all deployments of a repository.
    """
    success = True
    deployments = _get_deployment_list(token, owner, repo)
    for deployment in deployments:
        try:
            delete_deployment(token, owner, repo, deployment["id"])
        except Exception as e:
            print(e)
            success = False
    return success
