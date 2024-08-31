import unittest
from admin_penal.api_functions.functions.admin_func import generate_token


class MyTestCase(unittest.TestCase):
    def test_something(self):


        out= generate_token("email")
        self.assertEqual(out,10,'failed')


if __name__ == '__main__':
    unittest.main()
