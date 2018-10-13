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
    available_opts = ["server_mode", "agent_mode"]

    def add_arguments(self, parser):
        parser.add_argument("--server", action="store_true", dest="server_mode", help="Run GEYE as server.")
        parser.add_argument("--agent", action="store_true", dest="agent_mode", help="Run GEYE as agent.")

    def handle(self, *args, **options):
        self.stdout.write(self.style.INFO("Starting GEYE application."))

        if not any([options.get(opt) for opt in self.available_opts]):
            raise CommandError("Must specify mode.")

        run_mode = "server" if options.get("server_mode") else "agent"

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
