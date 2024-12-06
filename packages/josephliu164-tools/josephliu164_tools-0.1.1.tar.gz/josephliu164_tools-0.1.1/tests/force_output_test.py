# force_output_test.py
import sys
import os

# 方法1：使用sys.stdout.write
sys.stdout.write("Testing sys.stdout.write\n")
sys.stdout.flush()  # 强制刷新输出缓冲区

# 方法2：使用os.write
os.write(1, b"Testing os.write\n")

# 方法3：使用sys.stderr
print("Testing stderr", file=sys.stderr)

# 方法4：使用logging
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Testing logging")

if __name__ == "__main__":
    # 添加这些状态检查
    print("Python version:", sys.version, file=sys.stderr)
    print("stdout isatty:", sys.stdout.isatty(), file=sys.stderr)
    print("stderr isatty:", sys.stderr.isatty(), file=sys.stderr)
    print("stdout fileno:", sys.stdout.fileno(), file=sys.stderr)
    print("stderr fileno:", sys.stderr.fileno(), file=sys.stderr)