# PythonPro
a daily usage on my python life
## agent router
agent.py usage: python agent.py -s <BOOTSTRAP_SERVERS>, 
then you can send command to topic and client 
will receive then execute. 
wait three seconds or long time.
the result of command will send to other topic.  
timed task can use producer-consumer.
use socket method for this scene.  
or use web application. start web server in client.
register web info on server in start up.  
then we know those server online.  
and server can use some health probe to monitor agent status.  

i think can use fastapi in client, and use django in server  
don't operate anything, just report system info  
and server easy implment anything use django  


schedule task to get vm info  

## implement health monitor

use django-apscheduler implement timely task  
Q. restart django server and will start new schedule task. it's name like before task.  
A. remove schedule task when restart server  

Q. can't import module from other dir  
A. move cron_task and wsgj file in one folder  

## instance metrics
cpu_usage,disk_usage,collect_time, use echarts to display these data  
use echarts to display data  



## kafka-rest-proxy  
can't use kafka-rest-proxy in these dockers. maybe will change docker instance in the future 

basic info
![img.png](md_image/img.png)


# Kafka Cluster
use `docker/docker-compose.yaml` fast build zk and kafka cluster then use `docker-compose up` run kafka cluster

# Develope Guide
## Project Folder
* shell  
  shell file to collect host info
* md_image  
  image about markdown document 
* docker  
  compose file about docker
* agentserver  
  a django project as server, interact with database and kafka
* backend  
  fastapi project and use in client. aim to fast and lightweight build app.  
* 