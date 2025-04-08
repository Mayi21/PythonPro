#!/bin/bash

# 定义变量
PACKAGE_NAME="agent-plugin"
VERSION="1.0.0"
SOURCE_DIR="../"
BUILD_DIR="$HOME/rpmbuild"
SPEC_FILE="agent.spec"
ARCHIVE_NAME="${PACKAGE_NAME}-${VERSION}.tar.gz"

# 确保 rpmdevtools 已安装
if ! rpm -q rpmdevtools > /dev/null 2>&1; then
    echo "Installing rpmdevtools..."
    sudo yum install -y rpmdevtools
fi

# 创建 RPM 构建目录结构
rpmdev-setuptree

# 打包源码为 tar.gz
echo "Creating source tarball..."
cd "$SOURCE_DIR" || exit
tar --exclude="$PACKAGE_NAME/rpm" \
    --exclude="$PACKAGE_NAME/logs" \
    -czf "$BUILD_DIR/SOURCES/$ARCHIVE_NAME" "$PACKAGE_NAME"

# 构建 RPM 包
echo "Building RPM package..."
rpmbuild -ba "$SOURCE_DIR/$PACKAGE_NAME/rpm/$SPEC_FILE"

# 检查构建结果
if [ $? -eq 0 ]; then
    echo "RPM package built successfully!"
    echo "Find it in $BUILD_DIR/RPMS/noarch/"
else
    echo "Failed to build RPM package."
    exit 1
fi