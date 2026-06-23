import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard MBG Nasional",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS — MODERN DESIGN
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global ── */
    html, body, [data-testid="stApp"] {
        background-color: #EFF2F7 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .main .block-container {
        padding: 1.5rem 2rem 2rem 2rem;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, #1B2A4A 0%, #0F1E35 100%) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown small { color: #94A3B8 !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stSelectbox > label { display: none; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #243555 !important;
        border: 1px solid #334E7E !important;
        color: white !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #94A3B8 !important; }
    [data-testid="stSidebar"] hr { border-color: #243555 !important; }

    /* ── Page Title ── */
    h1 {
        color: #1B2A4A !important;
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
    }

    /* ── Metric Cards ── */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-top: 4px solid #F5A623;
    }
    /* PERBAIKAN: Label keterangan dipaksa gelap dan tebal */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] div {
        color: #1A202C !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700 !important;
    }
    /* PERBAIKAN: Angka metrik dipaksa dongker pekat */
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #0F1E35 !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
    }

    /* ── Section Header Banner ── */
    .section-header {
        background: linear-gradient(90deg, #1B2A4A 0%, #2D4A7A 100%);
        color: white !important;
        padding: 10px 18px;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        letter-spacing: 0.3px;
    }

    /* ── Chart Wrapper Card ── */
    .stPlotlyChart {
        background: white;
        border-radius: 14px;
        padding: 0.4rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    }
    [data-testid="stDataFrame"] th {
        color: #1B2A4A !important;
        font-weight: 700 !important;
        background-color: #EBF4FF !important;
    }
    [data-testid="stDataFrame"] td {
        color: #1A202C !important;
        font-weight: 500 !important;
    }

    /* ── Divider ── */
    hr {
        border: none !important;
        border-top: 1px solid #DDE3EF !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Text Input ── */
    [data-testid="stTextInput"] input {
        border-radius: 8px;
        border: 1px solid #DDE3EF;
        background: white;
        padding: 0.5rem 0.8rem;
        color: #1A202C !important;
        font-weight: 500 !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #1B2A4A;
        box-shadow: 0 0 0 2px rgba(27,42,74,0.15);
    }

    /* ── Caption ── */
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #2D3748 !important;
        font-weight: 500 !important;
    }

    /* ── Tabel Ranking di dalam div putih ── */
    .white-card p, .white-card span, .white-card div {
        color: #1A202C !important;
    }

    /* ── Heading h3 di area konten (Buku Induk) ── */
    .main h3 {
        color: #1B2A4A !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# KOORDINAT CENTROID PROVINSI INDONESIA
# ==========================================
PROV_COORDS = {
    "Aceh": (4.695, 96.749), "Sumatera Utara": (2.115, 99.545), "Sumatera Barat": (-0.739, 100.801),
    "Riau": (0.293, 101.707), "Kepulauan Riau": (3.945, 108.142), "Jambi": (-1.610, 103.614),
    "Bengkulu": (-3.793, 102.260), "Sumatera Selatan": (-3.319, 103.914), "Kepulauan Bangka Belitung": (-2.741, 106.440),
    "Lampung": (-4.558, 105.405), "Banten": (-6.406, 106.064), "DKI Jakarta": (-6.200, 106.816),
    "Jawa Barat": (-7.090, 107.668), "Jawa Tengah": (-7.150, 110.140), "DI Yogyakarta": (-7.879, 110.366),
    "Jawa Timur": (-7.536, 112.239), "Bali": (-8.409, 115.188), "Nusa Tenggara Barat": (-8.652, 117.361),
    "Nusa Tenggara Timur": (-8.657, 121.079), "Kalimantan Barat": (-0.027, 109.342), "Kalimantan Tengah": (-1.681, 113.382),
    "Kalimantan Selatan": (-3.093, 115.284), "Kalimantan Timur": (1.681, 116.419), "Kalimantan Utara": (3.073, 116.041),
    "Sulawesi Utara": (0.627, 123.975), "Gorontalo": (0.544, 123.058), "Sulawesi Tengah": (-1.431, 121.445),
    "Sulawesi Barat": (-2.840, 119.233), "Sulawesi Selatan": (-3.659, 119.982), "Sulawesi Tenggara": (-3.971, 122.514),
    "Maluku": (-3.238, 130.145), "Maluku Utara": (1.571, 127.808), "Papua Barat": (-1.336, 133.174),
    "Papua": (-4.269, 138.080), "Papua Selatan": (-6.0, 140.0), "Papua Tengah": (-4.0, 136.0),
    "Papua Pegunungan": (-4.5, 139.0), "Papua Barat Daya": (-1.5, 132.0),
}

# ==========================================
# KOORDINAT SPESIFIK KABUPATEN/KOTA (MASTER LIST)
# ==========================================
# ==========================================
# KOORDINAT SPESIFIK KABUPATEN/KOTA (MASTER LIST SELURUH INDONESIA)
# ==========================================
KAB_COORDS = {
    # ── PAPUA & MALUKU ──
    "Kota Sorong": (-0.88, 131.25), "Kab. Sorong": (-1.13, 131.62), "Kab. Tolikara": (-3.58, 138.5),
    "Kab. Yahukimo": (-4.5, 139.5), "Kab. Pegunungan Bintang": (-4.5, 140.5), "Kab. Mappi": (-6.5, 139.5),
    "Kab. Boven Digoel": (-6.1, 140.3), "Kab. Merauke": (-8.4, 140.4), "Kab. Mimika": (-4.5, 136.5),
    "Kab. Paniai": (-3.9, 136.5), "Kab. Puncak Jaya": (-3.6, 137.9), "Kab. Nabire": (-3.3, 135.5),
    "Kab. Kaimana": (-3.6, 133.7), "Kota Jayapura": (-2.5, 140.7), "Kab. Mamberamo Raya": (-2.5, 137.5),
    "Kab. Keerom": (-3.3, 140.6), "Kab. Biak Numfor": (-1.0, 136.0), "Kab. Jayapura": (-2.9, 140.0),
    "Kota Tual": (-5.6, 132.7), "Kota Ambon": (-3.7, 128.1), "Kab. Buru Selatan": (-3.5, 126.5),
    "Kab. Maluku Barat Daya": (-8.1, 127.8), "Kab. Kepulauan Aru": (-6.1, 134.2), 
    "Kab. Seram Bagian Barat": (-3.0, 128.3), "Kab. Kepulauan Tanimbar": (-7.5, 131.4),
    "Kab. Buru": (-3.2, 126.6), "Kab. Maluku Tenggara": (-5.7, 132.7), "Kab. Maluku Tengah": (-3.1, 128.9),
    "Kota Tidore Kepulauan": (0.6, 127.4), "Kota Ternate": (0.8, 127.3), "Kab. Pulau Morotai": (2.3, 128.4),
    "Kab. Halmahera Timur": (1.3, 128.2), "Kab. Halmahera Selatan": (-0.6, 127.8), "Kab. Halmahera Utara": (1.6, 127.9),
    "Kab. Halmahera Barat": (1.2, 127.5), "Kab. Halmahera Tengah": (0.4, 127.9), "Kab. Pulau Taliabu": (-1.8, 124.8),

    # ── SULAWESI ──
    "Kota Bau Bau": (-5.4, 122.6), "Kota Kendari": (-3.9, 122.5), "Kab. Buton Tengah": (-5.3, 122.3),
    "Kab. Buton Selatan": (-5.6, 122.6), "Kab. Muna Barat": (-4.8, 122.4), "Kab. Kolaka Timur": (-4.0, 121.9),
    "Kab. Buton Utara": (-4.7, 123.0), "Kab. Konawe Utara": (-3.4, 122.0), "Kab. Kolaka Utara": (-3.3, 121.0),
    "Kab. Bombana": (-4.7, 121.8), "Kab. Wakatobi": (-5.3, 123.5), "Kab. Konawe Selatan": (-4.2, 122.2),
    "Kab. Kolaka": (-4.1, 121.5), "Kab. Buton": (-5.2, 122.8), "Kab. Muna": (-4.8, 122.7), "Kab. Konawe": (-3.8, 121.9),
    "Kota Palopo": (-3.0, 120.1), "Kota Parepare": (-4.0, 119.6), "Kota Makassar": (-5.1, 119.4),
    "Kab. Toraja Utara": (-2.8, 119.8), "Kab. Luwu Timur": (-2.5, 121.1), "Kab. Luwu Utara": (-2.5, 120.1),
    "Kab. Tana Toraja": (-3.0, 119.7), "Kab. Luwu": (-3.2, 120.2), "Kab. Enrekang": (-3.5, 119.8),
    "Kab. Sidenreng Rappang": (-3.9, 119.9), "Kab. Pinrang": (-3.7, 119.6), "Kab. Kepulauan Selayar": (-6.1, 120.4),
    "Kab. Sinjai": (-5.2, 120.1), "Kab. Bulukumba": (-5.5, 120.1), "Kab. Bantaeng": (-5.5, 119.9),
    "Kab. Soppeng": (-4.3, 119.8), "Kab. Wajo": (-4.0, 120.1), "Kab. Bone": (-4.8, 120.1),
    "Kab. Barru": (-4.3, 119.6), "Kab. Jeneponto": (-5.6, 119.7), "Kab. Takalar": (-5.4, 119.4),
    "Kab. Gowa": (-5.3, 119.5), "Kab. Pangkajene Dan Kepulauan": (-4.7, 119.5), "Kab. Maros": (-4.9, 119.6),
    "Kota Palu": (-0.9, 119.8), "Kab. Morowali Utara": (-1.8, 121.3), "Kab. Banggai Laut": (-1.7, 123.5),
    "Kab. Sigi": (-1.3, 119.9), "Kab. Tojo Una Una": (-1.0, 121.5), "Kab. Parigi Moutong": (-0.1, 120.0),
    "Kab. Morowali": (-2.6, 121.9), "Kab. Tolitoli": (1.0, 120.8), "Kab. Buol": (1.0, 121.3),
    "Kab. Banggai": (-1.2, 122.8), "Kab. Poso": (-1.4, 120.6), "Kab. Donggala": (-0.6, 119.7),
    "Kab. Banggai Kepulauan": (-1.3, 123.1), "Kota Kotamobagu": (0.7, 124.3), "Kota Bitung": (1.4, 125.1),
    "Kab. Bolaang Mongondow Selatan": (0.3, 123.8), "Kab. Bolaang Mongondow Timur": (0.8, 124.5),
    "Kab. Minahasa Utara": (1.4, 124.9), "Kab. Minahasa": (1.2, 124.8), "Kab. Bolaang Mongondow": (0.8, 124.0),
    "Kab. Mamuju Tengah": (-2.0, 119.3), "Kab. Majene": (-3.0, 118.9), "Kab. Mamasa": (-2.9, 119.3),
    "Kab. Polewali Mandar": (-3.4, 119.3), "Kab. Pasangkayu": (-1.3, 119.4), "Kab. Mamuju": (-2.6, 119.0),

    # ── KALIMANTAN ──
    "Kota Tarakan": (3.3, 117.6), "Kab. Nunukan": (4.0, 116.5), "Kab. Bulungan": (2.9, 117.1), "Kab. Malinau": (2.5, 115.5),
    "Kota Bontang": (0.1, 117.4), "Kota Balikpapan": (-1.2, 116.8), "Kota Samarinda": (-0.5, 117.1),
    "Kab. Mahakam Ulu": (0.8, 114.9), "Kab. Penajam Paser Utara": (-1.2, 116.6), "Kab. Kutai Timur": (0.9, 117.1),
    "Kab. Kutai Kartanegara": (-0.4, 116.9), "Kab. Paser": (-1.8, 116.0), "Kota Banjarbaru": (-3.4, 114.8),
    "Kota Banjarmasin": (-3.3, 114.5), "Kab. Tanah Bumbu": (-3.4, 115.6), "Kab. Balangan": (-2.3, 115.4),
    "Kab. Tabalong": (-2.0, 115.4), "Kab. Hulu Sungai Utara": (-2.4, 115.1), "Kab. Hulu Sungai Tengah": (-2.5, 115.4),
    "Kab. Hulu Sungai Selatan": (-2.7, 115.1), "Kab. Tapin": (-2.9, 115.0), "Kab. Barito Kuala": (-3.0, 114.6),
    "Kab. Tanah Laut": (-3.8, 114.7), "Kab. Banjar": (-3.3, 115.0), "Kota Palangka Raya": (-2.2, 113.9),
    "Kab. Barito Timur": (-1.9, 115.1), "Kab. Sukamara": (-2.6, 111.2), "Kab. Seruyan": (-2.3, 112.2),
    "Kab. Kotawaringin Timur": (-2.0, 112.6), "Kab. Barito Utara": (-1.0, 114.8), "Kota Singkawang": (0.9, 108.9),
    "Kota Pontianak": (-0.0, 109.3), "Kab. Kubu Raya": (-0.2, 109.4), "Kab. Kayong Utara": (-1.1, 109.9),
    "Kab. Melawi": (-0.5, 111.7), "Kab. Sekadau": (0.0, 111.0), "Kab. Landak": (0.4, 109.8),
    "Kab. Bengkayang": (1.0, 109.6), "Kab. Ketapang": (-1.5, 110.4), "Kab. Kapuas Hulu": (0.8, 112.7),
    "Kab. Sintang": (0.0, 111.6), "Kab. Sanggau": (0.3, 110.3), "Kab. Mempawah": (0.3, 109.1), "Kab. Sambas": (1.3, 109.3),

    # ── SUMATERA & KEP. RIAU/BABEL ──
    "Kota Tanjung Pinang": (0.9, 104.4), "Kota Batam": (1.1, 104.0), "Kab. Karimun": (0.9, 103.4), "Kab. Bintan": (1.0, 104.5),
    "Kota Pangkal Pinang": (-2.1, 106.1), "Kab. Belitung Timur": (-2.9, 108.1), "Kab. Bangka Selatan": (-2.9, 106.3),
    "Kab. Bangka Barat": (-1.8, 105.4), "Kab. Bangka Tengah": (-2.4, 106.2), "Kab. Belitung": (-2.8, 107.7),
    "Kab. Bangka": (-1.8, 105.9), "Kota Bengkulu": (-3.8, 102.2), "Kab. Seluma": (-4.0, 102.5),
    "Kab. Kaur": (-4.7, 103.3), "Kab. Mukomuko": (-2.5, 101.1), "Kab. Rejang Lebong": (-3.4, 102.6),
    "Kab. Bengkulu Utara": (-3.1, 101.9), "Kota Metro": (-5.1, 105.3), "Kota Bandar Lampung": (-5.4, 105.2),
    "Kab. Pesisir Barat": (-5.1, 104.0), "Kab. Tulang Bawang Barat": (-4.4, 105.0), "Kab. Mesuji": (-4.0, 105.3),
    "Kab. Pringsewu": (-5.3, 104.9), "Kab. Pesawaran": (-5.4, 105.1), "Kab. Way Kanan": (-4.5, 104.5),
    "Kab. Lampung Timur": (-5.1, 105.6), "Kab. Tanggamus": (-5.4, 104.6), "Kab. Tulang Bawang": (-4.3, 105.5),
    "Kab. Lampung Barat": (-5.0, 104.1), "Kab. Lampung Utara": (-4.8, 104.8), "Kab. Lampung Tengah": (-4.9, 105.2),
    "Kab. Lampung Selatan": (-5.6, 105.5), "Kota Pagar Alam": (-4.0, 103.2), "Kota Lubuk Linggau": (-3.2, 102.8),
    "Kota Prabumulih": (-3.4, 104.2), "Kota Palembang": (-2.9, 104.7), "Kab. Musi Rawas Utara": (-2.7, 102.8),
    "Kab. Penukal Abab Lematang Ilir": (-3.2, 103.9), "Kab. Empat Lawang": (-3.6, 102.9), "Kab. Ogan Ilir": (-3.4, 104.6),
    "Kab. Ogan Komering Ulu Selatan": (-4.6, 104.0), "Kab. Ogan Komering Ulu Timur": (-4.1, 104.5),
    "Kab. Banyuasin": (-2.8, 104.3), "Kab. Musi Rawas": (-3.1, 103.2), "Kab. Lahat": (-3.8, 103.5),
    "Kab. Muara Enim": (-3.6, 103.7), "Kab. Ogan Komering Ulu": (-4.1, 104.1), "Kab. Ogan Komering Ilir": (-3.4, 105.0),
    "Kab. Musi Banyuasin": (-2.5, 103.7), "Kota Jambi": (-1.6, 103.6), "Kab. Merangin": (-2.0, 102.1),
    "Kab. Tanjung Jabung Timur": (-1.1, 103.9), "Kab. Muaro Jambi": (-1.5, 103.8), "Kab. Sarolangun": (-2.3, 102.6),
    "Kab. Batanghari": (-1.7, 103.2), "Kota Dumai": (1.6, 101.4), "Kota Pekanbaru": (0.5, 101.4),
    "Kab. Kepulauan Meranti": (0.9, 102.6), "Kab. Kuantan Singingi": (-0.5, 101.4), "Kab. Siak": (0.7, 102.0),
    "Kab. Rokan Hilir": (1.8, 100.8), "Kab. Rokan Hulu": (0.9, 100.3), "Kab. Pelalawan": (0.3, 102.0),
    "Kab. Indragiri Hilir": (-0.4, 103.1), "Kab. Indragiri Hulu": (-0.5, 102.3), "Kab. Bengkalis": (1.4, 102.1),
    "Kab. Kampar": (0.3, 101.0), "Kota Pariaman": (-0.6, 100.1), "Kota Payakumbuh": (-0.2, 100.6),
    "Kota Solok": (-0.7, 100.6), "Kota Sawahlunto": (-0.6, 100.7), "Kota Padang": (-0.9, 100.3),
    "Kota Bukittinggi": (-0.3, 100.3), "Kab. Pasaman Barat": (0.1, 99.8), "Kab. Dharmasraya": (-1.0, 101.5),
    "Kab. Solok Selatan": (-1.4, 101.1), "Kab. Tanah Datar": (-0.4, 100.5), "Kab. Pesisir Selatan": (-1.3, 100.5),
    "Kab. Padang Pariaman": (-0.6, 100.2), "Kab. Solok": (-0.9, 100.6), "Kab. Lima Puluh Kota": (0.0, 100.6),
    "Kab. Pasaman": (0.5, 100.1), "Kab. Agam": (-0.2, 100.0), "Kota Gunungsitoli": (1.2, 97.6),
    "Kota Padang Sidempuan": (1.3, 99.2), "Kota Sibolga": (1.7, 98.7), "Kota Tanjung Balai": (2.9, 99.8),
    "Kota Pematangsiantar": (2.9, 99.0), "Kota Tebing Tinggi": (3.3, 99.1), "Kota Binjai": (3.6, 98.4),
    "Kota Medan": (3.5, 98.6), "Kab. Nias Utara": (1.4, 97.3), "Kab. Nias Barat": (0.9, 97.5),
    "Kab. Labuhanbatu Selatan": (1.9, 100.0), "Kab. Labuhanbatu Utara": (2.3, 99.6), "Kab. Padang Lawas utara": (1.5, 99.6),
    "Kab. Batu Bara": (3.1, 99.4), "Kab. Serdang Bedagai": (3.3, 99.0), "Kab. Samosir": (2.6, 98.7),
    "Kab. Pakpak Bharat": (2.5, 98.2), "Kab. Nias Selatan": (0.6, 97.7), "Kab. Toba": (2.3, 99.2),
    "Kab. Mandailing Natal": (0.8, 99.5), "Kab. Nias": (1.1, 97.7), "Kab. Tapanuli Selatan": (1.5, 99.2),
    "Kab. Tapanuli Tengah": (1.9, 98.5), "Kab. Tapanuli Utara": (2.0, 98.9), "Kab. Labuhanbatu": (2.1, 99.8),
    "Kab. Asahan": (2.8, 99.4), "Kab. Dairi": (2.8, 98.2), "Kab. Simalungun": (2.9, 98.9),
    "Kab. Karo": (3.0, 98.4), "Kab. Langkat": (3.8, 98.1), "Kab. Deli Serdang": (3.4, 98.7),
    "Kota Subulussalam": (2.6, 97.9), "Kota Langsa": (4.4, 97.9), "Kota Lhokseumawe": (5.1, 97.1),
    "Kota Banda Aceh": (5.5, 95.3), "Kota Sabang": (5.8, 95.3), "Kab. Pidie Jaya": (5.1, 96.2),
    "Kab. Bener Meriah": (4.7, 96.8), "Kab. Gayo Lues": (3.9, 97.3), "Kab. Aceh Barat Daya": (3.8, 96.8),
    "Kab. Aceh Jaya": (4.7, 95.6), "Kab. Nagan Raya": (4.1, 96.3), "Kab. Aceh Tamiang": (4.3, 98.0),
    "Kab. Aceh Singkil": (2.3, 97.9), "Kab. Bireuen": (5.1, 96.6), "Kab. Simeulue": (2.6, 96.0),
    "Kab. Aceh Tenggara": (3.3, 97.8), "Kab. Aceh Selatan": (3.2, 97.2), "Kab. Aceh Barat": (4.4, 96.1),
    "Kab. Aceh Tengah": (4.5, 96.8), "Kab. Aceh Timur": (4.6, 97.7), "Kab. Aceh Utara": (5.0, 97.0),
    "Kab. Pidie": (5.0, 96.0), "Kab. Aceh Besar": (5.3, 95.5),

    # ── JAWA, BALI & NUSA TENGGARA ──
    "Kota Batu": (-7.8, 112.5), "Kota Probolinggo": (-7.7, 113.2), "Kota Pasuruan": (-7.6, 112.9),
    "Kota Blitar": (-8.1, 112.1), "Kota Mojokerto": (-7.4, 112.4), "Kota Kediri": (-7.8, 112.0),
    "Kota Madiun": (-7.6, 111.5), "Kota Malang": (-7.9, 112.6), "Kota Surabaya": (-7.2, 112.7),
    "Kab. Bangkalan": (-7.0, 112.7), "Kab. Sumenep": (-7.0, 113.8), "Kab. Sampang": (-7.1, 113.2),
    "Kab. Pamekasan": (-7.1, 113.4), "Kab. Banyuwangi": (-8.2, 114.3), "Kab. Jember": (-8.1, 113.6),
    "Kab. Situbondo": (-7.7, 113.9), "Kab. Bondowoso": (-7.9, 113.9), "Kab. Lumajang": (-8.1, 113.1),
    "Kab. Probolinggo": (-7.8, 113.3), "Kab. Pasuruan": (-7.7, 112.8), "Kab. Malang": (-8.1, 112.5),
    "Kab. Trenggalek": (-8.1, 111.7), "Kab. Tulungagung": (-8.0, 111.9), "Kab. Blitar": (-8.1, 112.2),
    "Kab. Nganjuk": (-7.6, 111.9), "Kab. Kediri": (-7.8, 112.1), "Kab. Pacitan": (-8.1, 111.1),
    "Kab. Ponorogo": (-7.9, 111.4), "Kab. Magetan": (-7.6, 111.3), "Kab. Ngawi": (-7.4, 111.4),
    "Kab. Madiun": (-7.6, 111.6), "Kab. Lamongan": (-7.1, 112.4), "Kab. Tuban": (-6.9, 111.9),
    "Kab. Bojonegoro": (-7.2, 111.8), "Kab. Jombang": (-7.5, 112.2), "Kab. Mojokerto": (-7.5, 112.5),
    "Kab. Sidoarjo": (-7.4, 112.7), "Kab. Gresik": (-7.1, 112.5), "Kota Yogyakarta": (-7.8, 110.3),
    "Kab. Kulon Progo": (-7.8, 110.1), "Kab. Gunungkidul": (-7.9, 110.6), "Kab. Sleman": (-7.7, 110.3),
    "Kab. Bantul": (-7.8, 110.3), "Kota Tegal": (-6.8, 109.1), "Kota Pekalongan": (-6.8, 109.6),
    "Kota Semarang": (-7.0, 110.4), "Kota Salatiga": (-7.3, 110.5), "Kota Surakarta": (-7.5, 110.8),
    "Kota Magelang": (-7.4, 110.2), "Kab. Brebes": (-6.9, 108.9), "Kab. Tegal": (-7.0, 109.1),
    "Kab. Pemalang": (-7.0, 109.4), "Kab. Pekalongan": (-7.0, 109.6), "Kab. Batang": (-7.0, 109.8),
    "Kab. Kendal": (-7.0, 110.1), "Kab. Temanggung": (-7.3, 110.1), "Kab. Semarang": (-7.2, 110.4),
    "Kab. Demak": (-6.9, 110.6), "Kab. Jepara": (-6.5, 110.7), "Kab. Kudus": (-6.8, 110.8),
    "Kab. Pati": (-6.7, 111.0), "Kab. Rembang": (-6.7, 111.3), "Kab. Blora": (-7.0, 111.4),
    "Kab. Grobogan": (-7.0, 110.9), "Kab. Sragen": (-7.4, 110.9), "Kab. Karanganyar": (-7.6, 111.0),
    "Kab. Wonogiri": (-7.9, 110.9), "Kab. Sukoharjo": (-7.6, 110.8), "Kab. Klaten": (-7.7, 110.6),
    "Kab. Boyolali": (-7.5, 110.6), "Kab. Magelang": (-7.5, 110.2), "Kab. Wonosobo": (-7.3, 109.9),
    "Kab. Purworejo": (-7.7, 110.0), "Kab. Kebumen": (-7.6, 109.6), "Kab. Banjarnegara": (-7.3, 109.6),
    "Kab. Purbalingga": (-7.3, 109.3), "Kab. Banyumas": (-7.4, 109.1), "Kab. Cilacap": (-7.6, 109.0),
    "Kota Banjar": (-7.3, 108.5), "Kota Tasikmalaya": (-7.3, 108.2), "Kota Cimahi": (-6.8, 107.5),
    "Kota Depok": (-6.4, 106.8), "Kota Bekasi": (-6.2, 106.9), "Kota Cirebon": (-6.7, 108.5),
    "Kota Sukabumi": (-6.9, 106.9), "Kota Bogor": (-6.5, 106.7), "Kota Bandung": (-6.9, 107.6),
    "Kab. Pangandaran": (-7.6, 108.5), "Kab. Bandung Barat": (-6.8, 107.4), "Kab. Bekasi": (-6.3, 107.1),
    "Kab. Karawang": (-6.3, 107.3), "Kab. Purwakarta": (-6.5, 107.4), "Kab. Subang": (-6.5, 107.7),
    "Kab. Indramayu": (-6.3, 108.1), "Kab. Cirebon": (-6.7, 108.4), "Kab. Majalengka": (-6.8, 108.2),
    "Kab. Kuningan": (-7.0, 108.4), "Kab. Ciamis": (-7.2, 108.3), "Kab. Tasikmalaya": (-7.4, 108.0),
    "Kab. Garut": (-7.3, 107.8), "Kab. Sumedang": (-6.8, 107.9), "Kab. Bandung": (-7.1, 107.5),
    "Kab. Cianjur": (-7.0, 107.1), "Kab. Sukabumi": (-7.1, 106.6), "Kab. Bogor": (-6.5, 106.6),
    "Kota Adm. Jakarta Timur": (-6.2, 106.9), "Kota Adm. Jakarta Selatan": (-6.26, 106.8),
    "Kota Adm. Jakarta Barat": (-6.16, 106.75), "Kota Adm. Jakarta Utara": (-6.13, 106.9),
    "Kota Adm. Jakarta Pusat": (-6.18, 106.82), "Kab. Adm. Kep. Seribu": (-5.73, 106.56),
    "Kota Denpasar": (-8.65, 115.2), "Kab. Karangasem": (-8.3, 115.5), "Kab. Bangli": (-8.2, 115.3),
    "Kab. Klungkung": (-8.5, 115.5), "Kab. Gianyar": (-8.4, 115.3), "Kab. Badung": (-8.5, 115.1),
    "Kab. Tabanan": (-8.4, 115.0), "Kab. Jembrana": (-8.3, 114.6), "Kab. Buleleng": (-8.2, 114.9),
    "Kab. Malaka": (-9.5, 124.9), "Kab. Manggarai Timur": (-8.6, 120.5), "Kab. Sumba Barat Daya": (-9.5, 119.0),
    "Kab. Nagekeo": (-8.8, 121.2), "Kab. Manggarai Barat": (-8.6, 120.0), "Kab. Rote Ndao": (-10.7, 123.0),
    "Kab. Lembata": (-8.4, 123.5), "Kab. Sumba Barat": (-9.6, 119.4), "Kab. Sumba Timur": (-9.8, 120.2),
    "Kab. Manggarai": (-8.5, 120.3), "Kab. Ngada": (-8.7, 120.9), "Kab. Ende": (-8.7, 121.6),
    "Kab. Alor": (-8.2, 124.5), "Kab. Belu": (-9.1, 124.8), "Kab. Timor Tengah Selatan": (-9.7, 124.2),
    "Kab. Kupang": (-9.9, 123.8), "Kota Bima": (-8.4, 118.7), "Kota Mataram": (-8.5, 116.1),
    "Kab. Lombok Utara": (-8.3, 116.2), "Kab. Dompu": (-8.5, 118.4), "Kab. Sumbawa": (-8.6, 117.4),
    "Kab. Lombok Timur": (-8.6, 116.5), "Kab. Lombok Tengah": (-8.7, 116.2), "Kab. Lombok Barat": (-8.6, 116.1)
}
#
# BASE CHART LAYOUT 
CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1A202C"),
    margin=dict(r=10, t=44, b=90), 
    xaxis=dict(gridcolor="#EDF2F7", zeroline=False, tickfont=dict(color="#1A202C"), automargin=True),
    yaxis=dict(gridcolor="#EDF2F7", zeroline=False, tickfont=dict(color="#1A202C"), automargin=True),
    legend=dict(font=dict(color="#1A202C"))
)

# LOAD DATA 
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("MASTER_DATASET_MBG_BI2026.csv")
        if len(df.columns) == 1:
            df = pd.read_csv("MASTER_DATASET_MBG_BI2026.csv", sep=";")
        df.columns = df.columns.str.lower()

        if "provinsi" in df.columns:
            df["provinsi"] = df["provinsi"].replace({
                "Prov. D.K.I. Jakarta": "Prov. DKI Jakarta",
                "Prov. D.I. Yogyakarta": "Prov. DI Yogyakarta",
                "Prov. D. I. Yogyakarta": "Prov. DI Yogyakarta",
                "Prov. Kep. Bangka Belitung": "Prov. Kepulauan Bangka Belitung",
                "Prov. Nanggroe Aceh Darussalam": "Prov. Aceh"
            })

        return df
    except FileNotFoundError:
        st.error("File 'MASTER_DATASET_MBG_BI2026.csv' tidak ditemukan. Pastikan file berada di folder yang sama.")
        return pd.DataFrame()

df = load_data()

# FUNGSI BANTUAN UNTUK PETA
def get_coords(prov_name):
    clean_name = str(prov_name).replace("Prov. ", "").strip()
    return PROV_COORDS.get(clean_name, (None, None))

def get_kab_coords(kab_name):
    clean_name = str(kab_name).strip()
    return KAB_COORDS.get(clean_name, (None, None))

# SIDEBAR
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding-bottom:0.5rem;">
            <span style="font-size:2rem;">🍽️</span>
            <h2 style="color:white; margin:0; font-size:1.1rem; font-weight:700;">Dashboard MBG</h2>
            <p style="color:#4A6FA5; font-size:0.75rem; margin:0;">Makan Bergizi Gratis</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    if not df.empty and "provinsi" in df.columns:
        st.markdown('<p style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:0.4rem;">🗺️ Filter Provinsi</p>', unsafe_allow_html=True)
        prov_list = ["Semua"] + sorted(df["provinsi"].dropna().unique().tolist())
        selected_prov = st.selectbox("Provinsi", prov_list)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(f"""
            <p style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:0.6rem;">📊 Info Dataset</p>
            <div style="color:#CBD5E0; font-size:0.84rem; line-height:2;">
                📁 Total Baris &nbsp;<b style="color:white; float:right;">{len(df):,}</b><br>
                🗺️ Provinsi &nbsp;<b style="color:white; float:right;">{df['provinsi'].nunique()}</b><br>
                🏙️ Kab/Kota &nbsp;<b style="color:white; float:right;">{df.get('kabupaten_kota', pd.Series()).nunique()}</b><br>
                📍 Kecamatan &nbsp;<b style="color:white; float:right;">{df.get('kecamatan', pd.Series()).nunique()}</b>
            </div>
        """, unsafe_allow_html=True)
    else:
        selected_prov = "Semua"

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p style="color:#334E7E; font-size:0.72rem; text-align:center;">by Kelompok 11 UPNVJ</p>', unsafe_allow_html=True)

if not df.empty and "provinsi" in df.columns:
    df_filtered = df[df["provinsi"] == selected_prov] if selected_prov != "Semua" else df.copy()
else:
    df_filtered = pd.DataFrame()

# HEADER
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 2rem; margin-top: -1rem;">
        <h1 style="font-size: 2.4rem; font-weight: 800; color: #1B2A4A; margin-bottom: 0.2rem;">
            🍽️ Dashboard Pemantauan Makan Bergizi Gratis (MBG)
        </h1>
        <p style="color: #2D3748; font-size: 1.05rem; font-weight: 500;">
            Visualisasi distribusi logistik dan kebutuhan gizi khusus per wilayah Indonesia
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if df_filtered.empty:
    st.stop()

# SECTION 1 — RINGKASAN
st.markdown('<div class="section-header">📌 &nbsp;Ringkasan</div>', unsafe_allow_html=True)

total_penerima = df_filtered.get("jumlah_penerima_manfaat", pd.Series([0])).sum()
total_satpen   = df_filtered.get("jumlah_satuan_pendidikan", pd.Series([0])).sum()
total_khusus   = df_filtered.get("jumlah_kondisi_khusus", pd.Series([0])).sum()
rasio_khusus   = (total_khusus / total_penerima * 100) if total_penerima > 0 else 0

st.markdown(
    f'<div style="color:#1A202C; font-size:0.95rem; margin-bottom:1.5rem; line-height:1.7; '
    f'background-color:#EBF8FF; padding:15px; border-radius:10px; border-left:4px solid #4299E1; font-weight:500;">'
    f'Berdasarkan data saat ini, program MBG mencakup <b>{total_satpen:,}</b> satuan pendidikan dengan total '
    f'<b>{total_penerima:,}</b> siswa penerima manfaat. '
    f'Dari jumlah tersebut, terdapat <b>{total_khusus:,} siswa ({rasio_khusus:.1f}%)</b> yang memiliki kondisi gizi '
    f'khusus (alergi, fobia, atau intoleransi). '
    f'Rasio ini menjadi peringatan bagi dapur umum dan tim logistik untuk menyiapkan menu substitusi yang tepat sasaran.'
    f'</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("🧑‍🎓 Total Penerima Manfaat", f"{total_penerima:,}")
with c2: st.metric("🏫 Satuan Pendidikan", f"{total_satpen:,}")
with c3: st.metric("⚠️ Siswa Kondisi Khusus", f"{total_khusus:,}")
with c4: st.metric("📊 Rasio Kondisi Khusus", f"{rasio_khusus:.1f}%")

st.divider()

# SECTION 2 — ANALISIS DAPUR & OPERASIONAL
st.markdown('<div class="section-header">🍳 &nbsp;Analisis Kebutuhan Dapur & Operasional</div>', unsafe_allow_html=True)

cd1, cd2, cd3 = st.columns(3)

with cd1:
    alergi      = df_filtered.get("jumlah_alergi", pd.Series([0])).sum()
    fobia       = df_filtered.get("jumlah_fobia", pd.Series([0])).sum()
    intoleransi = df_filtered.get("jumlah_intoleransi", pd.Series([0])).sum()

    fig_donut = px.pie(
        names=["Alergi", "Fobia", "Intoleransi"],
        values=[alergi, fobia, intoleransi],
        hole=0.5,
        title="🔍 Tipe Kondisi Khusus",
        color_discrete_sequence=["#1B2A4A", "#F5A623", "#E53E3E"],
    )
    fig_donut.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(size=11, color="#FFFFFF"))
    fig_donut.update_layout(**CHART_BASE, showlegend=True)
    st.plotly_chart(fig_donut, use_container_width=True, theme=None)

with cd2:
    if "jenjang" in df_filtered.columns:
        df_jenjang = df_filtered.groupby("jenjang")["jumlah_penerima_manfaat"].sum().reset_index().sort_values("jumlah_penerima_manfaat", ascending=False)
        fig_jenjang = px.bar(
            df_jenjang, x="jenjang", y="jumlah_penerima_manfaat",
            title="📚 Beban Porsi per Jenjang", text_auto=".2s",
            color="jumlah_penerima_manfaat", color_continuous_scale=[[0, "#90CDF4"], [1, "#1B2A4A"]],
        )
        fig_jenjang.update_traces(textposition="outside", textfont=dict(size=10, color="#1A202C"))
        fig_jenjang.update_layout(**CHART_BASE, coloraxis_showscale=False)
        st.plotly_chart(fig_jenjang, use_container_width=True, theme=None)

with cd3:
    if "jumlah_satpen_negeri" in df_filtered.columns and "jumlah_satpen_swasta" in df_filtered.columns:
        df_status = df_filtered.groupby("provinsi")[["jumlah_satpen_negeri", "jumlah_satpen_swasta"]].sum().reset_index().nlargest(8, "jumlah_satpen_negeri")
        fig_status = px.bar(
            df_status, x="provinsi", y=["jumlah_satpen_negeri", "jumlah_satpen_swasta"],
            title="🏫 Sekolah Negeri vs Swasta", barmode="stack",
            color_discrete_map={"jumlah_satpen_negeri": "#1B2A4A", "jumlah_satpen_swasta": "#F5A623"},
            labels={"value": "Jumlah", "variable": "", "jumlah_satpen_negeri": "Negeri", "jumlah_satpen_swasta": "Swasta"},
        )
        fig_status.update_layout(**CHART_BASE)
        fig_status.update_layout(xaxis_tickangle=-35, legend_orientation="h", legend_yanchor="bottom", legend_y=-0.45, legend_title_text="")
        st.plotly_chart(fig_status, use_container_width=True, theme=None)

st.divider()

# SECTION 3 — ANALISIS GEOGRAFIS + GEO MAP
st.markdown('<div class="section-header">🗺️ &nbsp;Pemetaan Wilayah Distribusi</div>', unsafe_allow_html=True)

cg1, cg2 = st.columns(2)

with cg1:
    if "kabupaten_kota" in df_filtered.columns:
        df_kab = df_filtered.groupby("kabupaten_kota")["jumlah_penerima_manfaat"].sum().reset_index().sort_values("jumlah_penerima_manfaat", ascending=False).head(10)
        fig_kab = px.bar(
            df_kab, y="kabupaten_kota", x="jumlah_penerima_manfaat", orientation="h",
            title="🏆 Top 10 Kab/Kota — Penerima Terbanyak", text_auto=".2s",
            color="jumlah_penerima_manfaat", color_continuous_scale=[[0, "#90CDF4"], [1, "#1B2A4A"]],
        )
        fig_kab.update_layout(**CHART_BASE)
        fig_kab.update_layout(yaxis=dict(categoryorder="total ascending", automargin=True), coloraxis_showscale=False)
        st.plotly_chart(fig_kab, use_container_width=True, theme=None)

with cg2:
    if "kecamatan" in df_filtered.columns:
        df_kec = df_filtered.groupby("kecamatan")["jumlah_kondisi_khusus"].sum().reset_index().sort_values("jumlah_kondisi_khusus", ascending=False).head(10)
        fig_kec = px.bar(
            df_kec, y="kecamatan", x="jumlah_kondisi_khusus", orientation="h",
            title="⚠️ Top 10 Kecamatan — Kondisi Khusus Tertinggi", color_discrete_sequence=["#E53E3E"], text_auto=".2s",
        )
        fig_kec.update_layout(**CHART_BASE)
        fig_kec.update_layout(yaxis=dict(categoryorder="total ascending", automargin=True))
        st.plotly_chart(fig_kec, use_container_width=True, theme=None)

st.markdown(
    '<div style="background-color: #1B2A4A; color: white; padding: 8px 15px; '
    'border-radius: 8px; font-size: 0.95rem; font-weight: 600; margin-bottom: 1rem; margin-top: 1.5rem;">'
    '🌏 &nbsp;Peta Sebaran Penerima Manfaat</div>',
    unsafe_allow_html=True
)
col_map, col_rank = st.columns([3, 1])

with col_map:
    if selected_prov == "Semua":
        df_map_data = df_filtered.groupby("provinsi").agg(
            penerima=("jumlah_penerima_manfaat", "sum"), kondisi_khusus=("jumlah_kondisi_khusus", "sum"), satuan_pendidikan=("jumlah_satuan_pendidikan", "sum")
        ).reset_index()
        df_map_data["lat"] = df_map_data["provinsi"].map(lambda p: get_coords(p)[0])
        df_map_data["lon"] = df_map_data["provinsi"].map(lambda p: get_coords(p)[1])
        df_map_data = df_map_data.dropna(subset=["lat", "lon"])
        hover_name, zoom_lvl, center_lat, center_lon = "provinsi", 3.6, -2.5, 118.0
    else:
        if "kabupaten_kota" in df_filtered.columns:
            df_map_data = df_filtered.groupby("kabupaten_kota").agg(
                penerima=("jumlah_penerima_manfaat", "sum"), kondisi_khusus=("jumlah_kondisi_khusus", "sum"), satuan_pendidikan=("jumlah_satuan_pendidikan", "sum")
            ).reset_index()
            base_lat, base_lon = get_coords(selected_prov)
            n_kab, radius = len(df_map_data), 0.5
            lats, lons = [], []
            for i, row in df_map_data.iterrows():
                kab_name = row["kabupaten_kota"]
                
                kab_lat, kab_lon = get_kab_coords(kab_name)
                
                if kab_lat is not None and kab_lon is not None:
                    lats.append(kab_lat)
                    lons.append(kab_lon)
                    
                else:
                    if n_kab == 1:
                        lats.append(base_lat)
                        lons.append(base_lon)
                    else:
                        angle = (2 * np.pi / n_kab) * i
                        lats.append(base_lat + radius * np.cos(angle))
                        lons.append(base_lon + radius * np.sin(angle))
            df_map_data["lat"], df_map_data["lon"] = lats, lons
            hover_name, zoom_lvl, center_lat, center_lon = "kabupaten_kota", 6.5, base_lat, base_lon
        else:
            df_map_data = pd.DataFrame()

    if not df_map_data.empty and center_lat is not None:
        fig_map = px.scatter_mapbox(
            df_map_data, lat="lat", lon="lon", size="penerima", color="kondisi_khusus", hover_name=hover_name,
            hover_data={"penerima": ":,", "kondisi_khusus": ":,", "satuan_pendidikan": ":,", "lat": False, "lon": False},
            color_continuous_scale=[[0, "#4299E1"], [0.5, "#F5A623"], [1, "#E53E3E"]], size_max=50, zoom=zoom_lvl,
            center={"lat": center_lat, "lon": center_lon}, mapbox_style="open-street-map",
            labels={"penerima": "Total Penerima", "kondisi_khusus": "Kondisi Khusus", "satuan_pendidikan": "Total Sekolah"}
        )
        fig_map.update_layout(**CHART_BASE)
        # Margin kiri bebas (dihapus)
        fig_map.update_layout(height=460, coloraxis_colorbar=dict(title="Kondisi<br>Khusus", len=0.65, thickness=12), margin=dict(r=0, t=10, b=0))
        st.plotly_chart(fig_map, use_container_width=True, theme=None)
    else:
        st.info("Koordinat wilayah tidak ditemukan untuk menampilkan peta.")

    st.caption("💡 **Mode Nasional:** 1 Gelembung = 1 Provinsi &nbsp;|&nbsp; **Mode Filter:** 1 Gelembung = 1 Kabupaten")

with col_rank:
    label_area = "Provinsi" if selected_prov == "Semua" else "Kab/Kota"
    col_group  = "provinsi" if selected_prov == "Semua" else "kabupaten_kota"
    
    if col_group in df_filtered.columns:
        st.markdown(f'<p style="color:#1B2A4A; font-weight:700; font-size:0.88rem; margin-bottom:0.5rem;">🏆 Top 5 {label_area} — Penerima</p>', unsafe_allow_html=True)
        top5 = df_filtered.groupby(col_group)["jumlah_penerima_manfaat"].sum().reset_index().nlargest(5, "jumlah_penerima_manfaat").reset_index(drop=True)
        top5.index += 1; top5.columns = [label_area, "Penerima"]; top5["Penerima"] = top5["Penerima"].apply(lambda x: f"{x:,}")
        st.dataframe(top5, use_container_width=True)

        st.markdown(f'<p style="color:#1B2A4A; font-weight:700; font-size:0.88rem; margin-top:1rem; margin-bottom:0.5rem;">⚠️ Top 5 {label_area} — Kondisi Khusus</p>', unsafe_allow_html=True)
        top5k = df_filtered.groupby(col_group)["jumlah_kondisi_khusus"].sum().reset_index().nlargest(5, "jumlah_kondisi_khusus").reset_index(drop=True)
        top5k.index += 1; top5k.columns = [label_area, "Kond. Khusus"]; top5k["Kond. Khusus"] = top5k["Kond. Khusus"].apply(lambda x: f"{x:,}")
        st.dataframe(top5k, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# SECTION 4 — DEMOGRAFI & TABEL OPERASIONAL
st.markdown('<div class="section-header">👥 &nbsp;Detail Demografi & Tabel Operasional</div>', unsafe_allow_html=True)

col_demo1, col_demo2 = st.columns([1, 2])

with col_demo1:
    laki = df_filtered.get("jumlah_laki", pd.Series([0])).sum()
    pr   = df_filtered.get("jumlah_perempuan", pd.Series([0])).sum()

    fig_gender = px.pie(names=["Laki-laki", "Perempuan"], values=[laki, pr], title="⚧ Distribusi Gender", color_discrete_sequence=["#1B2A4A", "#F5A623"], hole=0.45)
    fig_gender.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(size=11, color="#FFFFFF"))
    
    fig_gender.update_layout(**CHART_BASE)
    fig_gender.update_layout(showlegend=True, legend_orientation="h", legend_yanchor="bottom", legend_y=-0.15, margin=dict(r=10, t=44, b=40))
    
    st.plotly_chart(fig_gender, use_container_width=True, theme=None)

with col_demo2:
    if "provinsi" in df_filtered.columns and "kabupaten_kota" in df_filtered.columns and "jenjang" in df_filtered.columns:
        if selected_prov == "Semua":
            kolom_y = "provinsi"
            judul_heat = "🔥 Heatmap Satuan Pendidikan per Jenjang & Provinsi"
        else:
            kolom_y = "kabupaten_kota"
            judul_heat = "🔥 Heatmap Satuan Pendidikan per Jenjang & Kab/Kota"
            
        pivot_heatmap = df_filtered.pivot_table(index=kolom_y, columns="jenjang", values="jumlah_satuan_pendidikan", aggfunc="sum").fillna(0)
        
        pivot_heatmap["Total"] = pivot_heatmap.sum(axis=1)
        pivot_heatmap = pivot_heatmap.sort_values("Total", ascending=True).drop(columns=["Total"])
        jumlah_baris = len(pivot_heatmap)
        tinggi_dinamis = max(400, jumlah_baris * 25)

        fig_heatmap = px.imshow(pivot_heatmap, text_auto=True, aspect="auto", title=judul_heat, color_continuous_scale=[[0, "#EBF8FF"], [0.5, "#4299E1"], [1, "#1B2A4A"]])
        fig_heatmap.update_layout(**CHART_BASE)
        # Margin kiri bebas (dihapus)
        fig_heatmap.update_layout(height=tinggi_dinamis, margin=dict(r=10, t=44, b=10))
        st.plotly_chart(fig_heatmap, use_container_width=True, theme=None)

# Tabel Buku Induk 
st.markdown('<h3 style="color:#1B2A4A; font-weight:700; margin-top:1rem;">📋 Buku Induk — Data Operasional</h3>', unsafe_allow_html=True)
search = st.text_input("search", label_visibility="collapsed", placeholder="🔍 Cari berdasarkan provinsi / kab-kota / kecamatan...")

kolom_tabel = [c for c in ["provinsi", "kabupaten_kota", "kecamatan", "jenjang", "jumlah_satuan_pendidikan", "jumlah_penerima_manfaat", "jumlah_kondisi_khusus"] if c in df_filtered.columns]

if search and len(kolom_tabel) > 0:
    mask = df_filtered[["provinsi", "kabupaten_kota", "kecamatan"]].astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
    df_display = df_filtered[mask][kolom_tabel]
else:
    df_display = df_filtered[kolom_tabel]

st.dataframe(df_display, use_container_width=True, height=360)
st.caption(f"Menampilkan **{len(df_display):,}** dari **{len(df_filtered):,}** baris data")