
# 从仓库拉取 自己build的 带有 python 3.7 的 Alpine Linux 环境的镜像
FROM hwnet/django-blog:1.11.26

# 维护者信息
LABEL "author"="HONGWEI"
LABEL "blog"="https://www.zhwei.cn/"
LABEL "E-mail"="i@zhwei.cn"

# 构建参数，工作目录
ARG work_dir=/opt/hw-blog

RUN mkdir -p ${work_dir}
WORKDIR ${work_dir}

# 将当前目录复制到容器的工作目录
ADD ./django ${work_dir}

