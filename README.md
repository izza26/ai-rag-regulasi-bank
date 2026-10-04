# 🤖 MCSA — Sistem RAG Regulasi Perbankan

> Asisten AI yang menjawab pertanyaan seputar **regulasi perbankan Indonesia**
> (POJK, PBI, UU Perbankan) dengan teknik **Retrieval-Augmented Generation (RAG)** —
> jawaban selalu bersumber dari dokumen resmi, bukan halusinasi model.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35)
![Ollama](https://img.shields.io/badge/Ollama-000000)

---

## 📌 Latar Belakang

Regulasi perbankan seperti POJK, PBI, dan UU Perbankan sangat panjang dan tersebar di banyak file PDF.
Mencari pasal tertentu secara manual memakan waktu. Sistem ini membangun **basis pengetahuan vektor**
dari dokumen-dokumen tersebut, lalu menggunakan LLM untuk menjawab pertanyaan pengguna
**hanya berdasarkan isi dokumen** yang relevan (grounded answer), lengkap dengan referensi pasal.

Dikembangkan sebagai proyek mata kuliah / riset **MCSA (Mandiri Compliance Smart Assistant)**.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|---|---|
| 📄 **Ingest Dokumen** | Upload PDF regulasi → otomatis di-chunk & disimpan ke vector database |
| 🔍 **Semantic Search** | Pencarian makna, bukan sekadar kata kunci (embedding `nomic-embed-text`) |
| 💬 **Chat RAG** | Jawaban grounded + menyebutkan nama Peraturan/Pasal sebagai referensi |
| 👥 **Multi-role Login** | Dashboard terpisah untuk **Admin** dan **Staff** |
| 👤 **Manajemen User** | CRUD pengguna (NIP, nama, departemen) |
| 🕘 **Riwayat Chat** | Menyimpan histori percakapan per pengguna |
| 📚 **Kelola Dokumen** | Lihat & hapus dokumen dari basis pengetahuan |
| ⚙️ **Settings** | Konfigurasi model & aplikasi |
| 🎨 **UI Streamlit** | Tema modern (sidebar, kartu, custom CSS) |

---

## 🏗️ Arsitektur RAG

```
                    ┌─────────────────────────────────────────────┐
                    │              DOKUMEN PDF                     │
                    │   POJK · PBI · UU Perbankan · Materi         │
                    └───────────────────┬─────────────────────────┘
                                        │  (1) Load (PyPDFLoader)
                                        ▼
                              ┌───────────────────┐
                              │  Text Splitter    │  chunk 1000 / overlap 200
                              └─────────┬─────────┘
                                        │  (2) Embed
                                        ▼
                         ┌──────────────────────────┐
                         │  nomic-embed-text        │
                         │  (Ollama Embeddings)     │
                         └────────────┬─────────────┘
                                      │  (3) Simpan
                                      ▼
                         ┌──────────────────────────┐
                         │      ChromaDB            │  vector store
                         └────────────┬─────────────┘
                                      │
    ┌──────────────┐   pertanyaan     │  (4) Retrieve top-k (k=3)
    │    USER      │ ────────────────►│
    └──────┬───────┘                  ▼
           │              ┌───────────────────────┐
           │              │  Konteks dokumen      │
           │              └───────────┬───────────┘
           │                          │  (5) Augment + Generate
           │                          ▼
           │              ┌───────────────────────┐
           └◄─────────────│  Llama 3.2 (Ollama)   │  jawaban + referensi
      jawaban grounded     └───────────────────────┘
```

---

## 🛠️ Teknologi

**Framework:** Streamlit · LangChain 0.2.x
**Vector DB:** ChromaDB
**Embedding & LLM:** Ollama (`nomic-embed-text`, `llama3.2`) — 100% berjalan lokal
**Database:** SQLite (users, chat history)
**Dokumen:** pypdf

---

## 🚀 Cara Menjalankan

### Prasyarat
1. **Python 3.10+**
2. **[Ollama](https://ollama.com)** terinstal & berjalan
3. Unduh model yang dibutuhkan:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Instalasi

```bash
# Clone
git clone https://github.com/izza26/ai-rag-regulasi-bank.git
cd ai-rag-regulasi-bank

# Virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Dependensi
pip install -r requirements.txt

# Siapkan folder dokumen & letakkan PDF regulasi di dalamnya
mkdir -p data

# Jalankan
streamlit run app.py
```

Aplikasi terbuka di `http://localhost:8501`.

### Login Default

| Role | NIP | Password |
|---|---|---|
| Admin | `999` | `admin` |
| Staff | `2001` | `kaila123` |

---

## 📁 Struktur Proyek

```
.
├── app.py                    # Entry point + halaman login
├── rag_engine.py             # Inti RAG (ingest, embed, retrieve, answer)
├── pages/
│   ├── Admin_Dashboard.py    # Dashboard admin
│   ├── Staff_Dashboard.py    # Dashboard staff (chat)
│   ├── Dokumen.py            # Kelola dokumen
│   ├── Users.py              # Manajemen pengguna
│   ├── History_Chat.py       # Riwayat percakapan
│   └── Settings.py           # Konfigurasi
├── utils/
│   └── styles.py             # Custom CSS
├── images/                   # Logo & aset
├── data/                     # PDF regulasi (tidak di-commit)
├── chroma_db/                # Vector store (generated)
├── requirements.txt
└── .streamlit/config.toml    # Tema
```

---

## 🔒 Catatan Keamanan & Privasi

- **Seluruh pemrosesan berjalan lokal** melalui Ollama — dokumen tidak dikirim ke API cloud pihak ketiga.
- Database (`users.db`, `chat_history.db`) dan folder `chroma_db/` **tidak di-commit** ke Git (berisi data runtime).
- Dokumen PDF regulasi **tidak disertakan** di repository; gunakan file resmi dari situs OJK/BI.

---

## 🔮 Pengembangan Selanjutnya

- [ ] Hashing password (bcrypt) menggantikan penyimpanan plaintext
- [ ] Dukungan multi-dokumen dengan filter metadata (per jenis regulasi)
- [ ] Streaming jawaban real-time
- [ ] Export riwayat chat ke PDF/Excel
- [ ] Deployment via Docker

---

## 👤 Penulis

**Arhamiz Fegianti (Izza)**
Mahasiswa Sistem Informasi — Universitas Trunojoyo Madura (UTM)
📧 izzafegianti@gmail.com · 🐙 [@izza26](https://github.com/izza26)
