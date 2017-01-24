#!/usr/bin/env python
import json

events = json.loads(text_data['events'])

EXTRAVERT_YES = [1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53, 56]
EXTRAVERT_NO = [5, 15, 20, 29, 32, 34, 37, 41, 51]

NEUROTISM_YES = [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57]

LIE_YES = [6, 24, 36]
LIE_NO = [12, 18, 30, 42, 48, 54]

# Requested marks
extravert_score = 0
neurotism_score = 0
lie_score = 0


for event in events:
    if event['name'] == 'answer':
        question_id = event['args']['question']['id']
        answer = event['args']['answer']

        if answer == 'yes':
            if question_id in EXTRAVERT_YES:
                extravert_score += 1
            if question_id in NEUROTISM_YES:
                neurotism_score += 1
            if question_id in LIE_YES:
                lie_score += 1

        if answer == 'no':
            if question_id in EXTRAVERT_NO:
                extravert_score += 1
            if question_id in LIE_NO:
                lie_score += 1

if extravert_score > 15:
    extravert_score_comment = 'Яркий экстраверт'
elif extravert_score > 12:
    extravert_score_comment = 'Склонность к экстраверсии'
elif extravert_score == 12:
    extravert_score_comment = 'Среднее значение экстраверсии'
elif extravert_score > 9:
    extravert_score_comment = 'Склонность к экстраверсии'
elif extravert_score > 5:
    extravert_score_comment = 'Интроверт'
else:
    extravert_score_comment = 'Глубокий интроверт'

if neurotism_score > 19:
    neurotism_score_comment = 'Очень высокий уровень нейротизма'
if neurotism_score > 13:
    neurotism_score_comment = 'Высокий уровень нейротизма'
if neurotism_score > 9:
    neurotism_score_comment = 'Среднее значение нейротизма'
else:
    neurotism_score_comment = 'Низкий уровень нейротизма'

if lie_score > 4:
    lie_score_comment = 'Неискренность в ответах'
else
    lie_score_comment = 'Норма'
