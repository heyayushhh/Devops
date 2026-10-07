import unittest
import importlib
import login
import app

class TestDevOpsApp(unittest.TestCase):
    """
    Unit test suite for DevOps Application (Lab 1 CI/CD Pipeline)
    """

    def test_login_function_exists(self):
        """Test that the login function is defined and callable"""
        self.assertTrue(callable(getattr(login, 'login', None)), "login function must exist in login.py")

    def test_login_execution(self):
        """Test that login executes without error"""
        result = login.login()
        self.assertIsNone(result, "login() should execute and return None")

    def test_app_module_loaded(self):
        """Test that app module loads properly"""
        self.assertIsNotNone(app, "app.py must be importable")

if __name__ == '__main__':
    unittest.main(verbosity=2)
