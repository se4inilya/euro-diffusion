class City(object):
    INITIAL_COIN_COUNT = 1000000
    REPRESENTATIVE_PORTION = 1000

    def __init__(self, country_count, country_index, country_name):
        self.completed = False
        self.neighbors = None
        self.country_count = country_count
        self.country_name = country_name

        self.coins = [0] * country_count
        self.cache = [0] * country_count

        self.coins[country_index] = self.INITIAL_COIN_COUNT

    def share_with_neighbors(self):

        if all(map(lambda c: c > 0, self.coins)):
            self.completed = True

        index = 0

        for coin_count in self.coins:
            if coin_count >= self.REPRESENTATIVE_PORTION:
                share = coin_count // self.REPRESENTATIVE_PORTION

                for city in self.neighbors:
                    city.cache[index] += share
                    self.coins[index] -= share

            index += 1

    def update(self):
        for i in range(self.country_count):
            self.coins[i] += self.cache[i]
            self.cache[i] = 0


class Country(object):
    def __init__(self, name, xl, yl, xh, yh):
        self.cities = []
        self.name = name
        self.xl = xl
        self.yl = yl
        self.xh = xh
        self.yh = yh

    def add_city(self, city):
        self.cities.append(city)

    def is_completed(self):
        return all(map(lambda c: c.completed, self.cities))
    
    def is_island(self):
        for city in self.cities:
            for neighbor in city.neighbors:
                if neighbor.country_name != self.name:
                    return False
        return True

class Algorithm(object):
    MAX_XY_VALUE = 10

    def __init__(self):
        self.countries = []

    @staticmethod
    def check_max_xy_value(country_name, value, coord):
        if not 1 <= value <= Algorithm.MAX_XY_VALUE:
            raise Exception('In {}: value {} is not in range 1 ≤ {} ≤ {}'
                            .format(country_name, value, coord, Algorithm.MAX_XY_VALUE))

    @staticmethod
    def check_xy_range(country_name, value_l, value_h, coord_l, coord_h):
        if value_l > value_h:
            raise Exception('In {}: value {}:{} > {}:{}'
                            .format(country_name, coord_l, value_l, coord_h, value_h))

    def add_country(self, string):
        name, *coordinates = string.split()

        if len(name) > 25:
            raise Exception('Name has more than 25 characters')

        xl, yl, xh, yh = map(int, coordinates)

        Algorithm.check_max_xy_value(name, xl, 'xl')
        Algorithm.check_max_xy_value(name, yl, 'yl')
        Algorithm.check_max_xy_value(name, xh, 'xh')
        Algorithm.check_max_xy_value(name, yh, 'yh')

        Algorithm.check_xy_range(name, xl, xh, 'xl', 'xh')
        Algorithm.check_xy_range(name, yl, yh, 'yl', 'yh')

        self.countries.append(Country(name, xl - 1, yl - 1, xh - 1, yh - 1))

   
    def create_empty_area(self):
        xs = []
        ys = []

        for country in self.countries:
            xs.extend((country.xl, country.xh))
            ys.extend((country.yl, country.yh))

        y_range = range(max(ys) - min(ys) + 1)
        x_range = range(max(xs) - min(xs) + 1)

        return [[None for _ in y_range] for _ in x_range]

    def create_cities(self, area):
        country_count = len(self.countries)
        country_index = 0

        for country in self.countries:
            for i in range(country.xh - country.xl + 1):
                for j in range(country.yh - country.yl + 1):
                    x = country.xl + i
                    y = country.yl + j

                    city = City(country_count, country_index, country.name)

                    area[x][y] = city
                    country.add_city(city)

            country_index += 1

    def check_neighbors(self, area, x, y, width, height, neighbors):
        if x + 1 <= width - 1 and area[x + 1][y]:
            neighbors.append(area[x + 1][y])

        if x - 1 >= 0 and area[x - 1][y]:
            neighbors.append(area[x - 1][y])

        if y + 1 <= height - 1 and area[x][y + 1]:
            neighbors.append(area[x][y + 1])

        if y - 1 >= 0 and area[x][y - 1]:
            neighbors.append(area[x][y - 1])

    def add_neighbors(self, area):
        width = len(area)
        height = len(area[0])

        for x in range(width):
            for y in range(height):
                city = area[x][y]

                if city:
                    neighbors = []

                    self.check_neighbors(area, x, y, width, height, neighbors)

                    city.neighbors = neighbors

    def init(self):
        area = self.create_empty_area()

        self.create_cities(area)

        self.add_neighbors(area)

    def is_completed(self):
        return all(map(lambda x: x.is_completed(), self.countries))

    def check_islands(self):
        if len(self.country_list) != 1:
            for country in self.country_list:
                if country.is_island():
                    raise Exception(f'Country {country.name} is an island')
                
    def run(self):
        self.init()

        result = {}
        days = 0

        while True:
            for country in self.countries:
                for city in country.cities:
                    city.share_with_neighbors()

            
                if country.is_completed():
                    if country.name not in result:
                        result[country.name] = days

            
            if self.is_completed():
                break

            
            for country in self.countries:
                for city in country.cities:
                    city.update()

            days += 1

        return sorted(result.items(), key=lambda x: (x[1], x[0]))

def print_result(i, result):
    print('\nCase Number {}'.format(i))

    for r in result:
        print(r[0], r[1])


def fill_tasks(filename):
    with open(filename, 'r') as file:
        country_count = int(file.readline())

        tasks = []

        while country_count:
            if not 1 <= country_count <= 20:
                print('Error: The number of countries (1 ≤ c ≤ 20)')
                return None

            lines = []

            for i in range(country_count):
                lines.append(file.readline())

            tasks.append(lines)

            country_count = int(file.readline())

        return tasks


def make_tasks(tasks):
    case_number = 1

    for lines in tasks:
        try:
            algorithm = Algorithm()

            for line in lines:
                algorithm.add_country(line)

            print_result(case_number, algorithm.run())

            case_number += 1
        except Exception as e:
            print('\nCase Number {}'.format(case_number))
            print('Error: {}'.format(e))


def main():
    tasks = fill_tasks('input.txt')

    if tasks:
        make_tasks(tasks)


if __name__ == '__main__':
    main()
