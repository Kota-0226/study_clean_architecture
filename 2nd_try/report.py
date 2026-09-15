"""売上レポート（SRP・OCPを適用した版）

- SalesData      : 売上データの保持と集計だけを担当する（出力形式を一切知らない）
- ReportExporter : 「売上データを文字列に変換する」という抽象インターフェース
- CsvExporter    : CSV文字列の生成だけを担当する具象クラス
- PdfExporter    : PDFレイアウト文字列の生成だけを担当する具象クラス

新しい出力形式を足したくなったら、ReportExporter を継承したクラスを1つ追加するだけでよく、
SalesData も既存の Exporter も変更する必要がない（＝Open/Closed Principle）。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SalesItem:
    """1件分の売上（商品名と金額）を表すデータ"""

    item: str
    amount: int


class SalesData:
    """売上データの保持と集計だけを担当するクラス（Single Responsibility Principle）

    CSVやPDFといった「出力形式」については何も知らない。
    """

    def __init__(self, items: list[SalesItem]) -> None:
        self._items = list(items)

    @property
    def items(self) -> list[SalesItem]:
        """保持している売上データ（呼び出し側から書き換えられないようコピーを返す）"""
        return list(self._items)

    def total_sales(self) -> int:
        """すべての売上の合計金額"""
        return sum(item.amount for item in self._items)


class ReportExporter(ABC):
    """出力形式の抽象インターフェース（Open/Closed Principle の拡張点）"""

    @abstractmethod
    def export(self, data: SalesData) -> str:
        """売上データを、その形式の文字列に変換して返す"""
        raise NotImplementedError


class CsvExporter(ReportExporter):
    """CSV文字列の生成だけを担当するクラス

    要件どおり、合計金額は含めない（ヘッダー行と明細行だけ）。
    """

    HEADER = "item,amount"

    def export(self, data: SalesData) -> str:
        lines = [self.HEADER]
        lines.extend(f"{item.item},{item.amount}" for item in data.items)
        return "\n".join(lines)


class PdfExporter(ReportExporter):
    """PDF用レイアウト文字列の生成だけを担当するクラス

    要件どおり、合計金額を含める。
    """

    def export(self, data: SalesData) -> str:
        return f"[PDF Data] Total Sales: {data.total_sales()}"


def main() -> None:
    """動作確認用のエントリポイント"""
    data = SalesData([SalesItem("Apple", 100), SalesItem("Banana", 200)])

    # 出力形式は ReportExporter 型として扱えるので、増やしてもこのループは変わらない
    exporters: list[ReportExporter] = [CsvExporter(), PdfExporter()]
    for exporter in exporters:
        print(f"--- {type(exporter).__name__} ---")
        print(exporter.export(data))
        print()


if __name__ == "__main__":
    main()
