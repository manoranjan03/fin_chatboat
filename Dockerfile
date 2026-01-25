FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Create a start script to run both
RUN echo '#!/bin/bash\nuvicorn main_api:app --host 0.0.0.0 --port 8000 & streamlit run ui_app.py --server.port 8501 --server.address 0.0.0.0' > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]