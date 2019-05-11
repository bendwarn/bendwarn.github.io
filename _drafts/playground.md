---
layout: post
title: playground
---

place to see variable

## Global Variables
site: {{ site }}

page = this page

layout: {{ layout }}

content = liquid generate

paginator: {{ paginator }}

## Site Variables
time: {{ site.time }}

pages = all pages

posts = all posts

related_posts: need no explain

static_files: {{ site.static_files }}

html_pages: A subset of `site.pages` listing those which end in `.html`.

html_files: {{ site.html_files }}

collections: {{ site.collections }}

data: {{ site.data }}

documents: A list of all the documents in every collection.

categories: {{ site.categories }}

tags: {{ site.tags }}

url: {{ site.url }}

baseurl: {{ site.baseurl }}

## Page Variables
content = this content

title: {{ page.title }}

excerpt: {{ page.excerpt }}

url: {{ page.url }}

date: {{ page.date }}

id: {{ page.id }}

categories: {{ page.categories }}

tags: {{ page.tags }}

path: {{ page.path }}

next: need no explain

previous: need no explain
