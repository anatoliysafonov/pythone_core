def input_error(func):

    def inner(*args):
        result = ''
        try:
            result = func(*args)
        except ValueError as err:
            print(err)
        except KeyError as err:
            print(err)
        except IndexError as err:
            print(err)
        return result
    return inner
