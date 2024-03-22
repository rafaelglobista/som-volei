import cv2
import time
from collections import deque

# Endereço da câmera IP
camera_ip = "rtsp://admin:vigia2456@192.168.0.104:554/user=admin_password=vigia2456_channel=1_stream=1.sdp?real_stream"

# Configurações de vídeo
output_fps = 13
output_width = 640
output_height = 480

# Buffer para armazenar os últimos frames durante 20 segundos
buffer_size = 20 * output_fps  # 20 segundos de vídeo
frame_buffer = deque(maxlen=buffer_size)

# Função para lidar com a tecla pressionada
def on_key_press(key):
    global should_record
    if key == ord('r'):
        should_record = True

# Inicia a captura de vídeo da câmera IP
cap = cv2.VideoCapture(camera_ip)

# Verifica se a captura foi bem sucedida
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

# Obtém as configurações de captura de vídeo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_fps = (cap.get(cv2.CAP_PROP_FPS))
output_width = frame_width
output_height = frame_height

# Cria uma janela para exibir a imagem
cv2.namedWindow("Camera IP")

# Variável para controlar a gravação
should_record = False

# Loop principal
while True:
    # Captura um frame
    ret, frame = cap.read()

    if ret:
        # Adiciona o frame ao buffer
        frame_buffer.append(frame.copy())

        # Exibe o frame em tempo real
        cv2.imshow("Camera IP", frame)

        # Verifica se a tecla foi pressionada
        key = cv2.waitKey(1)
        on_key_press(key)

        # Se a gravação estiver ativada, salva o vídeo do buffer
        if should_record:
            # Gera um nome de arquivo único baseado no timestamp atual
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_filename = f"output_video_{timestamp}.mp4"  # Alterado para usar o formato AVI
            
            # Determina o intervalo de frames correspondente aos últimos 20 segundos
            start_frame_index = max(0, len(frame_buffer) - buffer_size)
            end_frame_index = len(frame_buffer)

            # Cria um objeto VideoWriter para salvar o vídeo
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_filename, fourcc, output_fps, (output_width, output_height))

            # Grava os frames do buffer correspondentes aos últimos 20 segundos
            for i in range(start_frame_index, end_frame_index):
                out.write(frame_buffer[i])

            # Libera o objeto VideoWriter
            out.release()

            should_record = False  # Reseta a flag de gravação após a gravação do vídeo

    # Verifica se o usuário pressionou 'q' para sair
    if key == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()