# aiohttp benchmarks


## Usage

```shell
virtualenv -p `which python3.6` env
. env/bin/activate
pip install requests
```

**With vagrant:**

```shell
vagrant up
vagrant ssh -c /vagrant/remote-setup/setup.sh
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
ssh -i benchmarks.pem $SSH_ADDRESS "sudo ~/env35/bin/python server.py"
# now open $HTTP_ADDRESS/plaintext in your browser and check the server is working.

python run.py
python process.py
```

# Results 2017-09-10

(Run locally with vagrant)

```
               URL   python       DB  queries     Conc        2.0             2.2            2.3a 
             /json      3.6        -        -       32      6,808     5,907 |-13%     5,349 |-21% 
             /json      3.6        -        -       64      6,922     6,634 | -4%     6,299 | -9% 
             /json      3.6        -        -      128      5,941     5,904 | -1%     5,354 |-10% 
             /json      3.6        -        -      256      5,606     4,636 |-17%     5,013 |-11% 

        /plaintext      3.6        -        -       32      5,544     5,754 |  4%     6,081 | 10% 
        /plaintext      3.6        -        -       64      5,812     6,016 |  4%     6,384 | 10% 
        /plaintext      3.6        -        -      128      5,815     6,748 | 16%     5,506 | -5% 
        /plaintext      3.6        -        -      256      6,066     5,872 | -3%     5,476 |-10% 

           /{c}/db      3.6      orm        -       32      1,391     1,355 | -3%     1,267 | -9% 
           /{c}/db      3.6      orm        -       64      1,280     1,384 |  8%     1,197 | -6% 
           /{c}/db      3.6      orm        -      128      1,358     1,314 | -3%     1,223 |-10% 
           /{c}/db      3.6      orm        -      256      1,325     1,189 |-10%     1,177 |-11% 
           /{c}/db      3.6      raw        -       32      2,170     2,346 |  8%     2,446 | 13% 
           /{c}/db      3.6      raw        -       64      2,348     2,184 | -7%     2,456 |  5% 
           /{c}/db      3.6      raw        -      128      2,123     2,354 | 11%     2,136 |  1% 
           /{c}/db      3.6      raw        -      256      2,361     2,171 | -8%     2,209 | -6% 

     /{c}/fortunes      3.6      orm        -       32        789       572 |-28%       826 |  5% 
     /{c}/fortunes      3.6      orm        -       64        782       772 | -1%       796 |  2% 
     /{c}/fortunes      3.6      orm        -      128        780       769 | -1%       793 |  2% 
     /{c}/fortunes      3.6      orm        -      256        770       801 |  4%       766 | -1% 
     /{c}/fortunes      3.6      raw        -       32      1,024     1,102 |  8%     1,096 |  7% 
     /{c}/fortunes      3.6      raw        -       64      1,008     1,082 |  7%     1,040 |  3% 
     /{c}/fortunes      3.6      raw        -      128      1,016     1,049 |  3%     1,067 |  5% 
     /{c}/fortunes      3.6      raw        -      256        989     1,014 |  2%     1,074 |  9% 

  /{c}/queries/{q}      3.6      orm        5      256        398       382 | -4%       352 |-12% 
  /{c}/queries/{q}      3.6      orm       10      256        212       205 | -3%       177 |-17% 
  /{c}/queries/{q}      3.6      orm       20      256        105        96 | -9%        98 | -7% 
  /{c}/queries/{q}      3.6      raw        5      256      1,534     1,393 | -9%     1,477 | -4% 
  /{c}/queries/{q}      3.6      raw       10      256      1,249     1,171 | -6%     1,166 | -7% 
  /{c}/queries/{q}      3.6      raw       20      256        810       714 |-12%       741 | -9% 

  /{c}/updates/{q}      3.6      orm        5      256        212       229 |  8%       215 |  2% 
  /{c}/updates/{q}      3.6      orm       10      256        106       113 |  7%       113 |  6% 
  /{c}/updates/{q}      3.6      orm       20      256         58        53 |-10%        57 | -2% 
  /{c}/updates/{q}      3.6      raw        5      256        924       893 | -3%       979 |  6% 
  /{c}/updates/{q}      3.6      raw       10      256        649       598 | -8%       652 |  0% 
  /{c}/updates/{q}      3.6      raw       20      256        382       363 | -5%       389 |  2% 
```

# Old Results 2017-02-18

## Results - remote server

Tests were run between aws `t2.medium` in `eu-west` running the standard ubuntu 16.04 ami
and my desktop in London with a 20Mb up/down dedicated EFM line.

### Comparing aiohttp versions

```
               URL   python       DB  queries     Conc        1.2             1.3            2.0a 
             /json      3.5        -        -       32      2,112     2,118 |  0%     2,192 |  4% 
             /json      3.5        -        -       64      4,172     4,124 | -1%     4,341 |  4% 
             /json      3.5        -        -      128      5,425     6,087 | 12%     8,196 | 51% 
             /json      3.5        -        -      256      6,585     6,239 | -5%    10,050 | 53% 

        /plaintext      3.5        -        -       32      2,151     2,124 | -1%     2,186 |  2% 
        /plaintext      3.5        -        -       64      4,181     4,166 | -0%     4,326 |  3% 
        /plaintext      3.5        -        -      128      6,074     6,207 |  2%     8,464 | 39% 
        /plaintext      3.5        -        -      256      6,701     6,318 | -6%    10,966 | 64% 

           /{c}/db      3.5      orm        -       32      1,304     1,308 |  0%     1,303 | -0% 
           /{c}/db      3.5      orm        -       64      1,816     1,742 | -4%     1,897 |  4% 
           /{c}/db      3.5      orm        -      128      1,875     1,823 | -3%     2,449 | 31% 
           /{c}/db      3.5      orm        -      256      1,827     1,794 | -2%     2,254 | 23% 
           /{c}/db      3.5      raw        -       32      1,897     1,912 |  1%     2,017 |  6% 
           /{c}/db      3.5      raw        -       64      2,959     2,829 | -4%     3,350 | 13% 
           /{c}/db      3.5      raw        -      128      3,101     2,969 | -4%     4,237 | 37% 
           /{c}/db      3.5      raw        -      256      3,112     2,897 | -7%     4,034 | 30% 

     /{c}/fortunes      3.5      orm        -       32      1,543     1,416 | -8%     1,540 | -0% 
     /{c}/fortunes      3.5      orm        -       64      1,538     1,538 |  0%     1,537 | -0% 
     /{c}/fortunes      3.5      orm        -      128      1,527     1,491 | -2%     1,524 | -0% 
     /{c}/fortunes      3.5      orm        -      256      1,496     1,495 | -0%     1,503 |  0% 
     /{c}/fortunes      3.5      raw        -       32      1,530     1,541 |  1%     1,540 |  1% 
     /{c}/fortunes      3.5      raw        -       64      1,539     1,538 | -0%     1,538 | -0% 
     /{c}/fortunes      3.5      raw        -      128      1,528     1,526 | -0%     1,525 | -0% 
     /{c}/fortunes      3.5      raw        -      256      1,512     1,510 | -0%     1,514 |  0% 

  /{c}/queries/{q}      3.5      orm        5      256        610       608 | -0%       630 |  3% 
  /{c}/queries/{q}      3.5      orm       10      256        313       314 |  0%       324 |  4% 
  /{c}/queries/{q}      3.5      orm       20      256        156       157 |  1%       159 |  2% 
  /{c}/queries/{q}      3.5      raw        5      256      2,022     2,044 |  1%     2,441 | 21% 
  /{c}/queries/{q}      3.5      raw       10      256      1,470     1,459 | -1%     1,673 | 14% 
  /{c}/queries/{q}      3.5      raw       20      256        963       954 | -1%       973 |  1% 

  /{c}/updates/{q}      3.5      orm        5      256        306       300 | -2%       316 |  3% 
  /{c}/updates/{q}      3.5      orm       10      256        154       160 |  4%       162 |  6% 
  /{c}/updates/{q}      3.5      orm       20      256         76        80 |  5%        83 |  9% 
  /{c}/updates/{q}      3.5      raw        5      256      1,087     1,129 |  4%     1,057 | -3% 
  /{c}/updates/{q}      3.5      raw       10      256        660       620 | -6%       653 | -1% 
  /{c}/updates/{q}      3.5      raw       20      256        397       401 |  1%       376 | -5% 

             /json      3.6        -        -       32      2,143     2,123 | -1%     2,134 | -0% 
             /json      3.6        -        -       64      4,136     4,163 |  1%     4,295 |  4% 
             /json      3.6        -        -      128      6,308     5,901 | -6%     8,194 | 30% 
             /json      3.6        -        -      256      6,561     6,205 | -5%    10,066 | 53% 

        /plaintext      3.6        -        -       32      2,146     2,125 | -1%     2,164 |  1% 
        /plaintext      3.6        -        -       64      4,121     4,100 | -0%     4,335 |  5% 
        /plaintext      3.6        -        -      128      5,524     5,953 |  8%     8,226 | 49% 
        /plaintext      3.6        -        -      256      6,535     6,169 | -6%    10,945 | 67% 

           /{c}/db      3.6      orm        -       32      1,280     1,305 |  2%     1,282 |  0% 
           /{c}/db      3.6      orm        -       64      1,827     1,637 |-10%     1,886 |  3% 
           /{c}/db      3.6      orm        -      128      1,873     1,864 | -0%     2,485 | 33% 
           /{c}/db      3.6      orm        -      256      1,847     1,831 | -1%     2,272 | 23% 
           /{c}/db      3.6      raw        -       32      1,920     1,898 | -1%     2,005 |  4% 
           /{c}/db      3.6      raw        -       64      2,930     2,885 | -2%     3,338 | 14% 
           /{c}/db      3.6      raw        -      128      3,181     3,093 | -3%     4,185 | 32% 
           /{c}/db      3.6      raw        -      256      3,122     3,053 | -2%     4,160 | 33% 

     /{c}/fortunes      3.6      orm        -       32      1,541     1,336 |-13%     1,541 |  0% 
     /{c}/fortunes      3.6      orm        -       64      1,539     1,538 | -0%     1,534 | -0% 
     /{c}/fortunes      3.6      orm        -      128      1,521     1,496 | -2%     1,528 |  0% 
     /{c}/fortunes      3.6      orm        -      256      1,497     1,476 | -1%     1,506 |  1% 
     /{c}/fortunes      3.6      raw        -       32      1,542     1,541 | -0%     1,541 | -0% 
     /{c}/fortunes      3.6      raw        -       64      1,526     1,540 |  1%     1,536 |  1% 
     /{c}/fortunes      3.6      raw        -      128      1,525     1,507 | -1%     1,530 |  0% 
     /{c}/fortunes      3.6      raw        -      256      1,513     1,513 | -0%     1,511 | -0% 

  /{c}/queries/{q}      3.6      orm        5      256        614       611 | -1%       637 |  4% 
  /{c}/queries/{q}      3.6      orm       10      256        323       320 | -1%       329 |  2% 
  /{c}/queries/{q}      3.6      orm       20      256        158       159 |  0%       161 |  2% 
  /{c}/queries/{q}      3.6      raw        5      256      2,139     2,024 | -5%     2,542 | 19% 
  /{c}/queries/{q}      3.6      raw       10      256      1,496     1,480 | -1%     1,632 |  9% 
  /{c}/queries/{q}      3.6      raw       20      256        956       950 | -1%       929 | -3% 

  /{c}/updates/{q}      3.6      orm        5      256        297       311 |  5%       305 |  3% 
  /{c}/updates/{q}      3.6      orm       10      256        155       159 |  2%       164 |  6% 
  /{c}/updates/{q}      3.6      orm       20      256         80        79 | -1%        82 |  2% 
  /{c}/updates/{q}      3.6      raw        5      256      1,060     1,128 |  6%     1,030 | -3% 
  /{c}/updates/{q}      3.6      raw       10      256        581       646 | 11%       697 | 20% 
  /{c}/updates/{q}      3.6      raw       20      256        390       393 |  1%       395 |  1% 
```

### Comparing python versions

```
               URL  aiohttp       DB  queries     Conc        3.5             3.6 
             /json      1.2        -        -       32      2,112     2,143 |  1% 
             /json      1.2        -        -       64      4,172     4,136 | -1% 
             /json      1.2        -        -      128      5,425     6,308 | 16% 
             /json      1.2        -        -      256      6,585     6,561 | -0% 

        /plaintext      1.2        -        -       32      2,151     2,146 | -0% 
        /plaintext      1.2        -        -       64      4,181     4,121 | -1% 
        /plaintext      1.2        -        -      128      6,074     5,524 | -9% 
        /plaintext      1.2        -        -      256      6,701     6,535 | -2% 

           /{c}/db      1.2      orm        -       32      1,304     1,280 | -2% 
           /{c}/db      1.2      orm        -       64      1,816     1,827 |  1% 
           /{c}/db      1.2      orm        -      128      1,875     1,873 | -0% 
           /{c}/db      1.2      orm        -      256      1,827     1,847 |  1% 
           /{c}/db      1.2      raw        -       32      1,897     1,920 |  1% 
           /{c}/db      1.2      raw        -       64      2,959     2,930 | -1% 
           /{c}/db      1.2      raw        -      128      3,101     3,181 |  3% 
           /{c}/db      1.2      raw        -      256      3,112     3,122 |  0% 

     /{c}/fortunes      1.2      orm        -       32      1,543     1,541 | -0% 
     /{c}/fortunes      1.2      orm        -       64      1,538     1,539 |  0% 
     /{c}/fortunes      1.2      orm        -      128      1,527     1,521 | -0% 
     /{c}/fortunes      1.2      orm        -      256      1,496     1,497 |  0% 
     /{c}/fortunes      1.2      raw        -       32      1,530     1,542 |  1% 
     /{c}/fortunes      1.2      raw        -       64      1,539     1,526 | -1% 
     /{c}/fortunes      1.2      raw        -      128      1,528     1,525 | -0% 
     /{c}/fortunes      1.2      raw        -      256      1,512     1,513 |  0% 

  /{c}/queries/{q}      1.2      orm        5      256        610       614 |  1% 
  /{c}/queries/{q}      1.2      orm       10      256        313       323 |  3% 
  /{c}/queries/{q}      1.2      orm       20      256        156       158 |  2% 
  /{c}/queries/{q}      1.2      raw        5      256      2,022     2,139 |  6% 
  /{c}/queries/{q}      1.2      raw       10      256      1,470     1,496 |  2% 
  /{c}/queries/{q}      1.2      raw       20      256        963       956 | -1% 

  /{c}/updates/{q}      1.2      orm        5      256        306       297 | -3% 
  /{c}/updates/{q}      1.2      orm       10      256        154       155 |  1% 
  /{c}/updates/{q}      1.2      orm       20      256         76        80 |  6% 
  /{c}/updates/{q}      1.2      raw        5      256      1,087     1,060 | -3% 
  /{c}/updates/{q}      1.2      raw       10      256        660       581 |-12% 
  /{c}/updates/{q}      1.2      raw       20      256        397       390 | -2% 

             /json      1.3        -        -       32      2,118     2,123 |  0% 
             /json      1.3        -        -       64      4,124     4,163 |  1% 
             /json      1.3        -        -      128      6,087     5,901 | -3% 
             /json      1.3        -        -      256      6,239     6,205 | -1% 

        /plaintext      1.3        -        -       32      2,124     2,125 |  0% 
        /plaintext      1.3        -        -       64      4,166     4,100 | -2% 
        /plaintext      1.3        -        -      128      6,207     5,953 | -4% 
        /plaintext      1.3        -        -      256      6,318     6,169 | -2% 

           /{c}/db      1.3      orm        -       32      1,308     1,305 | -0% 
           /{c}/db      1.3      orm        -       64      1,742     1,637 | -6% 
           /{c}/db      1.3      orm        -      128      1,823     1,864 |  2% 
           /{c}/db      1.3      orm        -      256      1,794     1,831 |  2% 
           /{c}/db      1.3      raw        -       32      1,912     1,898 | -1% 
           /{c}/db      1.3      raw        -       64      2,829     2,885 |  2% 
           /{c}/db      1.3      raw        -      128      2,969     3,093 |  4% 
           /{c}/db      1.3      raw        -      256      2,897     3,053 |  5% 

     /{c}/fortunes      1.3      orm        -       32      1,416     1,336 | -6% 
     /{c}/fortunes      1.3      orm        -       64      1,538     1,538 | -0% 
     /{c}/fortunes      1.3      orm        -      128      1,491     1,496 |  0% 
     /{c}/fortunes      1.3      orm        -      256      1,495     1,476 | -1% 
     /{c}/fortunes      1.3      raw        -       32      1,541     1,541 | -0% 
     /{c}/fortunes      1.3      raw        -       64      1,538     1,540 |  0% 
     /{c}/fortunes      1.3      raw        -      128      1,526     1,507 | -1% 
     /{c}/fortunes      1.3      raw        -      256      1,510     1,513 |  0% 

  /{c}/queries/{q}      1.3      orm        5      256        608       611 |  1% 
  /{c}/queries/{q}      1.3      orm       10      256        314       320 |  2% 
  /{c}/queries/{q}      1.3      orm       20      256        157       159 |  1% 
  /{c}/queries/{q}      1.3      raw        5      256      2,044     2,024 | -1% 
  /{c}/queries/{q}      1.3      raw       10      256      1,459     1,480 |  1% 
  /{c}/queries/{q}      1.3      raw       20      256        954       950 | -0% 

  /{c}/updates/{q}      1.3      orm        5      256        300       311 |  3% 
  /{c}/updates/{q}      1.3      orm       10      256        160       159 | -1% 
  /{c}/updates/{q}      1.3      orm       20      256         80        79 | -1% 
  /{c}/updates/{q}      1.3      raw        5      256      1,129     1,128 | -0% 
  /{c}/updates/{q}      1.3      raw       10      256        620       646 |  4% 
  /{c}/updates/{q}      1.3      raw       20      256        401       393 | -2% 

             /json     2.0a        -        -       32      2,192     2,134 | -3% 
             /json     2.0a        -        -       64      4,341     4,295 | -1% 
             /json     2.0a        -        -      128      8,196     8,194 | -0% 
             /json     2.0a        -        -      256     10,050    10,066 |  0% 

        /plaintext     2.0a        -        -       32      2,186     2,164 | -1% 
        /plaintext     2.0a        -        -       64      4,326     4,335 |  0% 
        /plaintext     2.0a        -        -      128      8,464     8,226 | -3% 
        /plaintext     2.0a        -        -      256     10,966    10,945 | -0% 

           /{c}/db     2.0a      orm        -       32      1,303     1,282 | -2% 
           /{c}/db     2.0a      orm        -       64      1,897     1,886 | -1% 
           /{c}/db     2.0a      orm        -      128      2,449     2,485 |  1% 
           /{c}/db     2.0a      orm        -      256      2,254     2,272 |  1% 
           /{c}/db     2.0a      raw        -       32      2,017     2,005 | -1% 
           /{c}/db     2.0a      raw        -       64      3,350     3,338 | -0% 
           /{c}/db     2.0a      raw        -      128      4,237     4,185 | -1% 
           /{c}/db     2.0a      raw        -      256      4,034     4,160 |  3% 

     /{c}/fortunes     2.0a      orm        -       32      1,540     1,541 |  0% 
     /{c}/fortunes     2.0a      orm        -       64      1,537     1,534 | -0% 
     /{c}/fortunes     2.0a      orm        -      128      1,524     1,528 |  0% 
     /{c}/fortunes     2.0a      orm        -      256      1,503     1,506 |  0% 
     /{c}/fortunes     2.0a      raw        -       32      1,540     1,541 |  0% 
     /{c}/fortunes     2.0a      raw        -       64      1,538     1,536 | -0% 
     /{c}/fortunes     2.0a      raw        -      128      1,525     1,530 |  0% 
     /{c}/fortunes     2.0a      raw        -      256      1,514     1,511 | -0% 

  /{c}/queries/{q}     2.0a      orm        5      256        630       637 |  1% 
  /{c}/queries/{q}     2.0a      orm       10      256        324       329 |  1% 
  /{c}/queries/{q}     2.0a      orm       20      256        159       161 |  1% 
  /{c}/queries/{q}     2.0a      raw        5      256      2,441     2,542 |  4% 
  /{c}/queries/{q}     2.0a      raw       10      256      1,673     1,632 | -2% 
  /{c}/queries/{q}     2.0a      raw       20      256        973       929 | -5% 

  /{c}/updates/{q}     2.0a      orm        5      256        316       305 | -3% 
  /{c}/updates/{q}     2.0a      orm       10      256        162       164 |  1% 
  /{c}/updates/{q}     2.0a      orm       20      256         83        82 | -1% 
  /{c}/updates/{q}     2.0a      raw        5      256      1,057     1,030 | -3% 
  /{c}/updates/{q}     2.0a      raw       10      256        653       697 |  7% 
  /{c}/updates/{q}     2.0a      raw       20      256        376       395 |  5% 
```

## Results - local server

### Comparing aiohttp versions

```
               URL   python       DB  queries     Conc       1.2.0           1.3.1         2.0.0a0 
               /db      3.5      orm        -       32       5,309     5,005 | -6%     6,125 | 15% 
               /db      3.5      orm        -       64       5,417     5,133 | -5%     6,290 | 16% 
               /db      3.5      orm        -      128       5,445     5,272 | -3%     6,305 | 16% 
               /db      3.5      orm        -      256       5,584     5,387 | -4%     6,174 | 11% 
               /db      3.5      raw        -       32       7,080     7,372 |  4%     9,728 | 37% 
               /db      3.5      raw        -       64       7,617     7,486 | -2%    10,405 | 37% 
               /db      3.5      raw        -      128       8,126     7,827 | -4%    10,635 | 31% 
               /db      3.5      raw        -      256       8,043     7,933 | -1%    10,757 | 34% 

         /fortunes      3.5      orm        -       32       3,925     3,808 | -3%     3,803 | -3% 
         /fortunes      3.5      orm        -       64       4,390     4,283 | -2%     5,304 | 21% 
         /fortunes      3.5      orm        -      128       4,570     4,405 | -4%     5,421 | 19% 
         /fortunes      3.5      orm        -      256       4,589     4,514 | -2%     5,385 | 17% 
         /fortunes      3.5      raw        -       32       5,394     5,347 | -1%     6,548 | 21% 
         /fortunes      3.5      raw        -       64       5,914     5,593 | -5%     7,009 | 19% 
         /fortunes      3.5      raw        -      128       6,140     5,936 | -3%     7,131 | 16% 
         /fortunes      3.5      raw        -      256       6,207     6,076 | -2%     7,231 | 16% 

             /json      3.5        -        -       32      12,232    11,614 | -5%    16,832 | 38% 
             /json      3.5        -        -       64      17,214    17,481 |  2%    34,090 | 98% 
             /json      3.5        -        -      128      17,793    15,896 |-11%    33,126 | 86% 
             /json      3.5        -        -      256      18,839    16,302 |-13%    33,638 | 79% 

        /plaintext      3.5        -        -       32      17,574    14,142 |-20%    30,872 | 76% 
        /plaintext      3.5        -        -       64      17,208    14,762 |-14%    30,303 | 76% 
        /plaintext      3.5        -        -      128      17,866    16,071 |-10%    30,337 | 70% 
        /plaintext      3.5        -        -      256      17,130    15,613 | -9%    31,626 | 85% 

/queries/{queries}      3.5      orm        5      256       1,767     1,675 | -5%     1,853 |  5% 
/queries/{queries}      3.5      orm       10      256         936       925 | -1%       956 |  2% 
/queries/{queries}      3.5      orm       20      256         489       481 | -2%       497 |  2% 
/queries/{queries}      3.5      raw        5      256       4,893     4,727 | -3%     5,772 | 18% 
/queries/{queries}      3.5      raw       10      256       3,422     3,407 | -0%     3,695 |  8% 
/queries/{queries}      3.5      raw       20      256       2,138     2,094 | -2%     2,129 | -0% 

/updates/{queries}      3.5      orm        5      256         864       871 |  1%       876 |  1% 
/updates/{queries}      3.5      orm       10      256         413       447 |  8%       444 |  7% 
/updates/{queries}      3.5      orm       20      256         214       226 |  5%       236 | 10% 
/updates/{queries}      3.5      raw        5      256       2,932     2,830 | -3%     3,004 |  2% 
/updates/{queries}      3.5      raw       10      256       1,826     1,754 | -4%     1,724 | -6% 
/updates/{queries}      3.5      raw       20      256       1,000       973 | -3%     1,062 |  6% 

               /db      3.6      orm        -       32       4,934     4,579 | -7%     5,747 | 16% 
               /db      3.6      orm        -       64       5,087     4,610 | -9%     5,751 | 13% 
               /db      3.6      orm        -      128       5,127     4,813 | -6%     5,901 | 15% 
               /db      3.6      orm        -      256       5,274     4,614 |-13%     5,845 | 11% 
               /db      3.6      raw        -       32       7,149     6,633 | -7%     9,127 | 28% 
               /db      3.6      raw        -       64       7,135     7,081 | -1%     9,529 | 34% 
               /db      3.6      raw        -      128       7,458     7,057 | -5%     9,705 | 30% 
               /db      3.6      raw        -      256       7,497     7,042 | -6%    10,028 | 34% 

         /fortunes      3.6      orm        -       32       3,466     2,004 |-42%     3,351 | -3% 
         /fortunes      3.6      orm        -       64       3,927     3,781 | -4%     4,519 | 15% 
         /fortunes      3.6      orm        -      128       3,863     3,879 |  0%     4,606 | 19% 
         /fortunes      3.6      orm        -      256       4,036     4,042 |  0%     4,486 | 11% 
         /fortunes      3.6      raw        -       32       4,930     4,602 | -7%     5,931 | 20% 
         /fortunes      3.6      raw        -       64       4,984     4,927 | -1%     6,194 | 24% 
         /fortunes      3.6      raw        -      128       5,263     5,198 | -1%     6,386 | 21% 
         /fortunes      3.6      raw        -      256       5,423     5,346 | -1%     6,553 | 21% 

             /json      3.6        -        -       32      11,933     6,674 |-44%    22,730 | 90% 
             /json      3.6        -        -       64      14,983    14,379 | -4%    26,269 | 75% 
             /json      3.6        -        -      128      15,759    14,554 | -8%    25,988 | 65% 
             /json      3.6        -        -      256      15,933    14,352 |-10%    25,778 | 62% 

        /plaintext      3.6        -        -       32      12,334    13,836 | 12%    24,245 | 97% 
        /plaintext      3.6        -        -       64      14,767    14,098 | -5%    24,506 | 66% 
        /plaintext      3.6        -        -      128      15,293    13,669 |-11%    23,282 | 52% 
        /plaintext      3.6        -        -      256      14,769    13,812 | -6%    24,649 | 67% 

/queries/{queries}      3.6      orm        5      256       1,638     1,606 | -2%     1,684 |  3% 
/queries/{queries}      3.6      orm       10      256         827       881 |  7%       965 | 17% 
/queries/{queries}      3.6      orm       20      256         436       464 |  6%       486 | 11% 
/queries/{queries}      3.6      raw        5      256       4,503     4,437 | -1%     5,639 | 25% 
/queries/{queries}      3.6      raw       10      256       3,229     3,091 | -4%     3,571 | 11% 
/queries/{queries}      3.6      raw       20      256       2,009     2,022 |  1%     2,252 | 12% 

/updates/{queries}      3.6      orm        5      256         829       830 |  0%       858 |  3% 
/updates/{queries}      3.6      orm       10      256         405       451 | 11%       450 | 11% 
/updates/{queries}      3.6      orm       20      256         223       229 |  3%       198 |-11% 
/updates/{queries}      3.6      raw        5      256       2,800     2,763 | -1%     3,076 | 10% 
/updates/{queries}      3.6      raw       10      256       1,744     1,724 | -1%     1,869 |  7% 
/updates/{queries}      3.6      raw       20      256         959     1,000 |  4%     1,053 | 10%
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
