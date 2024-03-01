# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory to /app
WORKDIR /app

# Set a static IP address
ENV STATIC_IP 172.18.0.2

# Copy the current directory contents into the container at /app
COPY ./app-data/ /app

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install Flask and any other needed packages specified in requirements.txt
RUN pip install Flask Flask-MySQLdb Flask-Login Flask-Bcrypt Flask-SQLAlchemy

# Expose port 5000 to the outside world
EXPOSE 5000

# # Configure the network with the static IP
# RUN echo "auto eth0" >> /etc/network/interfaces && \
#     echo "iface eth0 inet static" >> /etc/network/interfaces && \
#     echo "    address $STATIC_IP" >> /etc/network/interfaces

# Run app.py when the container launches
CMD ["python", "chat-bot-api.py"]