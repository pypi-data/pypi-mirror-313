import pytest
from unittest.mock import patch, MagicMock
from hackbot.commands import hackbot_run
from hackbot.hack import (
    authenticate,
    hack_target,
    generate_issues,
)
from hackbot.utils import compress_source_code, url_format


@pytest.fixture
def test_params():
    return {
        "address": "https://app.hackbot.co",
        "port": None,
        "api_key": "test_api_key",
        "source": "test_source",
    }


@pytest.fixture
def mock_args(test_params):
    args = MagicMock()
    args.address = test_params["address"]
    args.port = test_params["port"]
    args.api_key = test_params["api_key"]
    args.source = test_params["source"]
    args.output = None
    args.auth_only = False
    args.issues_repo = None
    args.github_api_key = None
    return args


def test_url_format():
    """Test URL formatting with and without port"""
    assert url_format("https://app.hackbot.co", None) == "https://app.hackbot.co"
    assert url_format("https://app.hackbot.co", 8080) == "https://app.hackbot.co:8080"

    with pytest.raises(AssertionError):
        url_format("ftp://invalid.com", None)


@pytest.mark.asyncio
@patch("hackbot.hack.aiohttp.ClientSession")
async def test_authenticate_success(mock_session, test_params):
    # Create mock response
    mock_response = MagicMock()
    mock_response.status = 200

    # Setup session context manager
    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.get.return_value.__aenter__.return_value = mock_response
    mock_session.return_value = mock_session_context

    result = await authenticate(test_params["address"], test_params["port"], test_params["api_key"])
    assert result is True

    # Verify correct URL and headers
    expected_url = f"{test_params['address']}/api/authenticate"
    expected_headers = {"X-API-KEY": test_params["api_key"]}
    mock_session_context.get.assert_called_once_with(
        expected_url,
        headers=expected_headers,
    )


@pytest.mark.asyncio
@patch("hackbot.hack.aiohttp.ClientSession")
async def test_authenticate_failure(mock_session, test_params):
    mock_response = MagicMock()
    mock_response.status = 401

    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.get.return_value.__aenter__.return_value = mock_response
    mock_session.return_value = mock_session_context

    result = await authenticate(test_params["address"], test_params["port"], test_params["api_key"])
    assert result is False


def test_compress_source_code(tmp_path):
    """Test source code compression with temp directory"""
    # Create test files
    source_dir = tmp_path / "test_src"
    source_dir.mkdir()
    test_file = source_dir / "test_file.txt"
    test_file.write_text("Test content")

    zip_path = tmp_path / "src.zip"
    compress_source_code(str(source_dir), str(zip_path))

    assert zip_path.exists()
    assert zip_path.stat().st_size > 0

    # Test size limit
    big_file = source_dir / "big.txt"
    big_file.write_bytes(b"0" * (300 * 1024 * 1024))  # 300MB file

    with pytest.raises(RuntimeError, match="too large"):
        compress_source_code(str(source_dir), str(zip_path))


@pytest.mark.asyncio
@patch("hackbot.hack.aiohttp.ClientSession")
async def test_hack_target(mock_session, test_params):
    """Test the hack_target function with mocked responses"""
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.content.__aiter__.return_value = [
        b'data: {"message": "Starting analysis"}',
        b'data: {"title": "Test Bug Found"}',
    ]

    mock_session_context = MagicMock()
    mock_session_context.__aenter__.return_value = mock_session_context
    mock_session_context.post.return_value.__aenter__.return_value = mock_response
    mock_session.return_value = mock_session_context

    results = []
    async for result in hack_target(
        test_params["address"], test_params["port"], test_params["api_key"], test_params["source"]
    ):
        results.append(result)

    assert len(results) == 2
    assert "Starting analysis" in results[0]
    assert "Test Bug Found" in results[1]


@pytest.mark.asyncio
@patch("hackbot.hack.Github")
async def test_generate_issues(mock_github, test_params):
    """Test GitHub issue generation"""
    mock_repo = MagicMock()
    mock_issue = MagicMock()
    mock_issue.title = "HB-1"
    mock_repo.get_issues.return_value = [mock_issue]
    mock_repo.create_issue.return_value = mock_issue

    mock_github.return_value.get_repo.return_value = mock_repo

    test_results = [
        {"bug_id": "BUG-1", "bug_title": "Test Bug", "bug_description": "This is a test bug"}
    ]

    await generate_issues("test/repo", "test_token", test_results)

    # Verify issue creation
    mock_repo.create_issue.assert_called_once_with(title="HB-2")
    mock_issue.create_comment.assert_called_once_with(body="#BUG-1 - Test Bug\nThis is a test bug")


@patch("hackbot.commands.get_repo")
@patch("os.path.exists")
@patch("hackbot.commands.authenticate")
@patch("hackbot.commands.cli_hack_target")
def test_hackbot_run(mock_cli_hack, mock_auth, mock_exists, mock_get_repo, mock_args):
    """Test the main hackbot run command"""
    mock_get_repo.return_value = True
    mock_exists.return_value = True

    # Mock the coroutines with AsyncMock
    mock_auth.return_value = True
    mock_cli_hack.return_value = [{"bug_id": "TEST-1"}]

    result = hackbot_run(mock_args)
    assert result == 0

    # Test authentication failure
    mock_auth.return_value = False
    result = hackbot_run(mock_args)
    assert result == 1

    # Test with auth_only flag
    mock_args.auth_only = True
    mock_auth.return_value = True
    result = hackbot_run(mock_args)
    assert result == 0
