# Hackbot

CLI tool for source code analysis using the [GatlingX Hackbot](https://hackbot.co/) service.

## Installation

```bash
pip install hackbot
```

## Performing a scan
Execute the following command to perform a scan.
Visit your dashboard at [hackbot.co](https://hackbot.co/dashboard/api-keys/) to retrieve your API key.
Either set the API key as an environment variable `HACKBOT_API_KEY` or pass it as an argument to the command line tool.

```bash
cd your-project-directory
python -m hackbot run --api-key <api-key>
```

You will then see various messages and results in the terminal. If `--output` is provided, the complete output will also be written to a JSON file.
At the end of the scan, you will get a link to the dashboard where you can view the results.


## CLI options
See `python -m hackbot --help` for more information


## Generating issues
This module can generate issues in a GitHub repository. To do this, you will need to provide a GitHub API key with **write issue access** to the repository you want to report the issues to (`--issues_repo`). The scan will generate an issue with the title `HB-<number>`, where `<number>` is automatically generated, and will add the discovered bugs as comments to this issue.

```bash
python -m hackbot run --api-key <api-key> --issues_repo <owner>/<repo> --github_api_key <github-api-key>
```
