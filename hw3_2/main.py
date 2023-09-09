import multiprocessing
import time


def factorize_sync(*numbers):
    result = []
    for num in numbers:
        divisors = [i for i in range(1, num + 1) if num % i == 0]
        result.append(divisors)
    return result


def factorize_parallel(*numbers):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)
    results = pool.map(factorize_number, numbers)
    pool.close()
    pool.join()
    return results


def factorize_number(num):
    return [i for i in range(1, num + 1) if num % i == 0]


if __name__ == '__main__':
    start_time = time.time()
    a, b, c, d = factorize_sync(128, 255, 99999, 10651060)
    end_time = time.time()
    print("Синхронна версія зайняла час: {:.4f} секунд".format(end_time - start_time))

    start_time = time.time()
    e, f, g, h = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()
    print("Покращена версія з багатьма ядрами зайняла час: {:.4f} секунд".format(end_time - start_time))
