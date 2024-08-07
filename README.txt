

#!/bin/bash

# 


cd /app
# -v $HOME/path/config.yml: /app/config.yml, or edit config/config.yml
python3 -W ignore conn_oracle.py
python3 -W ignore conn_postgresql.py
python3 -W ignore conn_redis.py
python3 -W ignore conn_elasticsearch.py
python3 -W ignore conn_ecuat2.py
python3 -W ignore conn_kafkacdc.py
python3 -W ignore conn_ecuat2_update.py
while true; do p conn_ecuat2_update.py; sleep 10; done

#

python:3.9.6 with db connect test tools

docker build . -t jiechau/python:3.9 -t jiechau/python:latest -t jiechau/python
docker push jiechau/python
docker push jiechau/python:3.9

docker run -it --rm jiechau/python
docker run -it --rm registry.gitlab.com/jiechau/python
docker run -it --rm ghcr.io/jiechau/python
kubectl run my-shell -it --rm -n aiapi --image jiechau/python -- bash
kubectl run my-shell -it --rm -n aiapi --image registry.gitlab.com/jiechau/python -- bash
kubectl run my-shell -it --rm -n aiapi --image ghcr.io/jiechau/python -- bash

# or use a dummy command: ["/bin/bash", "-c", "tail -f /dev/null"]
kubectl apply -f pod_python.yaml -n aiapi
# or
kubectl apply -f https://gitlab.com/jiechau/python/-/raw/main/pod_python.yaml -n aiapi

# pod_python.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-shell
  namespace: aiapi
spec:
  containers:
  - name: my-shell
    image: jiechau/python
    #command: ["/bin/bash"]
    command: ["/bin/bash", "-c", "tail -f /dev/null"]
    imagePullPolicy: Always


# oracle
export ORACLE_HOME=/app/oracle_tools/instantclient
export TNS_ADMIN=/app/oracle_tools/instantclient
export LD_LIBRARY_PATH=/app/oracle_tools/instantclient:$LD_LIBRARY_PATH


# misc

# use host network
docker run --network host -it -v $HOME/ai_codes/fastapi-vm/service/config:/app/config jiechau/python
# cdc test
while true; do echo $(date +'%Y/%m/%d %H:%M:%S') $(p -W ignore conn_postgresql.py); echo $(date +'%Y/%m/%d %H:%M:%S') $(p -W ignore conn_ecuat2_update.py); sleep 60; done
