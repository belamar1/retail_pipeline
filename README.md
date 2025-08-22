🛒 Retail Sales Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline and interactive Streamlit dashboard for cleaning, transforming, analyzing, and visualizing retail sales data.

retail_pipeline/
│── data/                # Raw input CSV files (e.g., retail_data.csv)
│── output/              # Generated outputs (cleaned, aggregated, anomalies)
│── src/                 # Source code
│   └── pipeline.py      # Main ETL pipeline script
│── app.py               # Streamlit dashboard
│── venv/                # Virtual environment (excluded via .gitignore)
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation

⚙️ Installation

Clone the repository:

git clone https://github.com/belamar1/retail_pipeline.git

cd retail_pipeline


Create & activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage
1. Run the ETL pipeline
python src/pipeline.py


Outputs will be stored in the output/ directory:

cleaned_sales.csv → Cleaned retail dataset

monthly_sales_by_category.csv → Aggregated monthly sales

anomalies.csv → Any detected anomalies

1. Launch the Streamlit dashboard
streamlit run app.py


Then open your browser at:

Local URL → http://localhost:8501

Network URL → http://<your-ip>:8501

The dashboard provides:

Interactive visualizations of sales trends

Insights into seasonal or category performance

Ability to explore data dynamically

🛠 Requirements

Python >= 3.10

pandas >= 2.0.0

streamlit >= 1.25.0

matplotlib >= 3.8.0

jupyter >= 1.0.0