from seatools.ioc import run, Bean, Autowired


def start():
    run(scan_package_names='tests.test_ioc2', config_dir='config')


@Bean
class A:

    def print(self):
        print('A')


@Bean
class B(A):

    def print(self):
        print("B")


class C(A):

    def print(self):
        print("C")


def test_depends():
    start()

    c = Autowired('b', cls=A)
    c.print()
