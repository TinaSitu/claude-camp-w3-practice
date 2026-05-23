"""
csv_analyzer.py — 学员 CSV 数据分析器

Usage:
    python csv_analyzer.py students.csv
    python csv_analyzer.py students.csv --output my_report.json
"""

import json
import argparse
from pathlib import Path
import pandas as pd


def load_students(csv_path: str) -> pd.DataFrame:
    """从 CSV 文件加载学员数据，并校验必要列是否存在。

    Args:
        csv_path: CSV 文件路径。
    Returns:
        包含学员数据的 DataFrame。
    Raises:
        FileNotFoundError: 文件不存在时抛出。
        ValueError: 缺少必要列时抛出。
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到文件：{csv_path}")
    df = pd.read_csv(path)
    required_columns = {"name", "email", "joined_date", "country", "bet_status"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV 缺少必要列：{missing}")
    return df


def count_total(df: pd.DataFrame) -> int:
    """返回学员总人数。"""
    return len(df)


def count_by_country(df: pd.DataFrame) -> dict:
    """统计各国家的学员人数，按人数降序排列。"""
    return df["country"].value_counts().to_dict()


def bet_completion_rate(df: pd.DataFrame) -> dict:
    """计算对赌完成率及各状态分布。

    Returns:
        包含 status_counts、completion_rate_pct、total 的字典。
    """
    status_counts = df["bet_status"].value_counts().to_dict()
    completed = status_counts.get("completed", 0)
    total = len(df)
    rate = round(completed / total * 100, 2) if total > 0 else 0.0
    return {"status_counts": status_counts, "completion_rate_pct": rate, "total": total}


def build_report(df: pd.DataFrame) -> dict:
    """汇总所有统计结果，生成报告字典。"""
    return {
        "total_students": count_total(df),
        "students_by_country": count_by_country(df),
        "bet_statistics": bet_completion_rate(df),
    }


def save_report(report: dict, output_path: str = "report.json") -> None:
    """将报告字典序列化为 JSON 文件。"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"✅ 报告已保存至：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="学员 CSV 数据分析器")
    parser.add_argument("csv_file", help="学员 CSV 文件路径")
    parser.add_argument("--output", default="report.json", help="输出 JSON 路径")
    args = parser.parse_args()

    df = load_students(args.csv_file)
    report = build_report(df)
    save_report(report, args.output)

    print(f"\n📊 分析结果摘要")
    print(f"   总学员数：{report['total_students']}")
    print(f"   国家分布：{report['students_by_country']}")
    print(f"   对赌完成率：{report['bet_statistics']['completion_rate_pct']}%")


if __name__ == "__main__":
    main()
