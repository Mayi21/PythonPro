#!/bin/bash

# -------------------------------
# 一键 YUM 源搭建脚本（基于 nginx）
# -------------------------------

# 目录和路径
REPO_DIR="/var/www/html/myrepo"
REPO_NAME="myrepo"
NGINX_CONF="/etc/nginx/conf.d/${REPO_NAME}.conf"

# 安装 nginx 和 createrepo
echo "🚀 安装 nginx 和 createrepo..."
yum install -y nginx createrepo_c || {
    echo "❌ 安装失败，请检查 YUM 源连接"
    exit 1
}

# 创建 YUM 源目录
echo "📁 创建 YUM 源目录：$REPO_DIR"
mkdir -p "$REPO_DIR"

# （可选）复制 RPM 包进来（你可以取消注释后使用）
# echo "📦 复制 RPM 包到仓库"
# cp /path/to/your/*.rpm "$REPO_DIR"

# 生成索引
echo "🔄 生成 repodata 索引"
createrepo_c "$REPO_DIR"

# 配置 nginx 虚拟主机
echo "🌐 配置 nginx 发布路径：$NGINX_CONF"
mkdir -p /etc/nginx/conf.d
cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name localhost;

    location /$REPO_NAME/ {
        autoindex on;
        alias $REPO_DIR/;
    }
}
EOF

# 启动 nginx 并设置开机启动
echo "🚦 启动 nginx 服务"
systemctl enable nginx
systemctl restart nginx

echo "✅ YUM 源已准备完成！"
echo "👉 请访问： http://$(hostname -I | awk '{print $1}')/${REPO_NAME}/"
echo
echo "🔧 客户端配置示例："
echo "----------------------------------"
echo "[${REPO_NAME}]"
echo "name=My Local Repo"
echo "baseurl=http://$(hostname -I | awk '{print $1}')/${REPO_NAME}/"
echo "enabled=1"
echo "gpgcheck=0"
echo "----------------------------------"

# 机器重启后如果发现只能看到目录无法看到文件，首先查看nginx的日志：tail -f /var/log/nginx/error.log
# 一般是因为文件属组（概率很小），或者是SELinux（大概率）
## 使用 setenforce 0 临时设置为 Permissive 模式（重启后恢复）
## 完全禁用：编辑 /etc/selinux/config，修改：SELINUX=disabled
