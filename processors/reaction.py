import json
from utils.main import default_main

MIN_REACTION = 250.0  # ms
MAX_REACTION = 500.0  # ms


def reaction(text_data, **kwargs) -> dict:
    # files
    # text_data
    events = json.loads(text_data['events'])

    reactions = [e['args']['reaction'] for e in events if e['name'] == 'success']

    # Requested marks
    fails = len([e for e in events if e['name'] == 'fail'])
    reaction_avg = sum(reactions) / float(len(reactions))
    reaction_min = min(reactions)
    reaction_max = max(reactions)

    if reaction_avg <= MIN_REACTION:
        score = 100
    elif MIN_REACTION < reaction_avg < MAX_REACTION:
        score = 100 - 100 * (reaction_avg - MIN_REACTION) / (MAX_REACTION - MIN_REACTION)
    else:
        score = 0
    return {
        'score': score,
        'reaction_avg': reaction_avg,
        'reaction_min': reaction_min,
        'reaction_max': reaction_max,
    }


if __name__ == '__main__':
    default_main(reaction)
