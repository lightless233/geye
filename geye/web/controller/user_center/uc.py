#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    uc.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    user center api

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2021 lightless. All rights reserved
"""
from django.http import JsonResponse

from geye import constant
from geye.web.controller.base import BaseView, RequestValidator


class UserRegisterView(BaseView):
    """
    注册用户
    """

    def post(self, request):
        cr = RequestValidator.check_params(request, ("username", "email", "password"), check_empty=True)
        if cr.has_error:
            err_resp = self.quick_error(constant.ResponseCode.PARAM_ERROR.value, cr.error_message)
            return JsonResponse(err_resp.to_dict())

        request_params = cr.params
        username = request_params.get("username", None)
        email = request_params.get("email", None)
        password = request_params.get("password", None)

        # service.do_register(username, email, password)
