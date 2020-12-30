# aiohttp benchmarks


## Usage

```shell
virtualenv -p `which python3` env
. env/bin/activate
pip install requests
```

**With vagrant:**

```shell
vagrant up
python run.py
python process.py
```

**With a remote machine:**

(this assumes you have a pem file `benchmarks.pem` for connecting to the remote host in the current directory.)

```shell
export REMOTE=true
export SSH_ADDRESS="<user>@<host>"
export HTTP_ADDRESS="http://<host>"
scp -i benchmarks.pem -r app $SSH_ADDRESS:
scp -i benchmarks.pem -r remote-setup $SSH_ADDRESS:
ssh -i benchmarks.pem $SSH_ADDRESS remote-setup/setup.sh

# everything should now be setup, you can run the server
ssh -i benchmarks.pem $SSH_ADDRESS "sudo ~/env38/bin/python server.py"
# now open $HTTP_ADDRESS/plaintext in your browser and check the server is working.

python run.py
python process.py
```

# Results 2020-12-27 - remote server

Tests were run between two aws `t2.medium` in `eu-west` running the standard ubuntu 20.04 ami.  
Performance is measured in RPC (requests per second). So **the higher** the number the better.

### Comparing aiohttp versions

```
               URL   python       DB  queries     Conc        3.6             3.7
             /json      3.7        -        -       32      7,140     6,723 | -6%
             /json      3.7        -        -       64      7,143     7,335 |  3%
             /json      3.7        -        -      128      7,565     5,894 |-22%
             /json      3.7        -        -      256      6,938     6,538 | -6%

        /plaintext      3.7        -        -       32      7,056     6,714 | -5%
        /plaintext      3.7        -        -       64      6,938     6,848 | -1%
        /plaintext      3.7        -        -      128      6,398     5,996 | -6%
        /plaintext      3.7        -        -      256      6,975     6,425 | -8%

           /{c}/db      3.7      orm        -       32      1,148     1,123 | -2%
           /{c}/db      3.7      orm        -       64      1,103     1,150 |  4%
           /{c}/db      3.7      orm        -      128      1,095     1,145 |  5%
           /{c}/db      3.7      orm        -      256      1,067     1,096 |  3%
           /{c}/db      3.7      raw        -       32      2,460     2,407 | -2%
           /{c}/db      3.7      raw        -       64      2,339     2,310 | -1%
           /{c}/db      3.7      raw        -      128      2,494     2,300 | -8%
           /{c}/db      3.7      raw        -      256      2,318     2,298 | -1%

     /{c}/fortunes      3.7      orm        -       32        885       899 |  2%
     /{c}/fortunes      3.7      orm        -       64        893       862 | -4%
     /{c}/fortunes      3.7      orm        -      128        866       891 |  3%
     /{c}/fortunes      3.7      orm        -      256        864       837 | -3%
     /{c}/fortunes      3.7      raw        -       32      1,588     1,582 | -0%
     /{c}/fortunes      3.7      raw        -       64      1,559     1,549 | -1%
     /{c}/fortunes      3.7      raw        -      128      1,543     1,525 | -1%
     /{c}/fortunes      3.7      raw        -      256      1,474     1,555 |  5%

  /{c}/queries/{q}      3.7      orm        5      256        330       330 | -0%
  /{c}/queries/{q}      3.7      orm       10      256        170       169 | -1%
  /{c}/queries/{q}      3.7      orm       20      256         85        82 | -3%
  /{c}/queries/{q}      3.7      raw        5      256      1,091     1,090 | -0%
  /{c}/queries/{q}      3.7      raw       10      256        815       876 |  8%
  /{c}/queries/{q}      3.7      raw       20      256        571       611 |  7%

  /{c}/updates/{q}      3.7      orm        5      256        168       164 | -2%
  /{c}/updates/{q}      3.7      orm       10      256         96        83 |-13%
  /{c}/updates/{q}      3.7      orm       20      256         49        50 |  1%
  /{c}/updates/{q}      3.7      raw        5      256        724       779 |  7%
  /{c}/updates/{q}      3.7      raw       10      256        478       493 |  3%
  /{c}/updates/{q}      3.7      raw       20      256        277       312 | 13%

             /json      3.8        -        -       32      8,558     7,199 |-16%
             /json      3.8        -        -       64      9,278     8,626 | -7%
             /json      3.8        -        -      128      8,045     7,310 | -9%
             /json      3.8        -        -      256      8,511     7,472 |-12%

        /plaintext      3.8        -        -       32      7,306     7,151 | -2%
        /plaintext      3.8        -        -       64      7,840     9,219 | 18%
        /plaintext      3.8        -        -      128      8,649     9,536 | 10%
        /plaintext      3.8        -        -      256      8,820     8,795 | -0%

           /{c}/db      3.8      orm        -       32      1,279     1,360 |  6%
           /{c}/db      3.8      orm        -       64      1,288     1,283 | -0%
           /{c}/db      3.8      orm        -      128      1,232     1,240 |  1%
           /{c}/db      3.8      orm        -      256      1,217     1,267 |  4%
           /{c}/db      3.8      raw        -       32      2,777     2,781 |  0%
           /{c}/db      3.8      raw        -       64      2,600     2,668 |  3%
           /{c}/db      3.8      raw        -      128      2,645     2,751 |  4%
           /{c}/db      3.8      raw        -      256      2,516     2,565 |  2%

     /{c}/fortunes      3.8      orm        -       32      1,047     1,051 |  0%
     /{c}/fortunes      3.8      orm        -       64      1,025       985 | -4%
     /{c}/fortunes      3.8      orm        -      128        969     1,010 |  4%
     /{c}/fortunes      3.8      orm        -      256        974     1,015 |  4%
     /{c}/fortunes      3.8      raw        -       32      1,781     1,759 | -1%
     /{c}/fortunes      3.8      raw        -       64      1,637     1,714 |  5%
     /{c}/fortunes      3.8      raw        -      128      1,688     1,771 |  5%
     /{c}/fortunes      3.8      raw        -      256      1,677     1,647 | -2%

  /{c}/queries/{q}      3.8      orm        5      256        401       407 |  1%
  /{c}/queries/{q}      3.8      orm       10      256        205       198 | -3%
  /{c}/queries/{q}      3.8      orm       20      256         98       101 |  2%
  /{c}/queries/{q}      3.8      raw        5      256      1,110     1,191 |  7%
  /{c}/queries/{q}      3.8      raw       10      256        844       847 |  0%
  /{c}/queries/{q}      3.8      raw       20      256        593       596 |  0%

  /{c}/updates/{q}      3.8      orm        5      256        194       201 |  4%
  /{c}/updates/{q}      3.8      orm       10      256        100       102 |  3%
  /{c}/updates/{q}      3.8      orm       20      256         55        58 |  4%
  /{c}/updates/{q}      3.8      raw        5      256        786       777 | -1%
  /{c}/updates/{q}      3.8      raw       10      256        521       523 |  0%
  /{c}/updates/{q}      3.8      raw       20      256        314       314 |  0%

             /json      3.9        -        -       32      8,616     7,951 | -8%
             /json      3.9        -        -       64      8,466     9,366 | 11%
             /json      3.9        -        -      128      9,670     7,642 |-21%
             /json      3.9        -        -      256      7,685     8,055 |  5%

        /plaintext      3.9        -        -       32      9,365     7,795 |-17%
        /plaintext      3.9        -        -       64     10,148     8,799 |-13%
        /plaintext      3.9        -        -      128     10,091     7,654 |-24%
        /plaintext      3.9        -        -      256      8,263     7,007 |-15%

           /{c}/db      3.9      orm        -       32      1,311     1,348 |  3%
           /{c}/db      3.9      orm        -       64      1,315     1,263 | -4%
           /{c}/db      3.9      orm        -      128      1,236     1,312 |  6%
           /{c}/db      3.9      orm        -      256      1,297     1,291 | -0%
           /{c}/db      3.9      raw        -       32      2,799     2,667 | -5%
           /{c}/db      3.9      raw        -       64      2,713     2,594 | -4%
           /{c}/db      3.9      raw        -      128      2,530     2,491 | -2%
           /{c}/db      3.9      raw        -      256      2,573     2,505 | -3%

     /{c}/fortunes      3.9      orm        -       32        995     1,014 |  2%
     /{c}/fortunes      3.9      orm        -       64      1,016     1,014 | -0%
     /{c}/fortunes      3.9      orm        -      128      1,035     1,032 | -0%
     /{c}/fortunes      3.9      orm        -      256      1,007       995 | -1%
     /{c}/fortunes      3.9      raw        -       32      1,727     1,766 |  2%
     /{c}/fortunes      3.9      raw        -       64      1,672     1,669 | -0%
     /{c}/fortunes      3.9      raw        -      128      1,619     1,630 |  1%
     /{c}/fortunes      3.9      raw        -      256      1,581     1,676 |  6%

  /{c}/queries/{q}      3.9      orm        5      256        393       382 | -3%
  /{c}/queries/{q}      3.9      orm       10      256        194       193 | -1%
  /{c}/queries/{q}      3.9      orm       20      256         96        99 |  2%
  /{c}/queries/{q}      3.9      raw        5      256      1,102     1,098 | -0%
  /{c}/queries/{q}      3.9      raw       10      256        871       872 |  0%
  /{c}/queries/{q}      3.9      raw       20      256        572       593 |  4%

  /{c}/updates/{q}      3.9      orm        5      256        214       201 | -6%
  /{c}/updates/{q}      3.9      orm       10      256        104       102 | -3%
  /{c}/updates/{q}      3.9      orm       20      256         58        57 | -0%
  /{c}/updates/{q}      3.9      raw        5      256        744       789 |  6%
  /{c}/updates/{q}      3.9      raw       10      256        497       519 |  4%
  /{c}/updates/{q}      3.9      raw       20      256        306       305 | -0%
```

### Comparing python versions

```
               URL  aiohttp       DB  queries     Conc        3.7             3.8             3.9
             /json      3.6        -        -       32      7,140     8,558 | 20%     8,616 | 21%
             /json      3.6        -        -       64      7,143     9,278 | 30%     8,466 | 19%
             /json      3.6        -        -      128      7,565     8,045 |  6%     9,670 | 28%
             /json      3.6        -        -      256      6,938     8,511 | 23%     7,685 | 11%

        /plaintext      3.6        -        -       32      7,056     7,306 |  4%     9,365 | 33%
        /plaintext      3.6        -        -       64      6,938     7,840 | 13%    10,148 | 46%
        /plaintext      3.6        -        -      128      6,398     8,649 | 35%    10,091 | 58%
        /plaintext      3.6        -        -      256      6,975     8,820 | 26%     8,263 | 18%

           /{c}/db      3.6      orm        -       32      1,148     1,279 | 11%     1,311 | 14%
           /{c}/db      3.6      orm        -       64      1,103     1,288 | 17%     1,315 | 19%
           /{c}/db      3.6      orm        -      128      1,095     1,232 | 13%     1,236 | 13%
           /{c}/db      3.6      orm        -      256      1,067     1,217 | 14%     1,297 | 22%
           /{c}/db      3.6      raw        -       32      2,460     2,777 | 13%     2,799 | 14%
           /{c}/db      3.6      raw        -       64      2,339     2,600 | 11%     2,713 | 16%
           /{c}/db      3.6      raw        -      128      2,494     2,645 |  6%     2,530 |  1%
           /{c}/db      3.6      raw        -      256      2,318     2,516 |  9%     2,573 | 11%

     /{c}/fortunes      3.6      orm        -       32        885     1,047 | 18%       995 | 12%
     /{c}/fortunes      3.6      orm        -       64        893     1,025 | 15%     1,016 | 14%
     /{c}/fortunes      3.6      orm        -      128        866       969 | 12%     1,035 | 20%
     /{c}/fortunes      3.6      orm        -      256        864       974 | 13%     1,007 | 17%
     /{c}/fortunes      3.6      raw        -       32      1,588     1,781 | 12%     1,727 |  9%
     /{c}/fortunes      3.6      raw        -       64      1,559     1,637 |  5%     1,672 |  7%
     /{c}/fortunes      3.6      raw        -      128      1,543     1,688 |  9%     1,619 |  5%
     /{c}/fortunes      3.6      raw        -      256      1,474     1,677 | 14%     1,581 |  7%

  /{c}/queries/{q}      3.6      orm        5      256        330       401 | 21%       393 | 19%
  /{c}/queries/{q}      3.6      orm       10      256        170       205 | 20%       194 | 14%
  /{c}/queries/{q}      3.6      orm       20      256         85        98 | 16%        96 | 13%
  /{c}/queries/{q}      3.6      raw        5      256      1,091     1,110 |  2%     1,102 |  1%
  /{c}/queries/{q}      3.6      raw       10      256        815       844 |  4%       871 |  7%
  /{c}/queries/{q}      3.6      raw       20      256        571       593 |  4%       572 |  0%

  /{c}/updates/{q}      3.6      orm        5      256        168       194 | 16%       214 | 28%
  /{c}/updates/{q}      3.6      orm       10      256         96       100 |  4%       104 |  9%
  /{c}/updates/{q}      3.6      orm       20      256         49        55 | 13%        58 | 17%
  /{c}/updates/{q}      3.6      raw        5      256        724       786 |  8%       744 |  3%
  /{c}/updates/{q}      3.6      raw       10      256        478       521 |  9%       497 |  4%
  /{c}/updates/{q}      3.6      raw       20      256        277       314 | 13%       306 | 10%

             /json      3.7        -        -       32      6,723     7,199 |  7%     7,951 | 18%
             /json      3.7        -        -       64      7,335     8,626 | 18%     9,366 | 28%
             /json      3.7        -        -      128      5,894     7,310 | 24%     7,642 | 30%
             /json      3.7        -        -      256      6,538     7,472 | 14%     8,055 | 23%

        /plaintext      3.7        -        -       32      6,714     7,151 |  7%     7,795 | 16%
        /plaintext      3.7        -        -       64      6,848     9,219 | 35%     8,799 | 28%
        /plaintext      3.7        -        -      128      5,996     9,536 | 59%     7,654 | 28%
        /plaintext      3.7        -        -      256      6,425     8,795 | 37%     7,007 |  9%

           /{c}/db      3.7      orm        -       32      1,123     1,360 | 21%     1,348 | 20%
           /{c}/db      3.7      orm        -       64      1,150     1,283 | 12%     1,263 | 10%
           /{c}/db      3.7      orm        -      128      1,145     1,240 |  8%     1,312 | 15%
           /{c}/db      3.7      orm        -      256      1,096     1,267 | 16%     1,291 | 18%
           /{c}/db      3.7      raw        -       32      2,407     2,781 | 16%     2,667 | 11%
           /{c}/db      3.7      raw        -       64      2,310     2,668 | 15%     2,594 | 12%
           /{c}/db      3.7      raw        -      128      2,300     2,751 | 20%     2,491 |  8%
           /{c}/db      3.7      raw        -      256      2,298     2,565 | 12%     2,505 |  9%

     /{c}/fortunes      3.7      orm        -       32        899     1,051 | 17%     1,014 | 13%
     /{c}/fortunes      3.7      orm        -       64        862       985 | 14%     1,014 | 18%
     /{c}/fortunes      3.7      orm        -      128        891     1,010 | 13%     1,032 | 16%
     /{c}/fortunes      3.7      orm        -      256        837     1,015 | 21%       995 | 19%
     /{c}/fortunes      3.7      raw        -       32      1,582     1,759 | 11%     1,766 | 12%
     /{c}/fortunes      3.7      raw        -       64      1,549     1,714 | 11%     1,669 |  8%
     /{c}/fortunes      3.7      raw        -      128      1,525     1,771 | 16%     1,630 |  7%
     /{c}/fortunes      3.7      raw        -      256      1,555     1,647 |  6%     1,676 |  8%

  /{c}/queries/{q}      3.7      orm        5      256        330       407 | 23%       382 | 16%
  /{c}/queries/{q}      3.7      orm       10      256        169       198 | 17%       193 | 14%
  /{c}/queries/{q}      3.7      orm       20      256         82       101 | 22%        99 | 20%
  /{c}/queries/{q}      3.7      raw        5      256      1,090     1,191 |  9%     1,098 |  1%
  /{c}/queries/{q}      3.7      raw       10      256        876       847 | -3%       872 | -0%
  /{c}/queries/{q}      3.7      raw       20      256        611       596 | -2%       593 | -3%

  /{c}/updates/{q}      3.7      orm        5      256        164       201 | 23%       201 | 23%
  /{c}/updates/{q}      3.7      orm       10      256         83       102 | 23%       102 | 22%
  /{c}/updates/{q}      3.7      orm       20      256         50        58 | 16%        57 | 16%
  /{c}/updates/{q}      3.7      raw        5      256        779       777 | -0%       789 |  1%
  /{c}/updates/{q}      3.7      raw       10      256        493       523 |  6%       519 |  5%
  /{c}/updates/{q}      3.7      raw       20      256        312       314 |  1%       305 | -2%
```
