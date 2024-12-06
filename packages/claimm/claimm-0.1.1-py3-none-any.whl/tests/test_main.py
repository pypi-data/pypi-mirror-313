from claimm.main import main


def test_main_function():
    """Ensure the main function runs without errors."""
    assert main() == "App initialized"
