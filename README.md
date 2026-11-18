bendwarn.github.io
==================

My profile blog. Start from [Lanyon](https://github.com/poole/lanyon).

文章可以在 front matter 中設定多個標籤：

```yaml
tags: [Functional Programming, Data Structures]
```

標籤會顯示於文章頁，並自動收錄至 `/tags/`。

作品集在 GitHub Actions 建置時，會從網站擁有者的公開 GitHub repo 找出已啟用 Pages 的專案（不含本站），並產生 `/portfolio/`。每次本站重新建置才會更新清單；也可從 Actions 手動執行部署。

本機預覽時先執行 `python3 scripts/fetch-portfolio.py`，再執行 `bundle exec github-pages build`。可選擇設定 `GITHUB_TOKEN` 以提高 GitHub API 配額。若 token 能讀取專案的 Pages 設定，會使用其實際網址；否則使用標準的 `https://帳號.github.io/專案/` 網址，因此使用自訂網域的專案需要可讀取該專案 Pages 設定的 token。
