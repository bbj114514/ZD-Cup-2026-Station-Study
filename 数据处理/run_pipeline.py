from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run_script(script_path: Path, step: int, total: int) -> None:
    print(f"[{step}/{total}] Running: {script_path}")
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    result = subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent))
    if result.returncode != 0:
        raise RuntimeError(f"Script failed with exit code {result.returncode}: {script_path}")


def copy_file(src: Path, dst: Path) -> None:
    print(f"Copying: {src} -> {dst}")
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    root = Path(__file__).resolve().parent

    rider_scripts = [
        root / "数据处理_rider" / "scripts" / "seperate.py",
        root / "数据处理_rider" / "scripts" / "rename.py",
        root / "数据处理_rider" / "scripts" / "categorize.py",
        root / "数据处理_rider" / "scripts" / "clean.py",
        root / "数据处理_rider" / "scripts" / "reliability.py",
        root / "数据处理_rider" / "scripts" / "validity.py",
        root / "数据处理_rider" / "scripts" / "encode.py",
        root / "数据处理_rider" / "scripts" / "descriptive_statistic.py",
        root / "数据处理_rider" / "scripts" / "pain_point_and_need.py",
        root / "数据处理_rider" / "scripts" / "difference.py",
        root / "数据处理_rider" / "scripts" / "TAM.py",
        root / "数据处理_rider" / "scripts" / "willingness_to_pay.py",
    ]

    merchant_scripts = [
        root / "数据处理_merchant" / "scripts" / "clean.py",
        root / "数据处理_merchant" / "scripts" / "encode.py",
        root / "数据处理_merchant" / "scripts" / "descriptive_statistic.py",
        root / "数据处理_merchant" / "scripts" / "difference.py",
        root / "数据处理_merchant" / "scripts" / "driver_regression.py",
        root / "数据处理_merchant" / "scripts" / "mismatch.py",
    ]

    resident_scripts = [
        root / "数据处理_resident" / "scripts" / "clean.py",
        root / "数据处理_resident" / "scripts" / "encode.py",
        root / "数据处理_resident" / "scripts" / "descriptive_statistic.py",
        root / "数据处理_resident" / "scripts" / "NIMBY.py",
        root / "数据处理_resident" / "scripts" / "diff.py",
        root / "数据处理_resident" / "scripts" / "management.py",
        root / "数据处理_resident" / "scripts" / "three_party.py",
        root / "数据处理_resident" / "scripts" / "attachment_nimby.py",
    ]

    total_steps = len(rider_scripts) + len(merchant_scripts) + len(resident_scripts)
    total_steps += 5
    step = 0

    print("=== Stage 1: Rider ===")
    for script in rider_scripts:
        step += 1
        run_script(script, step, total_steps)

    rider_encoded = root / "数据处理_rider" / "data" / "rider_encoded.csv"

    step += 1
    print(f"[{step}/{total_steps}] Copy merchant.csv to merchant data as merchant.csv")
    copy_file(root / "数据处理_rider" / "data" / "merchant.csv", root / "数据处理_merchant" / "data" / "merchant.csv")

    step += 1
    print(f"[{step}/{total_steps}] Copy resident.csv to resident data as resident.csv")
    copy_file(root / "数据处理_rider" / "data" / "resident.csv", root / "数据处理_resident" / "data" / "resident.csv")

    step += 1
    print(f"[{step}/{total_steps}] Copy rider_encoded.csv to merchant data")
    copy_file(rider_encoded, root / "数据处理_merchant" / "data" / "rider_encoded.csv")

    step += 1
    print(f"[{step}/{total_steps}] Copy rider_encoded.csv to resident data as rider_final_Encoded.csv")
    copy_file(rider_encoded, root / "数据处理_resident" / "data" / "rider_final_Encoded.csv")

    print("=== Stage 2: Merchant ===")
    for script in merchant_scripts:
        step += 1
        run_script(script, step, total_steps)

    merchant_encoded = root / "数据处理_merchant" / "data" / "merchant_final_encoded.csv"

    step += 1
    print(f"[{step}/{total_steps}] Copy merchant_final_encoded.csv to resident data")
    copy_file(merchant_encoded, root / "数据处理_resident" / "data" / "merchant_final_encoded.csv")

    print("=== Stage 3: Resident ===")
    for script in resident_scripts:
        step += 1
        run_script(script, step, total_steps)

    print("All pipeline steps completed successfully.")


if __name__ == "__main__":
    main()