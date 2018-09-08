# -*- coding: utf-8 -*-
"""Test Apis."""
from flask import json
import types
import urllib
import pytest
from utils import *


@pytest.mark.usefixtures('db')
class TestApiProject:
    """api role testing"""
    uri_prefix = '/api/project'

    server_id = {}

    project_data = {
        "environment_id": 1,
        "excludes": u"*.log",
        "keep_version_num": 11,
        "name": u"walden-瓦尔登",
        "post_deploy": u"echo post_deploy",
        "post_release": u"echo post_release",
        "prev_deploy": u"echo prev_deploy",
        "prev_release": u"echo prev_release",
        "repo_mode": u"branch",
        "repo_password": u"",
        "repo_url": u"git@github.com:meolu/walle-web.git",
        "repo_username": u"",
        "server_ids": u"1,2",
        "target_releases": u"/tmp/walle/library",
        "target_root": u"/tmp/walle/root",
        "target_user": u"work",
        "task_vars": u"debug=1;\\napp=auotapp.py",
        "user_id": 1
    }


    # should be equal to project_data_2.name
    project_name_2 = u'walle-web'

    project_data_2 = {
        "environment_id": 2,
        "excludes": u"*.log",
        "keep_version_num": 10,
        "name": u"walle-web",
        "post_deploy": u"echo post_deploy",
        "post_release": u"echo post_release",
        "prev_deploy": u"echo prev_deploy",
        "prev_release": u"echo prev_release",
        "repo_mode": u"branch",
        "repo_password": u"",
        "repo_url": u"git@github.com:meolu/walle-web.git",
        "repo_username": u"",
        "server_ids": u"1,2",
        "target_releases": u"/tmp/walle/library",
        "target_root": u"/tmp/walle/root",
        "target_user": u"work",
        "task_vars": u"debug=1;\\napp=auotapp.py",
        "user_id": 1
    }

    project_data_2_update = {
        "environment_id": 1,
        "excludes": u"*.log",
        "keep_version_num": 11,
        "name": u"walle-web to walden edit",
        "post_deploy": u"echo post_deploy; pwd",
        "post_release": u"echo post_release; pwd",
        "prev_deploy": u"echo prev_deploy; pwd",
        "prev_release": u"echo prev_release; pwd",
        "repo_mode": u"tag",
        "repo_password": u"",
        "repo_url": u"git@github.com:meolu/walden.git",
        "repo_username": u"",
        "server_ids": u"1,2",
        "target_releases": u"/tmp/walden/library",
        "target_root": u"/tmp/walden/root",
        "target_user": u"work",
        "task_vars": u"debug=1;\\napp=auotapp.py; project=walden",
        "user_id": 1
    }

    project_data_remove = {
        'name': u'this server will be deleted soon',
        "environment_id": 1,
        "excludes": u"*.log",
        "keep_version_num": 11,
        "post_deploy": u"echo post_deploy",
        "post_release": u"echo post_release",
        "prev_deploy": u"echo prev_deploy",
        "prev_release": u"echo prev_release",
        "repo_mode": u"branch",
        "repo_password": u"",
        "repo_url": u"git@github.com:meolu/walle-web.git",
        "repo_username": u"",
        "server_ids": u"1,2",
        "target_releases": u"/tmp/walle/library",
        "target_root": u"/tmp/walle/root",
        "target_user": u"work",
        "task_vars": u"debug=1;\\napp=auotapp.py",
        "user_id": 1
    }

    def test_create(self, user, testapp, client, db):
        """create successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.project_data)

        response_success(resp)
        self.project_compare_req_resp(self.project_data, resp)

        self.project_data['id'] = resp_json(resp)['data']['id']

        f=open('run.log', 'w')
        f.write(str(self.project_data_2))
        # 2.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.project_data_2)

        response_success(resp)
        self.project_compare_req_resp(self.project_data_2, resp)

        self.project_data_2['id'] = resp_json(resp)['data']['id']

    def test_one(self, user, testapp, client, db):
        """item successful."""
        # Goes to homepage

        resp = client.get('%s/%d' % (self.uri_prefix, self.project_data['id']))

        response_success(resp)
        self.project_compare_req_resp(self.project_data, resp)

    def test_get_list_page_size(self, user, testapp, client):
        """test list should create 2 users at least, due to test pagination, searching."""

        query = {
            'page': 1,
            'size': 1,
        }
        response = {
            'count': 2,
        }
        resp = client.get('%s/?%s' % (self.uri_prefix, urllib.urlencode(query)))
        response_success(resp)
        resp_dict = resp_json(resp)

        self.project_compare_in(self.project_data_2, resp_dict['data']['list'].pop())
        self.project_compare_req_resp(response, resp)

    def test_get_list_query(self, user, testapp, client):
        """test list should create 2 users at least, due to test pagination, searching."""
        query = {
            'page': 1,
            'size': 1,
            'kw': self.project_name_2
        }
        response = {
            'count': 1,
        }
        resp = client.get('%s/?%s' % (self.uri_prefix, urllib.urlencode(query)))
        response_success(resp)
        resp_dict = resp_json(resp)

        self.project_compare_in(self.project_data_2, resp_dict['data']['list'].pop())
        self.project_compare_req_resp(response, resp)


    def test_get_update(self, user, testapp, client):
        """Login successful."""
        # 1.update
        resp = client.put('%s/%d' % (self.uri_prefix, self.project_data_2['id']), data=self.project_data_2_update)

        response_success(resp)
        self.project_compare_req_resp(self.project_data_2_update, resp)

        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, self.project_data_2['id']))
        response_success(resp)
        self.project_compare_req_resp(self.project_data_2_update, resp)

    def test_get_remove(self, user, testapp, client):
        """Login successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.project_data_remove)
        server_id = resp_json(resp)['data']['id']
        f = open('run.log', 'w')
        f.write(str(resp_json(resp)))
        response_success(resp)

        # 2.delete
        resp = client.delete('%s/%d' % (self.uri_prefix, server_id))
        response_success(resp)

        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, server_id))
        response_error(resp)

    def get_list_ids(self, projectOrigin):
        group_list = projectOrigin.copy()
        group_list['user_ids'] = map(int, projectOrigin['user_ids'].split(','))
        return group_list

    def project_compare_req_resp(self, req_obj, resp):
        """
        there is some thing difference in project api
        such as server_ids
        :param resp:
        :return:
        """
        resp_obj = resp_json(resp)['data']
        servers = []
        if resp_obj.has_key('server_ids'):
            for server in resp_obj['server_ids']:
                servers.append(str(server['id']))

        f=open('run.log', 'w')
        f.write('\n ===='+str(type(servers))+'\n')
        f.write('\n ===='+str(servers)+'\n')
        resp_obj['server_ids'] = ','.join(servers)
        self.project_compare_in(req_obj, resp_obj)

    def project_compare_in(self, req_obj, resp_obj):
        for k, v in req_obj.items():
            assert k in resp_obj.keys(), 'Key %r not in response (keys are %r)' % (k, resp_obj.keys())
            assert resp_obj[k] == v, 'Value for key %r should be %r but is %r' % (k, v, resp_obj[k])