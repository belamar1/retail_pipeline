import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# File paths
RAW = Path("data/retail_sales.csv")
OUT_CLEAN = Path("output/cleaned_sales.csv")
OUT_AGG = Path("output/monthly_sales_by_category.csv")
OUT_ANOMALIES = Path("output/anomalies.csv")

# Required columns for cleaning
REQUIRED = ("date", "category", "revenue")


def load_rows():
    """Load CSV and normalize headers"""
    with RAW.open("r", newline="", encoding="utf-8") as f:
        # 👇 force tab delimiter
        reader = csv.DictReader(f, delimiter="\t")
        raw_headers = reader.fieldnames
        norm_headers = [h.strip().lower().replace(" ", "_") for h in raw_headers]

        print("📑 Raw headers:", raw_headers)
        print("📑 Normalized headers:", norm_headers)

        rows = []
        for row in reader:
            norm_row = {nc: (row.get(oc) or "").strip()
                        for oc, nc in zip(raw_headers, norm_headers)}
            rows.append(norm_row)
        return norm_headers, rows


def clean_rows(cols, rows):
    """Validate and clean rows"""
    missing = [c for c in REQUIRED if c not in cols]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    seen = set()
    cleaned, anomalies = [], []

    for i, r in enumerate(rows, 1):
        # Parse date
        dt = None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(r["date"], fmt)
                break
            except Exception:
                pass
        if not dt:
            anomalies.append({"row": i, "issue": "Invalid date", "data": r})
            continue

        # Parse revenue
        try:
            revenue = float((r["revenue"] or "").replace(",", ""))
        except Exception:
            anomalies.append({"row": i, "issue": "Invalid revenue", "data": r})
            continue

        if revenue <= 0:
            anomalies.append({"row": i, "issue": "Zero/negative revenue", "data": r})

        # Normalize category
        cat = (r.get("category") or "").title()
        if not cat:
            anomalies.append({"row": i, "issue": "Missing category", "data": r})
            continue

        # Detect duplicates
        key = (dt.date().isoformat(), cat, round(revenue, 2))
        if key in seen:
            anomalies.append({"row": i, "issue": "Duplicate row", "data": r})
            continue
        seen.add(key)

        cleaned.append({"date": key[0], "category": cat, "revenue": f"{revenue:.2f}"})

    return cleaned, anomalies


def transform_monthly(cleaned_rows):
    """Aggregate monthly revenue by category"""
    bucket = defaultdict(float)
    for r in cleaned_rows:
        month = r["date"][:7]
        bucket[(month, r["category"])] += float(r["revenue"])

    out = [{"month": m, "category": c, "total_revenue": v}
           for (m, c), v in bucket.items()]
    out.sort(key=lambda x: (x["month"], x["category"]))
    return out


def detect_trends(monthly_rows):
    """Detect unusual revenue drops (>20%)"""
    anomalies = []
    last_revenue = {}
    for r in monthly_rows:
        key = r["category"]
        revenue = r["total_revenue"]
        if key in last_revenue:
            prev = last_revenue[key]
            if prev > 0 and (revenue < prev * 0.8):  # drop >20%
                anomalies.append({
                    "month": r["month"],
                    "category": key,
                    "issue": f"Revenue drop >20% (prev {prev:.2f}, now {revenue:.2f})"
                })
        last_revenue[key] = revenue
    return anomalies


def write_csv(path, rows, fields):
    """Write rows to CSV"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run():
    print("📥 Loading…")
    cols, rows = load_rows()
    print(f"Loaded {len(rows)} rows.")

    print("🧹 Cleaning…")
    cleaned, row_anomalies = clean_rows(cols, rows)
    print(f"Cleaned → {len(cleaned)} rows, anomalies detected → {len(row_anomalies)}")

    print("🔄 Transforming…")
    monthly = transform_monthly(cleaned)
    print(f"Aggregated → {len(monthly)} rows.")

    print("🔎 Detecting anomalies…")
    trend_anomalies = detect_trends(monthly)
    all_anomalies = row_anomalies + trend_anomalies
    print(f"Total anomalies → {len(all_anomalies)}")

    print("💾 Storing…")
    write_csv(OUT_CLEAN, cleaned, ["date", "category", "revenue"])
    write_csv(OUT_AGG, monthly, ["month", "category", "total_revenue"])
    if all_anomalies:
        all_fields = set()
        for a in all_anomalies:
            all_fields.update(a.keys())
        fields = list(all_fields)
        write_csv(OUT_ANOMALIES, all_anomalies, fields)
        print(f"⚠️  Anomalies saved → {OUT_ANOMALIES}")

    print("✅ Done.")


if __name__ == "__main__":
    run()
    print("Running retail sales pipeline...")
    