import datetime
import bitfinex
import time

api_v2 = bitfinex.bitfinex_v2.api_v2()
limit = 990
count_err = 0

support_period = {
    '1m': 60000,
    '3m': 180000,
    '5m': 300000,
    '15m': 900000,
    '30m': 1800000,
    '1h': 3600000,
    '4h': 14400000,
    '1d': 86400000,
    '1w': 604800000,
}

first_loop = True
ti = datetime.datetime.fromtimestamp(1483389600).isoformat()
first_time = datetime.datetime.fromisoformat(
    input('Enter First Time(ex: 2020-01-01T00:00:00 ):\n')).timestamp()

print('\nYour First Time:', datetime.datetime.fromtimestamp(first_time).isoformat())
first_time *= 1000

last_time = datetime.datetime.fromisoformat(
    input('\nEnter Last Time(ex: 2021-01-01T00:00:00 ):\n')).timestamp()

print('\nYour Last Time: ', datetime.datetime.fromtimestamp(last_time).isoformat(), '\n')
last_time *= 1000

period_time = input('\nEnter Period Time(ex: 5m,30m,1d,1w ):\n')

currency_name = input('\nEnter Currency Name(ex: btcusd,ethusd ):\n')

f = open(f"{currency_name}_{period_time}.csv", "a")

previous_time = int(first_time)
next_time = int(previous_time + (support_period[period_time] * limit))

while next_time <= last_time:
    result = api_v2.candles(
        symbol=currency_name, interval=period_time, start=previous_time, end=next_time)
    result = result[::-1]
    if len(result) < 5:
        if next_time < previous_time or count_err > 5:
            quit()
        print(result, previous_time, next_time, period_time)
        print("error")
        count_err += 1
        time.sleep(5)
        continue
    elif int(str(result[0])[1:14]) != previous_time and not first_loop:
        print('check time', str(result[0])[1:14], previous_time)
        quit()
    else:
        previous_time = next_time + support_period[period_time]
        next_time = next_time + (support_period[period_time] * limit)
        if next_time > last_time and next_time != last_time + support_period[period_time]:
            next_time = last_time

        for item in result:
            f.write(str(item)[1:-1] + '\n')

        if count_err != 0:
            count_err = 0

    print(datetime.datetime.fromtimestamp(next_time / 1000).isoformat())

    if first_loop:
        first_loop = False

    time.sleep(1)

f.close()
