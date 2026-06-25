# 贾的临时传输

一个无需登录的网页文件传输服务，支持文字实时同步和图片上传。

## 功能

- 实时文字同步（多端自动刷新）
- untitled-1: 图片粘贴上传（剪贴板图片自动识别，Ctrl+V/长按粘贴）
- 图片点击上传
- 多端实时同步（3秒轮询）
- 响应式布局，适配手机/电脑
- 白纸模式UI，无限延伸

## 快速开始

### Docker 部署

```bash
docker build -t upload-service .
docker run -d -p 5000:5000 -v $(pwd)/data:/data --name upload-service --restart unless-stopped upload-service
```

然后访问 `http://localhost:5000`

## 环境变量

- `DATA_DIR`: 数据存储目录，默认 `/data`

## 技术栈

- Python 3.11 + Flask
- 纯原生 JavaScript
- Docker
