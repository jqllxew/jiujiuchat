FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# 软件包 | 作用 |
#|--------|------|
#| `build-essential` | 安装 GCC、g++、make 等工具，支持编译 Python C 扩展（如 `mysqlclient`、`numpy`、`pandas` 等依赖）。 |
#| `default-libmysqlclient-dev` | 安装用于 Python 操作 MySQL 的底层客户端库，`mysqlclient` 或 `SQLAlchemy + MySQL` 等库会依赖它。 |
#| `pkg-config` | 协助编译时找到系统安装的库路径，用于构建 C/C++ 扩展。 |
#| `netcat-traditional` | 提供 `nc` 命令，常用于网络调试、端口连通性检测（可在启动脚本中用来等待某个服务就绪）。 |
#- `rm -rf /var/lib/apt/lists/*`：清除缓存，减小镜像体积（是 Dockerfile 中常见的优化做法）。
RUN apt-get update && apt-get install -y \
  build-essential \
  default-libmysqlclient-dev \
  pkg-config \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# 为什么不直接 COPY . .
# 因为 Docker 构建镜像时，每一行 Dockerfile 都是一个 构建层（layer），只要那一层的上下文没有变动，就会使用缓存，而不是重新执行命令。
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy application files
COPY . .

# Set Python path and environment
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7667"]
