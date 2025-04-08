#!/bin/bash

# 定义变量
PACKAGE_NAME="agent-plugin"
VERSION="1.0.0"
SOURCE_DIR="$(pwd)/.."  # 指向 /opt/agent-plugin
BUILD_DIR="$HOME/rpmbuild"
SPEC_FILE="agent.spec"
ARCHIVE_NAME="${PACKAGE_NAME}-${VERSION}.tar.gz"

# 调试：打印当前路径和 SOURCE_DIR
echo "Current directory: $(pwd)"
echo "Source directory: $SOURCE_DIR"

# 检查 SOURCE_DIR 是否正确包含所需文件
if [ ! -d "$SOURCE_DIR/src" ] || [ ! -d "$SOURCE_DIR/rpm" ]; then
    echo "Error: $SOURCE_DIR does not contain expected agent-plugin structure!"
    echo "Expected src/ and rpm/ directories in $SOURCE_DIR"
    exit 1
fi

# 确保 rpmdevtools 已安装
if ! rpm -q rpmdevtools > /dev/null 2>&1; then
    echo "Installing rpmdevtools..."
    sudo yum install -y rpmdevtools
fi

# 创建 RPM 构建目录结构
rpmdev-setuptree

# 打包源码为 tar.gz，指定顶级目录
echo "Creating source tarball..."
cd "$SOURCE_DIR" || exit
tar --exclude="rpm" \
    --exclude="logs" \
    -czf "$BUILD_DIR/SOURCES/$ARCHIVE_NAME" \
    -C "$SOURCE_DIR" \
    --transform "s,^\.,${PACKAGE_NAME}-${VERSION}," \
    .

# 检查 tarball 是否生成成功
if [ ! -f "$BUILD_DIR/SOURCES/$ARCHIVE_NAME" ]; then
    echo "Error: Failed to create tarball $ARCHIVE_NAME!"
    exit 1
fi

# 构建 RPM 包
echo "Building RPM package..."
rpmbuild -ba "$SOURCE_DIR/rpm/$SPEC_FILE"

# 检查构建结果
if [ $? -eq 0 ]; then
    echo "RPM package built successfully!"
    echo "Find it in $BUILD_DIR/RPMS/noarch/"
else
    echo "Failed to build RPM package."
    exit 1
fi