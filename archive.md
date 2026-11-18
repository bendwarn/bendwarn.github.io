---
layout: default
title: 歷史
permalink: /archive/
---

<div class="archive collection-page" lang="zh-Hant">
  <header class="collection-header">
    <h1 class="page-title">歷史</h1>
    <p>依時間瀏覽所有文章</p>
  </header>

  {% for post in site.posts %}
    {% assign year = post.date | date: '%Y' %}
    {% if year != previous_year %}
      {% unless forloop.first %}</ul></section>{% endunless %}
      <section class="collection-section" aria-labelledby="year-{{ year }}">
        <h2 class="collection-heading" id="year-{{ year }}">{{ year }}</h2>
        <ul class="collection-posts archive-posts">
      {% assign previous_year = year %}
    {% endif %}
          <li>
            <a class="archive-post-title" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%m / %d' }}</time>
          </li>
    {% if forloop.last %}</ul></section>{% endif %}
  {% else %}
    <p class="collection-empty">目前沒有文章。</p>
  {% endfor %}
</div>
