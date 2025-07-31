{
  "testDir": "./tests/e2e",
  "outputDir": "./test-results",
  "fullyParallel": true,
  "retries": 1,
  "workers": 1,
  "reporter": [
    ["list"],
    ["html", { "outputFolder": "playwright-report" }]
  ],
  "use": {
    "baseURL": "http://localhost:8501",
    "trace": "on-first-retry",
    "screenshot": "only-on-failure",
    "video": "retain-on-failure"
  },
  "projects": [
    {
      "name": "chromium",
      "use": {
        "browserName": "chromium"
      }
    }
  ],
  "webServer": {
    "command": "streamlit run src/web/app.py",
    "port": 8501,
    "timeout": 120000,
    "reuseExistingServer": true
  }
}