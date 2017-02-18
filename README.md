# aiohttp benchmarks


Usage

```shell
virtualenv -p `which python3.6` env
. env/bin/activate
```

**With vagrant:**

```shell
vagrant up
vagrant ssh -c /vagrant/remote-setup/setup.sh
python run.py
python process.py
```

**With a remote machine:**

(this assumes you have a pem file `benchmarks.pem` in the current directory.)

```shell
export REMOTE=true
export SSH_ADDRESS="<user>@<host>"
export HTTP_ADDRESS="http://<host>"
scp -i benchmarks.pem -r app $SSH_ADDRESS:
scp -i benchmarks.pem -r remote-setup $SSH_ADDRESS:
scp -i benchmarks.pem gunicorn_conf.py $SSH_ADDRESS:
ssh -i benchmarks.pem $SSH_ADDRESS remote-setup/setup.sh

# everything should now be setup, you can run gunicorn
ssh -i benchmarks.pem $SSH_ADDRESS "sudo ~/env35/bin/gunicorn app.gunicorn:app -c gunicorn_conf.py"
# now open $HTTP_ADDRESS/plaintext in your browser and check the server is working.

python run.py
python process.py
```

## Results as of (2017-02-18) - remote server

Tests were run between aws `t2.medium` in `eu-west` running the standard ubuntu 16.04 ami
and my desktop in London with a 20Mb up/down dedicated EFM line.

### Comparing aiohttp versions

```
TODO
```

### Comparing python versions

```
TODO
```

## Results as of (2017-02-16) - local server

### Comparing aiohttp versions

```
                 URL   python       DB  queries     Conc           1.2.0           1.3.1         2.0.0a0 
                 /db      3.5      orm        -       32           5,309     5,005 | -6%     6,125 | 15% 
                 /db      3.5      orm        -       64           5,417     5,133 | -5%     6,290 | 16% 
                 /db      3.5      orm        -      128           5,445     5,272 | -3%     6,305 | 16% 
                 /db      3.5      orm        -      256           5,584     5,387 | -4%     6,174 | 11% 
                 /db      3.5      raw        -       32           7,080     7,372 |  4%     9,728 | 37% 
                 /db      3.5      raw        -       64           7,617     7,486 | -2%    10,405 | 37% 
                 /db      3.5      raw        -      128           8,126     7,827 | -4%    10,635 | 31% 
                 /db      3.5      raw        -      256           8,043     7,933 | -1%    10,757 | 34% 

           /fortunes      3.5      orm        -       32           3,925     3,808 | -3%     3,803 | -3% 
           /fortunes      3.5      orm        -       64           4,390     4,283 | -2%     5,304 | 21% 
           /fortunes      3.5      orm        -      128           4,570     4,405 | -4%     5,421 | 19% 
           /fortunes      3.5      orm        -      256           4,589     4,514 | -2%     5,385 | 17% 
           /fortunes      3.5      raw        -       32           5,394     5,347 | -1%     6,548 | 21% 
           /fortunes      3.5      raw        -       64           5,914     5,593 | -5%     7,009 | 19% 
           /fortunes      3.5      raw        -      128           6,140     5,936 | -3%     7,131 | 16% 
           /fortunes      3.5      raw        -      256           6,207     6,076 | -2%     7,231 | 16% 

               /json      3.5        -        -       32          12,232    11,614 | -5%    16,832 | 38% 
               /json      3.5        -        -       64          17,214    17,481 |  2%    34,090 | 98% 
               /json      3.5        -        -      128          17,793    15,896 |-11%    33,126 | 86% 
               /json      3.5        -        -      256          18,839    16,302 |-13%    33,638 | 79% 

          /plaintext      3.5        -        -       32          17,574    14,142 |-20%    30,872 | 76% 
          /plaintext      3.5        -        -       64          17,208    14,762 |-14%    30,303 | 76% 
          /plaintext      3.5        -        -      128          17,866    16,071 |-10%    30,337 | 70% 
          /plaintext      3.5        -        -      256          17,130    15,613 | -9%    31,626 | 85% 

  /queries/{queries}      3.5      orm        5      256           1,767     1,675 | -5%     1,853 |  5% 
  /queries/{queries}      3.5      orm       10      256             936       925 | -1%       956 |  2% 
  /queries/{queries}      3.5      orm       20      256             489       481 | -2%       497 |  2% 
  /queries/{queries}      3.5      raw        5      256           4,893     4,727 | -3%     5,772 | 18% 
  /queries/{queries}      3.5      raw       10      256           3,422     3,407 | -0%     3,695 |  8% 
  /queries/{queries}      3.5      raw       20      256           2,138     2,094 | -2%     2,129 | -0% 

  /updates/{queries}      3.5      orm        5      256             864       871 |  1%       876 |  1% 
  /updates/{queries}      3.5      orm       10      256             413       447 |  8%       444 |  7% 
  /updates/{queries}      3.5      orm       20      256             214       226 |  5%       236 | 10% 
  /updates/{queries}      3.5      raw        5      256           2,932     2,830 | -3%     3,004 |  2% 
  /updates/{queries}      3.5      raw       10      256           1,826     1,754 | -4%     1,724 | -6% 
  /updates/{queries}      3.5      raw       20      256           1,000       973 | -3%     1,062 |  6% 

                 /db      3.6      orm        -       32           4,934     4,579 | -7%     5,747 | 16% 
                 /db      3.6      orm        -       64           5,087     4,610 | -9%     5,751 | 13% 
                 /db      3.6      orm        -      128           5,127     4,813 | -6%     5,901 | 15% 
                 /db      3.6      orm        -      256           5,274     4,614 |-13%     5,845 | 11% 
                 /db      3.6      raw        -       32           7,149     6,633 | -7%     9,127 | 28% 
                 /db      3.6      raw        -       64           7,135     7,081 | -1%     9,529 | 34% 
                 /db      3.6      raw        -      128           7,458     7,057 | -5%     9,705 | 30% 
                 /db      3.6      raw        -      256           7,497     7,042 | -6%    10,028 | 34% 

           /fortunes      3.6      orm        -       32           3,466     2,004 |-42%     3,351 | -3% 
           /fortunes      3.6      orm        -       64           3,927     3,781 | -4%     4,519 | 15% 
           /fortunes      3.6      orm        -      128           3,863     3,879 |  0%     4,606 | 19% 
           /fortunes      3.6      orm        -      256           4,036     4,042 |  0%     4,486 | 11% 
           /fortunes      3.6      raw        -       32           4,930     4,602 | -7%     5,931 | 20% 
           /fortunes      3.6      raw        -       64           4,984     4,927 | -1%     6,194 | 24% 
           /fortunes      3.6      raw        -      128           5,263     5,198 | -1%     6,386 | 21% 
           /fortunes      3.6      raw        -      256           5,423     5,346 | -1%     6,553 | 21% 

               /json      3.6        -        -       32          11,933     6,674 |-44%    22,730 | 90% 
               /json      3.6        -        -       64          14,983    14,379 | -4%    26,269 | 75% 
               /json      3.6        -        -      128          15,759    14,554 | -8%    25,988 | 65% 
               /json      3.6        -        -      256          15,933    14,352 |-10%    25,778 | 62% 

          /plaintext      3.6        -        -       32          12,334    13,836 | 12%    24,245 | 97% 
          /plaintext      3.6        -        -       64          14,767    14,098 | -5%    24,506 | 66% 
          /plaintext      3.6        -        -      128          15,293    13,669 |-11%    23,282 | 52% 
          /plaintext      3.6        -        -      256          14,769    13,812 | -6%    24,649 | 67% 

  /queries/{queries}      3.6      orm        5      256           1,638     1,606 | -2%     1,684 |  3% 
  /queries/{queries}      3.6      orm       10      256             827       881 |  7%       965 | 17% 
  /queries/{queries}      3.6      orm       20      256             436       464 |  6%       486 | 11% 
  /queries/{queries}      3.6      raw        5      256           4,503     4,437 | -1%     5,639 | 25% 
  /queries/{queries}      3.6      raw       10      256           3,229     3,091 | -4%     3,571 | 11% 
  /queries/{queries}      3.6      raw       20      256           2,009     2,022 |  1%     2,252 | 12% 

  /updates/{queries}      3.6      orm        5      256             829       830 |  0%       858 |  3% 
  /updates/{queries}      3.6      orm       10      256             405       451 | 11%       450 | 11% 
  /updates/{queries}      3.6      orm       20      256             223       229 |  3%       198 |-11% 
  /updates/{queries}      3.6      raw        5      256           2,800     2,763 | -1%     3,076 | 10% 
  /updates/{queries}      3.6      raw       10      256           1,744     1,724 | -1%     1,869 |  7% 
  /updates/{queries}      3.6      raw       20      256             959     1,000 |  4%     1,053 | 10%
```

### Comparing python versions

```
                 URL  aiohttp       DB  queries     Conc             3.5             3.6 
                 /db    1.2.0      orm        -       32           5,309     4,934 | -7% 
                 /db    1.2.0      orm        -       64           5,417     5,087 | -6% 
                 /db    1.2.0      orm        -      128           5,445     5,127 | -6% 
                 /db    1.2.0      orm        -      256           5,584     5,274 | -6% 
                 /db    1.2.0      raw        -       32           7,080     7,149 |  1% 
                 /db    1.2.0      raw        -       64           7,617     7,135 | -6% 
                 /db    1.2.0      raw        -      128           8,126     7,458 | -8% 
                 /db    1.2.0      raw        -      256           8,043     7,497 | -7% 

           /fortunes    1.2.0      orm        -       32           3,925     3,466 |-12% 
           /fortunes    1.2.0      orm        -       64           4,390     3,927 |-11% 
           /fortunes    1.2.0      orm        -      128           4,570     3,863 |-15% 
           /fortunes    1.2.0      orm        -      256           4,589     4,036 |-12% 
           /fortunes    1.2.0      raw        -       32           5,394     4,930 | -9% 
           /fortunes    1.2.0      raw        -       64           5,914     4,984 |-16% 
           /fortunes    1.2.0      raw        -      128           6,140     5,263 |-14% 
           /fortunes    1.2.0      raw        -      256           6,207     5,423 |-13% 

               /json    1.2.0        -        -       32          12,232    11,933 | -2% 
               /json    1.2.0        -        -       64          17,214    14,983 |-13% 
               /json    1.2.0        -        -      128          17,793    15,759 |-11% 
               /json    1.2.0        -        -      256          18,839    15,933 |-15% 

          /plaintext    1.2.0        -        -       32          17,574    12,334 |-30% 
          /plaintext    1.2.0        -        -       64          17,208    14,767 |-14% 
          /plaintext    1.2.0        -        -      128          17,866    15,293 |-14% 
          /plaintext    1.2.0        -        -      256          17,130    14,769 |-14% 

  /queries/{queries}    1.2.0      orm        5      256           1,767     1,638 | -7% 
  /queries/{queries}    1.2.0      orm       10      256             936       827 |-12% 
  /queries/{queries}    1.2.0      orm       20      256             489       436 |-11% 
  /queries/{queries}    1.2.0      raw        5      256           4,893     4,503 | -8% 
  /queries/{queries}    1.2.0      raw       10      256           3,422     3,229 | -6% 
  /queries/{queries}    1.2.0      raw       20      256           2,138     2,009 | -6% 

  /updates/{queries}    1.2.0      orm        5      256             864       829 | -4% 
  /updates/{queries}    1.2.0      orm       10      256             413       405 | -2% 
  /updates/{queries}    1.2.0      orm       20      256             214       223 |  4% 
  /updates/{queries}    1.2.0      raw        5      256           2,932     2,800 | -5% 
  /updates/{queries}    1.2.0      raw       10      256           1,826     1,744 | -4% 
  /updates/{queries}    1.2.0      raw       20      256           1,000       959 | -4% 

                 /db    1.3.1      orm        -       32           5,005     4,579 | -9% 
                 /db    1.3.1      orm        -       64           5,133     4,610 |-10% 
                 /db    1.3.1      orm        -      128           5,272     4,813 | -9% 
                 /db    1.3.1      orm        -      256           5,387     4,614 |-14% 
                 /db    1.3.1      raw        -       32           7,372     6,633 |-10% 
                 /db    1.3.1      raw        -       64           7,486     7,081 | -5% 
                 /db    1.3.1      raw        -      128           7,827     7,057 |-10% 
                 /db    1.3.1      raw        -      256           7,933     7,042 |-11% 

           /fortunes    1.3.1      orm        -       32           3,808     2,004 |-47% 
           /fortunes    1.3.1      orm        -       64           4,283     3,781 |-12% 
           /fortunes    1.3.1      orm        -      128           4,405     3,879 |-12% 
           /fortunes    1.3.1      orm        -      256           4,514     4,042 |-10% 
           /fortunes    1.3.1      raw        -       32           5,347     4,602 |-14% 
           /fortunes    1.3.1      raw        -       64           5,593     4,927 |-12% 
           /fortunes    1.3.1      raw        -      128           5,936     5,198 |-12% 
           /fortunes    1.3.1      raw        -      256           6,076     5,346 |-12% 

               /json    1.3.1        -        -       32          11,614     6,674 |-43% 
               /json    1.3.1        -        -       64          17,481    14,379 |-18% 
               /json    1.3.1        -        -      128          15,896    14,554 | -8% 
               /json    1.3.1        -        -      256          16,302    14,352 |-12% 

          /plaintext    1.3.1        -        -       32          14,142    13,836 | -2% 
          /plaintext    1.3.1        -        -       64          14,762    14,098 | -4% 
          /plaintext    1.3.1        -        -      128          16,071    13,669 |-15% 
          /plaintext    1.3.1        -        -      256          15,613    13,812 |-12% 

  /queries/{queries}    1.3.1      orm        5      256           1,675     1,606 | -4% 
  /queries/{queries}    1.3.1      orm       10      256             925       881 | -5% 
  /queries/{queries}    1.3.1      orm       20      256             481       464 | -4% 
  /queries/{queries}    1.3.1      raw        5      256           4,727     4,437 | -6% 
  /queries/{queries}    1.3.1      raw       10      256           3,407     3,091 | -9% 
  /queries/{queries}    1.3.1      raw       20      256           2,094     2,022 | -3% 

  /updates/{queries}    1.3.1      orm        5      256             871       830 | -5% 
  /updates/{queries}    1.3.1      orm       10      256             447       451 |  1% 
  /updates/{queries}    1.3.1      orm       20      256             226       229 |  2% 
  /updates/{queries}    1.3.1      raw        5      256           2,830     2,763 | -2% 
  /updates/{queries}    1.3.1      raw       10      256           1,754     1,724 | -2% 
  /updates/{queries}    1.3.1      raw       20      256             973     1,000 |  3% 

                 /db  2.0.0a0      orm        -       32           6,125     5,747 | -6% 
                 /db  2.0.0a0      orm        -       64           6,290     5,751 | -9% 
                 /db  2.0.0a0      orm        -      128           6,305     5,901 | -6% 
                 /db  2.0.0a0      orm        -      256           6,174     5,845 | -5% 
                 /db  2.0.0a0      raw        -       32           9,728     9,127 | -6% 
                 /db  2.0.0a0      raw        -       64          10,405     9,529 | -8% 
                 /db  2.0.0a0      raw        -      128          10,635     9,705 | -9% 
                 /db  2.0.0a0      raw        -      256          10,757    10,028 | -7% 

           /fortunes  2.0.0a0      orm        -       32           3,803     3,351 |-12% 
           /fortunes  2.0.0a0      orm        -       64           5,304     4,519 |-15% 
           /fortunes  2.0.0a0      orm        -      128           5,421     4,606 |-15% 
           /fortunes  2.0.0a0      orm        -      256           5,385     4,486 |-17% 
           /fortunes  2.0.0a0      raw        -       32           6,548     5,931 | -9% 
           /fortunes  2.0.0a0      raw        -       64           7,009     6,194 |-12% 
           /fortunes  2.0.0a0      raw        -      128           7,131     6,386 |-10% 
           /fortunes  2.0.0a0      raw        -      256           7,231     6,553 | -9% 

               /json  2.0.0a0        -        -       32          16,832    22,730 | 35% 
               /json  2.0.0a0        -        -       64          34,090    26,269 |-23% 
               /json  2.0.0a0        -        -      128          33,126    25,988 |-22% 
               /json  2.0.0a0        -        -      256          33,638    25,778 |-23% 

          /plaintext  2.0.0a0        -        -       32          30,872    24,245 |-21% 
          /plaintext  2.0.0a0        -        -       64          30,303    24,506 |-19% 
          /plaintext  2.0.0a0        -        -      128          30,337    23,282 |-23% 
          /plaintext  2.0.0a0        -        -      256          31,626    24,649 |-22% 

  /queries/{queries}  2.0.0a0      orm        5      256           1,853     1,684 | -9% 
  /queries/{queries}  2.0.0a0      orm       10      256             956       965 |  1% 
  /queries/{queries}  2.0.0a0      orm       20      256             497       486 | -2% 
  /queries/{queries}  2.0.0a0      raw        5      256           5,772     5,639 | -2% 
  /queries/{queries}  2.0.0a0      raw       10      256           3,695     3,571 | -3% 
  /queries/{queries}  2.0.0a0      raw       20      256           2,129     2,252 |  6% 

  /updates/{queries}  2.0.0a0      orm        5      256             876       858 | -2% 
  /updates/{queries}  2.0.0a0      orm       10      256             444       450 |  1% 
  /updates/{queries}  2.0.0a0      orm       20      256             236       198 |-16% 
  /updates/{queries}  2.0.0a0      raw        5      256           3,004     3,076 |  2% 
  /updates/{queries}  2.0.0a0      raw       10      256           1,724     1,869 |  8% 
  /updates/{queries}  2.0.0a0      raw       20      256           1,062     1,053 | -1% 
```
