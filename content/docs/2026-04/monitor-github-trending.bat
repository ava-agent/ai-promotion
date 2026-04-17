@echo off
echo 🔄 启动GitHub Trending监控...
cd /d C:\Users\PC\.openclaw\workspace
python scripts\github-trending-monitor.py
echo ✅ 监控完成
pause