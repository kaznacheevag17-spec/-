#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image, ImageFilter, ImageEnhance
import os

app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor')

but_folder = QPushButton('Папка')
but_left = QPushButton('Влево')
but_right = QPushButton('Вправо')
but_mirror = QPushButton('Отзеркалить')
but_sharpness = QPushButton('Резкость')
but_BW = QPushButton('Ч/Б')

list_buttons = []
list_buttons.append(but_folder)
list_buttons.append(but_left)
list_buttons.append(but_right)
list_buttons.append(but_mirror)
list_buttons.append(but_sharpness)
list_buttons.append(but_BW)

photo = QLabel('Картинка')
list_names_f = QListWidget()

layout1_h = QHBoxLayout()
layout2_h = QHBoxLayout()
layout_v = QVBoxLayout()

for i in list_buttons:
    layout1_h.addWidget(i)

layout2_h.addWidget(list_names_f, 1)
layout2_h.setSpacing(45)
layout2_h.addWidget(photo, 5)
layout_v.addLayout(layout2_h)
layout_v.addLayout(layout1_h)
window.setLayout(layout_v)

for i in list_buttons:
    i.setFont(QFont('Arial', 12))

def chooseWorkdir():
    global workdir 
    workdir = QFileDialog.getExistingDirectory().replace('/', '\\')
    
def filter(file_names, extensions):
    for i in file_names:
        for j in extensions:
            if i.endswith(j.lower()):
                list_names_f.addItem(i)
                break

extensions = ['.JPG','.PNG','.ICO','.GIF','.TIFF','.WebP','.EPS','.SVG']

def showFilenamesList():
    chooseWorkdir()
    file_names = os.listdir(workdir)
    filter(file_names, extensions)

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.file_path = None

    def loadimage(self, filename, file_path):
        self.filename = filename
        self.file_path = file_path
        self.fullname = os.path.join(self.file_path, self.filename)
        self.orig_photo = Image.open(self.fullname)

    def showimage(self):
        pixmapimage = QPixmap(self.fullname)
        width = photo.width()
        height = photo.height()
        pixmapimage = pixmapimage.scaled(width, height, Qt.KeepAspectRatio)
        photo.setPixmap(pixmapimage)

    def saveImage(self):
        global workdir
        self.file_path = os.path.join(workdir, 'modified')
        
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)

        self.fullname = os.path.join(self.file_path, self.filename)
        self.orig_photo.save(self.fullname)



    def do_bw(self):
        self.orig_photo = self.orig_photo.convert('L')
        self.saveImage()
        self.showimage()
        
    def do_mirror(self):
        self.orig_photo = self.orig_photo.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.showimage()
        
    def do_right(self):
        self.orig_photo = self.orig_photo.transpose(Image.ROTATE_270)
        self.saveImage()
        self.showimage()

    def do_left(self):
        self.orig_photo = self.orig_photo.transpose(Image.ROTATE_90)
        self.saveImage()
        self.showimage()
        
    def change_sharpness(self):
        self.orig_photo = ImageEnhance.Contrast(self.orig_photo)
        self.orig_photo = self.orig_photo.enhance(1.5)
        self.saveImage()
        self.showimage()
        
workimage = ImageProcessor()        

def show():
    if list_names_f.currentRow() >= 0:
        name = list_names_f.currentItem().text()
        workimage.loadimage(name, workdir)
        workimage.showimage()


but_folder.clicked.connect(showFilenamesList)
list_names_f.currentRowChanged.connect(show)
but_BW.clicked.connect(workimage.do_bw)
but_left.clicked.connect(workimage.do_left)
but_right.clicked.connect(workimage.do_right)
but_mirror.clicked.connect(workimage.do_mirror)
but_sharpness.clicked.connect(workimage.change_sharpness)



window.resize(800, 500)
window.show()
app.exec_()
