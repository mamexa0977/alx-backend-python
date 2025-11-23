# #!/usr/bin/env python3
# """
# Unit tests for utils module
# """

# import unittest
# from unittest.mock import Mock, patch
# from parameterized import parameterized
# from utils import access_nested_map, get_json, memoize


# class TestAccessNestedMap(unittest.TestCase):
#     """Test cases for access_nested_map function"""

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         """Test access_nested_map with valid paths"""
#         self.assertEqual(access_nested_map(nested_map, path), expected)

#     @parameterized.expand([
#         ({}, ("a",), 'a'),
#         ({"a": 1}, ("a", "b"), 'b'),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path, missing_key):
#         """Test access_nested_map raises KeyError for invalid paths"""
#         with self.assertRaises(KeyError) as context:
#             access_nested_map(nested_map, path)
#         self.assertEqual(str(context.exception), f"'{missing_key}'")


# class TestGetJson(unittest.TestCase):
#     """Test cases for get_json function"""

#     @parameterized.expand([
#         ("http://example.com", {"payload": True}),
#         ("http://holberton.io", {"payload": False}),
#     ])
#     @patch('utils.requests.get')
#     def test_get_json(self, test_url, test_payload, mock_get):
#         """Test get_json returns expected result without making actual HTTP calls"""
#         # Create a mock response object
#         mock_response = Mock()
#         mock_response.json.return_value = test_payload
#         mock_get.return_value = mock_response

#         # Call the function
#         result = get_json(test_url)

#         # Assertions
#         mock_get.assert_called_once_with(test_url)
#         self.assertEqual(result, test_payload)


# class TestMemoize(unittest.TestCase):
#     """Test cases for memoize decorator"""

#     def test_memoize(self):
#         """Test that memoize caches the result and calls the method only once"""
        
#         class TestClass:
#             def __init__(self):
#                 self.call_count = 0

#             def a_method(self):
#                 self.call_count += 1
#                 return 42

#             @memoize
#             def a_property(self):
#                 return self.a_method()

#         # Create instance and test memoization
#         with patch.object(TestClass, 'a_method') as mock_method:
#             mock_method.return_value = 42
#             test_instance = TestClass()
            
#             # First call should call a_method
#             result1 = test_instance.a_property
#             # Second call should use cached result
#             result2 = test_instance.a_property
            
#             # Assertions
#             self.assertEqual(result1, 42)
#             self.assertEqual(result2, 42)
#             mock_method.assert_called_once()
#!/usr/bin/env python3
"""
Unit tests for utils module
"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid paths"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """Test access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{missing_key}'")


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected result"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches the result"""
        class TestClass:
            def __init__(self):
                self.call_count = 0

            def a_method(self):
                self.call_count += 1
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()