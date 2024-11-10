# for the local run
'pip install flask requests'
or explicitly 
'python3.11 -m pip install flask requests'

# install minikube on windows https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download

run pover shell as admin

Download and run the installer for the latest release.
Or if using PowerShell, use this command:

`New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing`

Add the minikube.exe binary to your PATH.
Make sure to run PowerShell as Administrator.

`$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
[Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}`

# run minikube
docker context use default
minikube start --driver=docker
minikube status
minikube dashboard

# build artifacts (for publishing read how to publish them in artifactory)
powerschell (troubleshooting for using locally built images in minikube) > minikube -p minikube docker-env | Invoke-Expression

or in my repo

docker build -t pong-service .\services\pong\.
docker tag pong-service:latest arxemond777/pong-service:latest
docker push arxemond777/pong-service:latest
kubectl apply -f services/pong/pong-deployment.yaml

docker build -t ping-service .\services\ping
docker tag ping-service:latest arxemond777/ping-service:latest
docker push arxemond777/ping-service:latest


## ping-deployment.yaml & pong-deployment.yaml - are Kubernetes deployment YAML files
## ping-service.yaml & pong-service.yaml - for network detecting, load balancing, pod discovery
kubectl apply -f services/pong/pong-deployment.yaml
kubectl apply -f services/pong/pong-service.yaml
kubectl apply -f services/ping/ping-deployment.yaml
kubectl apply -f services/ping/ping-service.yaml

### if needs to remove
kubectl delete deployment pong-deployment













