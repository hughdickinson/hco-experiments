################################################################
# Methods for experiment collection

from . import DB

collection = DB().data
aggregate = collection.aggregate


def upload_trials(trials, experiment_name):
    data = []
    for trial in trials:
        print(trial)
        data += trial.db_export(experiment_name)

    print('uploading %d trials' % len(data))
    collection.insert_many(data)
    print('done')