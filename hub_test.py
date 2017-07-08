import fixer_exchange.exchangerate as exchangerate
from okcoin.Client import OkCoin
from kraken.test0 import kraken
from poloniex.poloniex_test import poloniex
import time as time
import datetime,pickle,os.path as path

CODES = ['BTC_USD', 'LTC_USD', 'ETH_USD', 'BTC_CNY', 'LTC_CNY', 'ETH_BTC']
TIME_FORMAT="%y%m%d-%H:%M:%S"

class datapoint:
    #deprecated
    '''    def __init__(self,p,k,okcom,okcn,ex,dif,nt={},dt=time.strftime(TIME_FORMAT)):
        self.codes=CODES
        self.polo=p
        self.krak=k
        self.ok_com=okcom
        self.ok_cn=okcn
        self.ex=ex
        self.notes=nt
        self.datatime=dt
        self.differences=dif
    '''

    def __init__(self,markts,ex,ods,nt={},dt=time.strftime(TIME_FORMAT)):
        self.markets=markts
        self.ex=ex
        self.notes=nt
        self.datatime=dt
        self.odds=ods
'''
get the currency code index, that a is significantly higher than b
'''
def a_above_b(m1,m2):
    ratio=[0]*len(m1)
    total_ratio=1
    for i in range(len(m1)):
        if m1[i] is None or m2[i] is None: continue
        if m1[i]['buy']>m2[i]['sell']*1.03:
            ratio[i]=m1[i]['buy']/m2[i]['sell']
            total_ratio=total_ratio*ratio[i]
    return ratio,total_ratio


def one_round(p,k,ok,ex):
    cpolo=[p.get_BTCUSD(),p.get_LTCUSD(),p.get_ETHUSD(),None,None,None]
    ckrak=[k.get_BTCUSD(),k.get_LTCUSD(),k.get_ETHUSD(),None,None,k.get_ETHBTC()]
    cok_com=[ok.get_OKCOINCOM_BTCUSD(),ok.get_OKCOINCOM_LTCUSD(),None,None,None,None]
    cok_cn=[None,None,None,ok.get_OKCOINCN_BTCCNY(),ok.get_OKCOINCN_LTCCNY(),None]
    ex={"usd2cny":exchangerate.get_USD2CNY(),'cny2usd':exchangerate.get_CNY2USD()}
    cok_cn[0]={'buy':cok_cn[3]['buy']*ex['cny2usd'],'sell':cok_cn[3]['sell']*ex['cny2usd']}
    cok_cn[1]={'buy':cok_cn[4]['buy']*ex['cny2usd'],'sell':cok_cn[4]['sell']*ex['cny2usd']}
    markets={'poloniex':cpolo,'kraken':ckrak,'cok_com':cok_com,'cok_cn':cok_cn}
    odds={}
    for k1 in markets.keys():
        for k2 in markets.keys():
            if k1==k2:continue
            ratios,total_ratio=a_above_b(markets[k1],markets[k2])
            if total_ratio>1.05:
                odds[k1+'>>'+k2]=total_ratio,ratios
    print (datetime.datetime.now().strftime(TIME_FORMAT)+"\t" + str(odds))
    return datapoint(markets,ex,odds)




if __name__=="__main__":
    p = poloniex()
    k = kraken()
    ok = OkCoin()
    ex = exchangerate
    dataset=[]
    log=[]
    run_length=datetime.timedelta(minutes=1,hours=10)
    endTime = datetime.datetime.now() + run_length
    while datetime.datetime.now() < endTime:
        dp=one_round(p,k,ok,ex)
        dataset.append(dp)
        if len(dp.odds)>0:
            log.append(datetime.datetime.now().strftime(TIME_FORMAT)+"\t" +str(dp.odds))
        time.sleep(150)
    pickle.dump(dataset,open(path.join('output',endTime.strftime(TIME_FORMAT).replace(':','')+'started_{}min_data'.format(run_length.seconds/60)),'wb'))
    with open(path.join('output',endTime.strftime(TIME_FORMAT).replace(':','')+'started_{}min_data_summary.txt'.format(run_length.seconds/60)),'w') as f:
        f.write('\n'.join(log))