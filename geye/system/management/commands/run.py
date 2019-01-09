#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    geye.system.management.commands.run
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    处理程序的启动参数，启动整个Application

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from django.core.management import BaseCommand, CommandError

from geye.application import GeyeApplication
from geye.core import data as gdata


class Command(BaseCommand):
    help = "Start the GEYE application."
    available_opts = ["server", "agent", "single"]

    def add_arguments(self, parser):
        parser.add_argument("--single", action="store_const", const="single", dest="run_mode",
                            help="Run GEYE as single app. (Default)")
        parser.add_argument("--server", action="store_const", const="server", dest="run_mode",
                            help="Run GEYE as server.")
        parser.add_argument("--agent", action="store_const", const="agent", dest="run_mode", help="Run GEYE as agent.")

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting GEYE application."))

        # check run_mode params
        run_mode = options.get("run_mode")
        if run_mode not in self.available_opts:
            raise CommandError("错误的启动参数，只能为: '--single', '--server', '--agent' 其中之一.")

        try:
            gdata.application = GeyeApplication(run_mode)
            gdata.application.start()
        except Exception as e:
            self.stdout.write("Error while starting application. {}".format(e))
            import sys
            import traceback

            # exc_type, exc_value, exc_tb = sys.exc_info()
            # tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
            tbe = traceback.TracebackException(*sys.exc_info())
            full_err = ''.join(tbe.format())
            self.stdout.write("Full error below:\n {}".format(full_err))
