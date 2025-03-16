from event.schemas import PotholeExistsMessage, PotholeFixedMessage, PotholeNotFixedMessage, PotholeNotRealMessage, RegisterPotholeMessage, UserLocationChangeEvent


def process_register_pothole(message):
    try:
        register_pothole_cmd = RegisterPotholeMessage().load(message)
        # save in db
    except Exception as e:
        print(e)

def process_pothole_exists(message):
    try:
        confirm_pothole_exists_cmd = PotholeExistsMessage().load(message)
        # update db
    except Exception as e:
        print(e)

def process_pothole_fixed(message):
    try:
        confirm_pothole_fixed_cmd = PotholeFixedMessage().load(message)
        # update db
    except Exception as e:
        print(e)

def process_pothole_not_real(message):
    try:
        confirm_pothole_not_real_cmd = PotholeNotRealMessage().load(message)
        # update db
    except Exception as e:
        print(e)

def process_pothole_not_fixed(message):
    try:
        confirm_pothole_not_fixed = PotholeNotFixedMessage().load(message)
        # update db
    except Exception as e:
        print(e)

def process_location_changed(message):
    try:
        user_location_changed = UserLocationChangeEvent().load(message)
        # determine whether to warn users
    except Exception as e:
        print(e)
