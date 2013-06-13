#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime
from flask import Markup

import markdown


def configure_helpers(app):

    @app.template_filter('md')
    def md_filter(s):
        return Markup(markdown.markdown(s))

    @app.template_filter()
    def timesince(dt, default=u"刚刚"):
        """
        Returns string representing "time since" e.g.
        3 days ago, 5 hours ago etc.
        """

        now = datetime.now()
        diff = now - dt

        periods = (
            (diff.days / 365, u" 年"),
            (diff.days / 30, u" 月"),
            (diff.days / 7, u" 周"),
            (diff.days, u" 天"),
            (diff.seconds / 3600, u" 小时"),
            (diff.seconds / 60, u" 分钟"),
        )

        for period, unit in periods:
            if period > 0:
                return u"%d%s前" % (period, unit)

        if diff.seconds > 1:
                return u"%d 秒前" % diff.seconds

        return default

