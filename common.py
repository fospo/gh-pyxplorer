import os
import logging
from github import Github
from github import Repository
import concurrent.futures


def dry_run(inputOrg: str) -> bool:
    """Working just on GitHub for the moment"""
    MAX_WORKERS = 10
    GH_TOKEN = os.getenv("GH_TOKEN")
    g = Github(GH_TOKEN)

    # get paginated result of repos
    orgRepos = g.get_organization(inputOrg).get_repos()

    try:
        # handle a pool of thread
        threadPool = concurrent.futures.ThreadPoolExecutor(MAX_WORKERS)
        threadPool.map(explore_licenses, orgRepos)
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
        print(repository.name + "," + licenseName)


def check_other_license_names(repository: Repository.Repository) -> str:
    """Heuristic: if I get 404 on get_license, let's dig a bit deeper.
    There may be some files other than `LICENSE.md` or `LICENSE` that fit
    the license definition. Let's find out"""

    licenseNameList = ["license", "licenza"]

    # Get all root repository contents to find a match with possible names
    for content in repository.get_contents(""):
        for license in licenseNameList:
            if license in content.path.lower():
                return content.path
    return "Empty"
