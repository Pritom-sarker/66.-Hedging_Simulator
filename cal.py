from dateutil.parser import parse

def is_between_dates(start_date_str, end_date_str, check_date_str):
    try:
        start_date = parse(start_date_str)
        end_date = parse(end_date_str)
        check_date = parse(check_date_str)

        if start_date <= check_date <= end_date:
            return True
        else:
            return False
    except ValueError:
        print("Incorrect datetime format provided.")
        return False

# Example usage:
start_date_str = "2024-05-10 08:00:00+00:00"
end_date_str = "2024-05-10 18:00:00+00:00"
check_date_str = "2024-05-10 12:00:00+00:00"

result = is_between_dates(start_date_str, end_date_str, check_date_str)
print("Is the check date between start and end dates?", result)
