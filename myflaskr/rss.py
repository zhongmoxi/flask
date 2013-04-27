#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import tempfile
import six
import feedgenerator
from flask import Blueprint

rss = Blueprint('rss',__name__)

feed = feedgenerator.Rss201rev2Feed(
    title="Feed from blog.zhongmoxi.com",
    link="blog.zhongmoxi.com/rss",
    description="""Hi moxi! """,

    language=u"zh-cn",
)

@rss.route('/')
def index():
    pass
feed.add_item(
    title="xxx",
    link="xxx",
    description="xxxx"
)

if six.PY3:
    FN_PREFIX = 'feed_py3-'
else:
    FN_PREFIX = 'feed_py2-'

fd, filename = tempfile.mkstemp(prefix=FN_PREFIX, suffix='.txt', text=True)
try:
    fh = os.fdopen(fd, 'w')
    feed.write(fh, 'utf-8')
finally:
    fh.close()

