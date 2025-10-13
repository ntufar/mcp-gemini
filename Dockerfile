FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/

# Expose the port that the app runs on
EXPOSE 8000

# Set default environment variables (optional)
ENV MCP_SERVER_ROOT_DIR=/app

# Run the application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]