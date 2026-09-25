@echo off
cd /d "C:\Users\white\Documents\PaperMod"

if "%~1"=="" (
    echo MarkdownファイルをこのBATファイルにドラッグ＆ドロップしてください。
    pause
    exit /b
)

python frontmatter_convert.py "%~1"

echo.
pause