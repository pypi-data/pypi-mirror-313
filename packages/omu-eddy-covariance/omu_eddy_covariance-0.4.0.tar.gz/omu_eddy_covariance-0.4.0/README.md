# omu-eddy-covariance

このパッケージは、大阪公立大学生態気象学研究グループで実施されている、大気観測で得られたデータファイルを解析するPythonパッケージです。渦相関法を主とする大気観測データを対象としています。

## インストール

### 必要条件

- Python >= 3.11
- pip または uv

### インストール方法

```bash
pip install omu-eddy-covariance
```

または

```bash
uv add omu-eddy-covariance
```

## ライセンス

本ソフトウェアの使用は、大阪公立大学生態気象学研究グループの構成員、または著作権者から明示的な許可を得た第三者に限定されます。詳細は [LICENSE](https://github.com/omu-meteorology/omu-eddy-covariance/blob/main/LICENSE) を参照してください。

## ドキュメント

開発者に向けてドキュメントを作成しています。`storage/docs`配下に格納しています。

- [リファレンス](./storage/docs/references.md)
- パッケージの開発
  - [1. プロジェクトの初期設定](./storage/docs/development/1-init-project.md)
  - [2. Gitを用いた開発の概要](./storage/docs/development/2-overview-git.md)
  - [3. 新機能の追加](./storage/docs/development/3-add-features.md)
- [パッケージのデプロイ](./storage/docs/deployment.md)
- [コマンド集](./storage/docs/cmd.md)

## 更新履歴

主要な更新履歴を掲載しています。

| Date | Version | Description |
| :--- | :--- | :--- |
| 2024-11-20 | `v0.2.0` | `MobileSpatialAnalyzer`を追加 |
| 2024-11-20 | `v0.3.0` | `MobileSpatialAnalyzer.plot_scatter_c2h6_ch4`を追加 |

## コントリビュータ

- [connect0459](https://github.com/connect0459)
