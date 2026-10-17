#!/usr/bin/env python3
"""
parse_traceback.py
Cắt tỉa log lỗi (Traceback Trimmer) cho vòng lặp Self-Healing.
Giúp thu gọn log kiểm thử còn 15-25 dòng trọng tâm nhất để tránh làm phình ngữ cảnh (token context).
"""

import re
import sys

MAX_LINES = 25

def trim_traceback(raw_text: str) -> str:
    lines = raw_text.splitlines()
    if len(lines) <= MAX_LINES:
        return raw_text

    # Tìm các dòng liên quan trực tiếp đến src/ và thông báo lỗi cuối cùng
    relevant_lines = []
    error_summary = []

    in_traceback = False
    for line in lines:
        if "Traceback (most recent call last):" in line or "FAILED " in line:
            in_traceback = True

        if in_traceback:
            # Ưu tiên các dòng liên quan đến src/ hoặc tests/
            if any(k in line for k in ["src/", "tests/", "AssertionError", "Error:", "Exception:"]):
                relevant_lines.append(line)
            elif line.startswith("E   ") or line.startswith(">   "):
                relevant_lines.append(line)

        # Bắt thông báo lỗi tổng kết cuối cùng
        if re.search(r"^(AssertionError|ValueError|TypeError|KeyError|HTTPException|Exception):", line):
            error_summary.append(line)

    if not relevant_lines:
        # Nếu không lọc được theo pattern, lấy 10 dòng đầu và 15 dòng cuối
        return "\n".join(lines[:10] + ["\n... [ĐÃ CẮT TỈA PHẦN GIỮA ĐỂ TIẾT KIỆM TOKEN] ...\n"] + lines[-15:])

    # Cắt gọn không quá MAX_LINES
    if len(relevant_lines) > MAX_LINES:
        trimmed = relevant_lines[-MAX_LINES:]
    else:
        trimmed = relevant_lines

    output = "[TÓM TẮT LỖI ĐÃ QUA BỘ LỌC CẮT TỈA TRỌNG TÂM]\n" + "\n".join(trimmed)
    if error_summary and error_summary[-1] not in output:
        output += "\n" + error_summary[-1]
    return output

def main():
    if len(sys.argv) > 1:
        # Đọc từ file
        with open(sys.argv[1], "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        # Đọc từ stdin
        content = sys.stdin.read()

    print(trim_traceback(content))

if __name__ == "__main__":
    main()
