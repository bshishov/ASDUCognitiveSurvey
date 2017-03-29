#!/usr/bin/env python
import json

# files
# text_data
events = json.loads(text_data['events'])

reactions = [e['args']['reaction'] for e in events if e['name'] == 'success']

# Requested marks
fails = len([e for e in events if e['name'] == 'fail'])
reaction_avg = sum(reactions) / float(len(reactions))
reaction_min = min(reactions)
reaction_max = max(reactions)


score = 0

MIN_REACTION = 250.0  # ms
MAX_REACTION = 500.0  # ms

if reaction_avg <= MIN_REACTION:
    score = 100
elif reaction_avg > MIN_REACTION and reaction_avg < MAX_REACTION:
    score = 100 - 100 * (reaction_avg - MIN_REACTION) / (MAX_REACTION - MIN_REACTION)
else:
    score = 0
