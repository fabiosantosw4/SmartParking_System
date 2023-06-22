import time
import subprocess
import os
import cv2
import numpy as np
import random
from datetime import datetime
import pymysql
import shutil
from PIL import Image
import pygetwindow as gw
import torch
from yolov5 import YOLOv5

# Configurações do modelo YOLOv5
model_car = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model_plate = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')

# Gerar ID aleatório para nomear as imagens
img_path_id = str(random.randint(1, 9999))




# Loop para processar o vídeo quadro a quadro
video_path = 'video3.mp4'  # Caminho para o vídeo
video = cv2.VideoCapture(video_path)

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Detecção de carros
    results_car = model_car(frame)

    # Verificar se a tag 'car' foi detectada
    if 'car' in results_car.pandas().xyxy[0]['name'].tolist():
        # Salvar a imagem do carro com um ID único
        car_image_path = f'runs/detect/{img_path_id}_car.jpg'
        Image.fromarray(frame).save(car_image_path)

        # Detecção da matrícula na imagem do carro
        car_image = Image.open(car_image_path)
        results_plate = model_plate(car_image)

        # Verificar se a matrícula foi detectada
        if 'license_plate' in results_plate.pandas().xyxy[0]['name'].tolist():
            # Salvar a imagem da matrícula com o mesmo ID do carro
            plate_image_path = f'runs/detect/{img_path_id}_plate.jpg'
            Image.fromarray(np.array(car_image)).save(plate_image_path)

            # Chamar o processo do MATLAB para o OCR
            matlab_function = 'C:/ProjetoVA_VS/yolov5-master/matlabteste/im_matricula.m'
            image_file = os.path.abspath(plate_image_path)
            matlab_process = subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-r', f"im_matricula('{image_file}');exit;"])
            matlab_process.wait()
            
            # Verificar se ocorreu um erro durante a leitura da matrícula
            matlab_error_file = 'C:/ProjetoVA_VS/yolov5-master/matlabteste/error.txt'
            if os.path.exists(matlab_error_file):
                with open(matlab_error_file, 'r') as error_file:
                    error_message = error_file.read()
                print(f'Erro durante a leitura da matrícula: {error_message}')
                # Fechar o processo do MATLAB
                matlab_process.terminate()
                matlab_window = gw.getWindowsWithTitle('MATLAB Command Window')[0]
                matlab_window.close()
                continue

            # Ler o resultado do OCR
            with open('C:/ProjetoVA_VS/yolov5-master/matlabteste/matricula.txt', 'r') as file:
                time.sleep(15)  # Aguardar tempo suficiente para o arquivo de resultado ser gerado
                matricula = file.read()
            
            if matricula:
                print(f'Matrícula detectada: {matricula}')
                
                # Copiar e renomear a imagem da matrícula
                destination_folder = 'C:/xampp/htdocs/img_matriculas'
                plate_destination_path = os.path.join(destination_folder, f'{matricula}.jpg')
                shutil.copy(plate_image_path, plate_destination_path)
                
                # Conectar ao banco de dados
                db = pymysql.connect(host='localhost', user='root', passwd='', db='va_teste')
                
                # Criar um objeto cursor para interagir com o banco de dados
                cursor = db.cursor()
                
                # Verificar se a matrícula já existe no banco de dados
                select_query = "SELECT * FROM users WHERE matricula = %s"
                cursor.execute(select_query, (matricula,))
                result = cursor.fetchone()
                
                if result:
                    # Se a matrícula já existe, atualizar o timestamp de saída
                    update_query = "UPDATE users SET out_park = %s WHERE matricula = %s"
                    cursor.execute(update_query, (datetime.now(), matricula))
                else:
                    # Se a matrícula não existe, inserir a matrícula e um timestamp de entrada
                    pin = str(random.randint(1000, 9999))
                    insert_query = "INSERT INTO users (matricula, pin, in_park) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (matricula, pin, datetime.now()))
                
                # Confirmar as alterações no banco de dados
                db.commit()
                
                # Fechar a conexão com o banco de dados
                db.close()
            else:
                print('Matrícula não foi lida (OCR)')
        else:
            print('Matrícula não detectada')
    else:
        print('Carro não detectado')
    
video.release()