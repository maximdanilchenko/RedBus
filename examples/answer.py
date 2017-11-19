from redbus import RedBus

if __name__ == '__main__':
    redbus = RedBus('main')
    redbus.add_func(sum)
    redbus.add_func(pow)
    redbus.add_func(max)
    redbus.add_func(min)
    redbus.listen()
