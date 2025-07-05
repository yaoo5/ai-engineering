# 使用官方支持的 Ubuntu 22.04
FROM ubuntu:22.04

# 设置非交互模式（避免apt安装卡住）
ENV DEBIAN_FRONTEND=noninteractive

# 更新系统并安装基础工具
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    # Playwright 所需依赖
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm-dev \
    libxkbcommon0 \
    libgbm-dev \
    libasound2 \
    libatspi2.0-0 \
    libxcomposite1

# 安装 Python 依赖
RUN pip3 install requests beautifulsoup4 playwright

# 安装 Playwright 浏览器（使用官方兼容版本）
RUN playwright install chromium --with-deps

# 验证安装
CMD ["python3", "-c", "import playwright; print('Playwright name is:', playwright.__name__)"]