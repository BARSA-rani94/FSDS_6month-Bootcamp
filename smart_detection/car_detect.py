import cv2

# Load car Haar cascade
car_classifier_path = r"C:\Users\HP\Downloads\New folder\13th- Haar cascade classifier\Haarcascades\haarcascade_car.xml"
car_classifier = cv2.CascadeClassifier(car_classifier_path)

if car_classifier.empty():
    print("Error: Could not load cascade")
    exit()

# Video
video_path = r"C:\Users\HP\Downloads\cars.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video")
    exit()

print("Video opened successfully. Starting car detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame or video has ended.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_classifier.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(60, 60)
    )

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    cv2.imshow("Car Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
