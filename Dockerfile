# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Install system dependencies required by Prophet & LightGBM
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port Streamlit uses
EXPOSE 8080

# 7. Run the app (Cloud Run provides a $PORT environment variable)
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0"]