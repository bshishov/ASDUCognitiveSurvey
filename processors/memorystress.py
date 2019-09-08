import json
from utils.main import default_main


def memory_stress(text_data, **kwargs) -> dict:
    events = json.loads(text_data['events'])

    # Requested marks
    time = 0
    correct = 0
    wrong = 0
    total_response_time = 0

    for event in events:
        if event['name'] == 'correct':
            total_response_time += event['args']['decisionTime']
            correct += 1

        if event['name'] == 'wrong':
            total_response_time += event['args']['decisionTime']
            wrong += 1

        if event['name'] == 'test_complete':
            time = event['time']

    if correct > 0:
        average_response_time = total_response_time / (correct + wrong)
    else:
        average_response_time = total_response_time

    score = correct * 3 + (correct - wrong) * 2 + (6 - int(average_response_time / 1000.0)) * 2
    if score > 100:
        score = 100
    if wrong > 15:
        score = 0

    return {
        'time': time,
        'score': score,
        'correct': correct,
        'wrong': wrong,
        'average_response_time': average_response_time,
        'total_response_time': total_response_time
    }


if __name__ == '__main__':
    default_main(memory_stress)
