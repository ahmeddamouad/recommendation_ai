# Use official Python image

FROM python:3.11-slim

# Install Tkinter and system dependencies
RUN apt-get update && \
	apt-get install -y python3-tk tk libtk8.6 libtcl8.6 && \
	rm -rf /var/lib/apt/lists/*

# Set working directory to project root
WORKDIR /Recommendation_IA

# Copy all project files and folders
COPY . /Recommendation_IA

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi



# Expose Flask port
EXPOSE 5000

# Run Flask web app
CMD ["python", "web_app.py"]
