@"
# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on user preferences. Built with Streamlit and machine learning.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movierecomendation-sagar-huw123.streamlit.app/)

## ✨ Features

- **Search Movies**: Find movies by title
- **Smart Filtering**: Filter by genres
- **Personalized Recommendations**: Get similar movies based on content
- **Clean Interface**: User-friendly design
- **Real-time Results**: Instant recommendations

## 🛠️ Installation

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/Sagar-huw123/MovieRecomendation.git
   cd MovieRecomendation
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the application**
   \`\`\`bash
   streamlit run app.py
   \`\`\`

## 📁 Project Structure

\`\`\`
MovieRecomendation/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── movies.pkl            # Movie dataset (via Git LFS)
├── similarity.pkl        # Similarity matrix (via Git LFS)
└── README.md             # Project documentation
\`\`\`

## 🎯 How It Works

1. **Content-Based Filtering**: Uses movie features like genres, overview, and keywords
2. **Cosine Similarity**: Calculates similarity between movies
3. **Real-time Search**: Instant filtering and recommendations

## 🎪 Usage

1. Launch the app using \`streamlit run app.py\`
2. Browse through the movie catalog
3. Use the search bar to find specific movies
4. Click \"Get Recommendations\" on any movie to find similar films
5. Filter movies by genres using the sidebar

## 📊 Dataset

- **Movies**: 4800+ movies with details
- **Features**: Title, genres, overview, release year
- **Similarity Matrix**: Pre-computed using machine learning

## 🛠️ Technologies Used

- **Python**: Primary programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning and similarity calculation
- **Git LFS**: Large file storage for dataset

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Sagar Panja**
- GitHub: [@Sagar-huw123](https://github.com/Sagar-huw123)
- Email: panjasagar89@gmail.com

## 🙏 Acknowledgments

- Movie data sourced from public datasets
- Built with Streamlit community
- Icons and UI components from Streamlit
\`\`\`"@ | Out-File -FilePath README.md -Encoding utf8