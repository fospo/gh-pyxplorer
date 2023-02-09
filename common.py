import os
import logging
import concurrent.futures
from github import Github, Repository


def dry_run(inputOrg: str) -> bool:
    """Working just on GitHub for the moment"""
    MAX_WORKERS = 10
    GH_TOKEN = os.getenv("GH_TOKEN")
    if GH_TOKEN is None:
        logging.error("GH_TOKEN is not set. Check your env variables.")
        return False
    g = Github(GH_TOKEN)

    # get paginated result of repos
    # this call should be in a try catch block
    orgRepos = g.get_organization(inputOrg).get_repos()

    try:
        # handle a pool of thread
        threadPool = concurrent.futures.ThreadPoolExecutor(MAX_WORKERS)
        for results in threadPool.map(explore_licenses, orgRepos):
            print(results)
    except Exception as e:
        logging.error("Error in thread pool execution. Check " + repr(e))
        return False
    finally:
        # Shutdown waits for all threads to finish by default
        threadPool.shutdown()

    return True


def explore_licenses(repository: Repository.Repository):
    """Exploring the repository (input) and printing the license.name"""
    licenseName = "Empty"
    try:
        repoLicense = repository.get_license()
        licenseName = repoLicense.license.name
    except Exception:
        # if repoLicense is empty, exception is raised
        licenseName = check_other_license_names(repository)
    finally:
        return repository.name + "," + licenseName


def check_other_license_names(repository: Repository.Repository) -> str:
    """Heuristic: if I get 404 on get_license, let's dig a bit deeper.
    There may be some files other than `LICENSE.md` or `LICENSE` that fit
    the license definition. Let's find out"""

    licenseNameList = ["license", "licenza", "EUPL", "GPL"]

    # Get all root repository contents to find a match with possible names
    for content in repository.get_contents(""):
        for license in licenseNameList:
            if license in content.path.lower():
                return content.path
    return "Empty"


def group_by_project(fileLines):
    """ Grouping the list of lines by project name."""
    dictionary = {}

    if fileLines:
        # Line in the form of "0, org/repo-name"
        for index, line in enumerate(fileLines):
            if line:
                name = line.split('/')[1].split(',')[0].strip()
                tok = name.split('-')[0]

                if tok not in dictionary.keys():
                    dictionary[tok] = [name]
                else:
                    dictionary[tok].append(name)

    return dictionary