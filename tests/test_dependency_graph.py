from app.dependency_graph import get_affected_files, get_affected_tests


def test_affected_tests():
    graph = {
        "tests/test_predictor.py": ["app/sample_code.py"],
        "app/other.py": ["app/sample_code.py"]
    }

    affected_files = get_affected_files(graph, "app/sample_code.py")
    affected_tests = get_affected_tests(graph, "app/sample_code.py")

    assert "tests/test_predictor.py" in affected_files
    assert "tests/test_predictor.py" in affected_tests