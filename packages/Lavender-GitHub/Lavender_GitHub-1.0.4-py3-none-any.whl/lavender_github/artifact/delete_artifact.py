import requests


def _get_artifact_list(token, owner, repo, per_page=100, _page=1):
    """
    Get all artifacts of a repository.
    """
    list = []
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    while True:
        params = {"per_page": per_page, "page": _page}
        res = requests.get(url, headers=headers, params=params).json()
        list += res["artifacts"]
        if len(res) < per_page:
            break
        else:
            page += 1
    return list


def delete_artifact(token, owner, repo, artifact_id):
    """
    Delete an artifact.
    """
    print(artifact_id)
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts/{artifact_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
    res = requests.delete(url, headers=headers)
    return res.status_code


def delete_all_artifacts(token, owner, repo):
    """
    Delete all artifacts of a repository.
    """
    artifacts = _get_artifact_list(token, owner, repo)
    print(artifacts)
    for artifact in artifacts:
        delete_artifact(token, owner, repo, artifact["id"])
    return True
