import argparse

parser = argparse.ArgumentParser(description="How to make trade safe?")

parser.add_argument("price", nargs='?', type=float, help="What is the current price?")
parser.add_argument("code", nargs='?', default="cost", help="What is the wanted code?")
parser.add_argument("-p", "--parameter", help="What are the parameters?")
parser.add_argument("-v", "--verbose", action='store_true', help="How does the number come?")

args = parser.parse_args()
print(f"given price {args.price}")
#print(f"Code: {args.code}")

def sell(price):
    #ratio = 0.05
    result = [price*0.90, price, price*1.05]
    if args.verbose: #print("ratio:", ratio)
        print("""do put from price %f to %f
do call from price %f to %f
or do trade by other options:[gann, elliot, benefit, gold]""" % (result[1], result[2], result[0], result[1])
)
    else: print("trade by cost:", result)

def gold(price):
    ratio = [0.5, 0.328,  0.618, 1]
    #ratiodown = [0.5, 0.618, 0.328]
    result = []
    result.append(price)
    ten = 1 * 100
    if 0.1 < price < 1: ten = 1 * 1
    if 1 < price < 10: ten = 1 * 10
    #if price < 0.1 or price > 1000: pass
    price = price * (1+ratio[0]/ten)
    result.append(price)
    price = price * (1-ratio[1]/ten)
    result.append(price)
    price = price * (1+ratio[2]/ten)
    result.append(price)
    price = price * (1-ratio[3]/ten)
    result.append(price)
    if args.verbose: print(list(zip(ratio, result)))
    else: print("trade by gold:", sorted(result[::2]))

def benefit(price):
    ratio = [-0.9, -0.5, -0.3, 0, 0.05, 0.1, 0.4, 0.7, 0.9, 1.15, 1.2, 2]
    priced = map(lambda x: (1+x) * price, ratio)
    result = list(priced)
    if args.verbose: print(list(zip(ratio, result)))
    else: print("trade by benefit:", (result[2:5]))




def get_gann(price):
# support and resistence
# sample: 19775.385009982252, 19810.556879991123, 19845.76, 19880.99437000887, 19916.259990017745
    root = price ** 0.5
    result = []
    for i in range(0, 405, 45): result.append((root - (i/360)) ** 2)
    result = (result[::-1])
    for i in range(45, 405, 45): result.append((root + (i/360)) ** 2)
    if args.verbose: print(list(zip(range(-360, 405, 45), result)))
        #print(result)
    else: print("trade by gann:", result[7:10])

def get_elliot(price):
# wave 1 and 2
# sample: 90, 92, 91, 96, 94, 100, 97.5, 98.5, 95
    result = []
    result.append(price)
    import random

    ratio = random.uniform(0.005, 0.08)
    ratio = ratio*random.choice([-1, 1])
    change = price*ratio
    dest = (price+change)   
    #print(ratio)
    if ratio > 0:
        wave = price+change*random.choice([-0.5, -0.618])
        result.append(wave)
        wave = price+change*random.choice([0.618, 1, 2.618])
        result.append(wave)
        wave = price+price*0.318
        result.append(wave) #4
        wave = price+change*random.choice([0.5, 0.618])
        result.append(wave)  #5
        wave = wave-change*random.choice([0.5, 0.618])
        result.append(wave)  #a
        wave =wave+change*random.choice([0.382, 0.5, 0.618])
        result.append(wave)  #b
        wave = wave-change*random.choice([0.5, 0.618, 1, 1.382, 1.618])
        result.append(wave)  #c
    else:
        wave = price+change*random.choice([-0.5, -0.618])
        result.append(wave)
        wave = price+change*random.choice([0.618, 1, 2.618])
        result.append(wave)
        wave = price+price*0.318
        result.append(wave) #4
        wave = price-change*random.choice([0.5, 0.618])
        result.append(wave)  #5
        wave = wave+change*random.choice([0.5, 0.618])
        result.append(wave)  #a
        wave =wave+change*random.choice([0.382, 0.5, 0.618])
        result.append(wave)  #b
        wave = wave+change*random.choice([0.5, 0.618, 1, 1.382, 1.618])
        result.append(wave)  #c
    if args.verbose: print(list(zip(["1","2","3","4","5","a","b","c"], result)))

        #print("from", price, "to", dest, result)
    else: print("trade by elliot:", result)


def get_stock(name):
    import efinance as ef
    s = ef.stock.get_latest_quote(name, suppress_error=True).to_string(index=False)
    s_list = s.split()
    #print(s_list)
    indices = [-1, 24, 31, 22]
    new_list = [s_list[index] for index in indices]
    new_list[-1] = '+'+new_list[-1]+'%' if float(new_list[-1]) > 0 else new_list[-1]+'%'
    print(name, "latest price:", new_list[:2])

def get_minutes(name):
    import efinance as ef
    s = ef.stock.get_quote_history(name, klt=1)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices])
    s_list = dfs.values.tolist()
   
    print(s_list)

def get_fdays(name):
    import efinance as ef
    s = ef.stock.get_quote_history(name, klt=101)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices]).tail(5)
    s_list = dfs.values.tolist()
   
    print("5days close price", s_list)

def get_tdays(name):
    import efinance as ef
    s = ef.stock.get_quote_history(name, klt=101)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices]).tail(10)
    s_list = dfs.values.tolist()
   
    print("10days close price", s_list)

def get_mdays(name):
    import efinance as ef

    s = ef.stock.get_quote_history(name, klt=101)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices]).tail(30)
    s_list = dfs.values.tolist()
   
    print("30days close price", s_list)

def payus(qty, prc):
    import math

    pos = abs(qty)
    a = pos * 0.0049 if pos * 0.0049 >= 0.99 else 0.99
    a = a if a <= pos * prc * 0.5 * 0.01 else pos * prc * 0.5 * 0.01
    b = pos * 0.005 if pos * 0.005 >= 1 else 1
    b = b if b <= pos * prc * 0.5 * 0.01 else pos * prc * 0.5 * 0.01
    c = 0.003 * pos
    d = 0
    e = 0
    if qty < 0:
        d = 0.0000278 * prc * pos; d = 0.01 if d <= 0.01 else d; e = 0.000166 * pos; e = 8.3 if d >= 8.3 else d; e = 0.01 if d <= 0.01 else d
    fee = a + b + c + d + e
    #print("US", a, b, c, d, e)

    fee = math.ceil(fee * 100) / 100
    return fee


def payhk(qty, prc):
    import math

    pos = abs(qty *prc)

    a = pos * 0.03 * 0.01 if pos * 0.03 * 0.01 >= 3 else 3
    b = 15
    c = 0.002 * 0.01 * pos
    c = c if c >= 2 else 2
    c = c if c <= 100 else 100
    d = math.ceil(0.1 * 0.01 * pos)
    e = 0.00565 * 0.01 * pos if 0.00565 * 0.01 * pos >= 0.01 else 0.01
    f = 0.0027 * 0.01 * pos if 0.0027 * 0.01 * pos >= 0.01 else 0.01
    g = 0.00015 * 0.01 * pos
    fee = a + b + c + d + e + f + g
    #print("HK", a, b, c, d, e, f, g)
    fee = math.ceil(fee * 100) / 100
    return fee

def payhketf(qty, prc):
    import math

    pos = abs(qty * prc)

    a = pos * 0.03 * 0.01 if pos * 0.03 * 0.01 >= 3 else 3
    b = 15
    c = 0.002 * 0.01 * pos
    c = c if c >= 2 else 2
    c = c if c <= 100 else 100
    d = 0#math.ceil(0.1 * 0.01 * pos)
    e = 0.00565 * 0.01 * pos if 0.00565 * 0.01 * pos >= 0.01 else 0.01
    f = 0.0027 * 0.01 * pos if 0.0027 * 0.01 * pos >= 0.01 else 0.01
    g = 0.00015 * 0.01 * pos
    fee = a + b + c + d + e + f + g
    #print("HK", a, b, c, d, e, f, g)
    fee = math.ceil(fee * 100) / 100
    return fee

def paymkt(mkt, qty, prc):
    if mkt == 1: return payus(qty, prc)
    elif mkt == 2: return payhk(qty, prc)
    elif mkt == 3: return payhketf(qty, prc)
    else: return 0

def fee(price):
    #qty = [100, 1000, 10000, 100000]
    result = [paymkt(1, 10, price), paymkt(2, 10, price), paymkt(3, 10, price)]
    if args.verbose: 
        print(100, list(zip(["US", "HK", "ETF"], [paymkt(1, 100, price), paymkt(2, 100, price), paymkt(3, 100, price)])))
        print(1000, list(zip(["US", "HK", "ETF"], [paymkt(1, 1000, price), paymkt(2, 1000, price), paymkt(3, 1000, price)])))
        print(10000, list(zip(["US", "HK", "ETF"], [paymkt(1, 10000, price), paymkt(2, 10000, price), paymkt(3, 10000, price)])))
        print(100000, list(zip(["US", "HK", "ETF"], [paymkt(1, 100000, price), paymkt(2, 100000, price), paymkt(3, 100000, price)])))

    else: print("trade 10 fee:", result)

def get_qdays(name):
    import efinance as ef

    s = ef.stock.get_quote_history(name, klt=101)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices]).tail(30)
    s_list = dfs.values.tolist()
   
    print("90days close price", s_list)

def get_to(name, days, verbose):
    day=days.split('to')
    if verbose: print("split the days", day)
    import efinance as ef
    st = day[0].replace('-', '')
    et = day[1].replace('-', '')

    s = ef.stock.get_quote_history(name, st, et, klt=101)
    #indices = [2, 3, 4, 5, 6, 7, 11]
    indices = [2, 6]

    dfs = (s.iloc[:, indices])
    s_list = dfs.values.tolist()
   
    print(days, "close price", s_list)



if args.code == "gann": get_gann(args.price)
elif args.code == "elliot": get_elliot(args.price)
elif args.code == "cost": sell(args.price) 
elif args.code == "gold": gold(args.price)
elif args.code == "benefit": benefit(args.price)
elif args.code == "fee": fee(args.price)

else: 
    import sys
    if args.verbose: print("connecting ef to get the latest price")
    #try: get_stock(args.code)
    #except Exception as e: sys.exit("error: no connection for", args.code)
    if args.parameter == "minutes": get_minutes(args.code)
    
    if args.parameter == "5days": get_fdays(args.code)
    if args.parameter == "10days": get_tdays(args.code)
    if args.parameter == "30days": get_mdays(args.code)

    if args.parameter == "quarter": get_qdays(args.code)
    #print(args.parameter)
    if "to" in args.parameter: get_to(args.code, args.parameter, args.verbose)

