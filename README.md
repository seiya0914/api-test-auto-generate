# ユーザー管理 API

このプロジェクトは、SQLAlchemy と FastAPI を使用したユーザー管理 API の実装です。データベースを使用してユーザー情報を管理し、RESTful API を通じてアクセスできます。

## 機能

- ユーザーの一覧取得
- ユーザーの詳細取得
- ユーザーの作成
- ユーザーの更新
- ユーザーの削除

## 技術スタック

- Python 3.13+
- FastAPI - Web API フレームワーク
- SQLAlchemy - ORM（オブジェクト関係マッピング）
- SQLite - データベース
- Pydantic - データバリデーション
- Uvicorn - ASGI サーバー
- Schemathesis - API テスト自動化ツール

## 前提条件

- Python 3.13 以上
- Poetry（依存関係管理ツール）

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <リポジトリURL>
cd API自動テスト生成
```

### 2. 依存関係のインストール

```bash
poetry install
```

### 3. アプリケーションの実行

```bash
poetry run python app.py
```

または

```bash
poetry run uvicorn app:app --reload
```

アプリケーションは http://localhost:8000 で実行されます。

## API ドキュメント

FastAPI の自動生成されたドキュメントは以下の URL で確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API テスト

### Schemathesis を使用した API テスト

Schemathesis は OpenAPI 仕様に基づいて API テストを自動生成・実行するツールです。以下のコマンドでテストを実行できます：

```bash
# OpenAPI 仕様ファイルを使用して API テストを実行
poetry run st run openapi.yaml --base-url=http://localhost:8000

# 詳細なレポートを出力
poetry run st run openapi.yaml --base-url=http://localhost:8000 --report

# 特定のエンドポイントのみテスト
poetry run st run openapi.yaml --base-url=http://localhost:8000 --endpoint "/users/"

# テストケース数を増やす
poetry run st run openapi.yaml --base-url=http://localhost:8000 --hypothesis-max-examples=100
```

## API エンドポイント

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| GET | / | ルートエンドポイント |
| GET | /users/ | ユーザー一覧の取得 |
| POST | /users/ | 新規ユーザーの作成 |
| GET | /users/{user_id} | 特定ユーザーの取得 |
| PUT | /users/{user_id} | ユーザー情報の更新 |
| DELETE | /users/{user_id} | ユーザーの削除 |

## OpenAPI 仕様

OpenAPI 仕様は `openapi.yaml` ファイルで定義されています。この仕様を使用して、クライアントコードの生成やテストの自動化が可能です。

### オンラインでの閲覧

以下のリンクからOpenAPI仕様をオンラインで閲覧できます：

- [GitHub Pages上のSwagger UI](https://seiya0914.github.io/api-test-auto-generate/) - 対話的なドキュメント
- [GitHub上のOpenAPI仕様ファイル](https://github.com/seiya0914/api-test-auto-generate/blob/main/openapi.yaml) - YAML形式の仕様ファイル

GitHub Pagesを有効にするには、GitHubリポジトリの「Settings」→「Pages」から設定してください。
