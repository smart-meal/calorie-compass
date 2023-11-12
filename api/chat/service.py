from api.util.auth import get_user_id_from_session


def send_message(message: str):
    user_id = get_user_id_from_session()
    # TODO send the message, get the response, store both and send the response back to the user
