from multiprocessing import Process
from process import calc_normalisation
import pickle


def process_pickle(f):

    with open("data_src/broken_hill_surface_samples_group_%s.pickle" % f, 'rb') as fin:
        group = pickle.load(fin)
        print('opened: %s' % f)
        print(type(group))

        lensubset = calc_normalisation(group, f)


if __name__ == '__main__':
    fidx = [0, 1, 2, 3, 4, 5, 6, 7]
    procs = []
 
    for idx, f in enumerate(fidx):
        print(f)
        f = str(f)
        proc = Process(target=process_pickle, args=(f))
        procs.append(proc)
        proc.start()
 
    for proc in procs:
        proc.join()
