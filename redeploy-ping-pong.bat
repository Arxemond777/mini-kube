@echo off

:: build
docker build -t ping-service .\services\ping
docker tag ping-service:latest arxemond777/ping-service:latest
docker push arxemond777/ping-service:latest
docker build -t pong-service .\services\pong
docker tag pong-service:latest arxemond777/pong-service:latest
docker push arxemond777/pong-service:latest

:: Sleep for 1 second
timeout /t 1 /nobreak >nul

:: delete current deployments
kubectl delete -n myapp deployment ping-deployment --force --grace-period=0
kubectl delete service ping-service -n myapp
kubectl delete -n myapp deployment pong-deployment --force --grace-period=0
kubectl delete service pong-service -n myapp

:: Sleep for 2 seconds
timeout /t 2 /nobreak >nul

:: roll out new
kubectl create namespace myapp
kubectl apply -f services\pong\pong-deployment.yaml -n myapp
kubectl apply -f services\pong\pong-service.yaml -n myapp
kubectl apply -f services\ping\ping-deployment.yaml -n myapp
kubectl apply -f services\ping\ping-service.yaml -n myapp
