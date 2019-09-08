import json
from utils.main import default_main


def real_survey(text_data, **kwargs) -> dict:
    events = json.loads(text_data['events'])

    # Requested marks
    answered = 0

    for event in events:
        if event['name'] == 'answer':
            answered += 1

    return {'answered': answered}


if __name__ == '__main__':
    default_main(real_survey)
