FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y  libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx
# Install any dependencies in the requirements file
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt
# RUN pip uninstall -y opencv-python-headless opencv-python
CMD ["python", "consumer.py"]
EXPOSE 7127