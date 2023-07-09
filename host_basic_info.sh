#!/bin/bash

function get_disk_usage_info() {
  # 执行df命令获取磁盘使用情况
  df_output=$(df -h)

  # 提取所需信息并打印
  echo "$df_output" | awk '{print "文件系统:", $1, "\n总容量:", $2, "\n已用:", $3, "\n可用:", $4, "\n使用率:", $5, "\n挂载点:", $6}'

}


function get_top_10_process() {
  # 执行top命令获取当前进程信息
  top_output=$(top -b -n 1 | tail -n +8 | head -n 10)
  # 打印进程信息
  echo "$top_output"
}

get_top_10_process