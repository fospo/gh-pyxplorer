import os
import logging
import concurrent.futures
from github import Github, Repository


def get_github_token():
    """Gets the GitHub token from the environment variables."""
    GH_TOKEN = os.getenv("GH_TOKEN")
    if not GH_TOKEN:
        logging.error("GH_TOKEN is not set. Check your env variables.")
        return None
    return GH_TOKEN


def crawl(inputType: str, inputName: str) -> bool:
    """Working just on GitHub for the moment"""
    """Returns True if everything went fine, False otherwise"""
    """Prints name, license and primary language of each repo"""
    MAX_WORKERS = 10
    GH_TOKEN = get_github_token()
    if GH_TOKEN is None:
        return False
    g = Github(GH_TOKEN)

    # 3 input possibilities: org, repo, list
    try:
        if inputType == "org":
            org = g.get_organization(inputName)
            repos = org.get_repos()
        elif inputType == "repo":
            repos = [g.get_repo(inputName)]
        elif inputType == "list":
            repos = [g.get_repo(repo_name) for repo_name in inputName.split(",")]
        else:
            logging.error("Invalid input type.")
            return False
    except Exception as e:
        logging.error(f"Error in getting repos: {e}")
        return False

    if not repos:
        logging.error("No repos found for the input.")
        return False

    results = []
    # ThreadPool to parallelize the exploration. Output in a thread safe list
    try:
        with concurrent.futures.ThreadPoolExecutor(MAX_WORKERS) as threadPool:
            for result in threadPool.map(explore_repository, repos):
                results.append(result)
    except Exception as e:
        logging.error("Error in thread pool execution. Check " + repr(e))
        return False
    finally:
        # Shutdown waits for all threads to finish by default
        threadPool.shutdown()

    return results


def explore_repository(repository: Repository.Repository):
    """Exploring the repository (input)"""
    if repository.size == 0:
        logging.warning(f"Repository {repository.name} is empty. Skipping.")
        return {"name": repository.name, "isEmpty": True}

    # Data structure
    repo_info = {
        "name": repository.name,
        "license": check_licenses(repository),
        "language": repository.language,
    }
    return repo_info


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

    licenseNameList = ["license", "licenza", "EUPL", "GPL", "licenza.txt", "license.txt"]

    # Get all root repository contents to find a match with possible names
    for content in repository.get_contents(""):
        for license in licenseNameList:
            if license in content.path.lower():
                return content.path
    return None


def group_by_name(results):
    """Grouping the list of results by the first token of the project name
    Example: my-app -> my, my-app-2 -> my, my-app-3 -> my, so the group is my
    and the count is 3"""
    dictionary = {}

    for result in results:
        if result.get("isEmpty", False):
            continue  # Skip empty repositories

        # Group by based on the name
        repo_name = result.get("name", "")
        tok = repo_name.split("-")[0]  # Split the repo name
        if tok not in dictionary:
            dictionary[tok] = {"count": 1, "repos": [result]}
        else:
            dictionary[tok]["count"] += 1
            dictionary[tok]["repos"].append(result)

    sorted_dict = dict(
        sorted(dictionary.items(), key=lambda x: x[1]["count"], reverse=True)
    )

    return sorted_dict


def print_details(results, fields):
    """Print the results"""
    for result in results:
        if result.get("isEmpty", False):
            print(f"{result['name']} is empty.")
        else:
            details = [f"{result.get(field, 'N/A')}" for field in fields]
            print(",".join(details))
