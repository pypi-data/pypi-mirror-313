# OpenI

> PYPI package for 启智 AI 协作平台。

## 安装

_适配 python3.8 及以上版本_

```bash
pip install openi
```

## 功能介绍

- 支持进行本地上传与下载文件到启智社区
- 支持代码调用函数，可在本地Python脚本或notebook使用；支持终端命令行，方便在服务器上使用。
- 具体请参考 [帮助文档](https://openi.pcl.ac.cn/docs/index.html#/api/intro)

## 使用示例
- `python` 代码中下载 [MNIST示例数据集](https://openi.pcl.ac.cn/OpenIOSSG/OpenI_Cloudbrain_Example/datasets) 为例：

```python
# 可复制到 python 文件中直接运行，函数的返回值为下载文件的本地保存路径
from openi import download_file
path = download_file(
    file="MnistDataset_mindspore.zip",
    repo_id="OpenIOSSG/OpenI_Cloudbrain_Example",
)
```

- 上述代码调用对应的终端命令（可直接复制到终端命令行中运行）

```bash
openi dataset download MnistDataset_mindspore.zip OpenIOSSG/OpenI_Cloudbrain_Example
```

- 执行结果，显示下载进度条与本地保存路径
```bash
✅ MnistDataset_mindspore.zip: 100%|██████████████████████████████████████████████| 10.3M/10.3M [00:00<00:00, 24.7MB/s]
文件已下载到: D:\MnistDataset_mindspore.zip
```

- 更多使用指南请参考 [帮助文档](https://openi.pcl.ac.cn/docs/index.html#/api/intro)