FROM tensorflow/tensorflow:2.12.0-gpu

COPY best_model_v2.keras /app/
COPY app.py utils.py /app/
COPY data_samples /app/data_samples
COPY .streamlit /app/.streamlit


WORKDIR /app
RUN pip install streamlit
CMD ["streamlit", "run", "app.py"]