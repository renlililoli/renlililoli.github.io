---
layout: home
permalink: /
title: "Guorui Zhu"
excerpt: "Ph.D. candidate at Fudan University working on efficient AI systems, high-performance computing, numerical algorithms, and quantum computing."
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<div class="home-page">
  <section class="home-hero" aria-labelledby="home-title">
    <p class="home-eyebrow">Computational Mathematics · Efficient AI Systems</p>
    <h1 id="home-title">Guorui Zhu</h1>
    <p class="home-role">Ph.D. Candidate at Fudan University</p>
    <p class="home-intro">
      I work at the intersection of efficient model inference, high-performance computing,
      numerical algorithms, and quantum computing. My current work focuses on making
      demanding AI and scientific workloads faster, more scalable, and easier to deploy.
    </p>

    <div class="home-actions" aria-label="Primary links">
      <a class="home-action home-action--primary" href="/cv/">
        <i class="fa-solid fa-file-lines" aria-hidden="true"></i>
        View CV
      </a>
      <a class="home-action" href="/publications/">
        <i class="fa-solid fa-book-open" aria-hidden="true"></i>
        Publications
      </a>
      <a class="home-action" href="https://github.com/renlililoli">
        <i class="fa-brands fa-github" aria-hidden="true"></i>
        GitHub
      </a>
    </div>

    <dl class="home-facts">
      <div>
        <dt>Current</dt>
        <dd>Research Intern, Huawei ICT BG</dd>
      </div>
      <div>
        <dt>Education</dt>
        <dd>School of Mathematical Sciences, Fudan University</dd>
      </div>
      <div>
        <dt>Advisor</dt>
        <dd><a href="https://yingzhouli.com">Prof. Yingzhou Li</a></dd>
      </div>
    </dl>
  </section>

  <section class="home-section" aria-labelledby="focus-title">
    <header class="home-section__header">
      <p class="home-section__index">01</p>
      <div>
        <h2 id="focus-title">Research Focus</h2>
        <p>Systems and algorithms for compute-intensive problems.</p>
      </div>
    </header>

    <div class="focus-grid">
      <article class="focus-item">
        <i class="fa-solid fa-gauge-high" aria-hidden="true"></i>
        <h3>Efficient AI Inference</h3>
        <p>Profiling, workload modeling, memory optimization, and systems design for video generation models.</p>
      </article>
      <article class="focus-item">
        <i class="fa-solid fa-network-wired" aria-hidden="true"></i>
        <h3>High-Performance Computing</h3>
        <p>Distributed scientific computing with C++, MPI, CUDA, Slurm, and multi-node clusters.</p>
      </article>
      <article class="focus-item">
        <i class="fa-solid fa-square-root-variable" aria-hidden="true"></i>
        <h3>Numerical Algorithms</h3>
        <p>Fast solvers, parallel PDE methods, numerical linear algebra, and scientific software.</p>
      </article>
      <article class="focus-item">
        <i class="fa-solid fa-atom" aria-hidden="true"></i>
        <h3>Quantum Computing</h3>
        <p>Quantum algorithms for basis transformation, orbital optimization, and excited-state calculation.</p>
      </article>
    </div>
  </section>

  <section class="home-section" aria-labelledby="work-title">
    <header class="home-section__header">
      <p class="home-section__index">02</p>
      <div>
        <h2 id="work-title">Selected Work</h2>
        <p>Recent engineering and research projects.</p>
      </div>
    </header>

    <div class="project-list">
      <article class="project-item">
        <div class="project-item__meta">
          <span>Huawei</span>
          <time datetime="2026-06">Jun 2026 – Present</time>
        </div>
        <div class="project-item__body">
          <h3>Video Generation Inference Optimization</h3>
          <p>
            Profiled video generation inference pipelines, identified performance bottlenecks,
            and modeled workload behavior. Built activation-offloading approaches that preserve
            output quality and inference speed while enabling long, high-resolution generation on consumer GPUs.
          </p>
          <ul class="tag-list" aria-label="Technologies">
            <li>CUDA C++</li>
            <li>Model Inference</li>
            <li>Performance Modeling</li>
          </ul>
          <div class="project-links">
            <a href="https://github.com/renlililoli/minimax-h3-seq-chunk-attn">MiniMax-H3 SeqAttn <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
            <a href="https://github.com/renlililoli/stream-attn">Stream-Attn <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
          </div>
        </div>
      </article>

      <article class="project-item">
        <div class="project-item__meta">
          <span>Scientific Computing</span>
          <time datetime="2026">2026</time>
        </div>
        <div class="project-item__body">
          <h3>Parallel PDE Solver</h3>
          <p>
            Implemented a parallel Poisson–Boltzmann solver in C++ and MPI using the HIF-SI library.
            Evaluated scaling on the Tianhe-3 supercomputer and commercial cloud platforms, with
            optimization centered on communication behavior and workload balance.
          </p>
          <ul class="tag-list" aria-label="Technologies">
            <li>C++</li>
            <li>MPI</li>
            <li>HIF-SI</li>
            <li>Tianhe-3</li>
          </ul>
        </div>
      </article>

      <article class="project-item">
        <div class="project-item__meta">
          <span>Huawei Collaboration</span>
          <time datetime="2024">2024 – 2025</time>
        </div>
        <div class="project-item__body">
          <h3>Macro Placement Algorithms</h3>
          <p>
            Developed and optimized 2D macro placement algorithms for an internal physical-design tool,
            with code merged into Huawei's internal repository. Also improved Open3DBench algorithms
            for 3D placement quality and runtime efficiency.
          </p>
          <ul class="tag-list" aria-label="Technologies">
            <li>C++</li>
            <li>EDA</li>
            <li>Optimization</li>
          </ul>
        </div>
      </article>

      <article class="project-item">
        <div class="project-item__meta">
          <span>Fudan University</span>
          <time datetime="2024">2024 – Present</time>
        </div>
        <div class="project-item__body">
          <h3>HPC Cluster Administration</h3>
          <p>
            Built and maintain a multi-node research cluster, including networking, storage,
            scientific software, user environments, and Slurm scheduling. Integrated Grafana and
            agent-assisted workflows for monitoring, anomaly identification, and job analysis.
          </p>
          <ul class="tag-list" aria-label="Technologies">
            <li>Linux</li>
            <li>Slurm</li>
            <li>Grafana</li>
            <li>Distributed Systems</li>
          </ul>
        </div>
      </article>
    </div>
  </section>

  <section class="home-section" aria-labelledby="publications-title">
    <header class="home-section__header">
      <p class="home-section__index">03</p>
      <div>
        <h2 id="publications-title">Publications</h2>
        <p>Quantum algorithms for electronic-structure calculations.</p>
      </div>
      <a class="section-link" href="/publications/">View all <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </header>

    <div class="publication-list">
      <article class="publication-item">
        <p class="publication-item__venue">npj Quantum Information · 2025</p>
        <h3>Quantum Circuit for Non-Unitary Linear Transformation of Basis Sets</h3>
        <p><strong>Guorui Zhu</strong>, J. Bierman, J. Lu, and Y. Li. <span class="publication-volume">11, 198 (2025).</span></p>
        <a href="https://doi.org/10.1038/s41534-025-01145-3">DOI <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
      </article>
      <article class="publication-item">
        <p class="publication-item__venue">arXiv preprint · 2025</p>
        <h3>State-Specific Orbital Optimization for Enhanced Excited-States Calculation on Quantum Computers</h3>
        <p><strong>Guorui Zhu</strong>, J. Bierman, J. Lu, and Y. Li. <span class="publication-volume">arXiv:2510.13544.</span></p>
        <a href="https://arxiv.org/abs/2510.13544">arXiv <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
      </article>
    </div>
  </section>

  <section class="home-section" aria-labelledby="writing-title">
    <header class="home-section__header">
      <p class="home-section__index">04</p>
      <div>
        <h2 id="writing-title">Recent Writing</h2>
        <p>Notes on model systems, parallel computing, and numerical methods.</p>
      </div>
      <a class="section-link" href="/blog/">Browse notes <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </header>

    {% assign recent_posts = site.blog | sort: "date" | reverse %}
    <div class="writing-list">
      {% for post in recent_posts limit: 4 %}
        <a class="writing-item" href="{{ post.url }}">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %Y" }}</time>
          <span>{{ post.title }}</span>
          <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
        </a>
      {% endfor %}
    </div>
  </section>

  <section class="home-contact" aria-labelledby="contact-title">
    <div>
      <p class="home-eyebrow">Contact</p>
      <h2 id="contact-title">Open to research and engineering conversations.</h2>
    </div>
    <a class="home-action home-action--primary" href="mailto:grzhu24@m.fudan.edu.cn">
      <i class="fa-solid fa-envelope" aria-hidden="true"></i>
      Email me
    </a>
  </section>
</div>
