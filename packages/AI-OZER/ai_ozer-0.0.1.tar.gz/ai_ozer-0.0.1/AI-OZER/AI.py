import cv2
import torch
from ultralytics import YOLO

def main():
    # Yüz ifadesi tanımak için model yükleyin
    # YOLOv5 modelini yükle (yolov5s en küçük modeldir)
    #model = torch.hub.load('ultralytics/yolov5', 'yolov5x')
    model = YOLO('yolo11x.pt')

    # Yüz ifadesi etiketleri
    #expressions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    # OpenCV yüz tespiti için Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000.caffemodel')

     # Cihazı kontrol et ve GPU kullanımı için ayar yap
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    print(f"Device being used: {device}")
    #print(torch.cuda.is_available())  # True dönerse CUDA kullanılabilir
    #print(torch.cuda.device_count())   # Kullanılabilir GPU sayısını gösterir
    #print(torch.cuda.current_device()) # Şu anda kullanılan GPU'yu gösterir

    # Kamerayı başlat
    cap = cv2.VideoCapture(0)
    target_fps = 60
    cap.set(cv2.CAP_PROP_FPS, target_fps)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Modeli kullanarak nesne tespiti yap
        results = model(frame)

        # Sonuçları görüntüle
        frame = results[0].plot()  # Nesneleri işaretler

        # Sonuçları ekranda göster
        cv2.imshow('YOLOv11 - Web Kamera', frame)

        # 'q' tuşuna basıldığında çıkış yap
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

main()