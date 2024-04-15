## Завдання 1
За допомогою bash команди чи bash скрипту вирішити наступну задачу (додаткова реалізація за допомогою python чи за допомогою іншої мови програмування буде плюсом): необхідно вивести всі назви файлів з двох директорій так щоб вони були унікальними (Врахувати негативні кейси). У разі необхідності попередніх налаштувань, надати step by step інструкцію.

**Приклад:**

Наявна директорія my_dir_1. З наступним контентом:
- my_dir_1
  - file1.txt
  - file2.txt
  - file3.txt

Наявна директорія my_dir_2. З наступним контентом:
- my_dir_2
  - file2.txt
  - file4.txt

Бажаний результат:
- file1.txt
- file2.txt
- file3.txt
- file4.txt

## Рішення
1. Найпростіше рішення, використовуючи команди bash і pipes, - отримуємо вміст каталогів `ls -al`, потім фільруємо тільки файли `grep '^-'`, отримуємо тільки імена файлів `grep -oE '[[:alnum:]_.-.-]+?[\.[:alnum:]_-]+?$'` і нарешті отримуємо відсортований список унікальних імен `sort -u`
```bash
ls -al my_dir_1 my_dir_2 | grep '^-' | grep -oE '[[:alnum:]_.-]+?[\.[:alnum:]_-]+?$' | sort -u
```
2. Невеликий пошук у мережі підказав більш елегантне рішення - використовуючи команду `find`. Отримуємо список тільки імен файлів у всіх каталогах `find my_dir_1 my_dir_2 -type f -exec basename {} \;` і сортуємо список, залишаючи тільки унікальні значення `sort -u`
```bash
find my_dir_1 my_dir_2 -type f -exec basename  {} \; | sort -u
```
### Негативні кейси
До негативних випадків я відніс неіснуюче ім'я каталогу і відмову доступу до каталогу. Обидві ситуації відпрацьовуються на рівні bash і додаткових дій не потрібно. 

### Python script
Скрипт отримує список каталогів і створює унікальний список усіх файлів у всіх каталогах. Скрипт опрацьовує негативні кейси так само як і bash команди - видає повідомлення для каталогів, у яких не вдалося отримати список файлів. 
Я також вирішив додати ключ, який включає в список також і символьні посилання.
```python
#!/usr/bin/python3

import os
import argparse

def get_uniq_fn(dirs, symlinks):
    """
    Returns a list of unique filenames which entries in all the input directory list.
    Args:
        dirs (list): list od directory names (paths)
        symlinks (bool): if True includes symbol links into result as well
    Return:
        list: list of filenames
    """
    uniq_fn = set()
    for dir in dirs:
        if not os.path.exists(dir):
            print(f"Error: Path {dir} does not exist.")
            continue
        if not os.access(dir, os.R_OK):
            print(f"Error: Permission denied to access {dir}.")
            continue
        with os.scandir(dir) as entries:
            for entry in entries:
                if entry.is_file() or (symlinks and entry.is_symlink):
                    uniq_fn.add(entry.name)
    return list(uniq_fn)

if __name__ == "__main__":

    # Parsing command line arguments:
    # > script.py [-l] dir1, dir2, ..., dirN
    # -l: if present it includes symbol links as well
    # dir1, dir2, ..., dirN: list of directori names
    parser = argparse.ArgumentParser(description="Get unique filenames from directories.", 
                                     usage="[-l] dir1 dir2 ... dirN")
    parser.add_argument("directories", nargs="+", 
                        help="List of directories to search for files")
    parser.add_argument("-l", "--include-symlinks", action="store_true", 
                        help="Include symbolic links in the result")
    args = parser.parse_args()

    uniq_fn = get_uniq_fn(args.directories, args.include_symlinks)
    for file in sorted(uniq_fn):
        print(file)
```
### Тестування
1. Клонуйте репозитарій
   ```bash
   git clone https://gitlab.com/test-works3/ed_test.git
   ```
2. Перейдіть до каталогу 
  ```bash
  cd ed_test/task1
  ```
3. Дозвольте виконання файлів: 
  ```bash
   chmod +x test_set.sh test.sh uniq_files.py
  ```
1. Підготуйте тестовий набір
  ```bash
  ./test_set.sh
  ```
1. тест рішень bash, Python
  ```bash
  ./test.sh
  ```
