import unittest


class OutputCheck(unittest.TestCase):
    def assert_output(self, expr, actual):
        """
        断言返回体
        1.
        2.
        3.
        4.
        :param expr: 期望值，dict demo：
        :param actual:
        """
        self.assertEqual(len(expr.keys()), len(actual.keys()), msg='actual keys er`ror!')
        for k, v in expr.items():
            self.assertIn(k, actual.keys())
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'{k} Dynamic value type assert fail！')
            elif isinstance(v, dict):
                self.assert_output(v, actual[k])
            elif isinstance(v, list):
                for index in range(len(v)):
                    if isinstance(v[index], dict):
                        self.assert_output(v[index], actual[k][index])
                    else:
                        self.assertEqual(v[index], actual[k][index], msg=f'{k}(type:list) index: {index} assert error!')
            else:
                self.assertEqual(v, actual[k], msg=f'key: {k} assert error!')
