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

### OpenAPI Linkを使用したステートフルテスト

OpenAPI仕様のLink機能を使用して、関連するエンドポイント間の依存関係をテストできます。これにより、リソース特定が必要なエンドポイント（例：`GET /users/{userId}`）のテストが可能になります。

```bash
# ステートフルテストの実行（実験的機能）
poetry run st run openapi.yaml --base-url=http://localhost:8000 --experimental=stateful-test-runner
```

#### ステートフルテストの仕組み

1. **OpenAPI Link**: OpenAPI仕様内で定義されたリンクにより、エンドポイント間の関連性が表現されます。
   - 例：`POST /users/` → `GET /users/{userId}`（作成したユーザーの取得）
   - 例：`GET /users/{userId}` → `PUT /users/{userId}`（取得したユーザーの更新）

2. **テストシナリオ**: Schemathesisは定義されたリンクに基づいて自動的にテストシナリオを生成します。
   - ユーザー作成 → 取得 → 更新 → 削除
   - ユーザー作成 → 更新 → 取得 → 削除
   - その他様々な組み合わせ

3. **レポート**: テスト結果には、各リンクの成功率や失敗したケースの詳細が含まれます。

この方法により、単一エンドポイントのテストだけでなく、APIの実際の利用シナリオに近いテストが可能になります。

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

### 自動更新の仕組み

このリポジトリには、OpenAPI仕様が更新されるたびに自動的にGitHub Pages上のドキュメントを更新するGitHub Actionsワークフローが設定されています。メインブランチの`openapi.yaml`ファイルに変更がプッシュされると、自動的に`docs/openapi.yaml`ファイルも更新され、最新の仕様がSwagger UIに反映されます。

この自動化により、APIドキュメントが常に最新の状態に保たれます。
