# First-Python-Script
Скрипт написанный на языке Python для сервера телефонии Asterisk. 

Основная цель данного скрипта, по одному из проекта состояла в отслеживании папки директории с аудиозаписями старого года и удалении всей папки, со всеми внутрилежащими файлами.

Скрипт запускается в crontab ежечасно, и при не прохождении условий - ничего не делает.
В ином случае - начинает сверку года и удаление директорий.
