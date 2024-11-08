import os
import streamlit as st
import pickle
import numpy as np
from tensorflow.keras.models import load_model, save_model
from sklearn.preprocessing import MinMaxScaler
import tempfile

# Fungsi untuk menyimpan scaler
@st.cache
def save_scaler(data):
    scaler = MinMaxScaler()
    scaler.fit(data)

    # Menggunakan direktori sementara
    temp_dir = tempfile.gettempdir()
    scaler_path = os.path.join(temp_dir, 'scaler.pkl')

    # Simpan scaler
    with open(scaler_path, 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)

    return scaler_path  # Kembalikan jalur scaler yang disimpan

# Fungsi untuk menyimpan model LSTM
def save_lstm_model(model):
    temp_dir = tempfile.gettempdir()
    model_path = os.path.join(temp_dir, 'lstm_model.h5')
    save_model(model, model_path)
    return model_path

# Fungsi untuk memuat model LSTM, SVM, dan Scaler
@st.cache
def load_models():
    lstm_model = None
    svm_classifier = None
    scaler = None
    error_message = None

    # Cek keberadaan file model LSTM
    lstm_model_path = os.path.join(tempfile.gettempdir(), 'lstm_model.h5')
    if not os.path.exists(lstm_model_path):
        error_message = f"LSTM model file not found at {lstm_model_path}"
        return lstm_model, svm_classifier, scaler, error_message

    try:
        lstm_model = load_model(lstm_model_path)
    except Exception as e:
        error_message = f"Error loading LSTM model: {e}"
    
    # Cek keberadaan file SVM
    svm_model_path = os.path.join(tempfile.gettempdir(), 'svm_classifier.pkl')
    if not os.path.exists(svm_model_path):
        error_message = f"SVM model file not found at {svm_model_path}"
        return lstm_model, svm_classifier, scaler, error_message

    try:
        with open(svm_model_path, 'rb') as svm_file:
            svm_classifier = pickle.load(svm_file)
    except Exception as e:
        error_message = f"Error loading SVM model: {e}"
    
    # Cek keberadaan file scaler
    scaler_path = os.path.join(tempfile.gettempdir(), 'scaler.pkl')
    if not os.path.exists(scaler_path):
        error_message = f"Scaler file not found at {scaler_path}"
        return lstm_model, svm_classifier, scaler, error_message

    try:
        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
    except Exception as e:
        error_message = f"Error loading scaler: {e}"

    return lstm_model, svm_classifier, scaler, error_message

# Menyimpan scaler jika diperlukan (gunakan data Anda sendiri untuk fit scaler)
data = np.random.rand(100, 6)  # Contoh data, ganti dengan data aktual Anda
scaler_path = save_scaler(data)

# Tampilkan pesan sukses setelah menyimpan scaler
st.success("Scaler saved successfully!")

# Memuat model LSTM, SVM, dan Scaler
lstm_model, svm_classifier, scaler, error_message = load_models()

# Jika ada pesan kesalahan, tampilkan dan hentikan eksekusi lebih lanjut
if error_message:
    st.error(error_message)
   