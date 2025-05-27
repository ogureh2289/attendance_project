import cv2
from pyzbar import pyzbar
from datetime import datetime
import time
from db import get_student_by_token, record_attendance
import threading
from db import get_all_students_by_class

# Глобальные переменные
scanner_active = False
cap = None
window_created = False
scanner_thread = None
scanned_tokens = set()
lesson_context = {}


def determine_status(start_time_str, arrival_time_str):
    fmt = "%H:%M"
    start = datetime.strptime(start_time_str, fmt)
    arrival = datetime.strptime(arrival_time_str, fmt)
    diff = (arrival - start).total_seconds() / 60
    if diff <= 15:
        return "присутствовал"
    else:
        return "опоздал"


def init_camera():
    global cap
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return True
    return False


def stop_scanner():
    global scanner_active, cap
    scanner_active = False
    if cap:
        cap.release()
        cap = None
    print("Флаг сканера сброшен, камера освобождена")


def camera_loop(process_frame_callback):
    global scanner_active, cap, window_created

    if not init_camera():
        if hasattr(process_frame_callback, '__self__') and hasattr(process_frame_callback.__self__, 'on_failure'):
            process_frame_callback.__self__.on_failure("Не удалось запустить камеру")
        return

    scanner_active = True
    window_created = True
    last_time = 0
    fps_limit = 15

    try:
        while scanner_active:
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            if now - last_time >= 1.0 / fps_limit:
                process_frame_callback(frame)
                last_time = now

            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                scanner_active = False
                break
    finally:
        if cap:
            cap.release()
        if window_created:
            cv2.destroyAllWindows()
            window_created = False
        print("Сканер остановлен")



def start_qr_scanner(lesson_name, lesson_date, lesson_start, student_class,
                     on_success=None, on_failure=None):
    global scanned_tokens, lesson_context
    scanned_tokens = set()
    lesson_context = {
        "lesson_name": lesson_name,
        "lesson_date": lesson_date,
        "lesson_start": lesson_start,
        "student_class": student_class,
    }


    def process_frame(frame):
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            barcodes = pyzbar.decode(small_frame)

            for barcode in barcodes:
                token = barcode.data.decode("utf-8").strip()
                if not token or token in scanned_tokens:
                    continue

                student = get_student_by_token(token)
                if student:
                    student_id, full_name, s_class = student

                    arrival_time = datetime.now().strftime("%H:%M")
                    status = determine_status(lesson_start, arrival_time)
                    record_attendance(
                        lesson_name, lesson_date, student_id, s_class,
                        lesson_start, arrival_time, status
                    )
                    scanned_tokens.add(token)

                    msg = f"{full_name} ({s_class}) — {status}"
                    print(msg)
                    if on_success:
                        on_success(msg)
                else:
                    msg = f"Ученик не найден: {token}"
                    print(msg)
                    if on_failure:
                        on_failure(msg)
        except Exception as e:
            print(f"Ошибка обработки кадра: {str(e)}")

    print("Запуск сканера...")
    camera_loop(process_frame)


# Запуск в потоке
def run_scanner_in_thread(lesson_name, lesson_date, lesson_start, student_class,
                          on_success=None, on_failure=None):
    global scanner_thread

    scanner_thread = threading.Thread(
        target=start_qr_scanner,
        args=(lesson_name, lesson_date, lesson_start, student_class, on_success, on_failure),
        daemon=True
    )
    scanner_thread.start()


# Остановка с ожиданием завершения потока
def stop_and_join_scanner():
    global scanner_thread
    stop_scanner()
    if scanner_thread and scanner_thread.is_alive():
        scanner_thread.join(timeout=2)
        scanner_thread = None


def mark_absent_students():
    global scanned_tokens, lesson_context
    if not lesson_context:
        return

    all_students = get_all_students_by_class(lesson_context["student_class"])
    for student in all_students:
        student_id, full_name, s_class, token = student
        if token not in scanned_tokens:
            record_attendance(
                lesson_context["lesson_name"],
                lesson_context["lesson_date"],
                student_id,
                s_class,
                lesson_context["lesson_start"],
                "-",  # отсутствовал, не пришёл
                "отсутствовал"
            )
            print(f"{full_name} ({s_class}) — отсутствовал (не показал QR)")
