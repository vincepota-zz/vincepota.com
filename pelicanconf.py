#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Vince Pota'
SITENAME = u'vincepota.com'
#SITEURL = 'http://www.vincepota.com'
TIMEZONE = 'Etc/Greenwich'
TITLE = "A data science blog."
DESCRIPTION = ""

# Variables for theme
THEME = 'void/'
#LOGO_IMAGE = '/images/logo.jpg'
COPYRIGHT_START_YEAR = 2013
NAVIGATION = [
    {'site': 'github', 'user': 'vincepota', 'url': 'https://github.com/vincepota'},
    {'site': 'linkedin', 'user': 'vincepota', 'url': 'https://www.linkedin.com/in/vincepota/'},
    {'site': 'stack-overflow', 'user': 'vincepota', 'url': 'https://stackoverflow.com/users/5497294/vincep/'}
]

# ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
# ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Static Pages
PAGE_PATHS = ['pages']
# PAGE_URL = '{slug}/'
# PAGE_SAVE_AS = '{slug}/index.html'
ABOUT_PAGE_HEADER = 'Welcome to my blog'

# DEFAULTS
DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'misc'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PAGINATION = False

# FEEDS
FEED_ALL_ATOM = "feeds/all.atom.xml"
TAG_FEED_ATOM = "feeds/tag/%s.atom.xml"

DISPLAY_PAGES_ON_MENU = True
MARKUP = ('md', 'ipynb')

# PLUGINS
PLUGIN_PATHS = ['pelican-plugins', 'pelican_dynamic']
PLUGINS = ['assets', 'pelican-ipynb.liquid', 'pelican_dynamic']

CODE_DIR = 'code'
NOTEBOOK_DIR = 'notebooks'
# EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

STATIC_PATHS = ['images', 'code', 'notebooks', 'extra', 'data']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

# TODO: SOCIAL - make it dynamic
TWITTER_CARDS = False
TWITTER_NAME = ""
FACEBOOK_SHARE = False
HACKER_NEWS_SHARE = False

#### Analytics
GOOGLE_ANALYTICS = 'UA-124125850-1'
DOMAIN = "vincepota.com"

# Other
MAILCHIMP = False
CACHE_CONTENT = False
