import unittest
from echobox.tool import strings


class TestUtils(unittest.TestCase):

    def test_all(self):
        map = {
            'a': 'A',
            '1.1': '1.1',
            'scaling_group': 'ScalingGroup',
        }
        for src, dst in map.items():
            self.assertEquals(strings.camelize_key(src), dst)


if __name__ == '__main__':
    unittest.main()
