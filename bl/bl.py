#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import datetime

import markdown
from jinja2 import Environment, FileSystemLoader


j2_env = Environment(loader=FileSystemLoader('_templates'))
j2_site = j2_env.get_template('site.html')
j2_blog = j2_env.get_template('blog.html')

class Menu:
    class Item:
        def __init__(self, link, title):
            self.link = link
            self.title = title

    def __init__(self, sites, blogs):
        self.items = []
        for site in sites :
            self.items.append(self.Item(site.file_n + '.html', site.file_n))
        for blog in blogs:
            self.items.append(self.Item(blog.file_n + '.html', blog.file_n))

class Site:
    def __init__(self, file_p):
        self.file_p = file_p
        self.file_n = os.path.basename(file_p).split('.')[0]

    def render(self, menu):
        # render markdown
        with open(self.file_p, 'r+', encoding='utf-8') as file:
            text = markdown.markdown(file.read(), extensions=['meta'])

        # pack it into jinj2templates
        html = j2_site.render(content=text, menu=menu)
        with open(os.path.join('docs', self.file_n + '.html'), 'w+') as file:
            file.write(html)

class Blog:
    class Post:
        def __init__(self, file_p):
            self.file_p = file_p
            self.file_n = os.path.basename(file_p).split('.')[0]

            self.creation_d = datetime.datetime.strptime(self.file_n, '%d%m%Y').date()
        
        def __str__(self):
            return self.text
        
        def render(self):
            # render markdown
            with open(self.file_p, 'r+', encoding='utf-8') as file:
                self.text = markdown.markdown(file.read(), extensions=['meta'])

    def __init__(self, file_p, paginate=False):
        self.file_p = file_p
        self.file_d = os.path.dirname(file_p)
        self.file_n = os.path.basename(file_p).split('.')[0]

    def paginate(self):
        # TODO
        pass

    def render(self, menu):
        # collect all posts
        posts = []
        posts_d = os.path.join(self.file_d, self.file_n)

        for file_p in glob.glob(os.path.join(posts_d, '*.md')):
            posts.append(self.Post(file_p))

        # sort them by date
        posts = list(reversed(sorted(posts, key=lambda x: x.creation_d)))

        # render all of them
        for post in posts:
            post.render()

        # pack it into jinj2templates
        html = j2_blog.render(posts=posts, menu=menu)
        with open(os.path.join('docs', self.file_n + '.html'), 'w+') as file:
            file.write(html)


def getSites(folder_p):
    sites = []

    for file_p in glob.glob(os.path.join(folder_p, '*.md')):
        sites.append(Site(file_p))
    
    return sites

def getBlogs(folder_p):
    blogs = []

    for file_p in glob.glob(os.path.join(folder_p, '*.md')):
        blogs.append(Blog(file_p))

    return blogs

def getMenu(sites, blogs):
    return Menu(sites, blogs)