

- `diango-1.11.26` 基于 Python 3.7 和 Django 1.11.26 的博客源码
- `diango` 基于 Python 3.7 和 Django 2.2.8 的博客源码


  [点我进行 Django 博客预览](https://blog.zhwei.cn/)

  [管理后台](https://blog.zhwei.cn/administrator) 体验账号： test / djangotest

  
# 说明

`Django` 是使用 `Python` 编写的一个开源 `Web` 框架，采用 `MVC` 的软件设计模式，可以用它来快速搭建一个高性能的网站。

目前：

- 基于 `windows` 的 `Django 1.11` 开发，已完成
- 基于 `macOS  Catalina 10.15` 的 `Django2.2 LTS` 开发，已完成，由 `1.11` 升级并修改
- 模板：基于 `Bootstarp V4` 和 `jQuery` 的主题修改为所需模板，使用 `FBV`，这个改的太多了
- 模型：对 `ORM` 新的认识，优化需求，替换为 `MySQL` 
- 搜索：`django-haystack + whoosh + jieba` 分词的方案，解决中文问题 
- 翻页：基于模板语言和自定义标签解决文章删除id跳跃、首尾页显示问题
- 后台：由 `xadmin` 换为 `simpleui`，简单复写页面
- 部署： `docker + docker-compose` 容器化部署，自动备份
- 展望：评论功能， 缓存功能，第三方登录暂不提供，`django-restframework` + `Vue` 前后端分离开发方案，提供 `Restful API`

# docker环境
- 参考 [centos7 安装 docker-ce 和 docker-compose](https://blog.csdn.net/z_johnny/article/details/103616602)
- 参考 [Debian9 安装 docker-ce 和 docker-compose](https://blog.csdn.net/z_johnny/article/details/104842240)
- 参考 [Github Actions：云打包创建 docker 镜像](https://www.zhwei.cn/docker-build-image-github-actions/)

# 部署
## 下载
```bash
git clone https://github.com/hongweifuture/Django-Blog
```

## 运行 `django 2.2.8` （默认）
```bash
docker-compose up -d
```

## 运行 `django 1.11.26`

更改 
1. `docker-compose.yml` 中 `website` 的 `Docker Image` 标签版本号
2. 将 `diango-1.11.26` 文件夹改名为 `diango`， 原 `diango` 文件夹更名
```bash

...

  website:
    image: hwnet/hw-website:1.11.26
    container_name: hw_django
...

```
运行
```bash
docker-compose up -d
```
## 创建后台管理员
```bash
docker-compose run website python manage.py createsuperuser
```

## 停止
```bash
docker-compose down
```

# 备份
## 定时备份
```bash
sh migrate.sh -t "0 3 * * *"
```
## 手动备份
```bash
sh migrate.sh -b
```
## 手动清理
```bash
sh migrate.sh -c
```
# 恢复备份
```bash
sh migrate.sh -r *.sql.gz *.tar.gz
```

# 访问
## 首页
默认`port`为`9000`，如需`80`，请修改 `docker-compose.yml` 中 `nginx` 的宿主机映射端口
```bash
  ...
  
  nginx:
    ...
    ports:
      - "80:8000"
      
  ...
```
## 后台
```bash
IP:Port/administrator
```

# 参考
- 基于 Docker 的 Django 容器化部署之一：定制属于自己的 docker 镜像 [个人博客地址](https://www.zhwei.cn/django-docker-images) | [CSDN 博客地址](https://blog.csdn.net/z_johnny/article/details/104914845)
- 基于 Docker 的 Django 容器化部署之二：docker-compose 部署 Django 项目  [个人博客地址](https://www.zhwei.cn/django-docker-compose-deploy) | [CSDN 博客地址](https://blog.csdn.net/z_johnny/article/details/104914953)
- 基于 Docker 的 Django 容器化部署之三：定时备份，两步实现服务器迁移 [个人博客地址](https://www.zhwei.cn/django-docker-backup-restore) | [CSDN 博客地址](https://blog.csdn.net/z_johnny/article/details/104915016)


# 问题
Docker内网络或外网连接不上，请检查服务器的安全组或者防火墙
- 端口查询 [PostJson](http://coolaf.com/tool/port) 和 [站长工具](http://tool.chinaz.com/port/)

## 腾讯云设置安全组放行`9000`端口
- 入站规则，添加类型`自定义`，来源`all`，协议端口`TCP:9000`，策略`允许`，备注`django`
- [腾讯云安全组官方文档](https://cloud.tencent.com/document/product/213/34601)

## Google Cloud 需设置防火墙
- 放通内网
- 设置出入站规则

