import pytest
from unittest.mock import patch, MagicMock
from footium_api import LogReportStrategy, DiscordReportStrategy, ReportStrategy
from logging import getLogger

logger = getLogger(__name__)

class TestMockReportStrategy(ReportStrategy):
    def __init__(self):
        self.messages = {"info": [], "event": [], "warning": [], "error": []}

    def info(self, content: str):
        self.messages["info"].append(content)

    def event(self, content: str):
        self.messages["event"].append(content)

    def warning(self, content: str):
        self.messages["warning"].append(content)

    def error(self, content: str):
        self.messages["error"].append(content)

@pytest.fixture
def mock_strategy():
    return TestMockReportStrategy()

@pytest.fixture
def log_strategy():
    return LogReportStrategy()

@pytest.fixture
def discord_strategy():
    with patch('footium_api.report.requests.post') as mock_post:
        strategy = DiscordReportStrategy()
        yield strategy, mock_post

def test_info(mock_strategy):
    mock_strategy.info("This is an info message")
    assert "This is an info message" in mock_strategy.messages["info"]

def test_event(mock_strategy):
    mock_strategy.event("This is an event message")
    assert "This is an event message" in mock_strategy.messages["event"]

def test_warning(mock_strategy):
    mock_strategy.warning("This is a warning message")
    assert "This is a warning message" in mock_strategy.messages["warning"]

def test_error(mock_strategy):
    mock_strategy.error("This is an error message")
    assert "This is an error message" in mock_strategy.messages["error"]

def test_log_info(log_strategy, caplog):
    with caplog.at_level(logger.level):
        log_strategy.info("Log info message")
        assert any(record.message == "Log info message" for record in caplog.records)

def test_log_event(log_strategy, caplog):
    with caplog.at_level(logger.level):
        log_strategy.event("Log event message")
        assert any(record.message == "Log event message" for record in caplog.records)

def test_log_warning(log_strategy, caplog):
    with caplog.at_level(logger.level):
        log_strategy.warning("Log warning message")
        assert any(record.message == "Log warning message" for record in caplog.records)

def test_log_error(log_strategy, caplog):
    with caplog.at_level(logger.level):
        log_strategy.error("Log error message")
        assert any(record.message == "Log error message" for record in caplog.records)

def test_discord_info(discord_strategy):
    strategy, mock_post = discord_strategy
    strategy.info("Discord info message")
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == strategy.info_url
    assert mock_post.call_args[1]['json']['content'] == "Discord info message"

def test_discord_event(discord_strategy):
    strategy, mock_post = discord_strategy
    strategy.event("Discord event message")
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == strategy.event_url
    assert mock_post.call_args[1]['json']['content'] == "Discord event message"

def test_discord_warning(discord_strategy):
    strategy, mock_post = discord_strategy
    strategy.warning("Discord warning message")
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == strategy.warning_url
    assert mock_post.call_args[1]['json']['content'] == "Discord warning message"

def test_discord_error(discord_strategy):
    strategy, mock_post = discord_strategy
    strategy.error("Discord error message")
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == strategy.error_url
    assert mock_post.call_args[1]['json']['content'] == "Discord error message"
