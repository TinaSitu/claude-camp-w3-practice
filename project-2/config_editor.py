"""
config_editor.py — JSON 配置文件读写器

Usage:
    python config_editor.py --show
    python config_editor.py --set theme light
    python config_editor.py --set font_size 18
"""

import json
import argparse
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

VALIDATORS = {
    "theme":         (str,  lambda v: v in ("dark", "light"), "必须是 dark 或 light"),
    "language":      (str,  lambda v: len(v) > 0,             "不能为空"),
    "font_size":     (int,  lambda v: 8 <= v <= 32,           "必须在 8 到 32 之间"),
    "notifications": (bool, lambda v: True,                   "必须是 true 或 false"),
    "auto_save":     (bool, lambda v: True,                   "必须是 true 或 false"),
}


def load_config(path: Path = CONFIG_PATH) -> dict:
    """从 JSON 文件加载配置。

    Raises:
        FileNotFoundError: 配置文件不存在时抛出。
    """
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在：{path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict, path: Path = CONFIG_PATH) -> None:
    """将配置字典保存回 JSON 文件。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已保存至：{path}")


def cast_value(key: str, raw: str):
    """将命令行字符串转换为配置项对应的类型。

    Args:
        key: 配置项名称。
        raw: 命令行传入的字符串值。
    Returns:
        转换后的值。
    Raises:
        KeyError: key 不在已知配置项中。
        ValueError: 类型转换失败或验证不通过。
    """
    if key not in VALIDATORS:
        raise KeyError(f"未知配置项：{key}，可用项：{list(VALIDATORS.keys())}")

    target_type, validator, hint = VALIDATORS[key]

    if target_type == bool:
        if raw.lower() not in ("true", "false"):
            raise ValueError(f"{key} 必须是 true 或 false")
        value = raw.lower() == "true"
    else:
        try:
            value = target_type(raw)
        except ValueError:
            raise ValueError(f"{key} 类型错误，期望 {target_type.__name__}")

    if not validator(value):
        raise ValueError(f"{key} 值无效：{hint}")

    return value


def show_config(config: dict) -> None:
    """打印当前所有配置项。"""
    print("\n📋 当前配置：")
    for k, v in config.items():
        print(f"   {k}: {v}")
    print()


def set_value(key: str, raw: str, path: Path = CONFIG_PATH) -> None:
    """读取配置、修改指定项、保存。"""
    config = load_config(path)
    value = cast_value(key, raw)
    old = config.get(key, "（无）")
    config[key] = value
    save_config(config, path)
    print(f"   {key}: {old} → {value}")


def main():
    parser = argparse.ArgumentParser(description="JSON 配置文件读写器")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--show", action="store_true", help="显示当前配置")
    group.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), help="修改配置项")
    args = parser.parse_args()

    if args.show:
        show_config(load_config())
    else:
        set_value(args.set[0], args.set[1])


if __name__ == "__main__":
    main()
