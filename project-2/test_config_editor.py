"""
test_config_editor.py — config_editor 单元测试

运行方式：
    pytest project-2/test_config_editor.py -v
"""

import json
import pytest
from pathlib import Path
from config_editor import load_config, save_config, cast_value, set_value


@pytest.fixture
def tmp_config(tmp_path):
    """在临时目录创建一份默认配置文件。"""
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({
        "theme": "dark", "language": "zh-CN",
        "font_size": 14, "notifications": True, "auto_save": True
    }))
    return cfg


# ── load / save ───────────────────────────────────────────────────────────────

def test_load_config(tmp_config):
    config = load_config(tmp_config)
    assert config["theme"] == "dark"
    assert config["font_size"] == 14

def test_load_config_missing():
    with pytest.raises(FileNotFoundError):
        load_config(Path("no_such.json"))

def test_save_config(tmp_config):
    config = load_config(tmp_config)
    config["theme"] = "light"
    save_config(config, tmp_config)
    reloaded = load_config(tmp_config)
    assert reloaded["theme"] == "light"


# ── cast_value ────────────────────────────────────────────────────────────────

def test_cast_font_size_valid():
    assert cast_value("font_size", "18") == 18

def test_cast_font_size_too_small():
    with pytest.raises(ValueError):
        cast_value("font_size", "7")

def test_cast_font_size_too_large():
    with pytest.raises(ValueError):
        cast_value("font_size", "33")

def test_cast_theme_valid():
    assert cast_value("theme", "light") == "light"

def test_cast_theme_invalid():
    with pytest.raises(ValueError):
        cast_value("theme", "blue")

def test_cast_bool_true():
    assert cast_value("notifications", "true") is True

def test_cast_bool_false():
    assert cast_value("auto_save", "false") is False

def test_cast_unknown_key():
    with pytest.raises(KeyError):
        cast_value("nonexistent", "value")


# ── set_value ─────────────────────────────────────────────────────────────────

def test_set_value_updates_file(tmp_config):
    set_value("theme", "light", tmp_config)
    config = load_config(tmp_config)
    assert config["theme"] == "light"

def test_set_value_font_size(tmp_config):
    set_value("font_size", "20", tmp_config)
    config = load_config(tmp_config)
    assert config["font_size"] == 20
