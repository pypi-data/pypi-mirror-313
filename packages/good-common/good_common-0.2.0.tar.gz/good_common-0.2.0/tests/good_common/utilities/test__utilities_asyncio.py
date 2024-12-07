import pytest
import asyncio
from unittest.mock import patch, MagicMock
from good_common.utilities._asyncio import run_async


def test_run_async_with_existing_loop():
    def sample_function():
        return "Hello, World!"

    with patch("asyncio.get_event_loop") as mock_get_loop:
        mock_loop = MagicMock()
        mock_loop.run_until_complete.return_value = "Hello, World!"
        mock_get_loop.return_value = mock_loop

        result = run_async(sample_function())

        mock_get_loop.assert_called_once()
        mock_loop.run_until_complete.assert_called_once()
        assert result == "Hello, World!"


def test_run_async_without_existing_loop():
    def sample_function():
        return "Hello, World!"

    with patch(
        "asyncio.get_event_loop", side_effect=[RuntimeError, MagicMock()]
    ), patch("asyncio.new_event_loop") as mock_new_loop, patch(
        "asyncio.set_event_loop"
    ) as mock_set_loop:
        mock_loop = MagicMock()
        mock_loop.run_until_complete.return_value = "Hello, World!"
        mock_new_loop.return_value = mock_loop

        result = run_async(sample_function())

        mock_new_loop.assert_called_once()
        mock_set_loop.assert_called_once_with(mock_loop)
        mock_loop.run_until_complete.assert_called_once()
        assert result == "Hello, World!"


def test_run_async_in_jupyter():
    def sample_function():
        return "Hello, Jupyter!"

    with patch.dict("sys.modules", {"IPython": MagicMock()}), patch(
        "nest_asyncio.apply"
    ) as mock_apply, patch("asyncio.get_event_loop") as mock_get_loop:
        mock_loop = MagicMock()
        mock_loop.run_until_complete.return_value = "Hello, Jupyter!"
        mock_get_loop.return_value = mock_loop

        result = run_async(sample_function())

        mock_apply.assert_called_once()
        assert result == "Hello, Jupyter!"


def test_run_async_with_exception():
    def sample_function():
        raise ValueError("Test exception")

    with patch("asyncio.get_event_loop") as mock_get_loop:
        mock_loop = MagicMock()
        mock_loop.run_until_complete.side_effect = ValueError("Test exception")
        mock_get_loop.return_value = mock_loop

        with pytest.raises(ValueError, match="Test exception"):
            run_async(sample_function())


def test_run_async_with_real_coroutine():
    async def sample_coroutine():
        await asyncio.sleep(0.1)
        return "Hello, Async World!"

    # Create a new event loop for this test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = run_async(sample_coroutine())
        assert result == "Hello, Async World!"
    finally:
        # Clean up the event loop
        loop.close()
