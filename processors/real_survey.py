#!/usr/bin/env python
import json

events = json.loads(text_data['events'])

# Requested marks
answered = 0

for event in events:
    if event['name'] == 'answer':
        answered += 1
