[English Version](./README-EN.md)

# Fujifilm Converter

这个程序可以把任意相机拍出来的 raw 格式照片通过修改 exif 信息的方式模拟成富士相机拍的, 从而在 lightroom 里面选出富士的胶片模拟。

## 使用方法

1. 安装 ExifTool
```sh
brew install exiftool
```

2. 安装本工具

```sh
pip install -e .
```

或者

```sh
pipx install -e .
```

3. 直接运行

```sh
fuji-convert ~/Downloads/temp/ # the directory including your raw files
```

处理完成后，同目录下会生成修改过 EXIF 的 .dng 文件，直接拖进 Lightroom 就可以选出富士的胶片模拟预设。原始 RAW 文件会移动到同目录的 originals/ 目录下。

也可以直接把仓库链接丢给 agent 执行。

### Docker 启动方式

```sh
docker build -t fujifilm-converter .
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

## 效果对比

- 索尼 PT 创意外观

![5](./resources/DSC08427-sony.jpg)

- 富士 NC 胶片模拟

![6](./resources/DSC08427-fuji.jpg)

- 索尼 PT 创意外观

![new-sony](./resources/DSC08784-sony.jpg)

- 富士 NC 胶片模拟

![new-fuji](./resources/DSC08784-fuji.jpg)
