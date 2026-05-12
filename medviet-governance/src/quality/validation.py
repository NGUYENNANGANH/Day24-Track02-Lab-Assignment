# src/quality/validation.py
import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite

def build_patient_expectation_suite() -> ExpectationSuite:
    context = gx.get_context()
    suite = context.add_expectation_suite("patient_data_suite")

    df = pd.read_csv("data/raw/patients_raw.csv")
    validator = context.sources.pandas_default.read_dataframe(df)

    # 1. patient_id không được null
    validator.expect_column_values_to_not_be_null("patient_id")

    # 2. cccd phải có đúng 12 ký tự
    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )

    # 3. ket_qua_xet_nghiem phải trong khoảng [0, 50]
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0,
        max_value=50
    )

    # 4. benh phải thuộc danh sách hợp lệ
    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )

    # 5. email phải match regex pattern
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"^\S+@\S+\.\S+$"
    )

    # 6. Không được có duplicate patient_id
    validator.expect_column_values_to_be_unique(column="patient_id")

    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    try:
        original_df = pd.read_csv("data/raw/patients_raw.csv")
    except FileNotFoundError:
        original_df = pd.DataFrame()

    if not original_df.empty:
        # Check 1: Không còn CCCD gốc dạng số thuần túy
        for orig_cccd in original_df["cccd"].astype(str):
            if orig_cccd in df["cccd"].astype(str).values:
                results["success"] = False
                results["failed_checks"].append("Check 1 Failed: CCCD gốc vẫn bị lọt ra output.")
                break

        # Check 3: Số rows phải bằng original
        if len(df) != len(original_df):
            results["success"] = False
            results["failed_checks"].append("Check 3 Failed: Số lượng records bị thay đổi.")

    # Check 2: Không có null values trong các cột quan trọng
    important_cols = ["patient_id", "ho_ten", "cccd", "benh"]
    for col in important_cols:
        if col in df.columns and df[col].isnull().any():
            results["success"] = False
            results["failed_checks"].append(f"Check 2 Failed: Cột '{col}' chứa giá trị null.")

    return results
