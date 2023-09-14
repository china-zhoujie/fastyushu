# 基于Python 3.9的官方镜像
FROM bitnami/python:3.10.13-debian-11-r18

# 将当前目录下的所有文件复制到容器的/app目录下
RUN mkdir /app/fastyushu -p
COPY . /app/fastyushu

# 设置工作目录为/fastyushu
WORKDIR /app/fastyushu

# 安装Python依赖
RUN echo "deb https://mirrors.163.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
echo "deb-src https://mirrors.163.com/debian/ bullseye main non-free contrib" >> /etc/apt/sources.list && \
echo "deb https://mirrors.163.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
echo "deb-src https://mirrors.163.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
echo "deb https://mirrors.163.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
echo "deb-src https://mirrors.163.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
echo "deb https://mirrors.163.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list && \
echo "deb-src https://mirrors.163.com/debian/ bullseye-backports main non-free contrib" >> /etc/apt/sources.list
RUN apt-get update -y && apt-get install libffi-dev -y && pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements2.txt -i https://mirrors.aliyun.com/pypi/simple/

# 暴露容器的端口
EXPOSE 8888

# 启动Python应用
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8888"]
