# GitHub pyxplorer

## Options

1. -d, --dry-run, Dry run option

This option allows to get the licenses of all the repos in the organization.
A Github token is needed in order to avoid GH API's rate limit. 
Pass the organization name after the `-d`. 

> NOTE: This relies exclusively on the GH heuristics: if a repo has a license 
with names different than `LICENSE.md` or `LICENSE` GH does not recognize it 
as a valid one. Further exploration of this will follow. 


```bash
export GH_TOKEN=<your_github_token>
python3 crawler.py -d <organization_name>
```

