# Core Pkgs
import streamlit as st
import sklearn
import joblib,os
import numpy as np 

# Loading Models
def load_prediction_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

def calculate_period(year, month, start_year=2022):
    period = ((year - start_year) * 12 + month)
    return period

def main():
	"""Regresi Linier Sederhana"""
	st.title("Prediksi Harga Emas Dunia (USD)")
	tahun = st.pills("Pilih Tahun",options=list(range(2026, 2031)), default=2026)
	bulan_dict = {"Januari": 1,"Februari": 2,"Maret": 3,"April": 4,"Mei": 5,"Juni": 6,"Juli": 7,"Agustus": 8,"September": 9,"Oktober": 10,"November": 11,"Desember": 12}
	bulan_nama = st.select_slider("Pilih Bulan",options=list(bulan_dict.keys()),value="Agustus")
	bulan = bulan_dict[bulan_nama]

	st.write(f"Prediksi untuk **{bulan_nama} {tahun}**")
	
	if st.button("Proses"):
		periode = calculate_period(tahun, bulan)
		regressor = load_prediction_model("linear_regression_emas.pkl")
		periode_reshaped = np.array(periode).reshape(-1, 1)
		predicted_price = regressor.predict(periode_reshaped)
		# trou ounce
		harga_prediksi = float(np.asarray(predicted_price).flatten()[0])
		# per gram
		harga_per_gram = harga_prediksi / 31.1034768
		st.divider()
		col1, col2 = st.columns(2)
		with col1:
			st.metric(label="Prediksi Harga Emas / Troy Ounce", value=f"USD {harga_prediksi:,.2f}")
		with col2:
			st.metric(label="Prediksi Harga Emas / Gram", value=f"USD {harga_per_gram:,.2f}")
		st.subheader("Evaluasi Model")
		mae = 269.4685277500109
		r2 = 0.8936750426892957
		mae_gram = mae/31.1034768
		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric("MAE (/Troy Ounce)",f"${mae:,.2f}")				
		with col2:
			st.metric("MAE (/Gram)",f"${mae_gram:,.2f}")
		with col3:
			st.metric("R² (Tingkat Kecocokan)",f"{r2 * 100:.2f}%")
		st.divider()
		st.caption(
			"""
			Model dilatih dengan menggunakan dataset dari https://datahub.io/core/gold-prices dari tahun 2022-2026 
			- **R²** menunjukkan besar variasi harga aktual yang dapat dijelaskan oleh model regresi.
			- **MAE** menunjukkan rata-rata kesalahan hasil prediksi model.
			"""
		) 
		
if __name__ == '__main__':
	main()