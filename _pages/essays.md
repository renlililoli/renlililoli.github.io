---
layout: archive
title: "Essays"
permalink: /essays/
author_profile: false
---

## 和学术与工作无关, 乱七八糟的东西都在这里

全部是随笔和杂谈

{% include base_path %}

{% for post in site.essays reversed %}
  {% include archive-single.html %}
{% endfor %}
