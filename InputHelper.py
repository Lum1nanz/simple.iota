def convert_input_to_int(menu_choice):
    try:
        return int(menu_choice)
    except (ValueError):
        print("Invalid Input")
        return 0