from typing import Optional, List, Dict, Any, Literal, AsyncGenerator
from dataclasses import dataclass
import aiohttp
import json
import tempfile
from pathlib import Path
from loguru import logger as log
from termcolor import colored
from tqdm import tqdm
from hackbot.utils import url_format, compress_source_code, get_repo_info
from github import Github, GithubException, Auth


@dataclass
class HackBotClientMessage:
    """A message sent to the hackbot client."""

    type: Literal["message", "progress", "error"]
    message: str

    def log(self) -> None:
        """Log the message to the console."""
        if self.type == "message":
            log.info(self.message)
        elif self.type == "progress":
            log.info(self.message, extra={"progress": True})
        elif self.type == "error":
            log.error(self.message)


async def process_stream(response: aiohttp.ClientResponse) -> AsyncGenerator[str, None]:
    """Process the streaming response from the hackbot service."""
    async for line in response.content:
        line = line.decode("utf-8")
        if line.startswith("data: "):
            try:
                json_str = line[5:].strip()  # Remove 'data: ' prefix
                yield json_str
            except json.JSONDecodeError:
                log.error(f"Failed to parse JSON: {json_str}")
    return


async def hack_target(
    invocation_args: Dict[str, Any], address: str, port: int, api_key: str, source_path: str = ".", output: Optional[str] = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Analyze the target source code using the hackbot service.

    Args:
        address: The hackbot service address
        port: The service port number
        api_key: Authentication API key
        source_path: Path to the source code to analyze
        output: Optional path to save results

    Returns:
        List of analysis results
    """

    # Search for closest enclosing git repo and info from there, can be None
    repo_info = get_repo_info(source_path)

    # Compress the source code into a tempfile
    with tempfile.NamedTemporaryFile(delete=True, suffix=".zip") as temp_zip:
        compress_source_code(source_path, temp_zip.name, git_info=repo_info)

        url = f"{url_format(address, port)}/api/hack"
        headers = {"X-API-KEY": api_key, "Connection": "keep-alive"}

        # Prepare the form data
        data = aiohttp.FormData()
        data.add_field(
            "file",
            open(temp_zip.name, "rb"),
            filename="compressed_source_code.zip",
            content_type="application/zip",
        )
        if repo_info:
            for key, value in repo_info.items():
                if key and value:
                    data.add_field(f"repo_info_{key}", value)

        # Invocation args into invocation_arg_* keys
        for key, value in invocation_args.items():
            data.add_field(f"invocation_arg_{key}", value)

        results = []
        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"Hack request failed with status {response.status}, and error: {await response.text()}")

                async for result in process_stream(response):
                    results.append(json.loads(result))
                    yield result

                # Save results if output path specified
                if output:
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "w") as f:
                        json.dump(results, f, indent=2)

                return


async def cli_hack_target(invocation_args: Dict[str, Any], address: str, port: int, api_key: str, source_path: str = ".", output: Optional[str] = None) -> None:

    results = []
    pbar = tqdm(desc=colored("\U0001F7E1" + " Analyzing code", "yellow"), unit=" findings")
    async for report in hack_target(invocation_args, address, port, api_key, source_path, output):
        result_json = json.loads(report)
        if result_json.get("message") is not None:
            log.info(result_json.get("message"))
            pbar.set_postfix_str(colored(result_json.get("message"), "yellow"))
        elif result_json.get("progress") is not None:
            pbar.set_postfix_str(colored(result_json.get("progress").get("message"), "yellow"))
        elif result_json.get("title") is not None:
            pbar.update(1)
            pbar.set_postfix_str(colored(result_json.get("title"), "yellow"))
            log.info("\U0001F41B Finding: " + colored(result_json.get("title"), "yellow"))
            results.append(result_json)
        elif result_json.get("error") is not None:
            pbar.set_description_str(colored("❌ Analyzing code", "red"))
            pbar.set_postfix_str(colored("Failed", "red"))
            pbar.close()
            print(colored(result_json.get("error"), "red"))
            return results

    pbar.set_description_str(colored("✅ Analyzing code", "green"))
    pbar.set_postfix_str(colored("Done", "green"))
    pbar.close()

    if len(results) == 0:
        log.info(
            colored(
                "✅ No issues found",
                "green",
            )
        )

    return results


async def authenticate(address: str, port: int, api_key: str) -> bool:
    """Verify API key authentication with the hackbot service."""
    url = f"{url_format(address, port)}/api/authenticate"
    headers = {"X-API-KEY": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200


async def get_selectable_models(address: str, port: int, api_key: str) -> List[str]:
    """Get the list of selectable models from the hackbot service."""
    url = f"{url_format(address, port)}/get_selectable_models"
    headers = {"X-API-KEY": api_key}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            assert response.status == 200, f"Failed to get selectable models: HTTP code {response.status} from backend endpoint"
            return (await response.json())["models"]


async def generate_issues(issues_repo: str, github_api_key: str, results: List[Dict[str, Any]]) -> None:
    """
    Generate GitHub issues for bugs discovered by the bot.

    This function creates a master issue in the specified GitHub repository
    containing all the bugs found. It uses the GitHub API to create issues
    and requires appropriate authentication and permissions.

    Args:
        issues_repo (str): The full name of the GitHub repository (e.g., "owner/repo").
        github_api_key (str): The GitHub token for authentication.
        results (List[Dict[str, Any]]): A list of dictionaries containing bug information.

    Returns:
        None

    Raises:
        Exception: If there are permission issues or other errors when interacting with the GitHub API.

    Note:
        - This function requires a GitHub token with 'issues: write' and 'contents: read' permissions.
        - It creates a master issue with a title format of "HB-{number}".
    """
    if not issues_repo:
        log.error("GitHub repository is not specified.")
        return

    # Authenticate with GitHub
    auth = Auth.Token(github_api_key)
    g = Github(auth=auth)

    # Get a list of the bugs discovered by the bot
    issues_found = [issue for issue in results if issue.get("bug_id") is not None]
    if len(issues_found) == 0:
        log.info("No bugs found, skipping issue generation")
        return

    # Get the output repository. This will fail if the github token does not have access to the repository
    repo = None
    try:
        repo = g.get_repo(issues_repo)
    except GithubException as e:
        log.error(f"Error accessing repository: {e}")
        return

    last_hb_issue = 0
    # Fetch all existing issues in the repository and find the last one created by the bot
    for issue in repo.get_issues(state="all"):
        if issue.title.startswith("HB-"):
            last_hb_issue = int(issue.title.split("-")[1])
            break

    # Create a master issue in the repository that will contain all the bugs.
    # This will fail if the github token does not have write access to the issues
    # permissions:
    # - issues: write
    master_issue = None
    try:
        master_issue = repo.create_issue(title=f"HB-{last_hb_issue + 1}")
    except GithubException as e:
        log.error(f"Error creating issue: {e}")
        if e.status == 422:
            raise Exception("Validation failed, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 403:
            raise Exception("Forbidden, aborting. This functionality requires a GITHUB_TOKEN with 'issues: write' in the workflow permissions section.")
        elif e.status == 410:
            raise Exception("Gone, aborting. The repository does not allow issues.")

    # Add each bug as a comment to the master issue
    for issue in issues_found:
        body = f"#{issue.get('bug_id')} - {issue.get('bug_title')}\n{issue.get('bug_description')}"
        master_issue.create_comment(body=body)

    log.info(f"Created issue: {master_issue.title}")
