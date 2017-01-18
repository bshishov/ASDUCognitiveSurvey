#!/usr/bin/env python
import json

# files
# text_data
events = json.loads(text_data['events'])

# Requested marks
time = 0
correct = 0
wrong = 0
score = 100.0
average_correct_time = 0

total_correct_time = 0

for event in events:
    if event['name'] == 'correct':
        total_correct_time += reaction
        correct += 1

    if event['name'] == 'wrong':
        wrong += 1

    if event['name'] == 'test_complete':
        time = event['time']

if correct > 0:
    average_correct_time = total_correct_time / correct

# Time penalty: decrease score by 1 for each second over 65s
if time > 65000:
    score -= 1 * (time - 65000) / 1000.0

# Wrong answers penalty: -10 points for each wrong answer
score -= wrong * 10
