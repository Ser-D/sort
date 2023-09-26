import os
import re
import shutil
import sys

dict_dir = {}
dict_file = {}
new_dict_file = {}
trans_map = {}
images_obj = []
video_obj = []
doc_obj = []
audio_obj = []
arh_obj = []
ident_ext = set()
unident_ext = set()

images_file = ['jpeg', 'png', 'jpg', 'svg', 'JPEG', 'PNG', 'JPG', 'SVG']
video_file = ['avi', 'mp4', 'mov', 'mkv', 'AVI', 'MP4', 'MOV', 'MKV']
doc_file = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
audio_file = ['mp3', 'ogg', 'wav', 'amr', 'MP3', 'OGG', 'WAV', 'AMR']
arh_file = ['zip', 'gz', 'tar', 'ZIP', 'GZ', 'TAR']
cyril_sym = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
transl_sym = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


def search_dir(path):
    for i in os.listdir(path):
        if os.path.isdir(path + '\\' + i):
            dict_dir[i] = path
            search_dir(path + '\\' + i)
        else:
            dict_file[i] = path
    return dict_dir, dict_file

def create_trans_dict():
    for c, l in zip(cyril_sym, transl_sym):
        trans_map[ord(c)] = l
        trans_map[ord(c.upper())] = l.upper()
    return trans_map

    
def normalize():
    new_key = ''
    file_in_list = []
    for key, value in dict_file.items():
        file_in_list = key.split('.')
        file_in_list[0] = file_in_list[0].translate(trans_map)
        file_in_list[0] = re.sub('\W', '_', file_in_list[0])
        new_key = '.'.join(file_in_list[i] for i in range(len(file_in_list)))
        new_dict_file[new_key] = value
        os.rename(f'{value}\\{key}', f'{value}\\{new_key}')
    return new_dict_file

def move_file():
    for key, value in new_dict_file.items():
        file_in_list = key.split('.')
        ident_ext.add(file_in_list[-1])
        if file_in_list[-1] in images_file:
            if not os.path.exists(f'{path}\\images'):
                os.mkdir(f'{path}\\images')
            shutil.move(f'{value}\\{key}', f'{path}\\images\\{key}')
            images_obj.append(key)
        elif file_in_list[-1] in video_file:
            if not os.path.exists(f'{path}\\video'):
                os.mkdir(f'{path}\\video')
            shutil.move(f'{value}\\{key}', f'{path}\\video\\{key}')
            video_obj.append(key)
        elif file_in_list[-1] in doc_file:
            if not os.path.exists(f'{path}\\documents'):
                os.mkdir(f'{path}\\documents')
            shutil.move(f'{value}\\{key}', f'{path}\\documents\\{key}')
            doc_obj.append(key)
        elif file_in_list[-1] in audio_file:
            if not os.path.exists(f'{path}\\audio'):
                os.mkdir(f'{path}\\audio')
            shutil.move(f'{value}\\{key}', f'{path}\\audio\\{key}')
            audio_obj.append(key)
        elif file_in_list[-1] in arh_file:
            if not os.path.exists(f'{path}\\archives'):
                os.mkdir(f'{path}\\archives')
            if not os.path.exists(f'{path}\\archives\\{file_in_list[0]}'):
                os.mkdir(f'{path}\\archives\\{file_in_list[0]}')
            shutil.unpack_archive(f'{value}\\{key}', f'{path}\\archives\\{file_in_list[0]}')
            arh_obj.append(key)
            os.remove(f'{value}\\{key}')
        else:
            unident_ext.add(file_in_list[-1])
    return images_obj, video_obj, doc_obj, audio_obj, arh_obj, ident_ext, unident_ext


def clean_dir():
    for key, value in dict_dir.items():
        print(dict_dir)
        try:    
            os.rmdir(f'{value}\\{key}')
        except OSError:
            print

def rezult_hw():
    if len(dict_file):
        print(F'Було знайдено {len(dict_file)} файл(ів), в тому числі:')
        if len(images_obj):
            print(f'Зображення {images_obj}')
        if len(video_obj):
            print(f'Відео файли {video_obj}')
        if len(doc_obj):
            print(f'Документи {doc_obj}')
        if len(audio_obj):
            print(f'Аудіо {audio_obj}')
        if len(arh_obj):
            print(f'Архівів {arh_obj}')
        print(f'Ідентифікованих розширеннь файлів {len(ident_ext) - len(unident_ext)} {ident_ext ^ unident_ext if ident_ext ^ unident_ext else ""}')
        print(f'Неідентифікованих розширеннь файлів {len(unident_ext)} {unident_ext if unident_ext else ""}')


if len(sys.argv) < 2:
    print('Введіть шлях до папки, що потребує сортування!')
else:
    path = sys.argv[1]
    try:
        os.listdir(path)
    except OSError:
        print('Перевірте правильність введеного шляху до папки, що потребує сортування!')
    else:
        if os.listdir(path):
            search_dir(path)
            create_trans_dict()
            normalize()
            move_file()
            clean_dir()
            rezult_hw()
        else:
            print("Об'єктів для сортування не знайдено")


