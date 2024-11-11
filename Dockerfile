FROM tensorflow/tensorflow:2.12.0

WORKDIR /app

COPY models /app/models
COPY app.py utils.py /app/
COPY data_samples /app/data_samples
COPY .streamlit /app/.streamlit

RUN pip install --no-cache-dir streamlit Pillow

# Expose Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]