import zipfile
import os

file = open('ban.txt', 'w')
for i in range(1000):
    file.write('123' * 100)
file.close()

jungle_zip = zipfile.ZipFile(f'{0}.zip', 'w')
jungle_zip.write('ban.txt', compress_type=zipfile.ZIP_DEFLATED)
jungle_zip.close()

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ban.txt')
os.remove(path)

for i in range(1, 11):
    jungle_zip = zipfile.ZipFile(f'{i}.zip', 'w')
    jungle_zip.write(f'{i - 1}.zip', compress_type=zipfile.ZIP_DEFLATED)
    file = open('ban.txt', 'w')

    for j in range(1000):
        file.write('123' * 100)
    file.close()


    jungle_zip.write('ban.txt', compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ban.txt')
    os.remove(path)

    jungle_zip.close()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{i - 1}.zip')
    os.remove(path)
