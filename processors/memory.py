import json
from utils.main import default_main


def memory(text_data, **kwargs) -> dict:
    # files
    # text_data
    events = json.loads(text_data['events'])

    # Requested marks
    remembered = 0
    score = 0
    time = 0
    total_response_time = 0

    for event in events:
        if event['name'] == 'success':
            remembered += 1
            reaction = event['args']['reaction']
            total_response_time += reaction
            if reaction < 4000:
                score += 5
            elif reaction < 8000:
                score += 4
            else:
                score += 3
        if event['name'] == 'test_complete':
            time = event['time']

    if remembered > 0:
        average_response_time = total_response_time / remembered
    else:
        average_response_time = total_response_time

    return {
        'time': time,
        'average_response_time': average_response_time,
        'total_response_time': total_response_time,
        'remembered': remembered,
        'score': score
    }


if __name__ == '__main__':
    default_main(memory)
