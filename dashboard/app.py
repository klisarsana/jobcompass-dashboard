import streamlit as st
import pandas as pd
import plotly.express as px
import collections
import re

# Page Configuration
st.set_page_config(
    page_title="JobCompass - Market Insights Dashboard",
    layout="wide"
)

# Konfigurasi Warna Tema (Gradasi Merah Gelap ke Terang)
RED_GRADIENT = ['#330000', '#660000', '#990000', '#CC0000', '#FF0000', '#FF4D4D', '#FF9999']
SOLID_RED = '#FF4D4D' # Untuk grafik yang tidak butuh gradasi (seperti Box Plot)

# Judul Utama Dashboard
st.title("JobCompass: Market Insights Dashboard")
st.markdown("Analisis komprehensif tren lowongan kerja, peta kompensasi global, dan kebutuhan keterampilan industri.")

# Load Data
@st.cache_data
def load_data():
# 1. Dapatkan lokasi folder dari file app.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Gabungkan lokasi tersebut dengan path menuju CSV
    file_path = os.path.join(current_dir, '../data/processed/dataset_clean.csv')

    # 3. Baca CSV menggunakan path yang sudah pasti tersebut
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.title('JobCompass')
    st.markdown('---')

# Filter Kategori Pekerjaan
    if 'category' in df.columns:
        all_categories = ['Semua Kategori'] + list(df['category'].dropna().unique())
        selected_category = st.sidebar.selectbox("Pilih Kategori Pekerjaan:", all_categories)
    else:
        selected_category = 'Semua Kategori'

    # Filter Rentang Gaji (USD)
    if 'avg_sal_dollar' in df.columns:
        min_val = float(df['avg_sal_dollar'].min())
        max_val = float(df['avg_sal_dollar'].max())
        
        selected_salary_range = st.sidebar.slider(
            "Rentang Gaji Rata-rata (USD):",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            step=1000.0
        )
        
    st.markdown('---')

# Menerapkan Filter ke Dataset
if 'avg_sal_dollar' in df.columns:
    df_filtered = df[(df['avg_sal_dollar'] >= selected_salary_range[0]) & (df['avg_sal_dollar'] <= selected_salary_range[1])]
else:
    df_filtered = df.copy()

if selected_category != 'Semua Kategori' and 'category' in df.columns:
    df_filtered = df_filtered[df_filtered['category'] == selected_category]


# Summary metrics
st.markdown("### 📊 Ringkasan Data Pasar Kerja")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Posisi Lowongan", f"{len(df_filtered)} lowongan")
with col2:
    if 'avg_sal_dollar' in df.columns and len(df_filtered) > 0:
        st.metric("Rata-rata Gaji Pasar", f"$ {df_filtered['avg_sal_dollar'].mean():,.0f} / tahun")
with col3:
    if 'category' in df_filtered.columns and len(df_filtered) > 0:
        top_cat = df_filtered['category'].value_counts().index[0]
        st.metric("Sektor Teraktif", str(top_cat))

st.markdown("---")


# Navigasi Tabs (Section)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Permintaan Pasar", 
    "💰 Analisis Kompensasi (USD)", 
    "🔑 Keterampilan Krusial (Key Skills)", 
    "🔍 Eksplorasi Master Data"
])


# TAB 1: PERMINTAAN PASAR KERJA

with tab1:
    st.subheader("Pertanyaan Bisnis: Kategori pekerjaan apa yang paling banyak dicari oleh pasar?")
    
    if 'category' in df_filtered.columns and len(df_filtered) > 0:
        category_counts = df_filtered['category'].value_counts().reset_index()
        category_counts.columns = ['Kategori', 'Jumlah Lowongan']
        
        # Grafik Bar dengan Gradasi Merah
        fig_bar = px.bar(
            category_counts, 
            x='Kategori', 
            y='Jumlah Lowongan',
            title="Distribusi Jumlah Lowongan per Kategori Pekerjaan",
            color='Jumlah Lowongan', 
            color_continuous_scale=RED_GRADIENT
        )
        st.plotly_chart(fig_bar, width='stretch')
        
        # SEKTOR INSIGHT & KESIMPULAN
        st.markdown("#### 💡 Insight & Kesimpulan Bisnis:")
        st.info(
            f"1. **Dominasi Pasar**: Berdasarkan volume lowongan saat ini, kategori **{category_counts.iloc[0]['Kategori']}** merupakan sektor yang paling agresif melakukan perekrutan tenaga kerja baru.\n"
            f"2. **Peta Penyerapan Tenaga Kerja**: Perbedaan tinggi batang grafik menunjukkan ketimpangan penyerapan kebutuhan industri. Sektor dengan volume rekrutmen tinggi mencerminkan area ekspansi bisnis utama korporasi saat ini.\n"
            f"3. **Kesimpulan**: Perusahaan sedang berfokus melakukan investasi besar-besaran pada sektor-sektor teratas. Bagi institusi pendidikan atau pencari kerja, menyelaraskan keahlian ke arah kategori dominan ini akan memperbesar peluang keterserapan di bursa kerja."
        )
    else:
        st.warning("Data kategori tidak memadai untuk ditampilkan.")


# TAB 2: ANALISIS KOMPENSASI GAJI
with tab2:
    st.subheader("Pertanyaan Bisnis: Bagaimana sebaran dan disparitas tawaran kompensasi keuangan antar kategori?")
    
    if 'category' in df_filtered.columns and 'avg_sal_dollar' in df_filtered.columns and len(df_filtered) > 0:
        # Agregasi gaji
        salary_agg = df_filtered.groupby('category')['avg_sal_dollar'].mean().sort_values(ascending=False).reset_index()
        
        # Bar Chart Rata-rata Gaji (Gradasi Merah)
        fig_salary = px.bar(
            salary_agg,
            x='category',
            y='avg_sal_dollar',
            title="Rata-rata Gaji Tahunan (USD) per Kategori",
            labels={'avg_sal_dollar': 'Rata-rata Gaji ($)', 'category': 'Kategori'},
            color='avg_sal_dollar',
            color_continuous_scale=RED_GRADIENT
        )
        st.plotly_chart(fig_salary, width='stretch')
        
        # Box Plot Sebaran Rentang Gaji (Warna Merah Solid)
        fig_box = px.box(
            df_filtered,
            x='category',
            y='avg_sal_dollar',
            title="Rentang Distribusi dan Variasi Gaji per Kategori",
            labels={'avg_sal_dollar': 'Gaji Rata-rata (USD)', 'category': 'Kategori'},
            color_discrete_sequence=[SOLID_RED]
        )
        st.plotly_chart(fig_box, width='stretch')
        
        # SEKTOR INSIGHT & KESIMPULAN
        st.markdown("#### 💡 Insight & Kesimpulan Bisnis:")
        st.success(
            f"1. **Komparasi Tertinggi**: Kategori pekerjaan dengan rata-rata nilai kompensasi tertinggi dipegang oleh **{salary_agg.iloc[0]['category']}** dengan nilai rata-rata mencapai ${salary_agg.iloc[0]['avg_sal_dollar']:,.0f}.\n"
            f"2. **Analisis Variasi (Boxplot)**: Rentang kotak yang lebar serta kemunculan titik outlier di atas garis whisker menandakan adanya stratifikasi gaji yang kuat di dalam kategori tersebut. Hal ini umumnya dipengaruhi oleh level senioritas ekstrem (misal: posisi dengan pengalaman 12+ tahun) atau skala finansial perusahaan perekrut.\n"
            f"3. **Kesimpulan**: Sektor yang memiliki volume lowongan sedikit (pada Tab Permintaan Pasar) seringkali mengompensasikannya dengan nilai rata-rata gaji yang jauh lebih tinggi demi memperebutkan talenta spesifik (*scarcity premium*)."
        )
    else:
        st.warning("Data gaji atau kategori tidak mencukupi.")

# TAB 3: PERTANYAAN BISNIS - KEY SKILLS
with tab3:
    st.subheader("Pertanyaan Bisnis: Keterampilan (Key Skills) apa saja yang paling krusial dan sering dicari oleh perusahaan?")
    
    # Algoritma Ekstraksi Skill
    if 'key_skills' in df_filtered.columns:
        skills_series = df_filtered['key_skills'].dropna().str.split(',')
        all_skills = [skill.strip().title() for sublist in skills_series for skill in sublist if skill.strip()]
        skills_df = pd.DataFrame(collections.Counter(all_skills).most_common(10), columns=['Keterampilan', 'Frekuensi'])
    else:
        text_col = 'description' if 'description' in df_filtered.columns else ('clean_desc' if 'clean_desc' in df_filtered.columns else 'job_title')
        common_market_skills = ['SQL', 'Python', 'Excel', 'Marketing', 'Sales', 'Management', 'Finance', 'Java', 'Graphic Design', 'Communication', 'Data Analysis', 'Project Management', 'HR', 'UI/UX']
        
        skill_counts = {}
        if text_col in df_filtered.columns:
            text_data = df_filtered[text_col].dropna().str.upper()
            for skill in common_market_skills:
                count = text_data.str.contains(r'\b' + re.escape(skill.upper()) + r'\b', regex=True).sum()
                if count > 0:
                    skill_counts[skill] = count
        skills_df = pd.DataFrame(list(skill_counts.items()), columns=['Keterampilan', 'Frekuensi']).sort_values(by='Frekuensi', ascending=False).head(10)

    if len(skills_df) > 0:
        # Grafik Bar Horizontal untuk Skill (Gradasi Merah)
        fig_skills = px.bar(
            skills_df,
            y='Keterampilan',
            x='Frekuensi',
            orientation='h',
            title="Top 10 Keterampilan (Key Skills) yang Paling Sering Muncul pada Lowongan Kerja",
            color='Frekuensi',
            color_continuous_scale=RED_GRADIENT
        )
        fig_skills.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_skills, width='stretch')

        # SEKTOR INSIGHT & KESIMPULAN
        st.markdown("#### 💡 Insight & Kesimpulan Bisnis (Analisis Keterampilan):")
        st.info(
            f"1. **Keterampilan Paling Utama**: Berdasarkan ekstraksi data tekstual lowongan, keterampilan **{skills_df.iloc[0]['Keterampilan']}** menempati posisi teratas sebagai core skill yang paling sering disyaratkan oleh korporasi.\n"
            f"2. **Pola Kebutuhan Korporasi**: Keterampilan dasar manajemen/komunikasi berdampingan erat dengan kapabilitas teknis (seperti pengolahan data atau teknologi informasi). Ini membuktikan bahwa industri saat ini mencari karakter kandidat yang bersifat *T-Shaped* (memiliki keahlian spesifik yang dalam namun ditunjang koordinasi umum yang luas).\n"
            f"3. **Kesimpulan Jawaban Bisnis**: Keterampilan yang paling krusial bukan lagi sekadar kemampuan teknis tunggal, melainkan kombinasi fleksibel antara alat produktivitas kerja (data-driven tools) dan kecakapan manajerial eksekusi proyek. Fokus pengembangan diri pada top 3 keahlian di atas akan memberikan keunggulan kompetitif terbesar bagi kandidat di pasar kerja global."
        )
    else:
        st.warning("Teks deskripsi atau kolom keterampilan tidak ditemukan untuk dianalisis frekuensinya.")

# TAB 4: EKSPLORASI DATA
with tab4:
    st.subheader("Eksplorasi Data Lanjutan")
    st.markdown("Gunakan kolom pencarian di bawah untuk memfilter data berdasarkan kata kunci jabatan spesifik.")
    
    search_query = st.text_input("Cari kata kunci pada judul pekerjaan (Job Title):")
    if search_query and 'job_title' in df_filtered.columns:
        tabel_tampil = df_filtered[df_filtered['job_title'].str.contains(search_query, case=False, na=False)]
    else:
        tabel_tampil = df_filtered
        
    st.dataframe(tabel_tampil, width='stretch')