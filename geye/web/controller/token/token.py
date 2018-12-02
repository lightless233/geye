#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.web.controller.web.token
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Token 相关的controller

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import json

from django.http import JsonResponse
from django.views import View

from geye.database.models import GeyeTokenModel
from geye.utils.log import logger
from geye.utils.validator import RequestValidator


def mask_token(token):
    return token[:8] + "*" * 24


class TokensView(View):
    """
    获取所有token信息
    """
    @staticmethod
    def get(request):
        rows = GeyeTokenModel.instance.get_all_tokens()

        data = []
        for row in rows:
            data.append({
                "id": row.id,
                "tokenName": row.token_name,
                "tokenContent": mask_token(row.token),
                "status": row.status,
                "remainLimit": row.remain_limit
            })
        return JsonResponse({"code": 1001, "message": "获取成功", "data": data})


class DeleteTokenView(View):
    """
    删除某条token
    """
    @staticmethod
    def post(request):
        token_id = json.loads(request.body).get("id", None)
        if not token_id or not GeyeTokenModel.instance.is_exist(token_id):
            return JsonResponse({"code": 1004, "message": "token id不存在"})

        obj = GeyeTokenModel.instance.fake_delete(token_id)
        if obj:
            return JsonResponse({"code": 1001, "message": "删除成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "删除失败!"})


class AddTokenView(View):
    """
    添加一条token
    """
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))

        result = RequestValidator.check_params(
            request, check_empty=True,
            check_params=["tokenName", "tokenContent", "status"]
        )
        if result.has_error:
            logger.error("error: {}".format(result.error_message))
            return JsonResponse({"code": 1004, "message": result.error_message})

        args = result.params

        token_name = args.get("tokenName", None)
        token = args.get("tokenContent", None)
        status = args.get("status", None)

        obj = GeyeTokenModel.objects.create(
            token_name=token_name, token=token, status=status, remain_limit=99999
        )
        if obj:
            return JsonResponse({"code": 1001, "message": "添加成功!", "data": {
                "id": obj.id,
                "tokenName": obj.token_name,
                "tokenContent": obj.token,
                "status": obj.status,
                "remainLimit": obj.remain_limit,
            }})
        else:
            return JsonResponse({"code": 1002, "message": "添加失败!"})


class EditTokenView(View):
    """
    编辑一条token
    """
    @staticmethod
    def post(request):
        logger.debug("POST: {}".format(request.body))

        result = RequestValidator.check_params(
            request, check_empty=True,
            check_params=["id", "tokenName", "tokenContent", "status"]
        )
        if result.has_error:
            logger.error("error: {}".format(result.error_message))
            return JsonResponse({"code": 1004, "message": result.error_message})

        args = result.params

        token_id = args.get("id", None)
        if not token_id or not GeyeTokenModel.instance.is_exist(token_id):
            return JsonResponse({"code": 1004, "message": "token id不存在!"})

        obj = GeyeTokenModel.instance.update_token(args)
        if obj:
            return JsonResponse({"code": 1001, "message": "更新成功!", "data": {
                "id": obj.id,
                "tokenName": obj.token_name,
                "tokenContent": mask_token(obj.token),
                "status": obj.status,
                "remainLimit": obj.remain_limit,
            }})
        else:
            return JsonResponse({"code": 1002, "message": "更新失败!"})


class UpdateStatus(View):
    """
    切换一条token状态
    """
    @staticmethod
    def post(request):
        token_id = json.loads(request.body).get("id", None)
        if not token_id or not GeyeTokenModel.instance.is_exist(token_id):
            return JsonResponse({"code": 1004, "message": "token id不存在!"})

        obj = GeyeTokenModel.instance.change_status(token_id)
        if obj:
            return JsonResponse({"code": 1001, "message": "切换成功!"})
        else:
            return JsonResponse({"code": 1002, "message": "切换失败!"})


class TokenDetailsView(View):
    """
    获取某条token的详细信息
    """
    @staticmethod
    def get(request):
        token_id = request.GET.get("id", None)
        if not token_id or not GeyeTokenModel.instance.is_exist(token_id):
            return JsonResponse({"code": 1004, "message": "token id不存在!"})

        obj = GeyeTokenModel.instance.get_details(token_id)
        if obj:
            obj["token"] = mask_token(obj["token"])
            return JsonResponse({"code": 1001, "message": "获取成功!", "data": obj})
        else:
            return JsonResponse({"code": 1002, "message": "获取失败!"})
