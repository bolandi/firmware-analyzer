from pathlib import Path

git sdef create_target_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
