# Use a single-stage build for simplicity with requirements.txt
FROM python:3.12-slim

# Set environment variables for a clean Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies using pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- CORRECTED SECTION ---
# Copy the contents of the src directory directly into the working directory
COPY src/ .

# Copy the FAISS index
COPY faiss_db/ ./faiss_db/

# Create a non-root user for improved security
RUN useradd --create-home --shell /bin/bash appuser
# Change ownership of the app directory to the new user
RUN chown -R appuser:appuser /app
# Switch to the non-root user
USER appuser

# Expose the port the app will run on to the outside world
EXPOSE 8080

# The command to run the application when the container starts
# This command will now work because the package is in the top-level directory
CMD ["uvicorn", "copilot_chatbot_rag_api.main:app", "--host", "0.0.0.0", "--port", "8080"]

