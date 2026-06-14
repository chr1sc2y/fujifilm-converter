[English Version](./README-EN.md)

# Fujifilm Converter

这个程序可以把任意相机拍出来的 raw 格式照片通过修改 exif 信息的方式模拟成富士相机拍的, 从而在 lightroom 里面选出富士的胶片模拟。

## 使用方法

第一步，安装 ExifTool：

```sh
brew install exiftool
```

第二步，安装本工具：

```sh
pip install -e .
```

或者使用 pipx：

```sh
pipx install -e .
```

使用方法：

直接运行转换（默认使用富士预设）：

```sh
fuji-convert ./photos/
```

指定其他预设：

```sh
fuji-convert --preset hasselblad ./photos/
fuji-convert --preset leica ./photos/
```

检查环境：

```sh
fuji-convert --check
```

Docker 使用方式：

```sh
docker build -t fujifilm-converter .

docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

处理完成后，同目录下得到修改过 EXIF 的 .dng 文件，可直接拖进 Lightroom。原始 RAW 文件移到同目录的 originals/ 文件夹。

使用 Agent 时，直接把这个仓库的链接发给它，它就可以执行转换。

## 效果对比

- 索尼 PT 创意外观

![5](./resources/DSC08427-sony.jpg)

- 富士 NC 胶片模拟

![6](./resources/DSC08427-fuji.jpg)

- 索尼 PT 创意外观

![new-sony](./resources/DSC08784-sony.jpg)

- 富士 NC 胶片模拟

![new-fuji](./resources/DSC08784-fuji.jpg)
