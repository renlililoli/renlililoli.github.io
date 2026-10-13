---
layout: archive
title: "Curriculum Vitae"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<div class="resume-page">
  <section class="resume-summary">
    <p>
      Ph.D. candidate in computational mathematics working on AI infrastructure,
      efficient model inference, parallel scientific computing, numerical algorithms,
      and quantum computing.
    </p>
    <div class="resume-contact" aria-label="Contact links">
      <a href="mailto:grzhu24@m.fudan.edu.cn"><i class="fa-solid fa-envelope" aria-hidden="true"></i> grzhu24@m.fudan.edu.cn</a>
      <a href="https://renlililoli.github.io/"><i class="fa-solid fa-globe" aria-hidden="true"></i> Website</a>
      <a href="https://github.com/renlililoli"><i class="fa-brands fa-github" aria-hidden="true"></i> GitHub</a>
      <span><i class="fa-solid fa-location-dot" aria-hidden="true"></i> Shanghai, China</span>
    </div>
  </section>

  <section class="resume-section" aria-labelledby="cv-education">
    <h2 id="cv-education">Education</h2>
    <article class="resume-entry">
      <div class="resume-entry__date">2024 – Present</div>
      <div class="resume-entry__content">
        <h3>Ph.D. Candidate in Computational Mathematics</h3>
        <p class="resume-entry__org">School of Mathematical Sciences, Fudan University</p>
        <p>Research focus: quantum computing and fast algorithms. Advised by <a href="https://yingzhouli.com">Prof. Yingzhou Li</a>.</p>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">2020 – 2024</div>
      <div class="resume-entry__content">
        <h3>B.Sc. in Mathematics and Applied Mathematics</h3>
        <p class="resume-entry__org">School of Mathematical Sciences, Fudan University</p>
        <p>Mathematics Talent Program. Awarded Outstanding Graduate of Fudan University.</p>
      </div>
    </article>
  </section>

  <section class="resume-section" aria-labelledby="cv-experience">
    <h2 id="cv-experience">Engineering & Research Experience</h2>
    <article class="resume-entry resume-entry--featured">
      <div class="resume-entry__date">Jun 2026 – Present</div>
      <div class="resume-entry__content">
        <h3>Research Intern, Data Storage Technology Development</h3>
        <p class="resume-entry__org">Huawei, ICT BG Data Storage Product Line</p>
        <ul>
          <li>Profile image and video generation inference pipelines and model workload characteristics, with practical understanding of Diffusion, Flow Matching, and Score Matching.</li>
          <li>Independently designed and implemented <a href="https://github.com/renlililoli/minimax-h3-seq-chunk-attn">MiniMax-H3 SeqAttn</a> and <a href="https://github.com/renlililoli/stream-attn">Stream-Attn</a>, combining sequence chunking, streaming execution, and activation offloading to reduce memory pressure while preserving output quality and inference speed.</li>
          <li>Enabled arbitrary-resolution and arbitrary-duration video generation on consumer GPUs through joint algorithm and systems optimization.</li>
        </ul>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">Jun 2026 – Present</div>
      <div class="resume-entry__content">
        <h3>Kimi K3 Training Systems &amp; Activation Offloading</h3>
        <p class="resume-entry__org">Huawei, ICT BG Data Storage Product Line</p>
        <ul>
          <li>Independently built the full training software stack for Ascend 910C and 950 systems, including the operating system, drivers, runtime, and distributed-training dependencies; brought up Kimi K3 pruned-model pretraining with FSDP2 on a single-node A3 system with 8 Ascend 910C cards (16 dies, 8 × 2 × 64 GB).</li>
          <li>Evaluated activation offloading on an A5/Ascend 950 setup with high-speed interconnects and an external memory box; read and traced recomputation and offloading mechanisms in MindSpeed MM and selected activations for offloading at operator granularity.</li>
          <li>Used MS Insight to analyze forward hotspots and arithmetic intensity, and studied the amount of data that can be offloaded while overlapping computation, I/O, and communication.</li>
          <li>Analyzed HCCS communication paths and DMA behavior in multi-card communication and activation transfers, achieving about 15% end-to-end speedup over the recomputation baseline.</li>
        </ul>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">Apr 2026 – Jun 2026</div>
      <div class="resume-entry__content">
        <h3>High-Frequency Futures Quantitative Research</h3>
        <p class="resume-entry__org">Pengfu Tech</p>
        <ul>
          <li>Used statistical and machine learning methods to mine alpha factors from tick-level limit-order-book snapshot data.</li>
          <li>Worked with data from the Chinese commodity futures market to study high-frequency signals and quantitative research workflows.</li>
        </ul>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">2026</div>
      <div class="resume-entry__content">
        <h3>Parallel PDE Solver</h3>
        <p class="resume-entry__org">Scientific Computing Project</p>
        <ul>
          <li>Implemented a parallel Poisson–Boltzmann solver in C++ and MPI using the HIF-SI algorithm library.</li>
          <li>Ran scaling studies on the Tianhe-3 supercomputer and commercial cloud platforms, focusing on communication, workload distribution, and parallel efficiency.</li>
        </ul>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">2024 – 2025</div>
      <div class="resume-entry__content">
        <h3>Macro Placement Algorithm Research</h3>
        <p class="resume-entry__org">Huawei Collaboration Project</p>
        <ul>
          <li>Developed and optimized C++ algorithms for 2D macro placement; evaluated results on industrial EDA workloads and merged code into Huawei's internal repository.</li>
          <li>Improved Open3DBench's 3D macro placement algorithm for placement quality and runtime efficiency.</li>
        </ul>
      </div>
    </article>
    <article class="resume-entry">
      <div class="resume-entry__date">2024 – Present</div>
      <div class="resume-entry__content">
        <h3>HPC Cluster Administrator</h3>
        <p class="resume-entry__org">Fudan University</p>
        <ul>
          <li>Built and maintain a multi-node HPC cluster, including networking, storage, user environments, and scientific software.</li>
          <li>Manage compute resources and jobs with Slurm; use Grafana and agent-assisted workflows for metrics collection, anomaly identification, and job analysis.</li>
        </ul>
      </div>
    </article>
  </section>

  <section class="resume-section" aria-labelledby="cv-publications">
    <h2 id="cv-publications">Publications</h2>
    <article class="resume-publication">
      <span>2026</span>
      <div>
        <h3>Structure-Aware Compilation for Scalable Neutral-Atom Quantum Computing</h3>
        <p>D. Dong, F. Zou, H. Chen, <strong>Zhu, G.</strong>, & Li, Y. <em>arXiv preprint</em> arXiv:2607.01787.</p>
        <a href="https://arxiv.org/abs/2607.01787">arXiv:2607.01787</a>
      </div>
    </article>
    <article class="resume-publication">
      <span>2025</span>
      <div>
        <h3>Quantum Circuit for Non-Unitary Linear Transformation of Basis Sets</h3>
        <p><strong>Zhu, G.</strong>, Bierman, J., Lu, J., & Li, Y. <em>npj Quantum Information</em>, 11, 198 (2025).</p>
        <a href="https://doi.org/10.1038/s41534-025-01145-3">DOI: 10.1038/s41534-025-01145-3</a>
      </div>
    </article>
    <article class="resume-publication">
      <span>2025</span>
      <div>
        <h3>State-Specific Orbital Optimization for Enhanced Excited-States Calculation on Quantum Computers</h3>
        <p><strong>Zhu, G.</strong>, Bierman, J., Lu, J., & Li, Y. <em>arXiv preprint</em> arXiv:2510.13544.</p>
        <a href="https://arxiv.org/abs/2510.13544">arXiv:2510.13544</a>
      </div>
    </article>
  </section>

  <div class="resume-two-column">
    <section class="resume-section" aria-labelledby="cv-honors">
      <h2 id="cv-honors">Honors</h2>
      <ul class="resume-compact-list">
        <li><strong>2024</strong> Outstanding Graduate of Fudan University</li>
        <li><strong>2021</strong> Second Prize, National Undergraduate Mathematics Competition, Shanghai Division</li>
        <li><strong>2019</strong> First Prize, National High School Physics Competition, Henan Division</li>
      </ul>
    </section>

    <section class="resume-section" aria-labelledby="cv-teaching">
      <h2 id="cv-teaching">Teaching</h2>
      <ul class="resume-compact-list">
        <li><strong>Spring 2026</strong> Teaching Assistant, Discrete Mathematics</li>
        <li><strong>Fall 2024</strong> Teaching Assistant, Numerical Linear Algebra and Optimization</li>
      </ul>
    </section>
  </div>

  <section class="resume-section" aria-labelledby="cv-skills">
    <h2 id="cv-skills">Technical Skills</h2>
    <dl class="resume-skills">
      <div>
        <dt>Programming &amp; Systems</dt>
        <dd>C++, Python, CUDA C++, Linux, MPI, Slurm</dd>
      </div>
      <div>
        <dt>AI Infrastructure &amp; Training</dt>
        <dd>Ascend 910C/950, CANN, FSDP2, MindSpeed MM, activation offloading, recomputation</dd>
      </div>
      <div>
        <dt>Distributed Performance</dt>
        <dd>HCCS, DMA, MS Insight, operator profiling, arithmetic-intensity analysis, compute/I/O/communication overlap</dd>
      </div>
      <div>
        <dt>Generative Models</dt>
        <dd>Diffusion, Flow Matching, Score Matching, image and video generation inference optimization</dd>
      </div>
      <div>
        <dt>Mathematics</dt>
        <dd>Linear algebra, numerical analysis, stochastic analysis, numerical PDEs, parallel algorithms, scientific computing</dd>
      </div>
      <div>
        <dt>Languages</dt>
        <dd>Chinese (native), English (CET-6)</dd>
      </div>
    </dl>
  </section>
</div>
