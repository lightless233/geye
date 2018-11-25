#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.database.models.token
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    存储github搜索用的token

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models, transaction

from .base import GeyeBaseModel


class TokenManager(models.Manager):
    def get_all_tokens(self):
        """
        获取所有的token
        :return:
        """
        return self.filter(is_deleted=0).order_by("id").all()

    def is_exist(self, token_id):
        """
        根据id判断某个token是否存在
        :param token_id:
        :return:
        """
        return self.filter(is_deleted=0, id=token_id).first()

    def fake_delete(self, token_id):
        """
        根据token id删除记录
        :param token_id:
        :return:
        """
        return self.filter(is_deleted=0, id=token_id).update(is_deleted=1)

    def change_status(self, token_id):
        """
        根据id切换token的状态
        :param token_id:
        :return:
        """
        with transaction.atomic():
            obj = self.select_for_update().filter(is_deleted=0, id=token_id).first()
            if not obj:
                return None
            else:
                obj.status = not obj.status
                obj.save()
                return obj

    def update_token(self, params):
        """
        更新某条token
        :param params:
        :return:
        """
        with transaction.atomic():
            obj = self.select_for_update().filter(is_deleted=0, id=params.token_id).first()
            if not obj:
                return None
            else:
                obj.token_name = params["tokenName"]
                obj.token = params["tokenContent"]
                obj.remain_limit = params["remainLimit"]
                obj.status = params["status"]
                obj.save()
                return obj

    def get_details(self, token_id):
        """
        根据id获取某个token的详细信息
        :param token_id:
        :return:
        """
        obj = self.filter(is_deleted=0, id=token_id).first()
        if not obj:
            return {}
        else:
            return {
                "id": obj.id,
                "tokenName": obj.token_name,
                "tokenContent": obj.token,
                "remainLimit": obj.remain_limit,
                "status": obj.status,
            }


class GeyeTokenModel(GeyeBaseModel):
    """
    token:
        github access token
    remain_limit:
        当前token的剩余可请求次数，从返回头中的X-RateLimit-Remaining获取
        每次搜索的时候，选取这个值最大的，并且更新该值
    status:
        token 状态，1-启用，0-关闭
    """

    class Meta:
        db_table = "geye_token"

    token_name = models.CharField(max_length=32, default="TokenName", null=False)
    token = models.CharField(max_length=64, default="", null=False)
    remain_limit = models.PositiveIntegerField(default=0, null=False)
    status = models.PositiveSmallIntegerField(default=1, null=False)

    objects = models.Manager()
    instance = TokenManager()
