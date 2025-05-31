# 🗄️ MySQL Handbook - Interactive Learning Platform

Sebuah aplikasi pembelajaran interaktif untuk menguasai MySQL dari tingkat dasar hingga mahir, dibangun dengan Streamlit.

## ✨ Fitur Unggulan

- **🎮 Interactive Learning** - Query Editor real-time dengan syntax highlighting
- **📚 7 Modul Lengkap** - Dari Basic Query hingga Advanced Topics
- **🎯 User-Friendly Interface** - Navigation yang intuitif dengan sidebar
- **💻 Praktik Langsung** - Hands-on experience dengan contoh nyata
- **📊 Progress Tracking** - Monitor kemajuan belajar Anda
- **📱 Responsive Design** - Optimal di desktop dan mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Installation

1. **Clone atau download project**
   ```bash
   git clone <repository-url>
   cd mysql-handbook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

4. **Buka browser**
   - Aplikasi akan otomatis terbuka di `http://localhost:8501`
   - Atau buka URL tersebut secara manual

## 📁 Struktur Project

```
mysql-handbook/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── .gitignore           # Git ignore file
├── assets/              # Static assets
│   ├── logo.png         # Application logo
│   └── style.css        # Custom CSS styling
├── pages/               # Page modules
│   ├── __init__.py      # Package initialization
│   ├── home.py          # Home page (01_Home.py)
│   ├── basic_query.py   # Basic Query module (02_BasicQuery.py)
│   ├── ddl.py           # DDL module (03_DDL.py)
│   ├── dml.py           # DML module (04_DML.py)
│   ├── dcl.py           # DCL module (05_DCL.py)
│   ├── tcl.py           # TCL module (06_TCL.py)
│   ├── aggregate_query.py # Aggregate module (07_AggregateQuery.py)
│   └── sql_query_editor.py # Query Editor (SQLQueryEditor.py)
├── config/              # Configuration files
├── data/                # Sample data files
└── log/                 # Application logs
```

## 📚 Modul Pembelajaran

### 🌱 Beginner Level
1. **🏠 Home** - Overview dan pengenalan platform
2. **🔍 Basic Query** - SELECT, WHERE, ORDER BY, LIMIT
3. **🏗️ DDL** - CREATE, ALTER, DROP TABLE
4. **📝 DML** - INSERT, UPDATE, DELETE

### 🚀 Intermediate Level
5. **📊 Aggregate & Functions** - COUNT, SUM, AVG, GROUP BY
6. **⚡ TCL** - Transaction Control Language
7. **🔐 DCL** - Data Control Language

### 💻 Practice
8. **SQL Query Editor** - Interactive practice environment

## 🎯 Learning Path Rekomendasi

### Path 1: Complete Beginner (2-3 minggu)
- Start: Home → Basic Query → DDL → DML → Query Editor
- Target: Memahami operasi dasar database MySQL

### Path 2: Intermediate (3-4 minggu)
- Continue: Aggregate & Functions → TCL → DCL → Advanced Practice
- Target: Menguasai operasi database lanjutan

### Path 3: Advanced (4-6 minggu)
- Focus: Complex queries, optimization, real-world projects
- Target: MySQL Expert level skills

## 🔧 Development

### Menambah Modul Baru

1. **Buat file modul** di folder `pages/`
   ```python
   # pages/new_module.py
   import streamlit as st
   
   def show():
       st.title("New Module")
       st.write("Content goes here...")
   ```

2. **Update app.py** untuk import modul baru
   ```python
   from pages import new_module
   
   # Tambah ke dictionary pages
   pages = {
       # ... existing pages
       "🆕 New Module": new_module,
   }
   ```

### Custom Styling

Edit file `assets/style.css` untuk mengubah tampilan:
- Colors dan themes
- Button styling
- Layout adjustments
- Responsive behavior

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
# Pastikan semua dependencies terinstall
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### Error: Port already in use
```bash
# Gunakan port berbeda
streamlit run app.py --server.port 8502
```

### CSS tidak loading
- Pastikan file `assets/style.css` exists
- Check file permissions
- Restart aplikasi

## 📖 Usage Tips

### Untuk Pembelajaran Optimal:
- **📝 Catat poin penting** dari setiap modul
- **💻 Praktik setiap syntax** di Query Editor
- **🔄 Ulangi materi** yang sulit dipahami
- **🎯 Fokus satu modul** sampai tuntas

### Keyboard Shortcuts (Query Editor):
- `Ctrl + Enter`: Execute query
- `Ctrl + /`: Comment/Uncomment
- `Ctrl + A`: Select all
- `Ctrl + Z`: Undo

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- **Documentation**: Check README dan komentar dalam code
- **Issues**: Create GitHub issue untuk bug reports
- **Questions**: Gunakan Query Editor untuk eksperimen langsung

## 🎉 Acknowledgments

- Built with ❤️ using [Streamlit](https://streamlit.io/)
- MySQL documentation dan community
- Open source Python ecosystem

---

**Happy Learning! 🚀**

*Mulai perjalanan MySQL Anda hari ini dan menjadi database expert!*