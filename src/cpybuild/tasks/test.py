def run() -> None:
    """
    Discover and run all unittests in the 'tests' directory.
    Looks for files matching 'test_*.py' and executes them using unittest.
    """
    import unittest
    import glob
    print('Discovering and running tests...')
    test_files: list[str] = glob.glob('tests/test_*.py')
    if not test_files:
        print('No test files found in tests/.')
        return
    loader: unittest.TestLoader = unittest.TestLoader()
    suite: unittest.TestSuite = loader.discover('tests', pattern='test_*.py')
    runner: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
    result: unittest.runner.TextTestResult = runner.run(suite)
    if result.wasSuccessful():
        print('All tests passed!')
    else:
        print('Some tests failed.')
