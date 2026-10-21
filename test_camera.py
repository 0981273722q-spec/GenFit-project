
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("無法開啟攝影機，請確認攝影機是否已連接。")
else:
    print("攝影機開啟成功！按 Q 可離開。")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("無法讀取攝影機畫面。")
            break

        cv2.imshow("GenFit Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
