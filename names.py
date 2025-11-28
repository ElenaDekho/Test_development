def find_same_name_courses(courses_list):
    """
    Для каждого курса находит преподавателей-тёзок (имя встречается >1 раза на курсе).
    Возвращает список строк в формате:
    'На курсе <название> есть тёзки: <ФИ, ФИ, ...>'
    """
    result = []
    for course in courses_list:
        # Извлекаем имена менторов
        names = [mentor.split()[0] for mentor in course["mentors"]]
        # Находим имена, встречающиеся более 1 раза
        duplicate_names = {name for name in set(names) if names.count(name) > 1}
        if not duplicate_names:
            continue
        # Собираем менторов с дублирующимися именами
        same_name_mentors = [
            mentor for mentor in course["mentors"]
            if mentor.split()[0] in duplicate_names
        ]
        same_name_mentors.sort()
        message = f'На курсе {course["title"]} есть тёзки: {", ".join(same_name_mentors)}'
        result.append(message)
    return result