# phonebook.py
import csv
import os
from connect import get_connection

# 1. ПОИСК ПО ПАТТЕРНУ (Функция)
def search_by_pattern(pattern):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            # Вызываем функцию поиска
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            results = cur.fetchall()
            
            print(f"\n--- Результаты поиска для '{pattern}' ---")
            if not results:
                print("Совпадений не найдено.")
            for row in results:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
    finally:
        conn.close()

# 2. ДОБАВЛЕНИЕ / ОБНОВЛЕНИЕ КОНТАКТА (Процедура)
def upsert_contact(name, phone):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            # Вызываем процедуру UPSERT
            cur.execute("CALL insert_or_update_contact(%s, %s)", (name, phone))
            conn.commit()
            print(f"Контакт {name} ({phone}) успешно добавлен/обновлен.")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
    finally:
        conn.close()

# 3. МАССОВОЕ ДОБАВЛЕНИЕ С ПРОВЕРКОЙ (Процедура с циклом и IF)
def insert_from_csv(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return
    
    names = []
    phones = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if len(row) == 2:
                    names.append(row[0])
                    phones.append(row[1])
                    
        if names and phones:
            conn = get_connection()
            if not conn: return
            try:
                with conn.cursor() as cur:
                    # Передаем списки как массивы PostgreSQL. Для OUT параметра используем NULL.
                    cur.execute("CALL bulk_insert_with_validation(%s, %s, NULL)", (names, phones))
                    result = cur.fetchone() # Получаем текст с ошибками (OUT параметр)
                    conn.commit()
                    
                    if result and result[0]:
                        print(f"Загрузка завершена, но найдены некорректные данные:\n{result[0]}")
                    else:
                        print("Все контакты из CSV успешно добавлены! Ошибок нет.")
            except Exception as e:
                print(f"Ошибка при массовой загрузке: {e}")
            finally:
                conn.close()
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")

# 4. ПАГИНАЦИЯ (Функция)
def get_paged_contacts(limit, offset):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            # Вызываем функцию пагинации
            cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (limit, offset))
            results = cur.fetchall()
            
            page_num = (offset // limit) + 1
            print(f"\n--- Контакты (Страница {page_num}) ---")
            for row in results:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    except Exception as e:
        print(f"Ошибка при пагинации: {e}")
    finally:
        conn.close()

# 5. УДАЛЕНИЕ (Процедура)
def delete_contact(target):
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            # Вызываем процедуру удаления
            cur.execute("CALL delete_contact_proc(%s)", (target,))
            conn.commit()
            print(f"Попытка удаления контактов с именем или телефоном: {target}")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    finally:
        conn.close()

# ==========================================
# ОСНОВНОЕ МЕНЮ
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n--- Телефонная Книга (Практика 8) ---")
        print("1. Найти контакт (по части имени или телефона)")
        print("2. Добавить/Обновить контакт (Upsert)")
        print("3. Массовая загрузка из CSV (С проверкой данных)")
        print("4. Показать контакты по страницам (Pagination)")
        print("5. Удалить контакт (по точному имени или телефону)")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ")

        if choice == "1":
            pattern = input("Введите часть имени или телефона для поиска: ")
            search_by_pattern(pattern)
        
        elif choice == "2":
            name = input("Имя: ")
            phone = input("Телефон: ")
            upsert_contact(name, phone)
            
        elif choice == "3":
            # Используем твой contacts.csv
            csv_path = input("Путь к CSV (например, contacts.csv): ")
            insert_from_csv(csv_path)
        
        elif choice == "4":
            try:
                limit = int(input("Сколько контактов на одной странице?: "))
                page = int(input("Какую страницу открыть?: "))
                offset = (page - 1) * limit
                get_paged_contacts(limit, offset)
            except ValueError:
                print("Ошибка: Введите число.")
        
        elif choice == "5":
            target = input("Введите точное имя или телефон для удаления: ")
            delete_contact(target)
        
        elif choice == "6":
            print("Выход...")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")