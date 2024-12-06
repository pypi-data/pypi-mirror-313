
# SuperFastPython.com
# load many files concurrently with processes and threads in batch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import threading
from cffi import FFI
from tqdm import tqdm
import time
from threading import Thread
from SharedData.Logger import Logger
import queue
from queue import Empty

# USAGE EXAMPLE:
# io_bound(thread_func, iterator, args)
# thread_func:define the task function to run parallel. Ie: read_files,days_trading_from_to
# iteration: single iteration items of parallel task
# args: commom task variables

# thread_func EXAMPLES

# IO BOUND EXAMPLE
# def read_files(iteration, args):
#     fileid = iteration[0]
#     file_list = args[0]
#     fpath = file_list[fileid]
#     df = pd.read_csv(fpath)
#     return [df]

# CPU BOUND EXAMPLE
# def days_trading_from_to(iteration, args):
#     cal = iteration[0]
#     start = iteration[1]
#     end = iteration[2]
#     calendars = args[0]
#     idx = (calendars[cal]>=start) & ((calendars[cal]<=end))
#     return [np.count_nonzero(idx)]

############## MULTI PROCESS MULTI THREAD ORDERED ##############


def io_bound(thread_func, iterator, args, maxproc=None, maxthreads=4):
    results = []
    # determine chunksize
    niterator = len(iterator)
    if niterator > 0:
        n_workers = multiprocessing.cpu_count() - 2
        n_workers = min(n_workers, niterator)
        if not maxproc is None:
            n_workers = min(n_workers, maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(io_bound_process,
                                         thread_func, proc_iterator, args, maxthreads)
                futures.append(future)
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]
    return results


def io_bound_process(thread_func, proc_iterator, args, maxthreads):
    results = []
    # create a thread pool
    nthreads = len(proc_iterator)
    nthreads = min(nthreads, maxthreads)
    if nthreads > 0:
        with ThreadPoolExecutor(nthreads) as exe:
            # load files
            futures = [exe.submit(thread_func, iteration, args)
                       for iteration in proc_iterator]
            # collect data
            for future in futures:
                res = future.result()
                results = [*results, *res]

    return results

############## MULTI PROCESS MULTI THREAD UNORDERED ##############

def multiprocess_multithread_workers(thread_func, args, maxproc=2, maxthreads=2):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    nworkers = multiprocessing.cpu_count() - 2
    if not maxproc is None:
        nworkers = min(nworkers, maxproc)
    
    workers = [multiprocessing.Process(target=multi_thread_worker_process,
                                       args=(thread_func, input_queue, output_queue, args, maxthreads))
               for _ in range(nworkers)]

    for w in workers:
        w.start()

    return input_queue, output_queue, workers

# def io_bound_unordered(thread_func, iterator, args, maxproc=None, maxthreads=1):
#     results = []
#     input_queue = multiprocessing.Queue()
#     output_queue = multiprocessing.Queue()
#     niterator = len(iterator)
#     nworkers = multiprocessing.cpu_count() - 2
#     if not maxproc is None:
#         nworkers = min(nworkers, maxproc)
#     if (niterator <= nworkers) \
#             | (niterator <= int(nworkers*maxthreads)):
#         maxthreads = 1
#         nworkers = niterator

#     workers = [multiprocessing.Process(target=multi_thread_worker_process,
#                                        args=(thread_func, input_queue, output_queue, args, maxthreads))
#                for _ in range(nworkers)]

#     for w in workers:
#         w.start()

#     for i in range(niterator):
#         input_queue.put(iterator.iloc[i])

#     desc = '%s(%i proc,%i threads)' % (thread_func.__name__,nworkers,maxthreads)
#     pbar = tqdm(range(niterator), desc=desc)
#     nresults = 0
#     watchdog = time.time()
#     while nresults < niterator:
#         try:
#             output = output_queue.get(block=False)
#             if output:
#                 results.extend(output)
#                 nresults += 1
#                 pbar.update(1)
#                 watchdog = time.time()
#         except Empty:
#             exitloop = False
#             for w in workers:
#                 if not w.is_alive():
#                     Logger.log.error('Worker stopped running %s' % (w.exitcode))
#                     exitloop=True
#                     break
#             if exitloop:
#                 for w in workers:
#                     try:
#                         w.terminate()
#                     except:
#                         pass
#                 raise Exception('Worker stopped running!')

#             if input_queue.qsize() == 0:
#                 if time.time()-watchdog > 300:
#                     Logger.log.error('Watchdog timeout!')
#                     break
#             time.sleep(0.1)
#         except Exception as e:
#             Logger.log.error('io_bound_unordered error %s' % (str(e)))

#     # Signal processes to terminate
#     for _ in range(nworkers):
#         input_queue.put(None)

#     for w in workers:
#         w.join()

#     if not input_queue.empty():
#         raise Exception('Input queue not totally consumed!')
    
#     if not output_queue.empty():
#         raise Exception('Output queue not totally consumed!')

#     return results


def io_bound_unordered(thread_func, iterator, args, maxproc=None, maxthreads=1, timeout=60):
    results = []
    with multiprocessing.Manager() as manager:
        input_queue = manager.Queue()
        output_queue = manager.Queue()
        niterator = len(iterator)
        nworkers = max(1, multiprocessing.cpu_count() - 2)
        if maxproc is not None:
            nworkers = min(nworkers, maxproc)
        if niterator <= nworkers or niterator <= int(nworkers * maxthreads):
            maxthreads = 1
            nworkers = niterator

        workers = [multiprocessing.Process(target=multi_thread_worker_process,
                                           args=(thread_func, input_queue, output_queue, args, maxthreads))
                   for _ in range(nworkers)]

        for w in workers:
            w.start()

        for i in range(niterator):
            input_queue.put(iterator.iloc[i])

        desc = f'{thread_func.__name__}({nworkers} proc,{maxthreads} threads)'
        with tqdm(total=niterator, desc=desc) as pbar:
            nresults = 0
            watchdog = time.time()
            while nresults < niterator:
                try:
                    output = output_queue.get(timeout=1)  # Wait for 1 second
                    if output:
                        results.extend(output)
                        nresults += 1
                        pbar.update(1)
                        watchdog = time.time()
                except Empty:
                    if not any(w.is_alive() for w in workers):
                        Logger.log.error('All workers stopped running')
                        break
                    if input_queue.empty() and time.time() - watchdog > timeout:
                        Logger.log.error('Watchdog timeout!')
                        break
                except Exception as e:
                    Logger.log.error(f'io_bound_unordered error: {str(e)}')

        # Signal processes to terminate
        for _ in range(nworkers):
            input_queue.put(None)

        for w in workers:
            w.join(timeout=5)  # Wait for 5 seconds for each worker to finish
            if w.is_alive():
                w.terminate()

        if not input_queue.empty():
            Logger.log.warning('Input queue not totally consumed!')
        
        if not output_queue.empty():
            Logger.log.warning('Output queue not totally consumed!')

    return results

def multi_thread_worker_process(thread_func, input_queue, output_queue, args, nthreads):
    threads = [threading.Thread(target=worker_thread,
                                args=(thread_func, input_queue, output_queue, args))
               for _ in range(nthreads)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def worker_thread(thread_func, input_queue, output_queue, args):
    while True:
        iteration = input_queue.get()
        if iteration is None:
            break        
        try:
            result = thread_func(iteration, args)
            if not isinstance(result, list):
                result = [result]
            output_queue.put(result)
        except Exception as e:
            Logger.log.error('Error in worker %s : %s ,%s\n' \
                             % (thread_func.__name__, str(iteration),str(e)))
            output_queue.put([-1])
        

################# MULTI PROCESS ORDERED #################


def cpu_bound(thread_func, iterator, args, maxproc=None):
    results = []
    # determine chunksize
    niterator = len(iterator)
    if niterator > 0:
        n_workers = multiprocessing.cpu_count() - 2
        n_workers = min(n_workers, niterator)
        if not maxproc is None:
            n_workers = min(n_workers, maxproc)
        chunksize = round(niterator / n_workers)
        # create the process pool
        with ProcessPoolExecutor(n_workers) as executor:
            futures = list()
            # split the load operations into chunks
            for i in range(0, niterator, chunksize):
                # select a chunk of filenames
                proc_iterator = iterator[i:(i + chunksize)]
                # submit the task
                future = executor.submit(
                    cpu_bound_process, thread_func, proc_iterator, args)
                futures.append(future)
            # process all results
            for future in futures:
                # open the file and load the data
                res = future.result()
                results = [*results, *res]
    return results


def cpu_bound_process(thread_func, proc_iterator, args):
    results = []
    for iteration in proc_iterator:
        res = thread_func(iteration, args)
        results = [*results, *res]
    return results

############## MULTI PROCESS UNORDERED ##############


def cpu_bound_unordered(thread_func, iterator, args, maxproc=None):
    results = []
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    niterator = len(iterator)
    nworkers = multiprocessing.cpu_count() - 2
    nworkers = min(nworkers, niterator)
    if not maxproc is None:
        nworkers = min(nworkers, maxproc)

    workers = [multiprocessing.Process(target=single_thread_worker_process,
                                       args=(thread_func, input_queue, output_queue, args))
               for _ in range(nworkers)]

    for w in workers:
        w.start()

    for i in range(niterator):
        input_queue.put(iterator[i])

    for i in tqdm(range(niterator), desc='cpu_bound_unordered:'):
        results.extend(output_queue.get())

    # Signal processes to terminate
    for _ in range(niterator):
        input_queue.put(None)

    for w in workers:
        w.join()

    return results


def single_thread_worker_process(thread_func, input_queue, output_queue, args):
    while True:
        iteration = input_queue.get()
        if iteration is None:
            break
        result = thread_func(iteration, args)
        output_queue.put(result)
