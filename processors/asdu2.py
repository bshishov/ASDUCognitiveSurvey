from utils.fuzzy import *
from utils.main import default_main

# Basic membership function names
BAD = 'bad'
NORMAL = 'normal'
GOOD = 'good'


def basic_trimf_set():
    return TriangularMf(BAD, -10, 0, 40),\
           TriangularMf(NORMAL, 15, 50, 90),\
           TriangularMf(GOOD, 60, 100, 100)


def mf_set(bounds=(0, 1), names=(BAD, NORMAL, GOOD)):
    min_val, max_val = bounds
    mf_size = float(max_val - min_val) / (len(names) - 1)
    mf_size_half = mf_size * 0.5
    mfs = []
    x = min_val
    for name in names:
        mfs.append(TriangularMf(name, x - mf_size, x, x + mf_size))
        #mfs.append(GaussianMf(name, x, mf_size_half))
        x += mf_size
    return mfs


class MemoryController:
    def __init__(self):
        m1 = Variable('visual_memory', (0, 100), *mf_set(bounds=(0, 100)))
        m2 = Variable('memory_stress', (0, 100), *mf_set(bounds=(0, 100)))
        m_out = Variable('memory', (0, 100), *mf_set(bounds=(0, 100)))

        rules = Rules(m_out)
        rules.add_rule(BAD,
                       (Is(m1, BAD) & Is(m2, BAD)) |
                       (Is(m1, BAD) & Is(m2, NORMAL)) |
                       (Is(m1, NORMAL) & Is(m2, BAD))
                       )

        rules.add_rule(NORMAL,
                       (Is(m1, NORMAL) & Is(m2, NORMAL)) |
                       (Is(m1, BAD) & Is(m2, GOOD)) |
                       (Is(m1, GOOD) & Is(m2, BAD))
                       )
        rules.add_rule(GOOD,
                       (Is(m1, GOOD) & Is(m2, GOOD)) |
                       (Is(m1, GOOD) & Is(m2, NORMAL)) |
                       (Is(m1, NORMAL) & Is(m2, GOOD))
                       )

        self.rules = rules
        self.mem_visual_var = m1
        self.mem_stress_var = m2
        self.mem_output_var = m_out

    def calc_score(self, visual_memory_score, memory_stress_score):
        return self.rules.evaluate(**{
            self.mem_visual_var.name: visual_memory_score,
            self.mem_stress_var.name: memory_stress_score
        })


class TemperamentController:
    def __init__(self):
        introversy_var = Variable('introversy', (0, 21),
                                  *mf_set(bounds=(0, 21),
                                          names=('I', 'SI', 'S', 'SE', 'E')))
        neurotism_var = Variable('neurotism', (0, 24),
                                 *mf_set(bounds=(0, 24), names=('L', 'N', 'H', 'VH')))
        temperament_var = Variable('temperament', (0, 100), *mf_set(bounds=(0, 100)))
        rules = Rules(temperament_var)

        rules.add_rule(GOOD,
                       (introversy_var.is_('S') & neurotism_var.is_('L')) |
                       (introversy_var.is_('S') & neurotism_var.is_('N')) |
                       (introversy_var.is_('SI') & neurotism_var.is_('L')) |
                       (introversy_var.is_('SE') & neurotism_var.is_('L')))

        rules.add_rule(NORMAL,
                       introversy_var.is_('I') |
                       (introversy_var.is_('SI') & neurotism_var.is_('N')) |
                       (introversy_var.is_('S') & neurotism_var.is_('H')) |
                       (introversy_var.is_('SE') & neurotism_var.is_('N')) |
                       (introversy_var.is_('SE') & neurotism_var.is_('H')) |
                       (introversy_var.is_('E') & neurotism_var.is_('L')) |
                       (introversy_var.is_('E') & neurotism_var.is_('N')))

        rules.add_rule(BAD,
                       (introversy_var.is_('SI') & neurotism_var.is_('H')) |
                       (introversy_var.is_('SI') & neurotism_var.is_('VH')) |
                       (introversy_var.is_('S') & neurotism_var.is_('VH')) |
                       (introversy_var.is_('SE') & neurotism_var.is_('VH')) |
                       (introversy_var.is_('E') & neurotism_var.is_('H')) |
                       (introversy_var.is_('E') & neurotism_var.is_('VH')))

        self.rules = rules
        self.introversy_var = introversy_var
        self.neurotism_var = neurotism_var
        self.temperament_var = temperament_var

    def temperament_score(self, introversy_score, neurotism_score):
        return self.rules.evaluate(**{
            self.introversy_var.name: introversy_score,
            self.neurotism_var.name: neurotism_score
        })


class AsduController:
    def __init__(self):
        m = Variable('m', (0, 100), *mf_set((0, 100)))
        o = Variable('o', (0, 100), *mf_set((0, 100)))
        p = Variable('p', (0, 100), *mf_set((0, 100)))
        r = Variable('r', (0, 100), *mf_set((0, 100)))
        t = Variable('t', (0, 100), *mf_set((0, 100)))

        res = Variable('res', (0, 100), *mf_set((0, 100), names=('YES', 'NO')))

        rules = Rules(res)
        rules.add_rule('NO', m.is_(BAD) | o.is_(BAD) | p.is_(BAD) | r.is_(BAD) | t.is_(BAD))
        rules.add_rule('YES', Not(m.is_(BAD) | o.is_(BAD) | p.is_(BAD) | r.is_(BAD) | t.is_(BAD)))

        self.rules = rules
        self.memory_var = m
        self.operation_var = o
        self.plasticity_var = p
        self.reaction_var = r
        self.temperament_var = t
        self.result_var = res

    def calc(self, memory_score, operation_score, plasticity_score, reaction_score, temperament_score):
        return self.rules.evaluate(**{
            self.memory_var.name: memory_score,
            self.operation_var.name: operation_score,
            self.plasticity_var.name: plasticity_score,
            self.reaction_var.name: reaction_score,
            self.temperament_var.name: temperament_score
        })


def main():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        install('matplotlib')
        import matplotlib.pyplot as plt

    """
    x = np.linspace(0, 100, 100)
    for mf in mf_set((0, 100), names=(1, 2, 3, 4, 5, 6, 7)):
        plt.plot(x, mf.sample(x), label=mf.name)
    plt.legend()
    plt.show()
    """

    mem = MemoryController()
    temp = TemperamentController()
    op = AsduController()

    import random
    results = []
    for i in range(10000):
        m1 = 100 * random.random()
        m2 = 100 * random.random()

        t1 = 100 * random.random()
        t2 = 100 * random.random()

        memory_score = mem.calc_score(visual_memory_score=m1, memory_stress_score=m2)
        temperament_score = temp.temperament_score(introversy_score=t1, neurotism_score=t2)

        operation_score = 100 * random.random()
        reaction_score = 100 * random.random()
        plasticity_score = 100 * random.random()

        res = op.calc(memory_score, operation_score, plasticity_score, reaction_score, temperament_score)
        results.append(res)

    plt.hist(results)
    plt.show()


    memory_score = np.zeros((20, 20), np.float32)
    for i in range(memory_score.shape[0]):
        s1 = 100 * (i / (memory_score.shape[0] - 1.0))
        for j in range(memory_score.shape[1]):
            s2 = 100 * (j / (memory_score.shape[1] - 1.0))
            #m[i, j] = mem.memory_score(s1, s2)
            memory_score[i, j] = temp.temperament_score(s1, s2)

    plt.imshow(memory_score)
    plt.show()


def asdu(test_results, **kwargs) -> dict:
    memory = MemoryController()
    temperament = TemperamentController()
    result_controller = AsduController()

    memory_score = memory.calc_score(visual_memory_score=test_results['memory']['score'],
                                     memory_stress_score=test_results['memorystress']['score'])
    temperament_score = temperament.temperament_score(introversy_score=test_results['temperament']['extravert_score'],
                                                      neurotism_score=test_results['temperament']['neurotism_score'])
    operation_score = test_results['operation']['score']
    plasticity_score = test_results['plasticity']['score']
    reaction_score = test_results['reaction']['score']

    result = result_controller.calc(memory_score=memory_score,
                                    temperament_score=temperament_score,
                                    operation_score=operation_score,
                                    plasticity_score=plasticity_score,
                                    reaction_score=reaction_score)

    return {'prigodnost': result}


if __name__ == '__main__':
    default_main(asdu)
