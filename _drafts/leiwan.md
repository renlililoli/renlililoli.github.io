---
title: "LEIWAN"
collection: essays
type: "Essay"
permalink: /essays/leiwan
date: 2025-05-14
excerpt: '关于LEIWAN的一些简介'
location: "Shanghi, China"
---

## Intro

`LEIWAN` (レイワン)  是成立于 2018 年的偶像团体. 她们最早使用 `AIQ` 的名号活动, 后于 2018 年 12 月停止活动. 此后于 2019 年初以 `Terror Rhythmn` (テロリズムン) 的名称从新出道. 在此后不久, 便更名为 `LEIWAN`.

`LEIWAN` 名称的由来为日本于 2019 年更改的年号 `令和 (Reiwa)`.

## Member

### `AIQ` 时期

- Futaba Momo (双葉モモ) (Original Member; Withdrew August 2018)
- Shion Rina (紫音リナ) (Original Member; Withdrew August 2018)
- Saki Scream (サキ・スクリーム) (Original Member; Graduated December 2018)
  
### `LEIWAN` 时期

- Anaru Rairai (愛成来来) (Joined November 4, 2022; Training ended November 13, 2022; Temporary Member)
- **<span style="color:yellow;">Yellow</span>**: [Kuroi Mashiro](#) 黒井マシロ (Original Member; Withdrew April 1, 2023)
- **<span style="color:purple;">Purple</span>**: [Nekono Nemuko](#) 猫乃ねむ子 (Joined August 2018; Graduated June 11, 2024)
  
### `现体制`

- **<span style="color:blue;">Blue</span>**: [Mio Monster](https://x.com/Mio_monster) 澪・モンスター (Joined February 2019)
- **<span style="color:pink;">Pink</span>**: [Uzuki Ayaka](https://x.com/Uzuki_megane) 卯月彩華 (Joined February 2019; Leader)
- **<span style="color:green;">Green</span>**: [Aguri Pico](https://x.com/aguri_pico) あぐりぴこ (Joined July 4, 2023)
- **<span style="color:red;">Red</span>**: [Shibuya Ryuka](https://x.com/Shibuya_ryuka) 渋谷龍華 (Joined July 4, 2023)
  
### TimeLine

![TimeLine](./images/leiwan/leiwan_timeline.svg)

### Gallery

<style>
  .gallery-container {
    position: relative;
    max-width: 600px;
    margin: auto;
  }

  .gallery-image {
    display: none;
    width: 100%;
  }

  .active {
    display: block;
  }

  .nav-buttons {
    text-align: center;
    margin-top: 10px;
  }

  .nav-buttons button {
    padding: 5px 10px;
    font-size: 16px;
  }
</style>

<div class="gallery-container">
  <img class="gallery-image" src="./images/leiwan/2025.jpg" alt="2025">
  <img class="gallery-image" src="./images/leiwan/2023l.png" alt="2023-late">
  <img class="gallery-image" src="./images/leiwan/2023e.jpg" alt="2023-early">
  <img class="gallery-image" src="./images/leiwan/2021.png" alt="2021">
  <img class="gallery-image active" src="./images/leiwan/2020e.jpg" alt="2020-early">
  <img class="gallery-image" src="./images/leiwan/2020l.png" alt="2020-late">
</div>

<div class="nav-buttons">
  <button onclick="prevImage()"><</button>
  <button onclick="nextImage()">></button>
</div>

<script>
  let currentIndex = 0;
  const images = document.querySelectorAll('.gallery-image');

  function showImage(index) {
    images.forEach((img, i) => {
      img.classList.toggle('active', i === index);
    });
  }

  function nextImage() {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
  }

  function prevImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
  }
</script>

## 
