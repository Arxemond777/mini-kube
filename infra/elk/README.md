the login is "elastic"  
extract the pass "kubectl get secret elasticsearch-master-credentials -o go-template='{{.data.password | base64decode}}' -n elk"
# todo redo correspondingly what is above
the alternative way of extracting the pass "PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')"  


# attention: pay attention to http://localhost:5601/login?next=%2F must be http not httpS in your browser
https://github.com/LianDuanTrain/Helm3/blob/master/3%20Helm%20Deep%20Dive/3-12%20Use%20Helm%203%20to%20Install%20ELK%20Stack%20on%20MiniKube%20in%2010%20Mins.md


# todo describe how surren created the index
http://localhost:5601/app/home#/ > search > data views > create data view >   
name - anyname  
indexPattern - filebeat-*   

to check logs go to http://localhost:5601/app/home#/ > open ... > discover > in the search bar enter "service-name-p" and you'll see messages  

using the custom namespace
kubectl create namespace myapp; kubectl apply -f services/pong/pong-deployment.yaml -n myapp; kubectl apply -f services/pong/pong-service.yaml -n myapp; kubectl apply -f services/ping/ping-deployment.yaml -n myapp; kubectl apply -f services/ping/ping-service.yaml -n myapp



----
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm upgrade prometheus prometheus-community/prometheus --namespace monitoring -f infra/prometheus/values.yaml

helm upgrade prometheus prometheus-community/prometheus --namespace monitoring --set server.files.prometheusYaml=infra/prometheus/values.yaml


helm install grafana grafana/grafana --namespace monitoring
grafana
login: admin
pass: kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

kubectl port-forward -n monitoring deploy/prometheus-server 9090:9090
You can now access Prometheus at http://localhost:9090.

kubectl port-forward -n monitoring deploy/grafana 3000:3000
You can now access Grafana at http://localhost:3000.


monitoring > config maps > prometheus-server > edit
scrape_configs:
- job_name: prometheus
static_configs:
- targets:
- localhost:9090
- pong-service.myapp.svc.cluster.local:5001

and pod > prometheus-server > exec in the container > vim /etc/config/prometheus.yml edit
scrape_configs:
- job_name: prometheus
  static_configs:
- targets:
- localhost:9090
- pong-service.myapp.svc.cluster.local:5001

RELOAD the pod manually in pods just delete it