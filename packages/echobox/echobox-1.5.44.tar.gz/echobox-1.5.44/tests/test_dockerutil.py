import unittest
from echobox.tool import dockerutil


class TestDockerUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all(self):
        ip = dockerutil.docker0_ip()


if __name__ == '__main__':
    unittest.main()
