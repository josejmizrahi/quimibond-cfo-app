# Quimibond CFO Dashboard - Backend
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Environment variables (override in docker-compose or .env)
ENV ODOO_URL=http://odoo:8069
ENV ODOO_DB=quimibond
ENV ODOO_USER=admin
ENV ODOO_PASSWORD=admin

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
