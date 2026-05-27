# schlarX: AI-Powered "Train a Document Classifier" Web Application

schlarX is a modern, production-grade, self-contained SaaS application designed to empower users to upload multi-format documents (PDF, DOCX, TXT), extract their raw text indices, organize them into color-coded categories, train interactive scikit-learn machine learning classifiers, and sandbox predictions with visual keyword triggers and PDF auditing report exports.

Built with a gorgeous, high-aesthetic **Glassmorphism CSS design system**, moving mesh background spots, light/dark responsive toggles, and smooth Framer Motion micro-animations, schlarX brings commercial-grade visual aesthetics to browser-based machine learning.

---

## 🚀 Key Features

1. **Secure JWT Multi-User Authentication**: Encrypted bcrypt hashing credentials store SQLite records, issuing expiring JWT authorization bearer headers.
2. **Dynamic Ingestion Center**: File drag-and-drop zone handling bulk PDF, DOCX, and TXT parsing. Integrates PyPDF2 and Word paragraph/table readers with grace OCR fallback.
3. **Dataset Curation Console**: Comprehensive table index providing searches matching name/text and tag filters. Features dynamic inline category re-mappings on the fly.
4. **Interactive ML Training Suite**: Trains a stratified scikit-learn TF-IDF + L2 Logistic Regression classification network. Calculates Accuracy, Precision, Recall, Weighted F1 scores, and an interactive confusion matrix heatmap grid.
5. **Prediction Sandbox**: Upload test documents or compose paragraphs to evaluate model confidence, showing confidence circles and glowing keyword highlights matching model weights.
6. **Demo Dataset Pre-Seeder**: Overcomes the cold-start problem with a single click. Instantly populates your database with 5 categories and 15 highly dense sample files.
7. **Interactive PDF Auditing Reports**: Print-friendly layouts optimized with dedicated media stylesheets for margin-perfect PDF report exports.
8. **Direct Model Downloads**: Download the trained `.joblib` model binary files directly from the browser for offline or edge deployments.

---

## 🛠️ Technology Stack

* **Frontend**: React (Vite) + Tailwind CSS (v3) + Lucide React + Recharts + Framer Motion
* **Backend**: Python FastAPI (REST API Engine) + Uvicorn
* **AI/ML**: scikit-learn + joblib + numpy
* **Database**: SQLite + SQLAlchemy ORM
* **Text Parsers**: pypdf (v4) + python-docx (v1) + pytesseract (Graceful OCR Fallback)

---

## 📂 System Directory Structure

```
schlarX/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI Application Entry
│   │   ├── config.py            # JWT Secrets, Directories configuration
│   │   ├── database.py          # SQLite engine connections
│   │   ├── models.py            # SQLAlchemy schema models
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # JWT tokens, password hashing triggers
│   │   ├── routes/
│   │   │   ├── auth.py          # User session management
│   │   │   ├── labels.py        # Categories CRUD
│   │   │   ├── documents.py     # Multi-file uploads & parsers
│   │   │   ├── classifier.py    # scikit-learn training & predict sandboxes
│   │   │   └── analytics.py     # Stats compilers & Demo pre-loader seeder
│   │   └── services/
│   │       ├── text_extractor.py # PDF/DOCX/TXT extraction
│   │       └── ml_pipeline.py    # TF-IDF + Logistic Regression fitters
│   ├── instance/                # SQLite app.db local folder
│   ├── uploads/                 # Ingested physical text folders
│   ├── models/                  # joblib model binary outputs (.joblib)
│   ├── requirements.txt         # Backend Python packages
│   └── run.py                   # FastAPI launcher
├── frontend/
│   ├── src/
│   │   ├── components/          # Glassmorphism shells, Skeletons, Sidebars
│   │   ├── context/             # AuthContext, ThemeContext
│   │   ├── pages/               # Dashboard, Upload, Dataset, Training, Predict
│   │   ├── utils/               # Axios central agent configuration
│   │   ├── App.jsx              # Central router registry
│   │   ├── index.css            # Premium custom animations and variables
│   │   └── main.jsx
│   ├── package.json             # React dependencies
│   ├── tailwind.config.js       # Custom design tokens
│   ├── postcss.config.js
│   └── vite.config.js
├── setup_demo.py                # Command-line database seeder
└── README.md                    # Installation manual
```

---

## ⚙️ Core Machine Learning Pipeline

1. **Ingestion & Text Cleaning**: Extracted strings are converted to lowercase, special symbols are collapsed, and spacing is stratified.
2. **Vectorization**: scikit-learn `TfidfVectorizer` computes word-importance weights using sublinear scaling, filtering standard English stop words and evaluating both unigrams and bigrams.
3. **Classification**: `LogisticRegression(class_weight='balanced')` computes linear probability margins. Balanced class weighting adjusts margins for category sizes.
4. **Insights Highlight Engine**: Extracted regression coefficients for the predicted target label map back onto words in your document snippet. Words with positive predictive weights are color-highlighted in the UI.

---

## 🚀 Installation & Running Instructions

### Prerequisites
* **Python**: 3.9 to 3.12 installed.
* **Node.js**: LTS version (18+) installed.

---

### Step 1: Set Up and Start the FastAPI Backend

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   * **Windows Powershell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
4. Install all Python packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the FastAPI development server:
   ```bash
   python run.py
   ```
   *The backend will boot on `http://localhost:8000`. You can explore the interactive API Swagger docs at `http://localhost:8000/docs`.*

---

### Step 2: Seed the Sandbox Demo Database

Before opening the React dashboard, pre-seed a default sandbox database containing 5 categories and 15 dense sample files.

1. Open a new terminal in the **root** `schlarX/` directory.
2. Run the database seeder:
   ```bash
   # Ensure your virtual environment is active!
   python setup_demo.py
   ```
   *This seeds a default test profile:*
   * **Username**: `demo_user`
   * **Password**: `password123`

---

### Step 3: Set Up and Start the React Frontend

1. Navigate to the `frontend/` directory:
   ```bash
   cd ../frontend
   ```
2. Install all frontend dependencies:
   ```bash
   npm install
   ```
3. Boot the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend dashboard will boot on `http://localhost:5173`.*

---

## 🧠 Step-by-Step Test Guide

1. Open your browser to `http://localhost:5173`.
2. Login using the seeder credentials:
   * **Username**: `demo_user`
   * **Password**: `password123`
3. Notice your dashboard statistics counters immediately loaded with pre-seeded values!
4. Navigate to **AI Model Training** in the sidebar. Click the **Train Model** button. Watch the training sequence complete and render the **Confusion Matrix Heatmap**.
5. Go to the **Prediction Sandbox** page:
   * Choose **Option B (Raw text sandbox)**.
   * Paste a custom invoice summary: `Please pay $400 consulting fees wire payable to ACME Chase bank RTN 9988 by June 12.`
   * Click **Classify** and watch the confidence meter score output, displaying key words highlighted in purple (e.g. *consulting*, *payable*, *due*).
6. Click the **Print (Printer)** icon inside prediction cards to preview the formatted audit PDF report!
