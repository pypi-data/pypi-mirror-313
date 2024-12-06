from .output import output_message


def validate_response(response):
    try:
        response.raise_for_status()
    except Exception as e:
        # keep a more user friendly error
        if response.text:
            output_message(response.text)
            raise Exception(response.text)
        else:
            raise e
