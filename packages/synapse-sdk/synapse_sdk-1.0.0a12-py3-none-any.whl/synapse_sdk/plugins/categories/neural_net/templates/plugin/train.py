import time


def train(run, dataset, hyperparameter, checkpoint=None):
    count_iterations = hyperparameter['iterations']
    run.set_progress(0, count_iterations, category='train')
    for i in range(1, count_iterations + 1):
        time.sleep(0.5)
        loss = float(round((count_iterations - i) / count_iterations, 2))
        miou = 1 - loss
        run.log_metric('iteration', i, loss=loss, miou=miou)
        run.set_progress(i, count_iterations, category='train')
    return './'
