import zipfile
import os
import random
import time



def rfile(dfile):
    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), dfile)
    os.remove(os.getcwd() + f'\\{dfile}')


def makelarch(iterations, arhname, fsize=100000):
    global itera
    arch = zipfile.ZipFile(arhname, 'w')
    for i in range(10):
        file = open(f'{i}.txt', 'w')
        for j in range(fsize):
            file.write('1')
        file.close()
        global size
        size += os.path.getsize(f'{i}.txt')
        arch.write(f'{i}.txt', compress_type=zipfile.ZIP_DEFLATED)
        rfile(f'{i}.txt')
    os.system('clear')
    print(f'{itera + 1}/{iterations ** 2}')
    itera += 1
    arch.close()


# makelarch(100, 'ban.zip')
def makemarch(iterations, arhname, fsize=100):
    archm = zipfile.ZipFile(arhname, 'w')
    for i in range(iterations):
        makelarch(iterations, f'{i}.zip', fsize)
        archm.write(f'{i}.zip', compress_type=zipfile.ZIP_DEFLATED)
        try:
            rfile(f'{i - 1}.zip')
        except Exception:
            pass
    archm.close()


def makebarch(iterations, arhname, fsize=100):
    archm = zipfile.ZipFile(arhname, 'w')
    try:
        os.mkdir('temp')
    except FileExistsError:
        pass
    cdir = os.getcwd() + '\\temp'
    os.chdir(cdir)
    for i in range(iterations):
        makemarch(iterations, f'{i}.zip', fsize)
        archm.write(f'{i}.zip', compress_type=zipfile.ZIP_DEFLATED)
        try:
            rfile(f'{i - 1}.zip')
        except Exception:
            pass
    archm.close()
    os.chdir(cdir[:-5])


bigr = int(input('Введите количество вложенных архивов (влияет на время выполнения)\n'))
start_time = time.time()
itera = 0
size = 0
makebarch(bigr, 'driga.zip', 1000000)
for i in os.listdir(os.getcwd() + '\\temp'):
    rfile(f'temp\\{i}')
os.rmdir('temp')
print("Время выполнения %s секунд" % (time.time() - start_time))
print(f'Вес распакованных файлов составляет {size} бит')
print(f'Вес архива: {os.path.getsize("driga.zip")} бита')
print(input('Нажмите Enter чтобы закрыть окно'))
