def chair_height_formula(user_height_input):
    return round(0.25 * user_height_input + 2.5, 1)


def desk_height_formula(user_height_input):
    return round(0.68 * user_height_input - 4.8, 1)

def dict_from_row(row):
    return dict(zip(row.keys(), row))
