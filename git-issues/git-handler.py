import os
import re
import subprocess
import requests

GITHUB_API_ADDRESS = "https://api.github.com/"


def get_git_address():

    response = subprocess.check_output(['git', 'remote', '-v'])
    dirty = response.split('\n')
    repos = {}
    for repo in dirty:
        rep = repo.split('\t')

        if len(rep) > 1:
            repos[rep[0]] = rep[1].replace(' (fetch)', '').replace(' (push)', '')
    return repos


def get_issues(repos):
    issues = []
    import re
    for k, v in repos.items():
        repo_slug_match = re.search("\:(.*\/.*)\.git", v)

        if repo_slug_match is not None:
            repo_slug = repo_slug_match.group(1)
            response = requests.get(GITHUB_API_ADDRESS + "repos/" +repo_slug + "/issues")
            issues += response.json()

    write_issues_to_disk(issues)

def write_issues_to_disk(issues)
    git_issues_dir = os.path.expanduser("~/.git-issues/")
    if not os.path.exists(git_issues_dir):
        os.makedirs(git_issues_dir)

    with open(git_issues_dir + "%s.json" % re.search("\:.*\/(.*)\.git", repos['origin']).group(1), 'w') as f:
        import json
        f.write(json.dumps(issues))


if __name__ == '__main__':
    repos = get_git_address()
    get_issues(repos)
