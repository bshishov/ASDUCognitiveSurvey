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

if reaction_avg <= 250:
    score = 100
elif reaction_avg > 250 and reaction_avg < 350:
    score = 100 - (reaction_avg - 250)
else:
    score = 0
