#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bl.bl import getSites, getBlogs, getMenu


def main():
    sites = getSites('_sites')
    blogs = getBlogs('_blogs')
    # prepare menu
    menu = getMenu(sites, blogs)

    # render everything
    for site in sites:
        site.render(menu)
    for blog in blogs:
        blog.render(menu)

if __name__ == "__main__":
    main()