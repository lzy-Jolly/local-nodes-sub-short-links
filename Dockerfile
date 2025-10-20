# 极简镜像
FROM alpine:3.20

# 设置工作目录
WORKDIR /app

# 复制编译好的二进制
COPY sub_server /app/sub_server

# 默认环境变量
ENV PORT=10096 \
    NODE_FILE=/app/merged_nodes.txt \
    CONVERTER_URL=http://192.168.20.237:15400/sub? \
    CONFIG_URL=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_NoAuto.ini

# 暴露端口
EXPOSE ${PORT}
# 启动服务
CMD ["/app/sub_server"]