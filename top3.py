def get_top_3_names(mentors):
    all_names = []
    for group in mentors:
        for mentor in group:
            name = mentor.split()[0]
            all_names.append(name)

    name_counts = {}
    for name in set(all_names):
        name_counts[name] = all_names.count(name)

    # Сортировка: сначала по частоте (убывание), потом по имени (возрастание)
    sorted_names = sorted(name_counts.items(), key=lambda x: (-x[1], x[0]))

    top_3 = sorted_names[:3]
    parts = [f"{name}: {count} раз(а)" for name, count in top_3]
    return ", ".join(parts)