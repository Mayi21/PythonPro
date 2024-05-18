#!/bin/bash

# 获取当前脚本所在目录的父目录

CUR_DIR=(`cd $(dirname "$0");pwd`)

SPEC_DIR=${CUR_DIR}/specs

PRO_DIR=(`dirname "${CUR_DIR}"`)


# 构建 RPM 包
rpmbuild -v -bb --define "_topdir ${SPEC_DIR}" --define "_pro_dir ${PRO_DIR}/agent" ${SPEC_DIR}/AgentClient.spec
