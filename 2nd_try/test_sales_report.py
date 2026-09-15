"""2nd_try/report.py のテスト

テスト関数の docstring の1行目に、日本語で「何を確認するテストか」を1行書くこと。
"""

import pytest

from report import CsvExporter, PdfExporter, ReportExporter, SalesData, SalesItem


@pytest.fixture
def sales_data() -> SalesData:
    """要件のサンプルと同じ売上データ"""
    return SalesData([SalesItem("Apple", 100), SalesItem("Banana", 200)])


class TestSalesData:
    """売上データの保持と集計"""

    def test_total_sales(self, sales_data: SalesData) -> None:
        """売上データの合計金額を正しく計算できること"""
        assert sales_data.total_sales() == 300

    def test_items_are_kept(self, sales_data: SalesData) -> None:
        """与えられた売上データをそのまま保持できること"""
        assert sales_data.items == [SalesItem("Apple", 100), SalesItem("Banana", 200)]

    def test_total_sales_of_empty_data(self) -> None:
        """売上データが空のとき合計金額が0になること"""
        assert SalesData([]).total_sales() == 0


class TestCsvExporter:
    """CSV出力"""

    def test_export(self, sales_data: SalesData) -> None:
        """CSV出力が仕様どおりの文字列になること"""
        expected = "item,amount\nApple,100\nBanana,200"
        assert CsvExporter().export(sales_data) == expected

    def test_export_does_not_contain_total(self, sales_data: SalesData) -> None:
        """CSV出力に合計金額が含まれないこと"""
        assert "300" not in CsvExporter().export(sales_data)


class TestPdfExporter:
    """PDF出力"""

    def test_export_contains_total(self, sales_data: SalesData) -> None:
        """PDF出力に合計金額が含まれること"""
        assert "300" in PdfExporter().export(sales_data)


class TestOpenClosedPrinciple:
    """拡張のしやすさ（Open/Closed Principle）"""

    def test_new_format_needs_no_change_to_existing_classes(
        self, sales_data: SalesData
    ) -> None:
        """新しい出力形式は既存クラスを変更せずに追加できること"""

        class JsonExporter(ReportExporter):
            def export(self, data: SalesData) -> str:
                body = ", ".join(
                    f'{{"item": "{i.item}", "amount": {i.amount}}}' for i in data.items
                )
                return f"[{body}]"

        expected = '[{"item": "Apple", "amount": 100}, {"item": "Banana", "amount": 200}]'
        assert JsonExporter().export(sales_data) == expected

    def test_exporters_share_the_same_interface(self, sales_data: SalesData) -> None:
        """すべての出力クラスを ReportExporter として同じように扱えること"""
        exporters: list[ReportExporter] = [CsvExporter(), PdfExporter()]
        for exporter in exporters:
            assert isinstance(exporter.export(sales_data), str)
