"""
test_csv_analyzer.py — csv_analyzer 单元测试

运行方式：
    pytest test_csv_analyzer.py -v
"""

import json
import pytest
import pandas as pd
from pathlib import Path
from csv_analyzer import (
    load_students,
    count_total,
    count_by_country,
    bet_completion_rate,
    build_report,
    save_report,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """提供标准测试数据集（10 条记录）。"""
    return pd.DataFrame({
        "name":        ["Alice", "Bob", "Charlie", "Diana", "Eve",
                        "Frank", "Grace", "Henry", "Iris", "Jack"],
        "email":       [f"{n.lower()}@test.com" for n in
                        ["Alice","Bob","Charlie","Diana","Eve",
                         "Frank","Grace","Henry","Iris","Jack"]],
        "joined_date": ["2026-05-01"] * 10,
        "country":     ["Singapore","Australia","Malaysia","Singapore","China",
                        "Australia","Malaysia","China","Singapore","Australia"],
        "bet_status":  ["active","completed","completed","active","completed",
                        "dropped","completed","active","completed","completed"],
    })


@pytest.fixture
def sample_csv(tmp_path, sample_df):
    """将测试 DataFrame 写入临时 CSV 文件并返回路径。"""
    csv_file = tmp_path / "students.csv"
    sample_df.to_csv(csv_file, index=False)
    return csv_file


# ── load_students ─────────────────────────────────────────────────────────────

def test_load_students_returns_dataframe(sample_csv):
    df = load_students(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10


def test_load_students_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_students("no_such_file.csv")


def test_load_students_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("name,email\nAlice,a@b.com\n")
    with pytest.raises(ValueError, match="缺少必要列"):
        load_students(bad_csv)


# ── count_total ───────────────────────────────────────────────────────────────

def test_count_total(sample_df):
    assert count_total(sample_df) == 10


def test_count_total_empty():
    empty = pd.DataFrame(columns=["name","email","joined_date","country","bet_status"])
    assert count_total(empty) == 0


# ── count_by_country ──────────────────────────────────────────────────────────

def test_count_by_country_keys(sample_df):
    result = count_by_country(sample_df)
    assert set(result.keys()) == {"Singapore", "Australia", "Malaysia", "China"}


def test_count_by_country_values(sample_df):
    result = count_by_country(sample_df)
    assert result["Singapore"] == 3
    assert result["Australia"] == 3
    assert result["Malaysia"] == 2
    assert result["China"] == 2


# ── bet_completion_rate ───────────────────────────────────────────────────────

def test_completion_rate_value(sample_df):
    # completed: Bob, Charlie, Eve, Grace, Iris, Jack = 6 out of 10 → 60%
    result = bet_completion_rate(sample_df)
    assert result["completion_rate_pct"] == 60.0
    assert result["total"] == 10


def test_completion_rate_empty():
    empty = pd.DataFrame(columns=["name","email","joined_date","country","bet_status"])
    result = bet_completion_rate(empty)
    assert result["completion_rate_pct"] == 0.0


def test_completion_rate_all_completed():
    df = pd.DataFrame({
        "name": ["A", "B"],
        "email": ["a@a.com", "b@b.com"],
        "joined_date": ["2026-01-01", "2026-01-02"],
        "country": ["SG", "SG"],
        "bet_status": ["completed", "completed"],
    })
    result = bet_completion_rate(df)
    assert result["completion_rate_pct"] == 100.0


# ── build_report & save_report ────────────────────────────────────────────────

def test_build_report_structure(sample_df):
    report = build_report(sample_df)
    assert "total_students" in report
    assert "students_by_country" in report
    assert "bet_statistics" in report


def test_save_report_creates_file(tmp_path, sample_df):
    report = build_report(sample_df)
    output = tmp_path / "report.json"
    save_report(report, str(output))
    assert output.exists()
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["total_students"] == 10
