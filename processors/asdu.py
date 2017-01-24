#!/usr/bin/env python
import random
import time

try:
    from fuzzle import lvars, mfs, operators, rules, controller, defuzz
except ImportError:
    import pip
    pip.main(['install', 'fuzzle'])
    from fuzzle import lvars, mfs, operators, rules, controller, defuzz

from fuzzle.utils import frange


def memory(memory_score, memorystress_score):
    #Дефаззифицированные результаты теста "Зрительная память" B-bad N-normal G-good
    mem = lvars.InputLVar('mem', (0, 100))
    mem['B'] = mfs.TriMF(0, 0, 40)
    mem['N'] = mfs.TriMF(10, 50, 90)
    mem['G'] = mfs.TriMF(60, 100, 100)
    #Дефаззифицированные результаты теста "Память стресс"
    ms = lvars.InputLVar('ms', (0, 100))
    ms['B'] = mfs.TriMF(0, 0, 40)
    ms['N'] = mfs.TriMF(10, 50, 90)
    ms['G'] = mfs.TriMF(60, 100, 100)
    #Дефаззифицированные обобщенные результаты тестов типа "Память"
    m = lvars.OutputLVar('m', domain=(0, 100), defuzz=defuzz.CoG())
    m['B'] = mfs.TriMF(0, 0, 40)
    m['N'] = mfs.TriMF(10, 50, 90)
    m['G'] = mfs.TriMF(60, 100, 100)


    rb = rules.RuleBlock(
        and_op=operators.Minimum(),
        or_op=operators.Maximum(),
        not_op=operators.Zadeh(),
        agg_op=operators.Minimum(),
        acc_op=operators.Maximum()
    )
    rb[1] = 'if mem is B and ms is B then m is B'
    rb[2] = 'if mem is B and ms is N then m is B'
    rb[3] = 'if mem is B and ms is G then m is N'
    rb[4] = 'if mem is N and ms is B then m is B'
    rb[5] = 'if mem is N and ms is N then m is N'
    rb[6] = 'if mem is N and ms is G then m is G'
    rb[7] = 'if mem is G and ms is B then m is N'
    rb[8] = 'if mem is G and ms is N then m is G'
    rb[9] = 'if mem is G and ms is G then m is G'
    fc = controller.FuzzyController([mem, ms], [m], rb)

    input_values = {
        'mem': memory_score,
        'ms': memorystress_score,
    }

    res = fc.eval(input_values)
    return res['m']


def temperament(introvert_score, neurotism_score):
    #Дефаззифицированные результаты теста "Интроверсия"
    # I - интроверсия SI - склонность к интроверсии S - средний результат
    #SE - склонность к экстраверсии E - экстраверсия
    intr = lvars.InputLVar('intr', (0, 100))
    intr['I'] = mfs.TriMF(0, 0, 27)
    intr['SI'] = mfs.TriMF(15, 27, 36)
    intr['S'] = mfs.TriMF(27, 36, 45)
    intr['SE'] = mfs.TriMF(36, 45, 57)
    intr['E'] = mfs.TriMF(42, 100, 100)
    #Дефаззифицированные результаты теста "Нейротизм"
    # L-low N-normal H-high VH-very high
    nei = lvars.InputLVar('nei', (0, 100))
    nei['L'] = mfs.TriMF(0, 0, 33)
    nei['N'] = mfs.TriMF(27, 33, 39)
    nei['H'] = mfs.TriMF(33, 45, 57)
    nei['VH'] = mfs.TriMF(42, 100, 100)
    #Дефаззифицированные обобщенные результаты тестов типа "Темперамент"
    temp = lvars.OutputLVar('temp', domain=(0, 100), defuzz=defuzz.CoG())
    temp['B'] = mfs.TriMF(0, 0, 40)
    temp['N'] = mfs.TriMF(10, 50, 90)
    temp['G'] = mfs.TriMF(60, 100, 100)


    rb = rules.RuleBlock(
        and_op=operators.Minimum(),
        or_op=operators.Maximum(),
        not_op=operators.Zadeh(),
        agg_op=operators.Minimum(),
        acc_op=operators.Maximum()
    )
    rb[1] = 'if intr is I and nei is L then temp is N'
    rb[2] = 'if intr is I and nei is N then temp is N'
    rb[3] = 'if intr is I and nei is H then temp is N'
    rb[4] = 'if intr is I and nei is VH then temp is N'
    rb[5] = 'if intr is SI and nei is L then temp is G'
    rb[6] = 'if intr is SI and nei is N then temp is N'
    rb[7] = 'if intr is SI and nei is H then temp is B'
    rb[8] = 'if intr is SI and nei is VH then temp is B'
    rb[9] = 'if intr is S and nei is L then temp is G'
    rb[10] = 'if intr is S and nei is N then temp is G'
    rb[11] = 'if intr is S and nei is H then temp is N'
    rb[12] = 'if intr is S and nei is VH then temp is B'
    rb[13] = 'if intr is SE and nei is L then temp is G'
    rb[14] = 'if intr is SE and nei is N then temp is N'
    rb[15] = 'if intr is SE and nei is H then temp is N'
    rb[16] = 'if intr is SE and nei is VH then temp is B'
    rb[17] = 'if intr is E and nei is L then temp is N'
    rb[18] = 'if intr is E and nei is N then temp is N'
    rb[19] = 'if intr is E and nei is H then temp is B'
    rb[20] = 'if intr is E and nei is VH then temp is B'
    fc = controller.FuzzyController([intr, nei], [temp], rb)

    input_values = {
        'intr': introvert_score,
        'nei': neurotism_score,
    }
    res = fc.eval(input_values)
    return res['temp']


def asdu(memory_score, operation_score, plasticity_score, reaction_score, temperament_score):
    # Память(общая) дефаззифицированные результаты(от 0 до 1) B-плохо N-нормально G-хорошо
    m = lvars.InputLVar('m', (0, 100))
    m['B'] = mfs.TriMF(0, 0, 40)
    m['N'] = mfs.TriMF(10, 50, 90)
    m['G'] = mfs.TriMF(60, 100, 100)

    # Оперативность мышления дефаззифицированные результаты(от 0 до 1) B-плохо N-нормально G-хорошо
    o = lvars.InputLVar('o', (0, 100))
    o['B'] = mfs.TriMF(0, 0, 40)
    o['N'] = mfs.TriMF(10, 50, 90)
    o['G'] = mfs.TriMF(60, 100, 100)

    # Пластичность дефаззифицированные результаты(от 0 до 1) B-плохо N-нормально G-хорошо
    p = lvars.InputLVar('p', (0, 100))
    p['B'] = mfs.TriMF(0, 0, 40)
    p['N'] = mfs.TriMF(10, 50, 90)
    p['G'] = mfs.TriMF(60, 100, 100)
    # Реакция дефаззифицированные результаты(от 0 до 1) B-плохо N-нормально G-хорошо
    r = lvars.InputLVar('r', (0, 100))
    r['B'] = mfs.TriMF(0, 0, 40)
    r['N'] = mfs.TriMF(10, 50, 90)
    r['G'] = mfs.TriMF(60, 100, 100)
    # Темперамент дефаззифицированные результаты(от 0 до 1) B-плохо N-нормально G-хорошо
    t = lvars.InputLVar('t', (0, 100))
    t['B'] = mfs.TriMF(0, 0, 40)
    t['N'] = mfs.TriMF(10, 50, 90)
    t['G'] = mfs.TriMF(60, 100, 100)


    # Рекомендации к работе диспетчером (от 0 до 1) N- не рекомендован R-рекомендован
    rd = lvars.OutputLVar('rd', domain=(0, 100), defuzz=defuzz.CoG())
    rd['N'] = mfs.TriMF(0, 0, 70)
    rd['R'] = mfs.TriMF(30, 100, 100)


    rb = rules.RuleBlock(
        and_op=operators.Minimum(),
        or_op=operators.Maximum(),
        not_op=operators.Zadeh(),
        agg_op=operators.Minimum(),
        acc_op=operators.Maximum()
    )
    rb[1] = 'if m is N and o is N and r is N and p is N and t is N then rd is R'
    rb[2] = 'if m is N and o is N and r is N and p is N and t is G then rd is R'
    rb[3] = 'if m is N and o is N and r is N and p is G and t is N then rd is R'
    rb[4] = 'if m is N and o is N and r is N and p is G and t is G then rd is R'
    rb[5] = 'if m is N and o is N and r is G and p is N and t is N then rd is R'
    rb[6] = 'if m is N and o is N and r is G and p is N and t is G then rd is R'
    rb[7] = 'if m is N and o is N and r is G and p is G and t is N then rd is R'
    rb[8] = 'if m is N and o is N and r is G and p is G and t is G then rd is R'
    rb[9] = 'if m is N and o is G and r is N and p is N and t is N then rd is R'
    rb[10] = 'if m is N and o is G and r is N and p is N and t is G then rd is R'
    rb[11] = 'if m is N and o is G and r is N and p is G and t is N then rd is R'
    rb[12] = 'if m is N and o is G and r is N and p is G and t is G then rd is R'
    rb[13] = 'if m is N and o is G and r is G and p is N and t is N then rd is R'
    rb[14] = 'if m is N and o is G and r is G and p is N and t is G then rd is R'
    rb[15] = 'if m is N and o is G and r is G and p is G and t is N then rd is R'
    rb[16] = 'if m is N and o is G and r is G and p is G and t is G then rd is R'
    rb[17] = 'if m is G and o is N and r is N and p is N and t is N then rd is R'
    rb[18] = 'if m is G and o is N and r is N and p is N and t is G then rd is R'
    rb[19] = 'if m is G and o is N and r is N and p is G and t is N then rd is R'
    rb[20] = 'if m is G and o is N and r is N and p is G and t is G then rd is R'
    rb[21] = 'if m is G and o is N and r is G and p is N and t is N then rd is R'
    rb[22] = 'if m is G and o is N and r is G and p is N and t is G then rd is R'
    rb[23] = 'if m is G and o is N and r is G and p is G and t is N then rd is R'
    rb[24] = 'if m is G and o is N and r is G and p is G and t is G then rd is R'
    rb[25] = 'if m is G and o is G and r is N and p is N and t is N then rd is R'
    rb[26] = 'if m is G and o is G and r is N and p is N and t is G then rd is R'
    rb[27] = 'if m is G and o is G and r is N and p is G and t is N then rd is R'
    rb[28] = 'if m is G and o is G and r is N and p is G and t is G then rd is R'
    rb[29] = 'if m is G and o is G and r is G and p is N and t is N then rd is R'
    rb[30] = 'if m is G and o is G and r is G and p is N and t is G then rd is R'
    rb[31] = 'if m is G and o is G and r is G and p is G and t is N then rd is R'
    rb[32] = 'if m is G and o is G and r is G and p is G and t is G then rd is R'

    rb[33] = 'if m is B or o is B or r is B or p is B or t is B then rd is N'

    fc = controller.FuzzyController([m, o, r, p, t], [rd], rb)


    input_values = {
        'm': memory_score,
        'o': operation_score,
        'p': plasticity_score,
        'r': reaction_score,
        't': temperament_score,
    }
    res = fc.eval(input_values)
    return res['rd']


#prigodnost = int(test_results['reading']['score']) * 10

memory_score = memory(test_results['memory']['score'],
                      test_results['memorystress']['score'])
operation_score = test_results['operation']['score']
plasticity_score = test_results['plasticity']['score']
reaction_score = test_results['reaction']['score']
temperament_score = temperament(test_results['temperament']['extravert_score'],
                                test_results['temperament']['neurotism_score'])

prigodnost = asdu(memory_score, operation_score, plasticity_score, reaction_score, temperament_score)

