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
  --wallet TEXT    Planet Wallet  [required]
  --currency TEXT  Currency to convert planets into.
  --csv            Export csv of all transactions for given wallet
  --help           Show this message and exit.
```



## Examples
```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency eur
The current price in eur is : 0.166475
amount                310.976000
current_value_eur      51.769730
purchase_value_eur     40.372615
gain_eur               11.397115
dtype: float64
   amount        date  purchase_price_eur  current_value_eur  purchase_value_eur  gain_eur
0  23.040  2021-09-10            0.159267           3.835584            3.669510  0.166074
1  22.720  2021-09-09            0.152454           3.782312            3.463757  0.318555
2  23.040  2021-09-08            0.149045           3.835584            3.433999  0.401585
3  23.040  2021-09-07            0.146756           3.835584            3.381269  0.454315
4  23.040  2021-09-06            0.135407           3.835584            3.119766  0.715818
5  23.040  2021-09-05            0.126531           3.835584            2.915269  0.920315
6  23.040  2021-09-04            0.123744           3.835584            2.851070  0.984514
7  20.512  2021-09-03            0.121153           3.414735            2.485092  0.929643
8  15.936  2021-09-02            0.120051           2.652946            1.913135  0.739810
9   3.360  2021-09-01            0.119421           0.559356            0.401253  0.158103
```


```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency usd
The current price in usd is : 0.196685
amount                310.976000
current_value_usd      61.164315
purchase_value_usd     47.790114
gain_usd               13.374201
dtype: float64
   amount        date  purchase_price_usd  current_value_usd  purchase_value_usd  gain_usd
0  23.040  2021-09-10            0.188485           4.531622            4.342697  0.188925
1  22.720  2021-09-09            0.180454           4.468683            4.099926  0.368757
2  23.040  2021-09-08            0.176202           4.531622            4.059700  0.471923
3  23.040  2021-09-07            0.174077           4.531622            4.010729  0.520894
4  23.040  2021-09-06            0.160621           4.531622            3.700707  0.830915
5  23.040  2021-09-05            0.150363           4.531622            3.464360  1.067263
6  23.040  2021-09-04            0.147052           4.531622            3.388068  1.143554
7  20.512  2021-09-03            0.143852           4.034403            2.950683  1.083720
8  15.936  2021-09-02            0.142276           3.134372            2.267304  0.867068
9   3.360  2021-09-01            0.141103           0.660862            0.474107  0.186755
```


### Export as CSV

```
❯ planets --wallet GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY --currency usd --csv
```
Will generate the same output expect it will also create a file called `GYLEOJFHACSCATPBVQ345UCMCOMSGV76X4XTVOLHGXKOCJL44YBUAHXJOY.csv`
