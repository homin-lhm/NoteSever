import requests
from common.yamlRead import YamlRead
import time


class Create:
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def create_group(self, userid, sid, num):
        """
        批量新增分组的方法
        :param userid:
        :param sid:
        :param num:
        :return:
        """
        url = self.host + f'/v3/notesvr/set/notegroup'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        group_list = []
        for i in range(num):
            groupId = str(int(time.time() * 1000)) + '_groupId'
            body = {
                'groupId': groupId,
                'groupName': 'Test'
            }
            res = requests.post(url, headers=headers, json=body)
            assert res.status_code == 200
            group_list.append(groupId)

        return group_list

    def create_group_note(self, userid, sid, groupId, num):
        """
        批量新增分组便签的方法
        :param userid:
        :param sid:
        :param groupId:
        :param num:
        :return: noteIds
        """
        note_info_url = self.host + f'/v3/notesvr/set/noteinfo'
        note_content_url = self.host + f'/v3/notesvr/set/notecontent'

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(userid)
        }
        noteIds = []
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + '_noteId'
            body = {
                'noteId': noteId,
                'groupId': groupId
            }
            res = requests.post(url=note_info_url, headers=headers, json=body)
            infoVersion = res.json()['infoVersion']

            # 新增便签内容
            body = {
                'noteId': noteId,
                'title': 'test',
                'summary': 'test',
                'body': 'test',
                'localContentVersion': infoVersion,
                'BodyType': 0
            }
            res = requests.post(url=note_content_url, headers=headers, json=body)
            assert res.status_code == 200
            noteIds.append(noteId)

        return noteIds
