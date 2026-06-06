import streamlit as st
 
# =========================================
# CONFIG PAGE
# =========================================
st.set_page_config(
    page_title="Calculator Standardisasi Larutan",
    page_icon="🧪",
    layout="wide"
)
 
# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
 
/* ---- BACKGROUND PATTERN ---- */
body, .stApp {
    background-color: #F0FDFA;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cdefs%3E%3Cpattern id='hex' patternUnits='userSpaceOnUse' width='120' height='104' x='0' y='0'%3E%3C!-- Hexagon outline --%3E%3Cpolygon points='60,4 110,32 110,72 60,100 10,72 10,32' fill='none' stroke='%2399f6e4' stroke-width='1.2' opacity='0.55'/%3E%3C!-- Atom center dot --%3E%3Ccircle cx='60' cy='52' r='3.5' fill='%2314B8A6' opacity='0.25'/%3E%3C!-- Electron orbits (3 ellipses) --%3E%3Cellipse cx='60' cy='52' rx='18' ry='7' fill='none' stroke='%2314B8A6' stroke-width='0.9' opacity='0.2'/%3E%3Cellipse cx='60' cy='52' rx='18' ry='7' fill='none' stroke='%2314B8A6' stroke-width='0.9' opacity='0.2' transform='rotate(60 60 52)'/%3E%3Cellipse cx='60' cy='52' rx='18' ry='7' fill='none' stroke='%2314B8A6' stroke-width='0.9' opacity='0.2' transform='rotate(120 60 52)'/%3E%3C!-- Small corner dots (bond nodes) --%3E%3Ccircle cx='10' cy='32' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3Ccircle cx='110' cy='32' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3Ccircle cx='10' cy='72' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3Ccircle cx='110' cy='72' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3Ccircle cx='60' cy='4' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3Ccircle cx='60' cy='100' r='2' fill='%2399f6e4' opacity='0.3'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23hex)'/%3E%3C/svg%3E");
}
 
.main {
    background-color: transparent;
}
 
h1, h2, h3 {
    color: #0F172A;
}
 
.stButton>button {
    background-color: #14B8A6;
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
 
.stButton>button:hover {
    background-color: #0D9488;
    color: white;
}
 
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 15px;
}
 
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
 
/* Progress bar steps */
.step-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0px;
    margin-bottom: 2rem;
}
 
.step {
    display: flex;
    align-items: center;
    gap: 8px;
}
 
.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 15px;
}
 
.step-circle.active {
    background-color: #14B8A6;
    color: white;
}
 
.step-circle.done {
    background-color: #0D9488;
    color: white;
}
 
.step-circle.inactive {
    background-color: #E2E8F0;
    color: #94A3B8;
}
 
.step-label {
    font-size: 13px;
    font-weight: 600;
}
 
.step-label.active {
    color: #14B8A6;
}
 
.step-label.inactive {
    color: #94A3B8;
}
 
.step-line {
    width: 60px;
    height: 3px;
    background-color: #E2E8F0;
    margin: 0 4px;
}
 
.step-line.done {
    background-color: #14B8A6;
}
 
</style>
""", unsafe_allow_html=True)
 
# =========================================
# SESSION STATE INIT
# =========================================
if "page" not in st.session_state:
    st.session_state.page = 0
 
if "hasil" not in st.session_state:
    st.session_state.hasil = {}
 
# =========================================
# DATABASE
# =========================================
database = {
    "Asam Oksalat": {"BM": 126.07, "valensi": 2},
    "Boraks":        {"BM": 381.37, "valensi": 2},
    "Kalium Dikromat": {"BM": 294.18, "valensi": 6},
    "CaCO3":         {"BM": 100.09, "valensi": 2},
}
 
# =========================================
# HELPER: PROGRESS INDICATOR
# =========================================
def show_progress(current_page):
    steps = ["Beranda", "Input Data", "Hasil"]
    circles = []
    for i, label in enumerate(steps):
        if i < current_page:
            state = "done"
        elif i == current_page:
            state = "active"
        else:
            state = "inactive"
        circles.append((label, state))
 
    html = '<div class="step-container">'
    for i, (label, state) in enumerate(circles):
        icon = "✓" if state == "done" else str(i + 1)
        html += f'''
        <div class="step">
            <div class="step-circle {state}">{icon}</div>
            <span class="step-label {'active' if state != 'inactive' else 'inactive'}">{label}</span>
        </div>
        '''
        if i < len(circles) - 1:
            line_class = "done" if i < current_page else ""
            html += f'<div class="step-line {line_class}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    st.divider()
 
# =========================================
# PAGE 0: BERANDA
# =========================================
def page_beranda():
    show_progress(0)
 
    st.markdown(
        """
        <h1 style='text-align: center;'>
        🧪 Calculator Standardisasi Larutan
        </h1>
        """,
        unsafe_allow_html=True
    )
 
    st.markdown(
        """
        <p style='text-align: center; font-size:18px; color:#475569;'>
        Kalkulator untuk menghitung konsentrasi Normalitas/Molaritas
        beserta %RPD hasil standardisasi larutan.
        </p>
        """,
        unsafe_allow_html=True
    )
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    col_a, col_b, col_c = st.columns(3)
 
    with col_a:
        st.markdown("""
        <div style='background:#FFFFFF; border:1px solid #E2E8F0;
                    border-radius:15px; padding:20px; text-align:center;'>
            <h2>⚗️</h2>
            <h4>5 Metode</h4>
            <p style='color:#64748B;'>Alkalimetri, Asidimetri,
            Permanganometri, Iodometri, Kompleksometri</p>
        </div>
        """, unsafe_allow_html=True)
 
    with col_b:
        st.markdown("""
        <div style='background:#FFFFFF; border:1px solid #E2E8F0;
                    border-radius:15px; padding:20px; text-align:center;'>
            <h2>🧮</h2>
            <h4>Otomatis</h4>
            <p style='color:#64748B;'>Database BM & valensi
            terisi otomatis sesuai metode yang dipilih</p>
        </div>
        """, unsafe_allow_html=True)
 
    with col_c:
        st.markdown("""
        <div style='background:#FFFFFF; border:1px solid #E2E8F0;
                    border-radius:15px; padding:20px; text-align:center;'>
            <h2>📋</h2>
            <h4>Transparan</h4>
            <p style='color:#64748B;'>Langkah perhitungan
            ditampilkan lengkap dengan rumus dan nilai</p>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("<br><br>", unsafe_allow_html=True)
 
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 Mulai Hitung →"):
            st.session_state.page = 1
            st.rerun()
 
# =========================================
# PAGE 1: INPUT DATA
# =========================================
def page_input():
    show_progress(1)
 
    st.markdown(
        "<h1 style='text-align:center;'>📥 Input Data</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
 
    # --- Pilih Metode ---
    metode = st.selectbox(
        "🧪 Pilih Metode Standardisasi",
        ["Alkalimetri", "Asidimetri", "Permanganometri", "Iodometri", "Kompleksometri"],
        index=["Alkalimetri", "Asidimetri", "Permanganometri",
               "Iodometri", "Kompleksometri"].index(
            st.session_state.hasil.get("metode", "Alkalimetri")
        )
    )
 
    if metode == "Alkalimetri":
        baku, titran, default_massa = "Asam Oksalat", "NaOH", 630.0
    elif metode == "Asidimetri":
        baku, titran, default_massa = "Boraks", "HCl", 500.0
    elif metode == "Permanganometri":
        baku, titran, default_massa = "Asam Oksalat", "KMnO4", 630.0
    elif metode == "Iodometri":
        baku, titran, default_massa = "Kalium Dikromat", "Tiosulfat", 500.0
    elif metode == "Kompleksometri":
        baku, titran, default_massa = "CaCO3", "EDTA", 100.0
 
    BM      = database[baku]["BM"]
    valensi = database[baku]["valensi"]
 
    st.info(f"**Standar baku:** {baku} &nbsp;|&nbsp; **Titran:** {titran}")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("#### ⚖️ Massa Standar Baku")
 
        massa = st.number_input(
            "Massa standar baku",
            value=float(st.session_state.hasil.get("massa", default_massa))
        )
 
        satuan = st.selectbox(
            "Satuan Massa",
            ["mg", "g"],
            index=["mg", "g"].index(st.session_state.hasil.get("satuan", "mg"))
        )
 
        massa_mg = massa * 1000 if satuan == "g" else massa
        st.info(f"Hasil konversi massa = **{massa_mg:.2f} mg**")
 
        st.markdown("#### 🧬 Data Kimia (Otomatis)")
 
        BM_input = st.number_input(
            "BM (g/mol)",
            value=float(st.session_state.hasil.get("BM_input", BM))
        )
 
        valensi_input = st.number_input(
            "Valensi",
            value=float(st.session_state.hasil.get("valensi_input", valensi))
        )
 
        if metode != "Kompleksometri":
            BE_input = BM_input / valensi_input
            st.info(f"BE = **{BE_input:.4f} mg/mgrek**")
        else:
            BE_input = None
 
    with col2:
        st.markdown(f"#### ⚗️ Volume Titran ({titran})")
 
        vol1 = st.number_input(
            f"Volume {titran} pertama (mL)",
            min_value=0.0,
            value=float(st.session_state.hasil.get("vol1", 0.0))
        )
 
        vol2 = st.number_input(
            f"Volume {titran} kedua (mL)",
            min_value=0.0,
            value=float(st.session_state.hasil.get("vol2", 0.0))
        )
 
        st.markdown("#### 🧪 Pengenceran")
 
        pengenceran = st.radio(
            "Apakah menggunakan pengenceran?",
            ["Ya", "Tidak"],
            index=["Ya", "Tidak"].index(
                st.session_state.hasil.get("pengenceran", "Ya")
            )
        )
 
        if pengenceran == "Ya":
            volume_total = st.number_input(
                "Volume total pengenceran (mL)",
                value=float(st.session_state.hasil.get("volume_total", 100.0))
            )
            volume_pipet = st.number_input(
                "Volume yang dipipet untuk titrasi (mL)",
                value=float(st.session_state.hasil.get("volume_pipet", 25.0))
            )
            FP = volume_total / volume_pipet
        else:
            volume_total = None
            volume_pipet = None
            FP = 1.0
 
        st.success(f"Faktor Pengali (FP) = **{FP:.2f}**")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    col_back, col_space, col_next = st.columns([1, 2, 1])
 
    with col_back:
        if st.button("← Kembali"):
            st.session_state.page = 0
            st.rerun()
 
    with col_next:
        if st.button("Hitung →"):
            if vol1 == 0 or vol2 == 0:
                st.error("❌ Volume titran tidak boleh 0!")
            else:
                # Simpan semua input ke session_state
                st.session_state.hasil = {
                    "metode":        metode,
                    "baku":          baku,
                    "titran":        titran,
                    "massa":         massa,
                    "satuan":        satuan,
                    "massa_mg":      massa_mg,
                    "BM_input":      BM_input,
                    "valensi_input": valensi_input,
                    "BE_input":      BE_input,
                    "vol1":          vol1,
                    "vol2":          vol2,
                    "pengenceran":   pengenceran,
                    "volume_total":  volume_total,
                    "volume_pipet":  volume_pipet,
                    "FP":            FP,
                }
                st.session_state.page = 2
                st.rerun()
 
# =========================================
# PAGE 2: OUTPUT / HASIL
# =========================================
def page_output():
    show_progress(2)
 
    st.markdown(
        "<h1 style='text-align:center;'>📤 Hasil Perhitungan</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
 
    h = st.session_state.hasil
 
    metode      = h["metode"]
    massa_mg    = h["massa_mg"]
    BM_input    = h["BM_input"]
    valensi_input = h["valensi_input"]
    BE_input    = h["BE_input"]
    vol1        = h["vol1"]
    vol2        = h["vol2"]
    FP          = h["FP"]
    titran      = h["titran"]
    baku        = h["baku"]
 
    # =====================================
    # HITUNG
    # =====================================
    if metode != "Kompleksometri":
        N1     = massa_mg / (FP * vol1 * BE_input)
        N2     = massa_mg / (FP * vol2 * BE_input)
        N_rata = (N1 + N2) / 2
        RPD    = abs((N1 - N2) / N_rata) * 100
        satuan_konsentrasi = "N"
        label_konsentrasi  = "Normalitas"
    else:
        N1     = massa_mg / (FP * vol1 * BM_input)
        N2     = massa_mg / (FP * vol2 * BM_input)
        N_rata = (N1 + N2) / 2
        RPD    = abs((N1 - N2) / N_rata) * 100
        satuan_konsentrasi = "M"
        label_konsentrasi  = "Molaritas"
 
    # =====================================
    # RINGKASAN INPUT
    # =====================================
    with st.expander("📌 Ringkasan Input", expanded=False):
        ci1, ci2, ci3 = st.columns(3)
        ci1.metric("Metode", metode)
        ci2.metric("Standar Baku", baku)
        ci3.metric("Titran", titran)
        ci4, ci5, ci6 = st.columns(3)
        ci4.metric("Massa", f"{massa_mg:.2f} mg")
        ci5.metric("Volume 1", f"{vol1:.2f} mL")
        ci6.metric("Volume 2", f"{vol2:.2f} mL")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # =====================================
    # METRIK UTAMA
    # =====================================
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{label_konsentrasi} 1", f"{N1:.4f} {satuan_konsentrasi}")
    c2.metric(f"{label_konsentrasi} 2", f"{N2:.4f} {satuan_konsentrasi}")
    c3.metric(f"Rerata {label_konsentrasi}", f"{N_rata:.4f} {satuan_konsentrasi}")
    c4.metric("%RPD", f"{RPD:.2f}%")
 
    # =====================================
    # KESIMPULAN
    # =====================================
    st.markdown("## 📋 Kesimpulan")
 
    if RPD < 10:
        st.success(
            f"Hasil standardisasi menunjukkan rerata konsentrasi sebesar "
            f"**{N_rata:.4f} {satuan_konsentrasi}** dengan nilai %RPD sebesar **{RPD:.2f}%**.\n\n"
            f"✅ Presisi pengujian dinyatakan **baik** karena %RPD < 10%."
        )
    else:
        st.warning(
            f"Hasil standardisasi menunjukkan rerata konsentrasi sebesar "
            f"**{N_rata:.4f} {satuan_konsentrasi}** dengan nilai %RPD sebesar **{RPD:.2f}%**.\n\n"
            f"⚠️ Presisi pengujian dinyatakan **kurang baik** karena %RPD > 10%."
        )
 
    # =====================================
    # TRANSPARANSI PERHITUNGAN
    # =====================================
    st.divider()
    st.markdown("## 🧮 Transparansi Perhitungan")
 
    if metode != "Kompleksometri":
 
        st.write("### Rumus Berat Ekuivalen")
        st.latex(r'BE = \frac{BM}{Valensi}')
        st.write(f"BE = {BM_input} / {valensi_input} = **{BE_input:.4f} mg/mgrek**")
 
        st.write("### Rumus Normalitas")
        st.latex(r'N = \frac{massa\ standar\ baku}{FP \times Volume \times BE}')
 
        st.write("### Perhitungan Normalitas 1")
        st.write(f"N1 = {massa_mg:.2f} / ({FP:.2f} × {vol1:.2f} × {BE_input:.4f})")
        st.write(f"N1 = **{N1:.4f} N**")
 
        st.write("### Perhitungan Normalitas 2")
        st.write(f"N2 = {massa_mg:.2f} / ({FP:.2f} × {vol2:.2f} × {BE_input:.4f})")
        st.write(f"N2 = **{N2:.4f} N**")
 
    else:
 
        st.write("### Rumus Molaritas")
        st.latex(r'M = \frac{massa\ standar\ baku}{FP \times Volume \times BM}')
 
        st.write("### Perhitungan Molaritas 1")
        st.write(f"M1 = {massa_mg:.2f} / ({FP:.2f} × {vol1:.2f} × {BM_input:.4f})")
        st.write(f"M1 = **{N1:.4f} M**")
 
        st.write("### Perhitungan Molaritas 2")
        st.write(f"M2 = {massa_mg:.2f} / ({FP:.2f} × {vol2:.2f} × {BM_input:.4f})")
        st.write(f"M2 = **{N2:.4f} M**")
 
    st.write("### Perhitungan Rerata")
    st.write(f"Rerata = ({N1:.4f} + {N2:.4f}) / 2 = **{N_rata:.4f} {satuan_konsentrasi}**")
 
    st.write("### Rumus %RPD")
    st.latex(r'\%RPD = \left|\frac{X_1 - X_2}{X_{rerata}}\right| \times 100\%')
    st.write(f"%RPD = |({N1:.4f} - {N2:.4f}) / {N_rata:.4f}| × 100%")
    st.write(f"%RPD = **{RPD:.2f}%**")
 
    # =====================================
    # TOMBOL NAVIGASI
    # =====================================
    st.markdown("<br>", unsafe_allow_html=True)
    col_back2, col_space2, col_ulang = st.columns([1, 2, 1])
 
    with col_back2:
        if st.button("← Edit Input"):
            st.session_state.page = 1
            st.rerun()
 
    with col_ulang:
        if st.button("🔄 Hitung Ulang"):
            st.session_state.page = 0
            st.session_state.hasil = {}
            st.rerun()
 
# =========================================
# ROUTER
# =========================================
if st.session_state.page == 0:
    page_beranda()
elif st.session_state.page == 1:
    page_input()
elif st.session_state.page == 2:
    page_output()
 
