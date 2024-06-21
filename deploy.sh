#!/bin/bash

# Pull the latest changes from GitHub
cd /home/ec2-user/cloud-microservices-application-enhanced
git pull origin master

# Build and run Docker containers
docker-compose down
docker-compose build
docker-compose up -d
