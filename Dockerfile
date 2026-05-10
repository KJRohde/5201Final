# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies listed in requirements.txt
RUN pip install streamlit pandas confluent_kafka streamlit-oauth

# Copy the rest of your app code into the container
COPY . .

# Expose the default Streamlit port (8501)
EXPOSE 8501

# Command to run your app
# Replace 'your_app.py' with your main script name
ENTRYPOINT ["/bin/oauth2-proxy"]
