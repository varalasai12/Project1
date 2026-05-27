import os
import sys
from pathlib import Path

# Add backend directory to path so we can import app modules
backend_path = Path(__file__).resolve().parent / "backend"
sys.path.append(str(backend_path))

from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import User, Label, Document, ActivityLog
from app.auth import get_password_hash
from app.config import settings

# Sample document templates with keyword-dense contents for effective classifier training
SAMPLE_DOCUMENTS = {
    "Resume": [
        {
            "filename": "john_doe_resume.txt",
            "text": """John Doe - Senior Software Engineer
Email: john.doe@email.com | Phone: (555) 019-2834 | Location: San Francisco, CA

SUMMARY
Experienced python developer and React specialist with 8+ years of engineering robust scalable systems. 
Proven track record of managing a team of software designers and leading cloud migration strategies.

EXPERIENCE
Lead Software Architect at TechCorp (2022 - Present)
- Engineered scalable systems using FastAPI, microservices, and PostgreSQL.
- Developed React web interfaces with Redux and Tailwind CSS, increasing page speeds by 40%.
- Managed team of 6 software developers, setting coding best practices and Git workflow pipelines.
- Implemented CI/CD pipelines using GitHub Actions and Docker container orchestration.

Software Developer at CloudSystems (2018 - 2022)
- Built REST APIs in Flask and Node.js for high-throughput messaging products.
- Refactored legacy SQL databases to improve query performance and transaction safety.
- Participated in Agile scrums, user story sizing, and system architecture planning.

EDUCATION
Bachelor of Science in Computer Science
Graduated with honors from Stanford University (2014 - 2018)

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL, Go, HTML, CSS
Frameworks: React, FastAPI, Node.js, Express, scikit-learn, PyTorch
Tools: Git, Docker, Kubernetes, AWS, PostgreSQL, Redis, Linux, Jest"""
        },
        {
            "filename": "jane_smith_cv.txt",
            "text": """Jane Smith - Professional CV
Contact: jane.smith@email.com | Portfolio: janesmith.dev | New York, NY

EXECUTIVE SUMMARY
Data Scientist and Machine Learning Engineer specializing in text analytics, TF-IDF vectorization, 
and natural language processing. 6 years of expertise building predictive analytics models.

PROFESSIONAL EXPERIENCE
Senior Data Scientist - FinanceGlobal (2021 - Present)
- Developed scikit-learn pipelines to automate customer sentiment analysis and ticket routing.
- Implemented natural language processing (NLP) models, achieving 94% validation accuracy.
- Analyzed large financial datasets, extracting key business intelligence insights.
- Managed database schemas and ETL data flows using SQL and Apache Spark.

Data Analyst - RetailVision (2020 - 2021)
- Formulated regression models to forecast seasonal sales fluctuations.
- Engineered Python scripts to scrape product reviews and extract descriptive keywords.
- Created beautiful interactive dashboards using Tableau and React charts.

EDUCATION
Master of Science in Data Science
Columbia University (2018 - 2020)

CORE COMPETENCIES
- Machine Learning: Logistic Regression, Naive Bayes, Random Forests, XGBoost, TF-IDF
- Python: pandas, numpy, scikit-learn, matplotlib, PyTorch, NLTK
- Cloud & DB: SQL, MongoDB, AWS SageMaker, Snowflake, Docker"""
        },
        {
            "filename": "alex_lee_developer_resume.txt",
            "text": """Alex Lee | Full-Stack Developer
Web: alexlee.io | Email: alex.lee@devmail.net | Chicago, IL

OBJECTIVE
Energetic Full-Stack Software Developer seeking a position to build highly responsive, 
modern web applications using React, Node.js, and glassmorphic CSS systems.

WORK HISTORY
Junior Web Developer at CreativeAgencies (2021 - 2024)
- Programmed user interfaces using React, Vite, Tailwind CSS, and Framer Motion.
- Set up custom REST APIs using Python Flask, sqlite3 database, and JWT authentication.
- Authored automated unit testing suites in Jest and Cypress, resolving 150+ bugs.
- Deployed web applications onto Netlify, Vercel, and AWS EC2 instances.

TECHNICAL SKILLS
- Frontend: HTML5, CSS3, JavaScript (ES6+), React, Tailwind, Framer Motion, Redux
- Backend: Python, Flask, SQLite, Node.js, JWT, RESTful API Design
- Developer Tools: Git, GitHub, VS Code, npm, Webpack, Postman, Vite"""
        }
    ],
    "Invoice": [
        {
            "filename": "invoice_1024_acme.txt",
            "text": """ACME CORPORATION
123 Enterprise Way, Suite 100
San Jose, CA 95131
Email: billing@acme.com | Tel: (800) 555-0199

INVOICE

Invoice Number: INV-2026-1024
Invoice Date: May 20, 2026
Payment Terms: Net 30
Due Date: June 19, 2026
Purchase Order Ref: PO-998822

BILL TO:
Global Logistics Inc.
Attn: Accounts Payable
456 Transport Blvd
Dallas, TX 75201

-----------------------------------------------------------------------------
Item Description                   Quantity    Unit Price    Discount    Total
-----------------------------------------------------------------------------
1. Cloud Server Hosting (Standard)     3       $150.00         0%      $450.00
2. Professional Consulting Services   12       $120.00         5%    $1,368.00
3. Database Migration Support Fee      1       $350.00         0%      $350.00
-----------------------------------------------------------------------------

SUBTOTAL: $2,168.00
TAX (8.25%): $178.86
TOTAL BALANCE DUE: $2,346.86

PAYMENT METHOD:
Please transfer funds payable to:
Bank Name: Enterprise Trust Bank
Routing Transit Number (RTN): 123498765
Account Number: 987654321
Wire Code: ACME-INV-1024

Thank you for your business!"""
        },
        {
            "filename": "invoice_consulting_services.txt",
            "text": """APEX TECH SOLUTIONS LLC
88 Innovator Blvd, Suite B
Seattle, WA 98101
Inquiries: billing@apextech.io

INVOICE FOR PROFESSIONAL CONSULTING SERVICES

Invoice Reference: ATS-7762
Date of Issue: May 24, 2026
Due Date: Upon Receipt
Billing Cycle: April 1, 2026 - April 30, 2026

CLIENT:
schlarX Enterprises
99 Sandbox Lane
Denver, CO 80202

DESCRIPTION OF CHARGES:
-----------------------------------------------------------------------------
Description                         Hours billed    Hourly Rate       Total
-----------------------------------------------------------------------------
Senior Systems Architecture             35.0          $150.00       $5,250.00
React Frontend Refactoring              20.0          $100.00       $2,000.00
REST API Security Auditing              15.0          $120.00       $1,800.00
Database Clustering Integration         10.0          $130.00       $1,300.00
-----------------------------------------------------------------------------

Total Hours: 80.0
NET AMOUNT DUE: $10,350.00
Late payment penalty: 1.5% compounding per month.

DIRECT BANK TRANSFER DETAILS:
Bank Name: Chase Manhattan
Account Holder: Apex Tech Solutions LLC
Account Number: 5544998833
Swift/BIC: APEXTECHSE

If you have any questions regarding this billing summary, please contact us immediately."""
        },
        {
            "filename": "office_supplies_bill_554.txt",
            "text": """OFFICE DEPOT & SUPPLIES LTD
Retail Billing Department
77 Stationery Way, Miami, FL 33101

INVOICE / BILL

Bill ID: OD-554109
Billing Date: May 15, 2026
Due Date: June 15, 2026

CLIENT:
Dr. Roberts Medical Clinic
88 Vitals Court, Chicago, IL 60611

SUMMARY OF TRANSACTIONS:
- Box of Premium Recycled Printer Paper (Qty: 10) x $35.00 = $350.00
- Ergonomic Office Chairs, Mesh Back (Qty: 4) x $180.00 = $720.00
- Desktop Organizer Drawers, Black (Qty: 5) x $25.00 = $125.00
- Whiteboard, Magnetic, 4x3 feet (Qty: 2) x $60.00 = $120.00
- Box of Fine Tip Multi-color Markers (Qty: 15) x $10.00 = $150.00

Subtotal Amount: $1,465.00
Shipping & Handling Charges: $45.00
Sales Tax (7.00%): $102.55
Total Amount Due: $1,612.55

Please pay within 30 days. Payments can be submitted via portal: officedepot-billing.com/pay/OD-554109"""
        }
    ],
    "Research Paper": [
        {
            "filename": "deep_learning_nlp_abstract.txt",
            "text": """A Novel Deep Learning Approach for Automated Document Classification
Authors: Dr. Emily Vance, Prof. Sarah Jenkins
Journal of Computer Science and Machine Learning, 2025

ABSTRACT
In this study, we propose a novel deep learning framework for automated document classification using advanced neural networks and optimized natural language processing (NLP) models. Traditional approaches, such as TF-IDF vectorization combined with Naive Bayes or Logistic Regression classifiers, serve as strong baselines but often fail to capture complex semantic context. 

METHODOLOGY
We compiled a dataset of 10,000 multi-domain texts. Our model employs a deep bidirectional transformer model coupled with multi-head self-attention mechanisms. The architecture consists of 12 transformer encoder layers, mapping inputs into high-dimensional dense vector embeddings. Optimization was performed using the AdamW optimizer with a learning rate of 2e-5 and batch size of 32.

EXPERIMENTAL RESULTS
Our experimental findings indicate substantial correlation between training epoch size and categorical classification precision. The proposed model achieved an overall accuracy of 97.4%, outperforming standard linear algorithms by 6.2%. The precision and recall metrics across Resume, Invoice, and Legal Contract categories were consistently high, demonstrating robust generalizability. Future studies will explore cross-lingual document classifications and real-time inference streaming pipelines."""
        },
        {
            "filename": "regression_analysis_climate_study.txt",
            "text": """Regression Analysis and Statistical Modeling of Climate Anomalies
By: Arthur Pendelton, Department of Environmental Sciences
Institute of Geophysics Research Paper (2026)

1. INTRODUCTION
Statistical modeling of climate anomalies relies on regression analysis to identify trends and long-term correlations. This research paper evaluates global temperature variations using multi-variable linear regression and Naive Bayes classifiers to categorize severity.

2. EXPERIMENTAL DESIGN & DATASET ANALYSIS
We examined satellite data spanning 40 years. Feature engineering was performed using principal component analysis (PCA) to reduce dimensionality while preserving 95% variance. Linear regression equations were established using ordinary least squares (OLS) criteria:
    Y = beta_0 + beta_1 * X_1 + beta_2 * X_2 + epsilon
Where Y represents temperature anomaly, X_1 greenhouse gas concentrations, X_2 solar radiation variance, and epsilon is the error distribution coefficient.

3. STATISTICAL RESULTS
Our results indicate substantial correlation (R-squared = 0.89) between fossil emissions and local anomalies. P-values for all regression coefficients fell below 0.001, confirming statistical significance. We cross-validated our predictive framework using a 10-fold cross-validation split, obtaining balanced precision and recall outputs across all geographical quadrants tested."""
        },
        {
            "filename": "quantum_computing_algorithms.txt",
            "text": """Quantum Computing Optimization Algorithms for Linear Systems
Journal of Theoretical Physics | Document Ref: JTP-2026-QA

ABSTRACT
We present quantum algorithms designed to solve linear systems of equations with exponential speedup compared to classical algorithms. Our study focuses on optimizing Shor's and HHL algorithms under noisy intermediate-scale quantum (NISQ) environments.

METHODOLOGY
We modeled quantum gate circuits using numerical simulations. The linear system Ax = b was mapped onto qubit states. Feature amplitudes were normalized and initialized using unitary operators. The HHL pipeline utilizes phase estimation and controlled rotation gates to evaluate the matrix inverse:
    |x> = sum (beta_i / lambda_i) |u_i>
We simulated the model on standard datasets using a noise-resilient optimizer.

RESULTS & CONCLUDING REMARKS
Our circuit simulations achieved convergence rates in agreement with theoretical quantum bounds. We observed that gate error rates are the primary limiting factors for precision. The scientific literature review underscores the necessity for active quantum error correction code layers before large-scale practical deployments can occur."""
        }
    ],
    "Legal Contract": [
        {
            "filename": "employment_agreement_template.txt",
            "text": """EMPLOYMENT AGREEMENT AND CONTRACT

This Employment Agreement (the "Agreement") is entered into this 25th day of May, 2026, by and between:
Employer: TechCorp Solutions Inc., located at 100 Cloud Street, San Francisco, CA (the "Company")
Employee: Johnathan Doe, residing at 450 Oak Avenue, San Jose, CA (the "Employee").

WHEREAS, the Company desires to retain the services of the Employee, and the Employee desires to render such services under the terms, covenants, and clauses herein.

NOW, THEREFORE, the parties agree to the following clauses:

1. POSITION AND DUTIES
The Employee shall serve in the position of Senior Systems Engineer. The Employee shall perform all duties customary to this position and obey all lawful instructions given by Company managers.

2. TERM AND TERMINATION
The term of this contract shall commence on June 1, 2026, and survive until terminated by either party. Either the Company or the Employee may terminate this agreement with 30 days written notice. In the event of a breach of contract by the Employee, the Company reserves the right to terminate employment immediately without severance.

3. CONFIDENTIALITY AND NON-DISCLOSURE
The Employee shall not disclose, copy, or distribute any proprietary or confidential information belonging to the Company. This non-disclosure covenant shall survive the expiration or termination of this Agreement.

4. INDEMNIFICATION AND GOVERNING LAW
This Contract shall be governed by, interpreted, and construed in accordance with the laws of the State of California. Any disputes arising from this lease or contract shall be resolved in San Francisco County courts.

IN WITNESS WHEREOF, the parties under signee have executed this Contract as of the date first written above.

Employer: ______________________ (TechCorp Authorized Signature)
Employee: ______________________ (Johnathan Doe Signature)"""
        },
        {
            "filename": "non_disclosure_agreement.txt",
            "text": """MUTUAL NON-DISCLOSURE AGREEMENT (NDA)

This Mutual Non-Disclosure Agreement (the "Agreement") is made and entered into by and between:
Disclosing Party: Apex Tech Solutions LLC ("Apex")
Receiving Party: schlarX Enterprises ("Partner").

1. PURPOSE AND DEFINITION OF CONFIDENTIAL INFORMATION
The parties intend to engage in discussions regarding a potential business relationship. During these discussions, Apex may disclose proprietary details regarding its machine learning algorithms and database schemas. "Confidential Information" refers to any data marked confidential, including source code, credentials, and API specifications.

2. COVENANTS AND RESTRICTIONS
The Receiving Party shall maintain all Confidential Information in absolute confidence. The Partner shall not utilize the information for any purpose outside the scope of this partnership. Copying, reverse engineering, or disseminating this data constitutes a severe breach of contract.

3. TERM AND DISPUTE RESOLUTION
This Agreement and the obligations of confidentiality shall survive for a period of five (5) years from the date of execution. Any dispute, controversy, or claim arising out of this contract, including its breach, termination, or invalidity, shall be governed by the laws of the State of Washington.

4. LEASE AND REMEDIES
Injunctive relief shall survive the expiration of this agreement. In case of breach, the disclosing party is entitled to seek full indemnification and legal fee recovery.

Signed:
Apex Representative: ______________________ (Date: May 25, 2026)
Partner Representative: ____________________ (Date: May 25, 2026)"""
        },
        {
            "filename": "lease_agreement_sandbox.txt",
            "text": """COMMERCIAL REAL ESTATE LEASE CONTRACT

This Lease Agreement (the "Lease") is entered into this 10th day of May, 2026, by and between:
Landlord: Commercial Properties LLC ("Landlord")
Tenant: schlarX Labs ("Tenant").

1. PREMISES AND TERM
The Landlord hereby leases to the Tenant the office space located at 99 Sandbox Lane, Suite 400, Denver, Colorado (the "Premises"). The lease term shall be for 12 months, commencing June 1, 2026.

2. RENT AND DEPOSIT
Tenant agrees to pay monthly rent in the amount of $3,500.00 due on the first day of each calendar month. A security deposit of $3,500.00 is required upon lease signing and shall survive in landlord's trust account until lease termination.

3. COVENANTS, CLAUSES, AND MAINTENANCE
Tenant shall maintain the office premises in good condition. Tenant shall not make structural modifications without prior written consent. Subletting the premises without permission constitutes a breach of contract.

4. INDEMNIFICATION & LIABILITY
Tenant agrees to indemnify and hold harmless the Landlord from any liability, damages, or claims arising from tenant's operations on the premises. This lease is governed by Colorado state law.

Signatures:
Landlord Authorized: ____________________
Tenant Authorized: ______________________"""
        }
    ],
    "Medical Report": [
        {
            "filename": "patient_cardiology_referral.txt",
            "text": """CLINICAL CARDIOLOGY REPORT AND REFERRAL
Roberts Medical Clinic | cardiology-referrals@robertsmedical.org
Vitals Date: May 22, 2026

PATIENT METADATA:
Name: Margaret Thompson | Age: 64 | Patient ID: MR-99482
Gender: Female | Physician: Dr. Robert Vance, MD

CLINICAL HISTORY & DIAGNOSIS:
Patient presented complaining of acute chest pain, shortness of breath, and mild respiratory distress during physical exertion. History is positive for chronic hypertension and high cholesterol. 

PHYSICIAN FINDINGS & VITALS:
- Blood Pressure: 148/92 mmHg (Hypertensive Stage 2)
- Heart Rate: 84 bpm
- Respiratory Rate: 18 breaths/min
- Temperature: 98.6 °F (Normal)
- Oxygen Saturation (SpO2): 96% on room air

ECG ANALYSIS:
Electrocardiogram (ECG) shows sinus rhythm with mild ST-segment depression in leads V4-V6, indicating potential myocardial ischemia. No acute ST-elevation myocardial infarction (STEMI) noted.

THERAPEUTIC TREATMENT PLAN:
- Prescribed Medication: Atorvastatin (40mg dosage once daily) for lipid control.
- Prescribed Medication: Lisinopril (10mg dosage once daily) for blood pressure regulation.
- Scheduled for an outpatient myocardial perfusion imaging stress test on June 2, 2026.
- Instructed to report immediately to the nearest emergency department if acute chest pain worsens or radiates to the left arm or neck.

Referral sent to Northwestern Cardiology Associates."""
        },
        {
            "filename": "clinical_hematology_labs.txt",
            "text": """ST. JUDE GENERAL HOSPITAL | PATHOLOGY & LABORATORY REPORT
Hematology division | Phone: (312) 555-0144

Patient Name: Arthur Pendelton | Age: 42 | Gender: Male
Physician: Dr. Sandra Carter, MD | Laboratory Ref: LAB-2026-887
Vitals Date: May 19, 2026

HEMOGRAM ANALYSIS SUMMARY:
-----------------------------------------------------------------------------
Test Parameter             Result Value      Reference Range     Evaluation
-----------------------------------------------------------------------------
White Blood Cell (WBC)     7.4 x10^3/uL      4.5 - 11.0 x10^3     Normal
Red Blood Cell (RBC)       4.85 x10^6/uL     4.30 - 5.90 x10^6    Normal
Hemoglobin (Hgb)           14.2 g/dL         13.5 - 17.5 g/dL     Normal
Hematocrit (Hct)           42.1 %            41.0 - 50.0 %        Normal
Platelet Count             245 x10^3/uL      150 - 450 x10^3      Normal
Mean Corpuscular Vol (MCV) 86.8 fL           80.0 - 100.0 fL      Normal
-----------------------------------------------------------------------------

BIOCHEMISTRY METABOLIC PANEL:
- Serum Fasting Glucose: 112 mg/dL (Elevated, borderline pre-diabetic)
- Blood Urea Nitrogen (BUN): 18 mg/dL (Normal: 7 - 20 mg/dL)
- Serum Creatinine: 0.95 mg/dL (Normal: 0.60 - 1.20 mg/dL)
- Glomerular Filtration Rate (eGFR): 94 mL/min/1.73m2 (Normal)

CLINICAL RECOMMENDATION:
Patient exhibits normal hematology. Fasting glucose is slightly elevated. Recommend dietary modifications, limiting refined carbohydrates, and retesting serum levels in 3 months."""
        },
        {
            "filename": "pediatric_otitis_diagnosis.txt",
            "text": """PEDIATRIC HEALTH ASSOCIATES
12 Wellness Way, Suite A, Chicago, IL 60614

CLINICAL ASSESSMENT & VISIT REPORT
Date of Visit: May 20, 2026

Patient Name: Leo Smith | Age: 5 | Parent/Guardian: Jane Smith
Pediatrician: Dr. Megan Kelly, MD | Patient ID: MR-10332

CHIEF COMPLAINT:
Child presenting with severe ear pain, high fever (101.4 °F), and irritability starting yesterday evening. Left ear pulling observed by parent.

PHYSICAL FINDINGS & VITALS:
- Temperature: 101.2 °F (Tympanic)
- Heart Rate: 110 bpm (Normal for age under distress)
- Vitals: ENT examination reveals bulging, erythematous left tympanic membrane with complete loss of light reflex and purulent effusion. Right tympanic membrane is clear, translucent.
- Chest: Lungs clear, normal vesicular breath sounds, no respiratory distress.

CLINICAL DIAGNOSIS:
Acute Left Otitis Media (middle ear infection).

THERAPEUTIC TREATMENT & MEDICATION PLAN:
- Prescribed Medication: Amoxicillin suspension (400mg/5mL, dosage: 5.5 mL twice daily for 10 days).
- Support Care: Ibuprofen infant drops (100mg/5mL, dosage: 5 mL every 6 hours as needed for ear pain and fever reduction).
- Return to clinic if symptoms do not improve within 48 hours or if neck stiffness develops."""
        }
    ]
}

def seed_database():
    print("----------------------------------------------------------------------")
    print("AI Document Classifier Demo Database Seeder Starting...")
    print("----------------------------------------------------------------------")
    
    # Create all tables first if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # 1. Create or retrieve demo user
        username = "demo_user"
        email = "demo@schlarx.io"
        password = "password123"
        
        demo_user = db.query(User).filter(User.username == username).first()
        if demo_user:
            print(f"[-] Demo User '{username}' already exists. Skipping user creation.")
        else:
            hashed_pwd = get_password_hash(password)
            demo_user = User(
                username=username,
                email=email,
                password_hash=hashed_pwd
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"[+] Created Demo User: '{username}' / '{password}'")
            
            # Log activity
            db.add(ActivityLog(
                action="AUTH_REGISTER",
                details="Demo user profile generated automatically.",
                user_id=demo_user.id
            ))
            db.commit()
            
        # 2. Seed Labels/Categories
        label_colors = {
            "Resume": "#10B981",         # Emerald Green
            "Invoice": "#F59E0B",        # Amber Gold
            "Research Paper": "#3B82F6", # Bright Blue
            "Legal Contract": "#EF4444", # Vibrant Red
            "Medical Report": "#8B5CF6"  # Royal Purple
        }
        
        seeded_labels = {}
        for name, color in label_colors.items():
            lbl = db.query(Label).filter(
                Label.user_id == demo_user.id,
                Label.name == name
            ).first()
            
            if lbl:
                seeded_labels[name] = lbl
                print(f"[-] Label Category '{name}' already exists. Skipping.")
            else:
                lbl = Label(
                    name=name,
                    color=color,
                    user_id=demo_user.id
                )
                db.add(lbl)
                db.commit()
                db.refresh(lbl)
                seeded_labels[name] = lbl
                print(f"[+] Seeded Label Category: '{name}' with color '{color}'")
                
                db.add(ActivityLog(
                    action="LABEL_CREATE",
                    details=f"Demo database seeder generated category '{name}'.",
                    user_id=demo_user.id
                ))
                db.commit()
                
        # Ensure upload folder exists
        settings.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        
        # 3. Seed Documents
        print("\nSeeding text files and document models...")
        for category, docs in SAMPLE_DOCUMENTS.items():
            label = seeded_labels[category]
            for doc_info in docs:
                filename = doc_info["filename"]
                text = doc_info["text"]
                
                # Check if document already exists
                existing_doc = db.query(Document).filter(
                    Document.user_id == demo_user.id,
                    Document.filename == filename
                ).first()
                
                if existing_doc:
                    print(f"[-] Document '{filename}' already seeded. Skipping.")
                    continue
                
                # Save physical file to uploads directory
                # First create a mock document entry to get a unique ID
                temp_doc = Document(
                    filename=filename,
                    filepath="",
                    file_type="txt",
                    extracted_text=text,
                    label_id=label.id,
                    user_id=demo_user.id
                )
                db.add(temp_doc)
                db.commit()
                db.refresh(temp_doc)
                
                # Save physically
                unique_filename = f"{temp_doc.id}_{filename}"
                dest_path = settings.UPLOAD_FOLDER / unique_filename
                
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(text)
                    
                temp_doc.filepath = str(dest_path)
                db.commit()
                
                print(f"  [+] Saved physical text file & seeded Document record: '{filename}'")
                
                db.add(ActivityLog(
                    action="DOCUMENT_UPLOAD",
                    details=f"Seeder generated and classified document '{filename}' under '{category}'.",
                    user_id=demo_user.id
                ))
                db.commit()
                
        print("\n----------------------------------------------------------------------")
        print("[SUCCESS] Demo Seeder Completed!")
        print(f"You can now run 'python backend/run.py' and login on React frontend using:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print("Model training can be triggered instantly from the UI!")
        print("----------------------------------------------------------------------")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
