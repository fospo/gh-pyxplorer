# GitHub pyxplorer

You have a GitHub organization and you want to explore it?
With this simple interactive crawler you can explore a GitHub {organization, repository, or a list of repositories} and 
extract some insightful information.
Please note: it uses GitHub's API. 

# Options

The crawler accepts the following command-line arguments:

- `-i` or `--input`: Specifies the input type. This should be either 'org' for a GitHub organization, 'repo' for a specific repository, or 'list' for a list of repositories. This argument is **required**.

- `<name>`: The name of the organization, repository or file name containing a list of repositories to explore. This is a positional argument and is **required**.

- `-o` or `--output`: Specifies the output type. This can be 'print' to print the results to the console, or 'file' to write the results to a file. The **default** is '*print*'.

- `-f` or `--fields`: Specifies the fields to include in the output. This should be a space-separated list of field names. The default is 'name license language'.


> NOTE: GH heuristics catches if a repo has a license 
by checking the `LICENSE.md` or `LICENSE` files. Here we are digging a bit 
deeper in order to see if there are other files that "may" contain licensing
info in the root of the repo.


## How to run

```bash
export GH_TOKEN=<your_github_token>
python3 crawler.py -i org <organization_name> -o print
```

#### Output

Depending on the type of parameter passed to the `-o` option, the output will be printed to the console or written to a file.

The output is a CSV-like structure with the following fields:

```csv
repo_name,license,primary_language
```

In case of file, this is the output (JSON-like):

```json
{
    {
    "nome del gruppo": {
        "count": numero totale di repository per il gruppo,
        "private-repos": [
            "nome del repository privato 1",
            "nome del repository privato 2",
            ...
        ],
        "public-repos": [
            "nome del repository pubblico 1",
            "nome del repository pubblico 2",
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