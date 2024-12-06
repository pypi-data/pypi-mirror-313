@echo off
cd /d %~dp0
python trans_excel_to_inventory.py
echo trans_excel_to_inventory completed.
pause