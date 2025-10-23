import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ====================================================================
# FUNGSI UTAMA UNTUK MENGATUR TAMPILAN PLOTLY
# ====================================================================
def update_plot_layout(fig):
    """Mengatur tata letak Plotly agar sesuai dengan tema gelap Streamlit."""
    fig.update_layout(
        # Latar belakang area plot (di dalam sumbu)
        plot_bgcolor='rgba(16, 42, 68, 0.7)',
        # Latar belakang keseluruhan figur (di luar sumbu)
        paper_bgcolor='rgba(10, 28, 51, 0.5)',
        # Warna teks default (label, legenda)
        font_color='#F5F5F5', 
        
        # Pengaturan Judul Plot
        title_font_color="#00C9FF", # Warna judul plot (Accent Cyan)
        title_font_size=24,         # Ukuran judul plot
        
        # Pengaturan Sumbu X (Garis dan Teks)
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)', 
            linecolor='rgba(255, 255, 255, 0.2)', 
            zerolinecolor='rgba(255, 255, 255, 0.2)',
            title_font_size=18,  # Ukuran Label Sumbu X
            tickfont_size=12,    # Ukuran Teks Ticks Sumbu X
            title_font_color='#FF6FB5' # Warna Label Sumbu X (Accent Pink)
        ),
        
        # Pengaturan Sumbu Y (Garis dan Teks)
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)', 
            linecolor='rgba(255, 255, 255, 0.2)', 
            zerolinecolor='rgba(255, 255, 255, 0.2)',
            title_font_size=18,  # Ukuran Label Sumbu Y
            tickfont_size=12,    # Ukuran Teks Ticks Sumbu Y
            title_font_color='#FF6FB5' # Warna Label Sumbu Y (Accent Pink)
        ),
    )
    return fig

# Page configuration
st.set_page_config(
    page_title="Hotel Occupancy Analysis Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================================
# Custom CSS untuk styling cantik
# ====================================================================
st.markdown("""
<style>
:root {
    --bg-main: #0B1E39;
    --bg-card: #102A44;
    --accent-blue: #00C9FF;
    --accent-purple: #6C63FF;
    --accent-cyan: #00C9FF;
    --accent-pink: #FF6FB5;
    --text-primary: #F5F5F5;
    --text-secondary: #C7C7C7;
}

/* ===== Hilangkan area putih header Streamlit ===== */
header[data-testid="stHeader"] {
    display: none !important;
}

/* ===== Background utama hanya untuk konten utama (bukan sidebar) ===== */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, var(--bg-main) 0%, var(--bg-card) 100%) !important;
    color: var(--text-primary) !important;
}

/* HILANGKAN SEMUA PADDING ATAS - INI YANG BIKIN PUTIH HILANG */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    margin-top: 0rem !important;
}

.main > div {
    padding-top: 0rem !important;
}

section[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem !important;
}

/* ===== Sidebar fix: muncul + tetap di atas background utama ===== */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1C33 0%, #0B1E39 100%) !important;
    color: var(--text-primary) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    position: relative !important;
    z-index: 10 !important;
    display: flex !important;
    flex-direction: column !important;
}

/* ===== Judul Dashboard ===== */
h1, h2, h3 {
    color: var(--accent-cyan);
    text-align: center;
    font-weight: 700;
}

/* ===== Metric Card ===== */
.metric-card, .stMetric {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
    color: var(--text-primary);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.25s ease-in-out;
}
.metric-card:hover, .stMetric:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 25px rgba(108,99,255,0.4);
}

/* ===== FONT METRIC ===== */
.stMetric label {
    font-size: 18px !important; /* Label (e.g., "📊 Total Bookings") dikecilkan sedikit */
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

.stMetric [data-testid="stMetricValue"] {
    font-size: 40px !important; /* Nilai metrik dibesarkan */
    font-weight: 900 !important;
    color: var(--text-primary) !important;
    text-shadow: 0 0 10px var(--accent-cyan);
}

.stMetric [data-testid="stMetricDelta"] {
    font-size: 18px !important; /* Delta (persentase di bawah) disesuaikan */
    font-weight: 600 !important;
    color: #ffffff !important;
}
/* ========================================= */

/* ===== Tabs ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: var(--bg-card);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
    color: var(--bg-main);
    font-weight: 800;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(108,99,255,0.2);
}

/* ===== Komponen Filter ===== */
div[data-baseweb="select"], .stDateInput, .stMultiSelect, .stTextInput {
    background-color: rgba(16, 42, 68, 0.9) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
div[data-baseweb="select"]:hover, .stDateInput:hover, .stMultiSelect:hover {
    border-color: var(--accent-cyan) !important;
}

/* Warna teks di dalam filter */
.stSelectbox label, .stMultiSelect label, .stDateInput label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}
.stSelectbox div, .stMultiSelect div, .stDateInput div {
    color: var(--text-primary) !important;
}

/* ====== Tag di Multiselect ====== */
.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(135deg, #6C63FF, #00C9FF) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease-in-out;
}
.stMultiSelect [data-baseweb="tag"]:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 10px rgba(0, 201, 255, 0.4);
}
.stMultiSelect [data-baseweb="tag"] svg {
    fill: #ffffff !important;
    opacity: 0.8;
    transition: all 0.2s ease;
}
.stMultiSelect [data-baseweb="tag"] svg:hover {
    fill: #00C9FF !important;
    opacity: 1;
}

/* ====== Border aktif saat filter diklik ====== */
div[data-baseweb="select"]:focus-within {
    border: 1px solid var(--accent-cyan) !important;
    box-shadow: 0 0 8px rgba(0, 201, 255, 0.5);
}

/* ==================================================================== */
/* CSS Khusus untuk Expander Insight */
[data-testid="stExpander"] {
    border-radius: 12px;
    border: 2px solid var(--accent-cyan) !important; /* Border tebal warna accent */
    background-color: rgba(10, 28, 51, 0.9) !important; /* Background agak gelap */
    box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); /* Shadow biru untuk menonjol */
    margin-bottom: 30px; /* Jarak dari tabs */
    padding: 0;
}
[data-testid="stExpander"] div[role="button"] p {
    color: var(--accent-cyan) !important;
    font-weight: 800;
    font-size: 20px;
}
[data-testid="stExpanderContent"] {
    color: var(--text-primary);
    padding: 15px 20px;
    border-top: 1px solid rgba(0, 201, 255, 0.1);
}
[data-testid="stExpanderContent"] h4 {
    color: var(--accent-pink) !important;
    text-align: left;
    font-size: 20px !important;
}
/* ==================================================================== */
</style>
""", unsafe_allow_html=True)

# Load data dengan caching
@st.cache_data
def load_data():
    # PASTIKAN PATH FILE ANDA SUDAH BENAR DI SINI
    df = pd.read_csv("C:/Users/USER/Documents/SEMESTER 3/Dashboard EDA/data/HOTEL_OKUPANSI_FIX.csv")
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    
    # Pastikan kolom event_name ada, kalau tidak buat default
    if 'Name' in df.columns:
        df['Name'] = df['Name'].fillna('No Event')
        df['Name'] = df['Name'].replace('', 'No Event')
        df['Name'] = df['Name'].str.strip()
        df.loc[df['Name'] == '', 'Name'] = 'No Event'
    else:
        df['Name'] = 'No Event'
    
    return df
# Load data

try:
    df = load_data()

    
    # Sidebar
    st.sidebar.title("🏨 Filter & Pengaturan")
    st.sidebar.markdown("---")
    
    # Filter Hotel
    st.sidebar.subheader("🏢 Filter Hotel")
    hotel_options = ['Semua Hotel'] + list(df['hotel'].unique())
    selected_hotel = st.sidebar.selectbox("Pilih Hotel", hotel_options)
    
    # Filter Tahun
    st.sidebar.subheader("📅 Filter Waktu")
    year_options = sorted(df['year'].unique())
    selected_years = st.sidebar.multiselect(
        "Pilih Tahun",
        options=year_options,
        default=year_options
    )
    
    # Date Range
    st.sidebar.subheader("🗓️ Rentang Tanggal")
    min_date = df['arrival_date'].min()
    max_date = df['arrival_date'].max()
    date_range = st.sidebar.date_input(
        "Pilih Rentang",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter Bulan
    st.sidebar.subheader("🗓️ Filter Bulan")
    month_options = sorted(df['month'].unique())
    selected_months = st.sidebar.multiselect(
        "Pilih Bulan",
        options=month_options,
        default=month_options
    )
    
    # Filter Season
    st.sidebar.subheader("🌤️ Filter Musim")
    season_options = df['season'].unique()
    selected_seasons = st.sidebar.multiselect(
        "Pilih Musim",
        options=season_options,
        default=season_options
    )
    
    # Filter Analisis Khusus
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Fokus Analisis")
    show_only_holidays = st.sidebar.checkbox("🎉 Hanya Hari Libur", False)
    show_only_events = st.sidebar.checkbox("🎪 Hanya Hari Event", False)
    exclude_canceled = st.sidebar.checkbox("✅ Exclude Cancellations", True)
    
    # Pengaturan Visualisasi
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Pengaturan Tampilan")
    
    # --- PERBAIKAN FATAL ERROR METRIK RATA-RATA ---
    metric_display_options = ["Rata-rata", "Median", "Total"]
    metric_type = st.sidebar.radio(
        "Metrik Okupansi",
        metric_display_options,
        index=0 # Default ke Rata-rata
    )
    
    # Peta label Bahasa Indonesia ke fungsi Pandas yang valid (Bahasa Inggris)
    metric_map = {
        "Rata-rata": "mean",
        "Median": "median",
        "Total": "sum"
    }
    selected_agg_func = metric_map.get(metric_type, "mean")
    # --------------------------------------------
    
    # Reset Button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Semua Filter"):
        st.rerun()
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_hotel != 'Semua Hotel':
        filtered_df = filtered_df[filtered_df['hotel'] == selected_hotel]
    
    if selected_years:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
    
    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df['arrival_date'] >= start_date) &
            (filtered_df['arrival_date'] <= end_date)
        ]
    
    if selected_months:
        filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]
    
    if selected_seasons:
        filtered_df = filtered_df[filtered_df['season'].isin(selected_seasons)]
    
    if show_only_holidays:
        filtered_df = filtered_df[filtered_df['is_holiday'] == 1]
    
    if show_only_events:
        filtered_df = filtered_df[filtered_df['is_event_day'] == 1]
    
    if exclude_canceled:
        filtered_df = filtered_df[filtered_df['is_canceled'] == 0]
    
    # Info Dataset di Sidebar
    st.sidebar.markdown("---")
    
    if len(filtered_df) == 0:
        st.sidebar.warning("Tidak ada data yang tersedia untuk filter ini.")
        st.title("❌ Tidak Ada Data")
        st.error("Tidak ada data yang cocok dengan kriteria filter yang dipilih.")
        st.stop()
        
    st.sidebar.info(f"""
    📊 **Info Dataset**
    - Total Bookings: **{len(filtered_df):,}**
    - Periode: **{filtered_df['arrival_date'].min().strftime('%d %b %Y')}** - **{filtered_df['arrival_date'].max().strftime('%d %b %Y')}**
    - Hotels: **{filtered_df['hotel'].nunique()}**
    """)
    
    # Main Dashboard
    st.title("🏨 Dashboard Analisis Pengaruh Hari Libur & Event")
    st.markdown("---")
    
    # Summary Metrics
    total_df_len = len(df)
    
    # Okupansi untuk Hari Biasa vs Libur
    df_normal = filtered_df[filtered_df['is_holiday'] == 0]['occupancy_per_hari']
    df_holiday = filtered_df[filtered_df['is_holiday'] == 1]['occupancy_per_hari']
    
    occupancy_normal = df_normal.agg(selected_agg_func) if len(df_normal) > 0 else 0
    occupancy_holiday = df_holiday.agg(selected_agg_func) if len(df_holiday) > 0 else 0
    
    # Okupansi untuk Hari Event vs Non-Event
    df_no_event = filtered_df[filtered_df['is_event_day'] == 0]['occupancy_per_hari']
    df_event = filtered_df[filtered_df['is_event_day'] == 1]['occupancy_per_hari']
    
    occupancy_no_event = df_no_event.agg(selected_agg_func) if len(df_no_event) > 0 else 0
    occupancy_event = df_event.agg(selected_agg_func) if len(df_event) > 0 else 0
    
    # ADR dan Cancellation Rate
    total_bookings = len(filtered_df)
    avg_adr = filtered_df['adr'].mean() if total_bookings > 0 else 0
    initial_filtered_df = df[df.index.isin(filtered_df.index)]
    cancellation_rate = (initial_filtered_df['is_canceled'].sum() / len(initial_filtered_df)) * 100 if len(initial_filtered_df) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📊 Total Bookings",
            value=f"{total_bookings:,}",
            delta=f"{(total_bookings/total_df_len*100):.1f}% dari total" if total_df_len > 0 else "0.0% dari total"
        )
    
    with col2:
        diff_holiday = ((occupancy_holiday - occupancy_normal) / occupancy_normal * 100) if occupancy_normal > 0 else 0
        st.metric(
            label="🎉 Okupansi Hari Libur",
            value=f"{occupancy_holiday:.2f}%",
            delta=f"{diff_holiday:+.1f}% vs normal"
        )
    
    with col3:
        diff_event = ((occupancy_event - occupancy_no_event) / occupancy_no_event * 100) if occupancy_no_event > 0 else 0
        st.metric(
            label="🎪 Okupansi Hari Event",
            value=f"{occupancy_event:.2f}%",
            delta=f"{diff_event:+.1f}% vs non-event"
        )
    
    with col4:
        st.metric(
            label="💰 Rata-rata ADR",
            value=f"${avg_adr:.2f}",
            delta=f"Cancel: {cancellation_rate:.1f}%"
        )
    
    st.markdown("---")

    # INSIGHTS (DITAMPILKAN DI BAWAH METRIC CARD SESUAI PERMINTAAN AWAL)
    diff_holiday = ((occupancy_holiday - occupancy_normal) / occupancy_normal * 100) if occupancy_normal > 0 else 0
    diff_event = ((occupancy_event - occupancy_no_event) / occupancy_no_event * 100) if occupancy_no_event > 0 else 0

    # Pastikan Expander selalu terlihat (expanded=True)
    with st.expander("✨ Klik untuk Ringkasan dan Insight Utama", expanded=True):
        st.markdown("#### **Kesimpulan Cepat dari Data Terfilter**")

        # Insight 1: Pengaruh Hari Libur
        holiday_msg = ""
        if diff_holiday > 5:
            holiday_msg = f"Okupansi di **Hari Libur** adalah **{occupancy_holiday:.2f}%**, yang berarti **{diff_holiday:+.1f}% lebih tinggi** dari hari biasa ({occupancy_normal:.2f}%). **Prioritaskan promosi saat liburan.**"
            holiday_emoji = "🚀"
        elif diff_holiday > 0:
            holiday_msg = f"Okupansi di **Hari Libur** ({occupancy_holiday:.2f}%) sedikit **lebih tinggi** ({diff_holiday:+.1f}%) dibandingkan hari biasa ({occupancy_normal:.2f}%)."
            holiday_emoji = "⬆️"
        elif diff_holiday < 0:
            holiday_msg = f"Okupansi di **Hari Libur** ({occupancy_holiday:.2f}%) sedikit **lebih rendah** ({diff_holiday:+.1f}%) dibandingkan hari biasa ({occupancy_normal:.2f}%). **Perlu tinjauan strategi liburan.**"
            holiday_emoji = "📉"
        else:
            holiday_msg = "Okupansi Hari Libur dan Hari Biasa menunjukkan nilai yang relatif sama."
            holiday_emoji = "⚖️"

        # Insight 2: Pengaruh Event
        event_msg = ""
        if diff_event > 5:
            event_msg = f"Hari **Event** menunjukkan Okupansi rata-rata **{occupancy_event:.2f}%**, **{diff_event:+.1f}% lebih tinggi** dari hari tanpa event ({occupancy_no_event:.2f}%). **Event sangat efektif meningkatkan hunian.**"
            event_emoji = "🎉"
        elif diff_event > 0:
            event_msg = f"Okupansi di **Hari Event** ({occupancy_event:.2f}%) sedikit **lebih tinggi** ({diff_event:+.1f}%) dibandingkan hari non-event ({occupancy_no_event:.2f}%)."
            event_emoji = "⬆️"
        elif diff_event < 0:
            event_msg = f"Hari **Event** ({occupancy_event:.2f}%) menunjukkan sedikit **penurunan** Okupansi ({diff_event:+.1f}%) dibandingkan hari tanpa event ({occupancy_no_event:.2f}%). **Perlu analisis event mana yang tidak optimal.**"
            event_emoji = "⚠️"
        else:
            event_msg = "Okupansi Hari Event dan Hari Non-Event menunjukkan nilai yang relatif sama."
            event_emoji = "⚖️"
        
        # Insight 3: Cancelation Rate
        cancel_msg = f"Dengan tingkat pembatalan **{cancellation_rate:.1f}%**, manajemen perlu meninjau kembali kebijakan booking dan deposit untuk mengurangi kerugian."
        cancel_emoji = "🛑"
        
        st.markdown(f"""
        - {holiday_emoji} **Okupansi Liburan**: {holiday_msg}
        - {event_emoji} **Okupansi Event**: {event_msg}
        """)
        
    st.markdown("---")
    # ====================================================================
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trend Analysis", 
        "📊 Comparison", 
        "🗓️ Calendar View", 
        "📋 Detailed Data",
        "🎪 Event List"
    ])
    
    with tab1:
        st.subheader("📈 Trend Okupansi dari Waktu ke Waktu")
        
        # Time series dengan highlight - tambahkan info event
        daily_data = filtered_df.groupby('arrival_date').agg({
            'occupancy_per_hari': selected_agg_func, # Menggunakan selected_agg_func yang sudah di-map
            'is_holiday': 'max',
            'is_event_day': 'max',
            'total_tamu': 'sum',
            'adr': 'mean',
            'Name': lambda x: ', '.join(x[x != 'No Event'].unique()) if len(x[x != 'No Event']) > 0 else 'Hari Biasa' 
        }).reset_index().sort_values('arrival_date')

        # --- PERBAIKAN LOGIKA DAY_TYPE AGAR HOVER AKURAT ---
        daily_data['Day_Type'] = 'Hari Biasa'
        
        # PENTING: Urutan penentuan kategori harus dari yang paling spesifik (Libur & Event) ke yang paling umum (Libur/Event)
        daily_data.loc[(daily_data['is_holiday'] == 1) & (daily_data['is_event_day'] == 1), 'Day_Type'] = '🥳 Libur & Event'
        daily_data.loc[(daily_data['is_holiday'] == 1) & (daily_data['is_event_day'] == 0), 'Day_Type'] = '🎉 Hari Libur'
        daily_data.loc[(daily_data['is_holiday'] == 0) & (daily_data['is_event_day'] == 1), 'Day_Type'] = '🎪 Hari Event'
        # Hari Biasa sudah default
        
        fig_trend = go.Figure()
        
        # Main line
        fig_trend.add_trace(go.Scatter(
            x=daily_data['arrival_date'],
            y=daily_data['occupancy_per_hari'],
            mode='lines',
            name='Okupansi',
            line=dict(color='#667eea', width=2),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)',
            customdata=daily_data[['Name', 'Day_Type', 'is_holiday', 'is_event_day']],
            hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                          'Tipe Hari: <b>%{customdata[1]}</b><br>' + # Menggunakan Day_Type yang sudah diklasifikasi
                          f'{metric_type} Okupansi: %{{y:.2f}}%<br>' + 
                          'Event/Libur: %{customdata[0]}<br>' +
                          '<extra></extra>'
        ))
        
        # Marker Hari Libur Murni (Hanya Libur, bukan Event)
        holidays_only = daily_data[(daily_data['is_holiday'] == 1) & (daily_data['is_event_day'] == 0)]
        if len(holidays_only) > 0:
            fig_trend.add_trace(go.Scatter(
                x=holidays_only['arrival_date'],
                y=holidays_only['occupancy_per_hari'],
                mode='markers',
                name='Hari Libur',
                marker=dict(color="#ff6b6b", size=5, line=dict(width=1, color='White')),
                showlegend=True,
                customdata=holidays_only[['Name', 'Day_Type']],
                hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                              'Tipe Hari: <b>🎉 Hari Libur</b><br>' +
                              f'{metric_type} Okupansi: %{{y:.2f}}%<br>' +
                              'Libur: %{customdata[0]}<br>' +
                              '<extra></extra>'
            ))
        
        # Marker Hari Event Murni (Hanya Event, bukan Libur)
        events_only = daily_data[(daily_data['is_event_day'] == 1) & (daily_data['is_holiday'] == 0)]
        if len(events_only) > 0:
            fig_trend.add_trace(go.Scatter(
                x=events_only['arrival_date'],
                y=events_only['occupancy_per_hari'],
                mode='markers',
                name='Hari Event',
                marker=dict(color='#feca57', size=5, line=dict(width=1, color='White')),
                showlegend=True,
                customdata=events_only[['Name', 'Day_Type']],
                hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                              'Tipe Hari: <b>🎪 Hari Event</b><br>' +
                              f'{metric_type} Okupansi: %{{y:.2f}}%<br>' +
                              'Event: %{customdata[0]}<br>' +
                              '<extra></extra>'
            ))

        # Marker Hari Libur & Event (Keduanya)
        both_days = daily_data[(daily_data['is_holiday'] == 1) & (daily_data['is_event_day'] == 1)]
        if len(both_days) > 0:
            fig_trend.add_trace(go.Scatter(
                x=both_days['arrival_date'],
                y=both_days['occupancy_per_hari'],
                mode='markers',
                name='Libur & Event',
                marker=dict(color='#9370DB', size=5, line=dict(width=1, color='White')),
                showlegend=True,
                customdata=both_days[['Name', 'Day_Type']],
                hovertemplate='<b>%{x|%d %b %Y}</b><br>' +
                              'Tipe Hari: <b>🥳 Libur & Event</b><br>' +
                              f'{metric_type} Okupansi: %{{y:.2f}}%<br>' +
                              'Detail: %{customdata[0]}<br>' +
                              '<extra></extra>'
            ))
        
        fig_trend.update_layout(
            title="Trend Okupansi Harian dengan Highlight Hari Libur & Event",
            xaxis_title="Tanggal Kedatangan", 
            yaxis_title=f"{metric_type} Okupansi Harian (%)", 
            hovermode='closest',
            height=500,
            template='plotly_white'
        )
        fig_trend = update_plot_layout(fig_trend)
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Monthly trend
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_data = filtered_df.groupby(['year', 'month'])['occupancy_per_hari'].agg(selected_agg_func).reset_index()
            monthly_data['year_month'] = monthly_data['year'].astype(str) + '-' + monthly_data['month'].astype(str).str.zfill(2)
            
            fig_monthly = px.line(
                monthly_data,
                x='year_month',
                y='occupancy_per_hari',
                title=f'Trend Okupansi Bulanan ({metric_type})',
                markers=True,
                color_discrete_sequence=['#764ba2']
            )
            fig_monthly.update_layout(
                xaxis_title="Tahun-Bulan", 
                yaxis_title=f"{metric_type} Okupansi (%)", 
                height=350
            )
            fig_monthly = update_plot_layout(fig_monthly)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            season_data = filtered_df.groupby('season')['occupancy_per_hari'].agg(selected_agg_func).reset_index()
            season_data.columns = ['Musim', 'Okupansi']

            fig_season = px.pie(
                season_data,
                names='Musim',
                values='Okupansi',
                title=f'{metric_type} Okupansi per Musim',
                color='Musim',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            fig_season.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#102A44', width=2)))
            fig_season.update_layout(height=350, margin=dict(t=50, b=0, l=0, r=0))
            fig_season = update_plot_layout(fig_season)
            st.plotly_chart(fig_season, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Perbandingan Okupansi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            comparison_holiday = pd.DataFrame({
                'Kategori': ['Hari Biasa', 'Hari Libur'],
                'Okupansi': [occupancy_normal, occupancy_holiday],
                'Jumlah Hari': [
                    len(filtered_df[filtered_df['is_holiday'] == 0]),
                    len(filtered_df[filtered_df['is_holiday'] == 1])
                ]
            })
            
            fig_holiday = go.Figure(data=[
                go.Bar(
                    x=comparison_holiday['Kategori'],
                    y=comparison_holiday['Okupansi'],
                    text=comparison_holiday['Okupansi'].round(2),
                    textposition='auto',
                    marker=dict(
                        color=['#667eea', '#ff6b6b'],
                        line=dict(color='white', width=2)
                    )
                )
            ])
            
            fig_holiday.update_layout(
                title=f"Perbandingan: Hari Libur vs Hari Biasa ({metric_type})",
                yaxis_title=f"{metric_type} Okupansi (%)",
                xaxis_title="Kategori Hari",
                height=400,
                showlegend=False
            )
            fig_holiday = update_plot_layout(fig_holiday)
            
            st.plotly_chart(fig_holiday, use_container_width=True)
        
        with col2:
            comparison_event = pd.DataFrame({
                'Kategori': ['Non-Event', 'Hari Event'],
                'Okupansi': [occupancy_no_event, occupancy_event],
                'Jumlah Hari': [
                    len(filtered_df[filtered_df['is_event_day'] == 0]),
                    len(filtered_df[filtered_df['is_event_day'] == 1])
                ]
            })
            
            fig_event = go.Figure(data=[
                go.Bar(
                    x=comparison_event['Kategori'],
                    y=comparison_event['Okupansi'],
                    text=comparison_event['Okupansi'].round(2),
                    textposition='auto',
                    marker=dict(
                        color=['#764ba2', '#feca57'],
                        line=dict(color='white', width=2)
                    )
                )
            ])
            
            fig_event.update_layout(
                title=f"Perbandingan: Hari Event vs Non-Event ({metric_type})",
                yaxis_title=f"{metric_type} Okupansi (%)",
                xaxis_title="Kategori Hari",
                height=400,
                showlegend=False
            )
            fig_event = update_plot_layout(fig_event)
            
            st.plotly_chart(fig_event, use_container_width=True)
        
        st.subheader("📦 Distribusi Okupansi")
        
        fig_box = go.Figure()
        
        fig_box.add_trace(go.Box(
            y=filtered_df[filtered_df['is_holiday'] == 0]['occupancy_per_hari'],
            name='Hari Biasa',
            marker_color='#667eea'
        ))
        
        fig_box.add_trace(go.Box(
            y=filtered_df[filtered_df['is_holiday'] == 1]['occupancy_per_hari'],
            name='Hari Libur',
            marker_color="#5fa6cc"
        ))
        
        fig_box.add_trace(go.Box(
            y=filtered_df[filtered_df['is_event_day'] == 1]['occupancy_per_hari'],
            name='Hari Event',
            marker_color='#feca57'
        ))
        
        fig_box.update_layout(
            title="Distribusi Okupansi: Hari Biasa vs Libur vs Event",
            yaxis_title="Okupansi (%)",
            height=400
        )
        fig_box = update_plot_layout(fig_box)
        
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        st.subheader("🗓️ Heatmap Okupansi")
        
        if 'arrival_date_day_of_month' not in filtered_df.columns:
            filtered_df['arrival_date_day_of_month'] = filtered_df['arrival_date'].dt.day
            
        heatmap_data = filtered_df.groupby(['month', 'arrival_date_day_of_month'])['occupancy_per_hari'].agg(selected_agg_func).reset_index()
        heatmap_pivot = heatmap_data.pivot(index='arrival_date_day_of_month', columns='month', values='occupancy_per_hari')
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='RdYlGn',
            text=heatmap_pivot.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title=f"Okupansi ({metric_type}) (%)")
        ))
        
        fig_heatmap.update_layout(
            title=f'Heatmap Okupansi ({metric_type}) per Bulan dan Tanggal',
            xaxis_title='Bulan',
            yaxis_title='Tanggal (Hari ke-)',
            height=600
        )
        fig_heatmap = update_plot_layout(fig_heatmap)
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        filtered_df['day_of_week'] = filtered_df['arrival_date'].dt.day_name()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_data = filtered_df.groupby('day_of_week')['occupancy_per_hari'].agg(selected_agg_func).reindex(dow_order).reset_index()
        
        fig_dow = px.bar(
            dow_data,
            x='day_of_week',
            y='occupancy_per_hari',
            title=f'{metric_type} Okupansi per Hari dalam Seminggu',
            color='occupancy_per_hari',
            color_continuous_scale='Plasma'
        )
        fig_dow.update_layout(
            xaxis_title='Hari dalam Seminggu',
            yaxis_title=f'{metric_type} Okupansi (%)',
            height=400
        )
        fig_dow = update_plot_layout(fig_dow)
        st.plotly_chart(fig_dow, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Data Detail")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🏆 Top 10 Hari Libur dengan Okupansi {metric_type} Tertinggi")
            top_holidays = filtered_df[filtered_df['is_holiday'] == 1].nlargest(10, 'occupancy_per_hari')[
                ['arrival_date', 'hotel', 'Name', 'occupancy_per_hari', 'adr', 'total_tamu']
            ]
            st.dataframe(top_holidays, use_container_width=True)
        
        with col2:
            st.markdown(f"#### 🎪 Top 10 Hari Event dengan Okupansi {metric_type} Tertinggi")
            top_events = filtered_df[filtered_df['is_event_day'] == 1].nlargest(10, 'occupancy_per_hari')[
                ['arrival_date', 'hotel', 'Name', 'occupancy_per_hari', 'adr', 'total_tamu']
            ]
            st.dataframe(top_events, use_container_width=True)
        
            st.markdown("---")
            st.markdown("#### 📥 Download Data Terfilter")
        
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"hotel_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
        
            st.markdown("#### 👀 Preview Data (100 baris pertama)")
            st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # TAB 5 - EVENT LIST
    with tab5:
        st.subheader("🎪 Daftar Event & Hari Libur")
        
        events_df = filtered_df[
            (filtered_df['is_holiday'] == 1) | 
            (filtered_df['is_event_day'] == 1)
        ].copy()
        
        if len(events_df) > 0:
            events_summary = events_df.groupby(['arrival_date', 'Name']).agg({
                'occupancy_per_hari': selected_agg_func,
                'is_holiday': 'max',
                'is_event_day': 'max',
                'total_tamu': 'sum',
                'adr': 'mean'
            }).reset_index().sort_values('arrival_date', ascending=False)
            
            events_summary['Kategori'] = events_summary.apply(
                lambda row: '🎉 Hari Libur' if row['is_holiday'] == 1 else '🎪 Event', 
                axis=1
            )
            
            events_summary_display = events_summary[[
                'arrival_date', 'Name', 'Kategori', 
                'occupancy_per_hari', 'total_tamu', 'adr'
            ]].copy()
            
            events_summary_display.columns = [
                'Tanggal', 'Nama Event', 'Kategori', 
                f'Okupansi ({metric_type}) (%)', 'Total Tamu', 'ADR ($)'
            ]
            
            events_summary_display[f'Okupansi ({metric_type}) (%)'] = events_summary_display[f'Okupansi ({metric_type}) (%)'].round(2)
            events_summary_display['ADR ($)'] = events_summary_display['ADR ($)'].round(2)
            
            st.dataframe(
                events_summary_display,
                use_container_width=True,
                height=600
            )
            
            st.markdown("---")
            csv_events = events_summary_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Daftar Event (CSV)",
                data=csv_events,
                file_name=f"event_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Event", len(events_summary))
            with col2:
                st.metric("Hari Libur", len(events_summary[events_summary['is_holiday'] == 1]))
            with col3:
                st.metric("Hari Event Khusus", len(events_summary[events_summary['is_event_day'] == 1]))
        else:
            st.info("Tidak ada event atau hari libur dalam data yang difilter.")

except FileNotFoundError:
    st.error("❌ File tidak ditemukan! Pastikan path file CSV sudah benar.")
    st.info("Path yang dicari: C:/Users/USER/Documents/SEMESTER 3/Dashboard EDA/data/HOTEL_OKUPANSI_FIX.csv")
except Exception as e:
    st.error(f"❌ Terjadi error: {str(e)}")
    st.info("Silakan cek kembali data dan format kolom CSV Anda.")