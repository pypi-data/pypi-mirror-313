from datetime import datetime


def dt_to_str(dt_obj: datetime):
    """
    Takes a datetime object and converts it to a STRING having a set datetime format (%Y-%m-%d %H:%M:%S)

    Parameters
    ----------
    dt_obj : A datetime object

    Returns
    -------
    str : A string representation of dt_obj
    """
    modified_date = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    modified_date = datetime.strptime(modified_date, "%Y-%m-%d %H:%M:%S")

    return modified_date


def update_end_date(start_date: datetime, dry_run_duration: datetime):
    """
    Takes start_date and dry_run_duration as an input to this function and updates the  end date  based on deafult_dry_run_duration_value

    Parameters
    ----------
    start_date : A datetime object
    dry_run_duration: A datetime object

    Returns
    -------
    datetime Object: Returns updated end date.

    """
    end_date = start_date + dry_run_duration
    return end_date


def is_duration_valid_for_dry_run(start_date: datetime, end_date: datetime, max_dry_run_duration_days: int):
    """
    Takes start_date and end_date as an input to this function and validates it based on different conditions.

    Parameters
    ----------
    start_date : A datetime object
    end_date   : A datetime object

    Returns
    -------
    bool : returns boolean value based on condition checks.
    """
    if start_date is None:
        raise ValueError("start_date cannot be None")
    elif end_date is None:
        return True
    else:
        if end_date < start_date:
            raise ValueError("end_date should be greater than start_date")
    start_date = dt_to_str(start_date)
    end_date = dt_to_str(end_date)
    date_delta = end_date - start_date
    num_of_days = date_delta.days
    return num_of_days <= max_dry_run_duration_days
