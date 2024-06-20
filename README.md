# Backend Flask Application

Welcome to the backend Flask application that serves as the server for a frontend React application. Below is an overview of its architecture and functionality. This is the website for the entire application.

- Website: [https://www.manuelprojectsinaws.com/](https://www.manuelprojectsinaws.com/)

## Architecture Overview

### Deployment

The Flask application is hosted on an EC2 instance within AWS. Deployment to this instance is managed by ECS (Elastic Container Service). Each new commit to the master branch triggers deployment via a Task Definition controlled by an ECS Service in an Docker image in the ECR. Integration with a Virtual Private Cloud (VPC) ensures security by isolating resources within a defined virtual network. Access controls are governed by security groups. The instance is mapped with Route53 for amore accesible address.

### Load Balancing

Incoming requests are routed through an Application Load Balancer (ALB). This ALB efficiently distributes traffic across the ECS cluster and monitors the health of underlying instances. Requests are forwarded to the appropriate target group associated with the ECS service, ensuring optimal service availability.

### Database

The application uses PostgreSQL as its database management system. It includes two models (ORM) that serve as tables in the database.

## Functionality

The Flask application exposes a set of APIs to interact with the frontend React application:

1. **`/login`**: Handles user login authentication.
2. **`/register`**: Manages user registration.
3. **`/contacts`**: Retrieves contacts based on the logged-in user.
4. **`/create_contact`**: Creates new contacts for the logged-in user.
5. **`/update_contact/<int:contact_id>`**: Updates existing contacts for the logged-in user.
6. **`/delete_contact/<int:contact_id>`**: Deletes contacts for the logged-in user.

These APIs facilitate basic CRUD operations for managing contacts in the database.

## Links

- Frontend React Application:
  - GitHub Repository: [https://github.com/mcabreraf/demoapp-frontend-react](https://github.com/mcabreraf/demoapp-frontend-react)
  

This Flask application serves as a foundational backend service, exploring Flask's capabilities within an AWS architecture setup.