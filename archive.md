---
layout: default
title: Archive
permalink: /archive/
---

<div class="archive">
  <h1 class="page-title">Archive</h1>

  <ul class="archive-posts">
    {% for post in site.posts %}
    <li>
      <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date_to_string }}</time>
      <a class="archive-post-title" href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
</div>
