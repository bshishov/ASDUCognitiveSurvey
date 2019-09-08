import json
from utils.main import default_main


def plasticity(text_data, **kwargs) -> dict:
    # files
    # text_data
    events = json.loads(text_data['events'])

    # Requested marks
    time = 0
    correct = 0
    wrong = 0
    score = 100.0
    total_response_time = 0

    for event in events:
        if event['name'] == 'correct':
            total_response_time += event['args']['reaction']
            correct += 1

        if event['name'] == 'wrong':
            total_response_time += event['args']['reaction']
            wrong += 1

        if event['name'] == 'test_complete':
            time = event['time']

    if correct > 0:
        average_response_time = total_response_time / (correct + wrong)
    else:
        average_response_time = total_response_time

    # Time penalty: decrease score by 2 for each second over 40s
    if time > 40000:
        score -= 2 * (time - 40000) / 1000.0

    # Wrong answers penalty: -10 points for each wrong answer
    score -= wrong * 10
    return {
        'score': wrong,
        'correct': correct,
        'wrong': wrong,
        'average_response_time': average_response_time,
        'total_response_time': total_response_time,
        'time': time
    }


if __name__ == '__main__':
    default_main(plasticity)
