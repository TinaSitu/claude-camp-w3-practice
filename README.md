# Claude Camp W3 练习

3 个 Python 数据处理项目，每个项目包含完整函数、文档和测试。

---

## 项目 1：CSV 学员数据分析器

读取学员 CSV 文件，统计总人数、各国家人数、对赌完成率，导出 report.json。

**运行：**
```bash
cd project-1
pip3 install pandas
python csv_analyzer.py students.csv
```

**测试：**
```bash
pytest test_csv_analyzer.py -v
```

---

## 项目 2：JSON 配置文件读写器

读取 config.json，支持命令行修改任意配置项，含数据验证。

**运行：**
```bash
cd project-2
python config_editor.py --show
python config_editor.py --set theme light
python config_editor.py --set font_size 18
```

**测试：**
```bash
pytest test_config_editor.py -v
```

---

## 项目 3：命令行 Todo 管理器

任务持久化存储到 todos.json，支持增删查改。

**运行：**
```bash
cd project-3
python todo_cli.py add "买牛奶"
python todo_cli.py list
python todo_cli.py done 1
python todo_cli.py delete 1
```

**测试：**
```bash
pytest test_todo_cli.py -v
```

---

## 测试结果

| 项目 | 测试数 | 结果 |
|------|--------|------|
| 项目 1 CSV 分析器 | 12 | ✅ 全部通过 |
| 项目 2 配置读写器 | 13 | ✅ 全部通过 |
| 项目 3 Todo CLI | 12 | ✅ 全部通过 |
