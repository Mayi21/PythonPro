# 获取CPU负载
cpu_load=$(top -bn1 | grep load | awk '{printf "%.2f%%\n", $(NF-2)}')

# 获取磁盘利用率
disk_usage=$(df -h | awk '$NF=="/"{printf "%s\n", $5}')

# 构造数据格式
data=$(echo '{"cpu_load": "'$cpu_load'", "disk_usage": "'$disk_usage'"}')

echo $data
#
## 上报到Kafka
#curl -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
#  --data "$data" \
#  http://<kafka_rest_proxy_host>:<port>/topics/<topic_name>