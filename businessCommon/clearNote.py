import requests
from common.yamlRead import YamlRead


class Clear:
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def clear_note(self, userid, sid):
        """
        清空用户下所有便签功能
        :param userid: 用户id
        :param sid: 用户的sid
        :return:None
        """
        get_note_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }

        # 获取用户下的所有便签数据
        res = requests.get(get_note_url, headers=headers)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        clear_body = {
            'noteIds': ['-1']
        }
        res = requests.post(clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200


if __name__ == '__main__':
    userId1 = '922061821'
    sid1 = 'V02SG3oIwfZGY3-EWrNqRBP1J1oAr6E00ab36a440036f58bfd'
    Clear().clear_note(userId1, sid1)
