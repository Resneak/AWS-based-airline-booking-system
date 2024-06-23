## Overview

This project is an enhanced cloud-based microservices application designed for an airline booking service. The application demonstrates the use of multiple microservices to manage different functionalities such as booking, flight management, notifications, and payments.

## Project Purpose

The purpose of this project is to showcase the implementation of a scalable and efficient microservices architecture using FastAPI, Docker, AWS ECS, and other cloud-based technologies. It is designed to provide a comprehensive example of how to build, deploy, and manage a microservices-based application in a cloud environment.

## Folder Structure

- **booking_service**: Handles booking-related operations. [API Documentation](http://18.219.238.65:80/docs)
- **flight_management_service**: Manages flight-related data and operations. [API Documentation](http://18.219.238.65:82/docs)
- **notification_service**: Sends notifications related to bookings and other events. [API Documentation](http://18.219.238.65:81/docs)
- **payment_service**: Manages payment processing and transactions. [API Documentation](http://18.219.238.65:84/docs)
- **cloudwatch-logs-policy.json**: Defines permissions for CloudWatch logs.
- **deploy.sh**: Script for pulling the latest changes from GitHub and deploying the Docker containers.
- **docker-compose.yml**: Docker Compose configuration file for setting up and running the microservices locally.
- **service-definition.json**: ECS service definition for deploying the services in AWS ECS.
- **sqs-policy.json**: Defines permissions for interacting with SQS.
- **task-definition.json**: ECS task definition for running the containers in AWS ECS.
- **ci-cd.yml**: GitHub Actions configuration for CI/CD pipeline.

## Getting Started

### Prerequisites

- Docker
- AWS CLI
- Git

### Installation

1. Clone the repository:
  
bash
  git clone https://github.com/your-username/enhanced-airline-booking-service.git
  cd enhanced-airline-booking-service


2. Build and run the services using Docker Compose:
  
bash
  docker-compose up --build


### Deployment

Use the deploy.sh script to deploy the latest changes:
bash
./deploy.sh


### API Documentation

Each service has its own API documentation available at the following URLs:
- [Booking Service API](http://18.219.238.65:80/docs)
- [Flight Management Service API](http://18.219.238.65:82/docs)
- [Notification Service API](http://18.219.238.65:81/docs)
- [Payment Service API](http://18.219.238.65:84/docs)

### Medium Article

[Medium Article](https://medium.com/@ndaniel275/improving-my-aws-cloud-based-airline-booking-service-from-prototype-to-production-c994bd578f0a)

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License
