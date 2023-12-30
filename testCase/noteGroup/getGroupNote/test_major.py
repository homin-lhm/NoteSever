import unittest
from common.yamlRead import YamlRead
from businessCommon.clearNote import Clear
from businessCommon.createNote import Create
from common.outputCheck import OutputCheck
from businessCommon.re import Re
from common.caseLog import info, error, step, class_case_log
from parameterized import parameterized


@class_case_log
class GetGroupNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    userId1 = envConfig['userId1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['GetGroupNote']['path']
    optionKeys = dataConfig['interface']['GetGroupNote']['optionKeys']
    base = dataConfig['interface']['GetGroupNote']['base']
    assertBase = {
            'responseTime': int,
            'webNotes': [
                {
                    'noteId': '',
                    'createTime': int,
                    'star': 0,
                    'remindTime': 0,
                    'remindType': 0,
                    'infoVersion': int,
                    'infoUpdateTime': int,
                    'groupId': '',
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': int,
                    'contentUpdateTime': int
                }
            ]
        }

    def setUp(self) -> None:
        Clear().clear_note(self.userId1, self.sid1)

    def testCase01(self):
        """查看分组下便签的主流程"""
        step('PRE-STEP: 新增一个分组')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        step('PRE-STEP: 在分组下新增一个便签')
        noteIds = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)
        step('STEP: 查看分组下便签的接口请求')
        body = self.base
        body['groupId'] = groupIds[0]

        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)

        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = noteIds[0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())

    def testCase02(self):
        """查看分组下便签的必填项校验"""
        step('STEP: 查看分组下便签的接口请求')
        body = {
            'startIndex': 0,
            'rows': 10
        }
        print('hello world')
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())


    @parameterized.expand(optionKeys)
    def testCase04(self, key):
        """查看分组下便签的非必填项校验"""
        step('PRE-STEP: 新增一个分组')
        groupIds = Create().create_group(self.userId1, self.sid1, 1)
        step('PRE-STEP: 在分组下新增一个便签')
        noteIds = Create().create_group_note(self.userId1, self.sid1, groupIds[0], 1)
        step('STEP: 查看分组下便签的接口请求')
        body = self.base
        body.pop(key)
        res = self.re.post(url=self.url, body=body, userId=self.userId1, sid=self.sid1)
        self.assertEqual(200, res.status_code)
