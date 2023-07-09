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

