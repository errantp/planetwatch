# planetwatch
Code to make it easier to figure out earnings and taxes for planetwatch


## Install
Clone the repo, install python 3.7 or greater, and then install.

```
git clone https://github.com/errantp/planetwatch.git
cd planetwatch
pip install .

```

([poetry](https://python-poetry.org/) is also supported with `poetry install`)

```
❯ planets --help
Usage: planets [OPTIONS]

Options:
  --wallet TEXT    Planet Wallet, or list of comma separated wallets
                   [required]
  --currency TEXT  Currency to convert planets into.
  --csv            Export csv of all transactions for given wallet
  --help           Show this message and exit.
```



## Examples
```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency eur


###### For wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY
The current price in eur is : 0.254848
amount                426.144000
current value eur     108.601946
initial value eur     62.867696
gain eur               45.734250
   amount        date  initial price eur  current value eur  initial value eur  gain eur
0  23.008  2021-09-15            0.227428           5.863543            5.232664  0.630879
1  23.040  2021-09-14            0.200080           5.871698            4.609846  1.261852
2  23.040  2021-09-14            0.200080           5.871698            4.609846  1.261852
3  23.040  2021-09-12            0.177932           5.871698            4.099553  1.772145
4  23.040  2021-09-11            0.171145           5.871698            3.943170  1.928528
5  23.040  2021-09-10            0.159267           5.871698            3.669510  2.202188
6  22.720  2021-09-09            0.152454           5.790147            3.463757  2.326390
7  23.040  2021-09-08            0.149045           5.871698            3.433999  2.437699
8  23.040  2021-09-07            0.146756           5.871698            3.381269  2.490429
9  23.040  2021-09-06            0.135407           5.871698            3.119766  2.751932
```

Multiple wallets
```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY,3KBG44MVZSKKOUDW7QJ2QS2FYHFIHNTLT3Q7MTQ2CLG65ZHQ6RL6ENZ7GQ --currency eur


###### For wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY
The current price in eur is : 0.254848
amount                426.144000
current value eur     108.601946
initial value eur     62.867696
gain eur               45.734250
   amount        date  initial price eur  current value eur  initial value eur  gain eur
0  23.008  2021-09-15            0.227428           5.863543            5.232664  0.630879
1  23.040  2021-09-14            0.200080           5.871698            4.609846  1.261852
2  23.040  2021-09-14            0.200080           5.871698            4.609846  1.261852
3  23.040  2021-09-12            0.177932           5.871698            4.099553  1.772145
4  23.040  2021-09-11            0.171145           5.871698            3.943170  1.928528


###### For wallet 3KBG44MVZSKKOUDW7QJ2QS2FYHFIHNTLT3Q7MTQ2CLG65ZHQ6RL6ENZ7GQ
The current price in eur is : 0.254848
amount                1740.640000
current value eur      443.598623
initial value eur     199.522137
gain eur               244.076486
   amount        date  initial price eur  current value eur  initial value eur  gain eur
0   23.04  2021-09-15            0.227428           5.871698            5.239942  0.631756
1   23.04  2021-09-14            0.200080           5.871698            4.609846  1.261852
2   23.04  2021-09-13            0.185853           5.871698            4.282061  1.589637
3   23.04  2021-09-12            0.177932           5.871698            4.099553  1.772145
4   23.04  2021-09-11            0.171145           5.871698            3.943170  1.928528
```


```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency usd

###### For wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY
The current price in usd is : 0.301106
amount                426.144000
current value usd     128.314515
initial value usd     74.360906
gain usd               53.953609
   amount        date  initial price usd  current value usd  initial value usd  gain usd
0  23.008  2021-09-15            0.268778           6.927847            6.184042  0.743805
1  23.040  2021-09-14            0.236209           6.937482            5.442256  1.495226
2  23.040  2021-09-14            0.236209           6.937482            5.442256  1.495226
3  23.040  2021-09-12            0.210221           6.937482            4.843501  2.093982
4  23.040  2021-09-11            0.202202           6.937482            4.658739  2.278744
5  23.040  2021-09-10            0.188485           6.937482            4.342697  2.594785
6  22.720  2021-09-09            0.180454           6.841128            4.099926  2.741202
7  23.040  2021-09-08            0.176202           6.937482            4.059700  2.877782
8  23.040  2021-09-07            0.174077           6.937482            4.010729  2.926753
9  23.040  2021-09-06            0.160621           6.937482            3.700707  3.236775
```


### Export as CSV

```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency usd --csv
```
Will generate the same output expect it will also create a file called `GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY.csv`
