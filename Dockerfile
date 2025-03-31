# 使用Python官方镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录和环境变量
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    python3-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件并安装依赖
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir Pillow

# 删除旧的数据库文件
RUN rm -f db.sqlite3
# 创建目录并执行 Django 命令

RUN mkdir -p static staticfiles \
    && python manage.py migrate \
    && python manage.py init_admin \
    && python manage.py collectstatic --noinput

# 暴露端口并启动
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
