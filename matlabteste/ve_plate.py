import time
from yolov5 import YOLOv5
from PIL import Image
import torch
import subprocess
import os
import numpy as np

import pymysql
import random
import shutil
from datetime import datetime
import random

with open('C:\ProjetoVA_VS\yolov5-master\matlabteste\matricula.txt', 'w') as file:
    file.write('')

img_path_id = random.randint(1, 9999)
print(img_path_id)
image1 = 'car9.jpg'
print(image1)
image = Image.open(image1)

model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')


results = model(image)

crops = results.crop(save=True, save_dir=f'runs/detect/'+str(img_path_id))

#-------------Abrir matlab-----------------
# Define o caminho do arquivo .m e da imagem
matlab_function = 'C:\ProjetoVA_VS\yolov5-master\matlabteste\im_matricula.m'
#image_file = 'C:/xampp/htdocs/img_matriculas/'+matricula+'.jpg'
image_file = 'C:/ProjetoVA_VS/yolov5-master/matlabteste/runs/detect/'+str(img_path_id)+'/crops/license_plate/'+image1

# Carrega a imagem usando a biblioteca PIL
#image = np.array(Image.open(image_file))

# Chama o Matlab e executa a função com a imagem como argumento
matlab_process=subprocess.Popen(['matlab', '-nodesktop', '-nosplash', '-r', f"im_matricula('{image_file}');exit;"])

# Wait for MATLAB subprocess to finish
matlab_process.wait()

# Continue with the rest of your Python code
print("MATLAB subprocess has finished.")

#---------------------------------------



with open('C:\ProjetoVA_VS\yolov5-master\matlabteste\matricula.txt', 'r') as file:
    time.sleep(15)
    matricula = file.read()



print(matricula)
#---------------------ENCONTRAR IMAGEM ORIGINAL----------------------------
# Set the directory path where the images are located
dir_path = os.path.join("C:/ProjetoVA_VS/yolov5-master/matlabteste/runs/detect/"+str(img_path_id))

# Get a list of all the files in the directory
file_list = os.listdir(dir_path)

# Use a list comprehension to filter out non-image files
image_list = [f for f in file_list if f.endswith('.jpg') or f.endswith('.png')]

# Get the name of the first image in the list
if len(image_list) > 0:
    image_encontrada_OR = image_list[0]
    print(image_encontrada_OR)
else:
    print('No images found in directory.')


#--------------COPIAR E MUDAR NOME DA IMAGEM--------------
# Set the source and destination folders
source_folder = 'C:/ProjetoVA_VS/yolov5-master/matlabteste/runs/detect/'
destination_folder = 'C:/xampp/htdocs/img_matriculas'

# Set the file name
file_name = image_encontrada_OR

# Get the full path to the source file
source_path = os.path.join(source_folder,str(img_path_id) , file_name)

# Get the full path to the destination file
destination_path = os.path.join(destination_folder, file_name)

# Move the file from source to destination
#shutil.copy(source_path, destination_path)

matricula1= 'C:/xampp/htdocs/img_matriculas/'+matricula+'.jpg'



#model = YOLOv5('C:/ProjetoVA_VS/yolov5-master/matlabteste/yolov5s.pt')




if os.path.exists(matricula1):
    print("O arquivo existe!")
else:
    shutil.copy(source_path, destination_path)
    os.rename(destination_path,matricula1)


#---------------------BASE DE DADOS ---------------------------------------------------
# Connect to the database
db = pymysql.connect(host='localhost', user='root', passwd='', db='va_teste')

# Create a cursor object to interact with the database
cursor = db.cursor()



# Prepare the SQL query to check if the text already exists in the database
select_query = "SELECT * FROM users WHERE matricula = %s"

# Execute the query with the text data as a parameter
cursor.execute(select_query, (matricula,))

# Check if the text already exists in the database
result = cursor.fetchone()
if result:
    # If the text exists, insert an "out_park" timestamp
    update_query = "UPDATE users SET out_park = %s WHERE matricula = %s"
    cursor.execute(update_query, (datetime.now(), matricula))
else:
    # If the text does not exist, insert the text and an "in_park" timestamp
    pin = str(random.randint(1000, 9999))
    insert_query = "INSERT INTO users (matricula, pin, in_park) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (matricula, pin,datetime.now()))

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()
#------------------------------------------------------------------------------------
