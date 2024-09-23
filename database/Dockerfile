# Use the official MySQL image as a base image
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_DATABASE=chatbot
ENV MYSQL_PASSWORD=1234

# Set a static IP address
ENV STATIC_IP 172.18.0.3

# Set the working directory to /app
WORKDIR /app

# Copy SQL script to initialize the database
COPY ./scripts/ /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306
