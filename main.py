import subprocess

scripts = [
    "spx_auto.py",
    "task_manager.py",
    "news_fetcher.py"
]

processes = []

for script in scripts:
    print(f"🚀 تشغيل: {script}")
    p = subprocess.Popen(["python3", script])
    processes.append(p)

# ننتظر جميع العمليات
for p in processes:
    p.wait()