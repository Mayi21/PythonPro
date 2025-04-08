host_agent：使用fastapi实现的可以运行在虚拟机上的运维通道服务。服务相关配置包含config.json中，配置server地址和其他自定义属性，用于上报当前节点状态和健康信息。



增加支持打包为RPM包，USAGE：切换至rpm目录，执行./build.sh即可完成打包，执行rpm -ivh xxx.rpm包即可安装。安装后的目录位于/usr/local/agent目录下