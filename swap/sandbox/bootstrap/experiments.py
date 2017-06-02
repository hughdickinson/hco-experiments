
import swap.plots.distributions as distributions
from swap import Control
from swap.utils.golds import GoldGetter
from swap.agents.agent import Stat
from swap.utils.scores import ScoreExport
import swap.db.experiment as dbe

import json
import os


class Trial:
    def __init__(self, consensus, controversial, golds, swap_export):
        """
            consensus, controversial: settings used to run swap; number of
                consensus  controversial subjects used to make gold set
            golds: Gold standard set used during run
            roc_export: ScoreExport of swap scores
        """
        self.consensus = consensus
        self.controversial = controversial

        self.golds = golds
        self.scores = swap_export

    def n_golds(self):
        n = {-1: 0, 0: 0, 1: 0}
        for gold in self.golds.values():
            n[gold] += 1

        return n

    def purity(self, cutoff):
        return self.scores.purity(cutoff)

    def completeness(self, purity):
        return self.scores.completeness(purity)

    def purify(self):
        pass

    def plot(self, cutoff):
        return (self.consensus, self.controversial,
                self.purity(cutoff), self.completeness(cutoff))

    @staticmethod
    def from_control(consensus, controversial, control):
        t = Trial(consensus, controversial,
                  control.gold_getter.golds,
                  control.getSWAP().score_export())
        return t

    def db_export(self, name):
        data = []
        for i in self.scores.sorted_scores:
            score = self.scores.scores[i]
            item = self._db_export_id(name)
            item.update({
                'subject': score.id,
                'gold': score.gold,
                'p': score.p,
                'used_gold': -1
            })
            if score.id in self.golds:
                item['used_gold'] = self.golds[score.id]
            data.append(item)
        return data

    def _db_export_id(self, name):
        return {
            'experiment': name,
            'consensus': self.consensus,
            'controversial': self.controversial
        }

    def __str__(self):
        s = 'trial cv %d cn %d' % (self.controversial, self.consensus)
        return s


class Experiment:
    def __init__(self, saver, cutoff=0.96):
        self.trials = []
        self.plot_points = []

        self.save_f = saver
        self.p_cutoff = cutoff

        self.save_count = 0

    @staticmethod
    def from_trial_export(directory, cutoff, saver, loader):
        files = get_trials(directory)

        e = Experiment(saver, cutoff)
        for fname in files:
            print(fname)
            trials = loader(fname)
            for trial in trials:
                e.add_trial(trial)
            e.trials = []

        return e

    def init_swap(self):
        control = Control()
        control.run()

        return control.getSWAP()

    def run(self):
        gg = GoldGetter()
        swap = self.init_swap()
        n = 1
        for cv in range(0, 1001, 50):
            for cn in range(0, 1001, 50):
                if cv == 0 and cn == 0:
                    continue
                gg.reset()

                print('\nRunning trial %d with cv=%d cn=%d' %
                      (n, cv, cn))
                if cv > 0:
                    gg.controversial(cv)
                if cn > 0:
                    gg.consensus(cn,)

                swap.set_gold_labels(gg.golds)
                swap.process_changes()
                self.add_trial(Trial(cn, cv, gg.golds, swap.score_export()))

                n += 1
            self.clear_mem(cv, cn)

    def clear_mem(self, cv, cn):
        """
            Saves trial objects to disk to free up memory
        """
        # fname = 'trials_cv_%s_cn_%s.pkl' % (cv, cn)
        self.save_trials()
        self.trials = []

    def save_trials(self, path):
        trials = sorted(
            self.trials,
            key=lambda trial: (trial.controversial, trial.consensus))

        for trial in enumerate(trials):
            fname = 'trials_%d' % self.save_count
            fname = os.path.join(path, fname)

            trial.to_json(fname)
            self.save_count += 1

    def add_trial(self, trial):
        self.trials.append(trial)
        self.plot_points.append(trial.plot(self.p_cutoff))

    def plot_purity(self, fname):
        data = []
        for point in self.plot_points:
            x, y, purity, completeness = point
            data.append((x, y, purity))

        distributions.multivar_scatter(
            fname, data, 'Purity in subjects with p>0.96')

    def plot_completeness(self, fname):
        data = []
        for point in self.plot_points:
            x, y, purity, completeness = point
            data.append((x, y, completeness))

        import pprint
        pprint.pprint(data)
        distributions.multivar_scatter(
            fname, data, 'Completeness in swap scores when purity >0.96')

    def plot_both(self, fname):
        data = []
        for point in self.plot_points:
            x, y, purity, completeness = point
            data.append((x, y, purity * completeness))

        import pprint
        pprint.pprint(data)
        distributions.multivar_scatter(
            fname, data, '')

    def __str__(self):
        s = '%d points\n' % len(self.plot_points)
        s += str(Stat([i[2] for i in self.plot_points]))
        return s

    def __repr__(self):
        return str(self)


def upload_trials(directory, loader):
    files = get_trials(directory)
    for fname in files:
        print(fname)
        trials = loader(fname)
        dbe.upload_trials(trials)


def get_trials(directory):
    import os
    import re

    pattern = re.compile('trials_cv_[0-9]{1,4}_cn_[0-9]{1,4}.pkl')

    def _path(fname):
        return os.path.join(directory, fname)

    def istrial(fname):
        if pattern.match(fname):
            return True
        else:
            return False

    files = []
    for fname in os.listdir(directory):
        path = _path(fname)
        if os.path.isfile(path) and istrial(fname):
            files.append(path)

    return files


if __name__ == "__main__":
    e = Experiment()
    e.run()

    import code
    code.interact(local=locals())

    # x_ = range(50)
    # y_ = range(50)
    # z = lambda x, y: x + y

    # data = []
    # for x in x_:
    #     for y in y_:
    #         data.append((x, y, z(x, y)))

    # print(data)
    # distributions.multivar_scatter(None, data)
