import time

import cv2
import time

class FPS:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.num_frames = 0

    def start(self):
        self.start_time = time.time()
        self.num_frames = 0

    def stop(self):
        self.end_time = time.time()

    def update(self):
        self.num_frames += 1

    def elapsed(self):
        return time.time() - self.start_time

    def fps(self):
        return self.num_frames / self.elapsed()


def print_FPS_used():
    print(
        """

from tatools import FPS
          
# Sử dụng class FPS
fps = FPS()
fps.start()

cap = cv2.VideoCapture(0)  # Mở camera mặc định
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Cập nhật số lượng khung hình và tính toán FPS
    fps.update()
    current_fps = fps.fps()

    # Hiển thị FPS lên khung hình
    cv2.putText(frame, f"FPS: {current_fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Hiển thị khung hình
    cv2.imshow('Frame', frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fps.stop()
cap.release()
cv2.destroyAllWindows()

print(f"Elapsed time: {fps.elapsed():.2f} seconds")
print(f"FPS: {fps.fps():.2f}")
"""
    )


class MultiTimer:
    def __init__(self):
        self.times = {}  # Lưu trữ thời gian của mỗi đoạn code
        self.start_time = None

    def start(self):
        """Bắt đầu đo thời gian."""
        self.start_time = time.time()
    def stop(self):
        """Bắt đầu đo thời gian."""
        self.start_time = None

    def update(self, label):
        """Dừng đo thời gian và lưu kết quả cho một đoạn code với nhãn (label)."""
        if self.start_time is None:
            raise Exception("Timer has not been started yet!")
        elapsed_time = time.time() - self.start_time
        if label in self.times:
            self.times[label].append(elapsed_time)
        else:
            self.times[label] = [elapsed_time]
        self.start_time = time.time()

    def reset(self):
        """Đặt lại bộ đếm thời gian."""
        self.start_time = None
        self.times = {}

    def summary(self):
        """In ra kết quả đo thời gian cho tất cả các đoạn code."""
        if not self.times:
            print("No times recorded.")
        else:
            print("\n=== Time Summary ===")
            for label, times in self.times.items():
                total_time = sum(times)
                avg_time = total_time / len(times)
                print(f"Code: {label}")
                print(f"  Total time: {total_time:.6f} seconds")
                print(f"  Average time: {avg_time:.6f} seconds")
                print(f"  Runs: {len(times)}\n")

if __name__ == "__main__":
    # Ví dụ sử dụng class MultiTimer
    timer = MultiTimer()

    # Đo thời gian cho đoạn code 1
    timer.start()
    # Đoạn code mà bạn muốn đo (ví dụ 1)
    for _ in range(1000000):
        pass
    timer.update("Code 1")

    # Đo thời gian cho đoạn code 2
    timer.start()
    # Đoạn code mà bạn muốn đo (ví dụ 2)
    time.sleep(1)
    timer.update("Code 2")

    # Đo lại thời gian cho Code 1
    timer.start()
    for _ in range(500000):
        pass
    timer.update("Code 1")

    # In ra kết quả cuối cùng
    timer.summary()
