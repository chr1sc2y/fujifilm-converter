[English Version](./README-EN.md)

# Fujifilm Converter

这个程序可以把 RAW/DNG 照片处理成 Lightroom 能识别的富士机型，从而选出富士的胶片模拟。

## 效果对比

| 原始效果 | 富士 NC 胶片模拟 |
| --- | --- |
| ![Sony PT Creative Style](./resources/DSC08427-sony.jpg) | ![Fujifilm NC Film Simulation](./resources/DSC08427-fuji.jpg) |
| ![Sony PT Creative Style](./resources/DSC08784-sony.jpg) | ![Fujifilm NC Film Simulation](./resources/DSC08784-fuji.jpg) |

## 三种使用方式

### 1. 本地执行

```sh
brew install exiftool dnglab
python3 -m pip install -e .
fuji-convert ./photos/  # ./photos/ 是存放 RAW 格式照片的目录
```

处理完成后，同目录下会生成修改过 EXIF 的 `.dng` 文件，直接拖进 Lightroom 就可以选富士胶片模拟。原始 RAW 文件默认会移动到同目录的 `originals/` 目录下。

### 2. Docker 执行

```sh
docker build -t fujifilm-converter .
docker run --rm -v "$PWD":/data -w /data fujifilm-converter ./photos/  # ./photos/ 是存放 RAW 格式照片的目录
```

### 3. 让 Agent 执行 Skill

```sh
npx skills@latest add chr1sc2y/fujifilm-film-sim-skill
```

然后直接对 Agent 说：

```text
使用 $unlock-fujifilm-film-simulations 处理 /Users/me/Pictures/trip。
```

Skill 仓库：[fujifilm-film-sim-skill](https://github.com/chr1sc2y/fujifilm-film-sim-skill)

目前主流程只推荐富士胶片模拟。不要期待通过改 EXIF 就一定能解锁其他品牌的预设，有些品牌在 Lightroom 里还有额外判断。

## 依赖

本地执行需要 Python 3.8+、[ExifTool](https://exiftool.org/) 和 [dnglab](https://github.com/dnglab/dnglab)。Docker 方式已经把 ExifTool 和 dnglab 放进镜像里。

## 说明

本项目是独立工具，和 Fujifilm、Adobe、Lightroom 都没有官方关系。最终显示哪些配置文件，取决于你的 Lightroom / Camera Raw 版本。
