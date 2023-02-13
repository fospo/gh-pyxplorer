import os
import logging
import concurrent.futures
from github import Github, Repository


def dry_run(inputOrg: str) -> bool:
    """Working just on GitHub for the moment"""
    """Returns True if everything went fine, False otherwise"""
    """Prints name, license and primary language of each repo"""
    MAX_WORKERS = 10
    GH_TOKEN = os.getenv("GH_TOKEN")
    if not GH_TOKEN:
        logging.error("GH_TOKEN is not set. Check your env variables.")
        return False
    g = Github(GH_TOKEN)

    # Get paginated result of repos
    try:
        org = g.get_organization(inputOrg)
        repos = org.get_repos()
    except Exception as e:
        logging.error(f"Error in getting repos: {e}")
        return False

    if not repos:
        logging.error("No repos found for the org.")
        return False

    try:
        with concurrent.futures.ThreadPoolExecutor(MAX_WORKERS) as threadPool:
            for results in threadPool.map(explore_repository, repos):
                # Dry run -> just print the results
                print(results)
    except Exception as e:
        logging.error("Error in thread pool execution. Check " + repr(e))
        return False
    finally:
        # Shutdown waits for all threads to finish by default
        threadPool.shutdown()

    return True


def explore_repository(repository: Repository.Repository):
    """Exploring the repository (input)"""
    license_name = check_licenses(repository)
    language = repository.language
    return f"{repository.name},{license_name},{language}"


def check_licenses(repository: Repository.Repository):
    """Exploring the repository (input) and returning the license name"""
    try:
        license = repository.get_license().license.name
    except Exception:
        license = check_other_license_names(repository)

    return license


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
    """Grouping the list of lines by project name."""
    dictionary = {}

    if fileLines:
        # Line in the form of "0, org/repo-name"
        for index, line in enumerate(fileLines):
            if line:
                name = line.split("/")[1].split(",")[0].strip()
                tok = name.split("-")[0]

                if tok not in dictionary.keys():
                    dictionary[tok] = [name]
                else:
                    dictionary[tok].append(name)

    return dictionary
