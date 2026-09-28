## uvのコマンド集

入っているライブラリのlist一覧
```
uv pip list
```

FastAPIのインストール
```
uv add "fastapi[standard]"
```

uvの初期化
```
uv init

// readmeを作成しないようにするコマンド
uv init --no-readme
```

FastAPIの起動
```
uv run uvicorn main:app --reload
```
