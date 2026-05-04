from google import genai
from google.genai import types
import streamlit as st
from datetime import date

@st.cache_resource
def setup_gemini_client():
    GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client

def get_gemini_market_insight(_client, top_laptops, selected_category):
    laptop_list_txt = ""

    exclude_cols = ['name', 'harga', 'score', 'rank'] 
    spec_cols = [col for col in top_laptops.columns if col not in exclude_cols]

    for _, row in top_laptops.iterrows():
            specs_summary = ", ".join([f"{'GEEKBENCH_BENCHMARK_' if col == 'prosesor' else ''}{col.upper()}: {row[col]} {'KG' if col == 'portabilitas' else 'GB' if col in ['ssd', 'ram'] else 'Jam' if col == 'baterai' else ''}" for col in spec_cols])
            
            laptop_list_txt += (
                f"- {row['name']}\n"
                f"  Harga di Sistem: Rp{row['harga']:,}\n"
                f"  Spesifikasi: {specs_summary}\n\n"
            )

    date_today = date.today().strftime("%B %d, %Y")

    # st.write(laptop_list_txt)

    prompt = f"""
    Cari harga pasar terbaru di Indonesia per {date_today} untuk laptop-laptop berikut:
    {laptop_list_txt}

    Konteks: User sedang mencari laptop untuk "{selected_category if selected_category != "Custom" else "kebutuhan kuliah"}"
    
    INSTRUKSI KHUSUS (Insightful Mode):
    1. Bandingkan harga sistem dengan benchmark harga laptop kompetitor (brand lain) yang speknya identik di internet.
    2. Format output: TABEL Markdown (Nama | Harga Sistem | Est. Harga Pasar | Status | Analisis Kritis).
    3. Di kolom 'Analisis Kritis', JANGAN ulangi spek. Berikan insight seperti:
    - "Harga ini kemahalan karena brand X dengan spek sama lebih murah 2jt."
    - "Value tinggi karena model ini punya build quality lebih premium dibanding rata-rata pasar."
    - "Waspada, spek ini mulai diskontinu/obsolete karena munculnya standar NPU baru."
    4. JANGAN ada basa-basi pembuka/penutup. Langsung tabel.
    5. Akhiri dengan satu baris: "**Rekomendasi Utama:** [Nama] karena [alasan]."
    
    Jawab dengan gaya bahasa asisten ahli gadget yang santai tapi akurat.
    """

    # Google Search Grounding
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        # temperature=1.0 
    )

    try:
        response = _client.models.generate_content_stream(
            model="gemini-2.5-flash-lite", 
            contents=prompt,
            config=config
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        # st.markdown(f"⚠️ Gagal mengambil insight pasar: {str(e)}")
        st.markdown(f"⚠️ Gagal mengambil insight pasar")