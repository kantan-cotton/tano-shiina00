@echo off

if "%~1"=="" (
    echo MarkdownファイルをこのBATファイルにドラッグ＆ドロップしてください。
    pause
    exit /b
)

python "%~dp0frontmatter_convert.py" "%~1"

echo.
pause