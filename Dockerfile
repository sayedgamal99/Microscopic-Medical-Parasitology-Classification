FROM tensorflow/tensorflow:latest-gpu
COPY models/model.keras /app/
COPY app.py /app/
WORKDIR /app
RUN pip install streamlit
CMD ["streamlit", "run", "app.py"]