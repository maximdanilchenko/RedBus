from functools import partial

from redbus import RedBus

if __name__ == '__main__':
    redbus = RedBus('caller')
    print(redbus.call('main', 'min', 1, 2, 3, 4, 5, 6))
    print(redbus.call('main', 'max', 1, 2, 3, 4, 5, 6))
    print(redbus.call('main', 'sum', [1, 2, 3, 4, 5, 6]))

    my_pow = partial(redbus.call, 'main', 'pow')

    print(my_pow(2, 4))
    print(my_pow(2))  # Exception
