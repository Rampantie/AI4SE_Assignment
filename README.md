# AI4SE_Assignment

## Photo Date Watermarker

**This program:**

1. 接受图像文件路径或目录路径作为输入
2. 使用piexif库提取EXIF日期信息
3. 支持通过命令行参数自定义字体大小、颜色及位置
4. 为目录内所有支持的图像添加日期水印
5. 将添加水印的图像保存至新子目录，文件名后缀为“_watermark”

**To use this program:**

安装必要的依赖：

```shell
pip install Pillow piexif
```

运行该程序的示例命令行输入: 

```shell
python main.py /path/to/images --font-size 100 --color white --position bottom-right
```

水印字号以像素为单位。

该程序支持常见图像格式（JPG、JPEG、PNG、TIFF），并将创建一个新目录，其中包含输入图片目录中所有图像的水印版本。

