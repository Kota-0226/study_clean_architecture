"""テスト結果を初学者向けに日本語で表示するための pytest 設定。

各テストの docstring の1行目を「説明」として扱い、

  - ターミナル: Before / After ごとにグループ分けした日本語の一覧
  - HTML レポート (reports/report.html): 「説明」列

の両方に反映します。テストを追加したときは docstring を1行書くだけで、
どちらの出力にも自動的に載ります。
"""

import pytest

# nodeid（テストの識別子）をキーに、表示用の情報を集めておく
_DESCRIPTIONS: dict[str, str] = {}  # nodeid -> テストの日本語説明
_GROUPS: dict[str, str] = {}  # nodeid -> 所属するグループの見出し
_GROUP_ORDER: list[str] = []  # 見出しの表示順（テストを集めた順）

# テスト結果に対応する記号
_MARKS = {
    "passed": "✅",
    "failed": "❌",
    "error": "❌",
    "skipped": "⏭️",
}


def _first_line(doc: str | None, fallback: str) -> str:
    """docstring の最初の1行を取り出す。書かれていなければ fallback を返す。"""
    for line in (doc or "").splitlines():
        line = line.strip()
        if line:
            return line
    return fallback


def pytest_collection_modifyitems(items):
    """テストを集め終えた時点で、各テストの説明とグループを控えておく。"""
    for item in items:
        _DESCRIPTIONS[item.nodeid] = _first_line(
            getattr(item.function, "__doc__", None), item.name)

        cls = getattr(item, "cls", None)
        group = _first_line(getattr(cls, "__doc__", None),
                            cls.__name__ if cls else "テスト")
        _GROUPS[item.nodeid] = group
        if group not in _GROUP_ORDER:
            _GROUP_ORDER.append(group)


def pytest_terminal_summary(terminalreporter):
    """ターミナルの最後に、日本語の結果一覧を表示する。"""
    if not _DESCRIPTIONS:
        return

    # nodeid ごとの結果（passed / failed / error / skipped）を集める
    outcomes: dict[str, str] = {}
    for key in ("passed", "failed", "error", "skipped"):
        for report in terminalreporter.stats.get(key, []):
            nodeid = getattr(report, "nodeid", None)
            if nodeid:
                outcomes.setdefault(nodeid, key)

    terminalreporter.write_sep("=", "テスト結果")
    for group in _GROUP_ORDER:
        terminalreporter.write_line("")
        terminalreporter.write_line(group, bold=True)
        for nodeid, description in _DESCRIPTIONS.items():
            if _GROUPS.get(nodeid) != group:
                continue
            mark = _MARKS.get(outcomes.get(nodeid, ""), "・")
            terminalreporter.write_line(f"  {mark} {description}")

    total = len(_DESCRIPTIONS)
    passed = sum(1 for nodeid in _DESCRIPTIONS
                 if outcomes.get(nodeid) == "passed")
    terminalreporter.write_line("")
    if passed == total:
        terminalreporter.write_line(f"{total}件すべて成功しました", green=True)
    else:
        terminalreporter.write_line(
            f"{total}件中 {passed}件が成功、{total - passed}件は失敗または未実行です",
            red=True)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """HTML レポート側から説明文を参照できるよう、結果に説明を持たせる。"""
    report = yield
    report.description = _DESCRIPTIONS.get(item.nodeid, "")
    return report


def pytest_html_report_title(report):
    """HTML レポートのタイトル。"""
    report.title = "SOLID原則の学習用テスト結果"


def pytest_html_results_table_header(cells):
    """HTML レポートの表に「説明」列を追加する。"""
    cells.insert(2, "<th>説明</th>")


def pytest_html_results_table_row(report, cells):
    """HTML レポートの各行に、そのテストの説明を入れる。"""
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")
