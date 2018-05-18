from zeep import Client
from math import ceil


def get_mean_temperature(file):
    temp = []
    with open(file, 'r') as f:
        for item in f:
            temp.append(int(item.split()[0]))
        mean_f = sum(temp)/len(temp)
        client = Client('https://www.w3schools.com/xml/tempconvert.asmx?WSDL')
        return round(float(client.service.FahrenheitToCelsius(str(mean_f))), 2)


def price_for_travel(file):
    client = Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    goal = 'RUB'
    with open(file, 'r') as f:
        for item in f:
            r = item.split()
            print(' '.join((r[0],
                            str(ceil(client.service.ConvertToNum(fromCurrency=r[2], toCurrency=goal, amount=r[1],
                                                                 rounding=True))),
                            goal)))


if __name__ == '__main__':
    print(f"Mean temperature - {get_mean_temperature('temps.txt')} C.\n")
    price_for_travel('currencies.txt')
