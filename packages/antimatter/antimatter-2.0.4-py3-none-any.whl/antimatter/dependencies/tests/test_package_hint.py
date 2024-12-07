from antimatter.dependencies.package_hint import as_install_hint


def test_as_install_hint():
    # For this to pass, the requirements will need to be findable and parseable
    hint = as_install_hint("pandas")
    assert "pip install pandas" in hint
