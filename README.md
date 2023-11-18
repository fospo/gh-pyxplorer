# GitHub pyxplorer

You have a GitHub organization and you want to explore it?
With this simple interactive crawler you can explore a GitHub {organization, repository, or a list of repositories} and 
extract some insightful information.
Please note: it uses GitHub's API. 

## Details

This tool is a fundamental asset for any *Open Source Program Office* (OSPO). In the complex landscape of open source software, it's crucial to have a clear understanding of your organization's repositories. This tool provides a comprehensive overview of your repositories, including details such as the repository name, license, and primary language.

Regular scans of your repositories are essential for maintaining compliance and ensuring the health of your open source projects. This tool makes it easy to perform these scans on a regular basis, providing you with up-to-date information and helping you to identify any potential issues early.


# How to run

### Install
```bash
pip3 install -r requirements.txt
```


### Launch

```bash
export GH_TOKEN=<your_github_token>
python3 crawler.py -i org <organization_name> -o print
```

## Options

The crawler accepts the following command-line arguments:

- `-i` or `--input` [**required**]: Specifies the input type. This should be either:

    * `org` for a GitHub organization, 
    * `repo` for a specific repository,
    * `list` for a list of repositories. 

- `<name>` [**required**]: The name of the organization, repository or file name containing a list of repositories to explore.

- `-o` or `--output` [**required**]: Specifies the output type. This can be:

    * `print` [**default**] to print the results to the console, 
    * `file` to write the results to a file. 



- `-f` or `--fields`: Specifies the fields to include in the output. This should be a space-separated list of field names. The default is **'name license language'**. The available fields are:

    * `name` for the repository name,
    * `license` for the repository license,
    * `language` for the repository's primary language,
    * `private` for private repositories [NOT IMPLEMENTED YET],
    * `public` for public repositories [NOT IMPLEMENTED YET]

For example, if you want just the `name` and `license` fields as output:

```bash
python3 crawler.py -i org <organization_name> -o print -f name license
```

> NOTE: GH heuristics catches if a repo has a license 
by checking the `LICENSE.md` or `LICENSE` files. Here we are digging a bit 
deeper in order to see if there are other files that "may" contain licensing
info in the root of the repo.



### Output

Depending on the type of parameter passed to the `-o` option, the output will be printed to the console or written to a file.

The output is a CSV-like structure with the following fields:

```csv
repo_name,license,primary_language
```

In case of file, this is the output (JSON-like):

```json
{
    "group name": {
        "count": total number of repositories for the group,
        "private-repos": [
            "name of private repository 1",
            "name of private repository 2",
            ...
        ],
        "public-repos": [
            "name of public repository 1",
            "name of public repository 2",
            ...
        ]
    },
    ...
}
```

#### Testing

Run

```bash
python3 -m unittest tests.py
```

# License

MIT License, see [LICENSE](LICENSE.md)