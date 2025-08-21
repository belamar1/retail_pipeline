🛒 Retail Sales Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline for cleaning, transforming, and analyzing retail sales data.

📂 Project Structure
retail_pipeline/
│── data/                # Raw input CSV files
│── output/              # Generated outputs (cleaned, aggregated, anomalies)
│── src/                 # Source code
│   └── pipeline.py      # Main pipeline script
│── venv/                # Virtual environment (excluded via .gitignore)
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation

⚙️ Installation

Clone the repository:

git clone https://github.com/<your-username>/retail_pipeline.git
cd retail_pipeline


Create & activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the ETL pipeline:

python src/pipeline.py


Outputs will be stored in the output/ directory:

cleaned_sales.csv → Cleaned retail dataset

monthly_sales_by_category.csv → Aggregated monthly sales

anomalies.csv → Any detected anomalies

🛠 Requirements

Python >= 3.10

pandas >= 2.0.0

jupyter >= 1.0.0