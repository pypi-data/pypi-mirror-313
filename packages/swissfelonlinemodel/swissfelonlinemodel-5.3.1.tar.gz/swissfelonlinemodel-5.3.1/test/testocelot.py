from onlinemodel.core import Facility
from onlinemodel.code.madxutil import getResponseMatrix

import matplotlib.pyplot as plt

SF =Facility()
SF.setBranch('Aramis','SARMA02','SARUN15')

BPM = SF.getBranchElements('.*-DBPM.*')
COR = SF.getBranchElements('SARMA02-MCRX.*')+ SF.getBranchElements('SARUN04-MCRX080') 
res = getResponseMatrix(SF,COR,BPM)

plt.plot(res['SARUN04-MCRX080']['s'],res['SARUN04-MCRX080']['R12'],'o-')
plt.plot(res['SARUN04-MCRX080']['s'],res['SARUN04-MCRX080']['R34'],'o-')
plt.show()
