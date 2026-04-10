import cv2
import mediapipe as mp
import pydirectinput

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Buka Kamera
cap = cv2.VideoCapture(0)
pydirectinput.FAILSAFE = False

# Daftar tombol yang kita pakai
current_keys = {'w': False, 'a': False, 's': False, 'd': False, 'space': False}

#
def update_keys(active_key):
    for key in current_keys:
        if key == active_key:
            if not current_keys[key]:
                pydirectinput.keyDown(key)
                current_keys[key] = True
        else:
            if current_keys[key]: 
                pydirectinput.keyUp(key)
                current_keys[key] = False

print("Sistem Hitung Jari Aktif! Buka 5 jari untuk Diam.")
print("Tekan 'q' di jendela kamera untuk keluar.")

while True:
    success, img = cap.read()
    if not success:
        break

   
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    active_key = None # Default: Tidak ada tombol yang ditekan (Diam)
    pesan_layar = "DIAM (5 Jari)"
    warna_teks = (0, 255, 0) # Hijau

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- LOGIKA MENGHITUNG JARI TERBUKA ---
            jari_terbuka = 0
            
            # Titik ujung jari (Tip) dan sendi bawah jari (PIP)
            # Telunjuk (8, 6), Tengah (12, 10), Manis (16, 14), Kelingking (20, 18)
            tips = [8, 12, 16, 20]
            pips = [6, 10, 14, 18]

            # Cek 4 jari utama (selain jempol)
            for tip, pip in zip(tips, pips):
                # Jika posisi Y ujung jari lebih tinggi (angka lebih kecil) dari sendinya, berarti jari terbuka
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    jari_terbuka += 1

          
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[2].x:
                jari_terbuka += 1

            if jari_terbuka == 0:
                active_key = 'space'
                pesan_layar = "LONCAT! (Kepal)"
                warna_teks = (0, 0, 255)
            elif jari_terbuka == 1:
                active_key = 'w'
                pesan_layar = "MAJU (1 Jari)"
                warna_teks = (255, 0, 0) 
                active_key = 'a'
                pesan_layar = "KIRI (2 Jari)"
                warna_teks = (255, 0, 0)
            elif jari_terbuka == 3:
                active_key = 'd'
                pesan_layar = "KANAN (3 Jari)"
                warna_teks = (255, 0, 0)
            elif jari_terbuka == 4:
                active_key = 's'
                pesan_layar = "MUNDUR (4 Jari)"
                warna_teks = (255, 0, 0)
            else:
                active_key = None
                pesan_layar = "DIAM (5 Jari)"
                warna_teks = (0, 255, 0)

            # Tampilkan teks di layar kamera
            cv2.putText(img, pesan_layar, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, warna_teks, 3)

    update_keys(active_key)

   
    cv2.imshow("Roblox Controller AI", img)

    # Keluar jika tekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan semua tombol sebelum aplikasi ditutup agar keyboard tidak nyangkut
update_keys(None)
cap.release()
cv2.destroyAllWindows()