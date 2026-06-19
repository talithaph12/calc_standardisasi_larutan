import streamlit as st

# =========================================
# CONFIG PAGE
# =========================================
st.set_page_config(
    page_title="Kalkulator Standardisasi Larutan",
    page_icon="🧪",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

body, .stApp {
    background-color: #F0FDFA;
}

h1, h2, h3 {
    color: #0F172A;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stButton>button {
    background-color: #14B8A6;
    color: white;
    border-radius: 14px;
    border: none;
    height: 60px;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #0D9488;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 15px;
}

.card-box {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

.step-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 25px;
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
}

.step-circle.active {
    background: #14B8A6;
    color: white;
}

.step-circle.done {
    background: #0D9488;
    color: white;
}

.step-circle.inactive {
    background: #E2E8F0;
    color: #94A3B8;
}

.step-line {
    width: 60px;
    height: 3px;
    background: #E2E8F0;
    margin: 0 5px;
}

.step-line.done {
    background: #14B8A6;
}

.divider-vertical {
    border-left: 2px solid #E2E8F0;
    height: 600px;
    margin: auto;
}

.creator-footer {
    text-align: center;
    color: #64748B;
    font-size: 14px;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SESSION STATE
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
    "Boraks": {"BM": 381.37, "valensi": 2},
    "Kalium Dikromat": {"BM": 294.18, "valensi": 6},
    "CaCO3": {"BM": 100.09, "valensi": 2},
}

# =========================================
# PROGRESS
# =========================================
def show_progress(current_page):
    steps = ["Beranda", "Input Data", "Hasil"]

    html = '<div class="step-container">'
    for i, step in enumerate(steps):
        state = "active" if i == current_page else "done" if i < current_page else "inactive"
        icon = "✓" if i < current_page else str(i+1)

        html += f"""
        <div class="step">
            <div class="step-circle {state}">{icon}</div>
            <span>{step}</span>
        </div>
        """

        if i < len(steps)-1:
            html += f'<div class="step-line {"done" if i < current_page else ""}"></div>'

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.divider()

# =========================================
# PAGE BERANDA
# =========================================
def page_beranda():
    show_progress(0)

    st.markdown("""
    <h1 style='text-align:center;'>🧪 Kalkulator Standardisasi Larutan</h1>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🧪 Mulai Hitung"):
            st.session_state.page = 1
            st.rerun()

    st.markdown("""
    <p style='text-align:center; font-size:18px; color:#475569;'>
    Kalkulator untuk menghitung konsentrasi Normalitas/Molaritas beserta %RPD.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    cards = [
        ("⚗️", "5 Metode", "Alkalimetri, Asidimetri, Permanganometri, Iodometri, Kompleksometri"),
        ("🧮", "Otomatis", "Database BM & valensi otomatis"),
        ("📋", "Transparan", "Menampilkan langkah perhitungan lengkap")
    ]

    for col, card in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div class='card-box'>
                <h2 style='text-align:center;'>{card[0]}</h2>
                <h4 style='text-align:center;'>{card[1]}</h4>
                <p style='text-align:center; color:#64748B;'>{card[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='creator-footer'>
    <b>Kreator:</b><br><br>
    Adila Candra Wijayanti (2560554)<br>
    Dafina Khaerunnisa (2560603)<br>
    Mohammad Raihan Fitrananda (2560673)<br>
    Pegi Sepyan Rahmadani (2560736)<br>
    Talitha Putri Hutomo (2560794)
    </div>
    """, unsafe_allow_html=True)

# =========================================
# PAGE INPUT
# =========================================
def page_input():
    show_progress(1)

    st.markdown("<h1 style='text-align:center;'>📥 Input Data</h1>", unsafe_allow_html=True)

    metode = st.selectbox(
        "Pilih Metode",
        ["Alkalimetri","Asidimetri","Permanganometri","Iodometri","Kompleksometri"]
    )

    baku_map = {
        "Alkalimetri": ("Asam Oksalat","NaOH",630),
        "Asidimetri": ("Boraks","HCl",500),
        "Permanganometri": ("Asam Oksalat","KMnO4",630),
        "Iodometri": ("Kalium Dikromat","Tiosulfat",500),
        "Kompleksometri": ("CaCO3","EDTA",100)
    }

    baku, titran, default_massa = baku_map[metode]

    col1, spacer, col2 = st.columns([1,0.08,1])

    with col1:
        massa = st.number_input("Massa standar baku", value=float(default_massa))
        satuan = st.selectbox("Satuan", ["mg","g"])
        massa_mg = massa*1000 if satuan=="g" else massa

        BM = database[baku]["BM"]
        valensi = database[baku]["valensi"]

        st.info(f"BM = {BM}")
        st.info(f"Valensi = {valensi}")

    with spacer:
        st.markdown("<div class='divider-vertical'></div>", unsafe_allow_html=True)

    with col2:
        vol1 = st.number_input("Volume titran pertama", min_value=0.0)
        vol2 = st.number_input("Volume titran kedua", min_value=0.0)

        pengenceran = st.radio("Pengenceran?", ["Ya","Tidak"])

        if pengenceran == "Ya":
            total = st.number_input("Volume total", value=100.0)
            pipet = st.number_input("Volume pipet", value=25.0)
            FP = total/pipet
        else:
            FP = 1

        st.success(f"FP = {FP:.2f}")

    col_back, col_next = st.columns(2)

    with col_back:
        if st.button("⬅️ Kembali"):
            st.session_state.page = 0
            st.rerun()

    with col_next:
        if st.button("🔍 Hitung"):
            BE = BM/valensi
            st.session_state.hasil = {
                "metode": metode,
                "baku": baku,
                "titran": titran,
                "massa_mg": massa_mg,
                "BM": BM,
                "valensi": valensi,
                "BE": BE,
                "vol1": vol1,
                "vol2": vol2,
                "FP": FP
            }
            st.session_state.page = 2
            st.rerun()

# =========================================
# PAGE HASIL
# =========================================
def page_output():
    show_progress(2)

    h = st.session_state.hasil

    if h["metode"] != "Kompleksometri":
        x1 = h["massa_mg"]/(h["FP"]*h["vol1"]*h["BE"])
        x2 = h["massa_mg"]/(h["FP"]*h["vol2"]*h["BE"])
        satuan = "N"
    else:
        x1 = h["massa_mg"]/(h["FP"]*h["vol1"]*h["BM"])
        x2 = h["massa_mg"]/(h["FP"]*h["vol2"]*h["BM"])
        satuan = "M"

    rata = (x1+x2)/2
    rpd = abs((x1-x2)/rata)*100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hasil 1", f"{x1:.4f} {satuan}")
    c2.metric("Hasil 2", f"{x2:.4f} {satuan}")
    c3.metric("Rerata", f"{rata:.4f} {satuan}")
    c4.metric("%RPD", f"{rpd:.2f}%")

    if rpd < 10:
        st.success(f"Rerata konsentrasi = {rata:.4f} {satuan} | %RPD = {rpd:.2f}% (Presisi baik)")
    else:
        st.warning(f"Rerata konsentrasi = {rata:.4f} {satuan} | %RPD = {rpd:.2f}% (Presisi kurang baik)")

    st.markdown("## 🧮 Transparansi Perhitungan")

    st.write(f"Hasil 1 = {x1:.4f}")
    st.write(f"Hasil 2 = {x2:.4f}")
    st.write(f"Rerata = {rata:.4f}")
    st.write(f"%RPD = {rpd:.2f}%")

    col_back, col_reset = st.columns(2)

    with col_back:
        if st.button("✏️ Edit Input"):
            st.session_state.page = 1
            st.rerun()

    with col_reset:
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
