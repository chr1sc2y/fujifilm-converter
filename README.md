[English Version](./README-EN.md) — English is the default / reference version of the documentation and skill definition.

# Fujifilm Converter

（命令行工具简称为 `fuji-convert` 或 `fujifilm-convert`，方便使用）

**注意**：本文档提供了中英文内容，但**默认以英文版本为准**（包括 skill 定义）。英文 README 包含最完整的使用说明。

这个程序可以通过修改 EXIF 的方式，把任意相机拍的 RAW/DNG 伪装成富士、哈苏、徕卡或其他任何相机的文件，让 Lightroom 以为它来自目标相机，从而解锁对应的相机配置文件和胶片模拟。

支持预设，也支持完全自定义任意厂商的 Make / Model / Unique Camera Model。

## 效果对比

### 示例 1

- 索尼 PT 创意外观

![5](./resources/DSC08427-sony.jpg)

- 富士 NC 胶片模拟

![6](./resources/DSC08427-fuji.jpg)

### 示例 2

- 索尼风格（转换前）

![new-sony](./resources/DSC08784-sony.jpg)

- 富士风格（转换后）

![new-fuji](./resources/DSC08784-fuji.jpg)

## 快速开始（解放双手）

**Docker 方式（想零依赖时推荐，两条命令）**

```sh
# 第 1 条命令：构建一次镜像（里面已经打包好了 exiftool + dnglab + 转换工具）
docker build -t fujifilm-converter .

# 第 2 条命令：扔照片进去处理（之后每次跑照片只用这一条）
docker run --rm -v "$(pwd)":/data -w /data fujifilm-converter ./photos/
```

（日常人类使用更推荐安装后直接用一条命令 `fuji-convert`，见上文“一 行命令跑完整流程”部分。）

处理完成后，修改过的 `.dng` 直接出现在你本地的 `./photos/`（或你指定的目录）里，可以直接丢进 Lightroom。

**归档说明（已大幅改进，只有一个目录）**：
- 默认只把**原始相机 RAW 文件**移动到同目录下的 `originals/` 文件夹。
- exiftool 默认使用 `-overwrite_original`，不会再额外生成一个 `archived/` 目录（以前常见的两个 Archive 目录混乱问题已解决）。

## 人类执行：一行命令跑完整流程

完成一次性的系统依赖安装（exiftool + dnglab 或 Adobe DNG Converter）和本工具安装后，**整个流程**（RAW 转 DNG + EXIF 修改 + 安全归档原文件）只需要**一条命令**：

```sh
fuji-convert ./你的照片文件夹/
fuji-convert --preset hasselblad /path/to/raws
fuji-convert --preset fujifilm ./photos/
```

这是人类日常使用的最推荐方式。

**零永久安装的一行命令**（适合偶尔使用）：

```sh
pipx run --spec "git+https://github.com/zintrulcre/fujifilm-converter.git" fuji-convert --preset fuji ./photos/
```

（你仍然需要在系统上一次性安装 `exiftool` 和 dnglab / Adobe DNG Converter。）

## Agent / Grok 使用方式（Skill）

本仓库同时提供了官方的 Grok skill，方便 Agent 直接读取并执行转换流程。

**Skill 位置（项目范围）：**  
`.grok/skills/fuji-convert/SKILL.md`

Skill 定义**默认使用英文**（这是参考版本）。它包含清晰可执行的指令，告诉 Agent：

- 什么时候触发（用户说 “make it Fuji”、“convert to Hasselblad”、“fujify these”、“解锁胶片模拟”等）。
- 如何选择正确的 `--preset`（支持丰富的别名：fuji、fujifilm、hasselblad、hassel、hassy、哈苏 等）。
- 如何使用**一行命令完整流程**运行 `fuji-convert`（或回退到 Docker 方式）。
- 如何处理用户的首次安装。
- 运行后应该如何反馈结果。

**对 Agent 的建议**：当用户提供照片路径并希望进行相机模拟 / 胶片模拟时，优先加载并遵循 `fuji-convert` skill。Skill 文件会告诉你具体要执行的终端命令以及预期行为。

这样人类（简单 CLI 一条命令）和 Agent（结构化的 skill + 直接执行指导）都能得到很好的支持。

**本地安装方式（macOS / Linux 用户，一次配置，之后一条命令）**

1. 用系统包管理器安装外部依赖（必须）：
   - macOS（推荐用 Homebrew）：
     ```sh
     brew install exiftool dnglab
     ```
   - Ubuntu / Debian：
     ```sh
     sudo apt update && sudo apt install -y exiftool
     # dnglab 用下面这行直接装最新版二进制（免编译）
     curl -fsSL -o /tmp/dnglab https://github.com/dnglab/dnglab/releases/latest/download/dnglab_linux_x64 && \
       sudo install -m 755 /tmp/dnglab /usr/local/bin/dnglab
     ```

2. 安装本工具（会获得 `fuji-convert` 和 `fujifilm-convert` 两个命令）。

**推荐方式：使用 pipx（最干净，无需每次激活 venv）**

```sh
pipx install -e .
```

**推荐方式二：在 macOS 上使用虚拟环境（避免系统 Python 权限问题）**

```sh
cd /Users/zintrulcre/repo/fujifilm-converter

# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 先升级 pip（你的系统 pip 很可能太旧，导致现代 pyproject.toml editable 安装失败）
python -m pip install --upgrade pip

# 再安装
pip install -e .
```

**遇到老 pip 报错时的快速修复（"editable mode currently requires a setuptools-based build"）**

```sh
cd /Users/zintrulcre/repo/fujifilm-converter

# 为老版本 pip 创建一个极简 setup.py
cat > setup.py << 'EOF'
from setuptools import setup
if __name__ == "__main__":
    setup()
EOF

python3 -m pip install --upgrade pip
python3 -m pip install -e . --user
```

安装完成后就可以直接运行（默认富士预设）：

```sh
fuji-convert ./photos/
fuji-convert --list-presets
fuji-convert --check
```

> 提示：直接从源码跑依然有效：`python3 process.py ./photos/`

更多示例见上文“一 行命令跑完整流程”。

### 支持的预设（现在非常简单）

你**只需要**输入类似下面这些就够了，工具会自动用固定好的配置，保证 Lightroom 能直接认出并提供对应配置文件/胶片模拟：

```sh
fuji-convert --preset fuji ./photos/          # 或者 fujifilm、fuji film
fuji-convert --preset hasselblad ./photos/    # 或者 hassel、hassy、hass、哈苏
fuji-convert --preset hassel ./photos/
fuji-convert --preset leica ./photos/
```

运行 `fuji-convert --list-presets` 可以看到所有支持的简单名字和它们对应的固定配置。

我们故意只提供几个固定的、经过验证的配置（Make + Model + UniqueCameraModel），这样用户不用操心具体机身和镜头型号，Lightroom 就能直接显示对应的选项。

只有极少数高级用户才需要用 `--make` / `--model` / `--uniquecameramodel` 那三个参数（我们已经在帮助里标成 ADVANCED 了）。正常情况完全不需要。

处理完成后:
- 同目录下得到修改过 EXIF 的 `.dng` 文件（可直接拖进 Lightroom 使用目标相机的配置文件）
- 原始 RAW 文件移到同目录的 `originals/` 文件夹（默认只这一个归档目录）
- 使用 `--keep-exif-backup` 才会产生额外的 exiftool 备份目录（极少需要）

### 手动分步（旧流程，已不推荐）

早期版本需要手动分步：用 Adobe DNG Converter 将 RAW 转为 DNG，再运行 `python3 fuji.py` 输入目录让 exiftool 修改 EXIF，最后拖进 Lightroom。

详细截图和步骤已移至历史归档（见 git 历史或 resources/ 下的旧图片）。现在推荐直接用 `fuji-convert` 一条命令完成全部流程。
