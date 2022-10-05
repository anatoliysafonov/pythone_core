def input_error(func):

    def inner(*args):
        try:
            return func(*args)
        except ValueError as err:
            print(err)
        except KeyError as err:
            print(err)
        except IndexError as err:
            print(err)
    return inner
