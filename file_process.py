def ip(arg):
    if(arg>=16):
        ip_str=":"+str(hex(arg)[2:])+str(hex(arg)[2:])
    else:
        arg=hex(arg)[2:]
        ip_str=":"+str(arg)+":"+str(arg)
    return ip_str

def delays_one_node(f, ind, pkts=range(1,100)):
    ls=[]
    summ=0
    first=0
    txcounter=0.0
    rxcounter=[0]*3000
    lsDelay=[]
    lsPDR=[]
    # print("Doing NODE "+str(ip(ind)))
    for i in pkts:
        f.seek(0)
        for line in f.readlines():
            numb = str(i) 
            if "Send to " in line  and "seqnum "+str(i)+"," in line:
                # sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                sTime=int(line.split(':')[0])
                # print (line)
                txcounter+=1
        
            if "Received from" in line and ip(ind)+"," in line and "seqnum " + str(i) +"," in line:
                
                if(first==0):
                    first=int(numb)
                
                rTime=int(line.split(':')[0])
                dTime=(rTime-sTime)/1000
                
                rxcounter[i]=1.0
                last=numb
                ls.append(dTime)
                # print (line)
                # print(dTime)
                break
        # if(dTime is not None):
        #     summ=summ+dTime.microseconds
    rx=0.0
    for el in rxcounter:
        rx+=el
    # print("avgDelay="+str(np.average(ls)))
    # print("node="+str(ind))

    # if txcounter==0:
    #     return 0
    # if(rx==0):
    #     # print("0")
    #     lsPDR.append(0)
    # else:
    #     # print("rx:%d"%(rx))
    #     # print("last"+str(txcounter))
    #     # print(rx/float(txcounter))
    #     lsDelay.append(ls)
    #     lsPDR.append(rx/float(txcounter))
    
    return ls

def process_file_for_nodes(f,nodes):
    # min=1000000
    # max=0
    last=0.0
    lsPDR=[]
    lsDelay=[]
    for ind in nodes:
        lsDelay.append(delays_one_node(f, ind))

        # print(first)
        # print((rx)/(txcounter-first+1))

    # print(lsPDR)
    # print(len(lsPDR))
    # print(lsDelay)
    # print(len(lsDelay))
    # print("SUMs:")
    # print(sum(lsPDR)/len(lsPDR))
    # print(sum(lsDelay)/len(lsDelay))
    return lsDelay

def process_files(path,name,range=range(1,5),T=1,UC=270,node=2):
    DVPs=[]
    all_delays=[]
    ls_delays=[]
    for i in range:
        fileName = path+name+"-"+str(i)+".log"
        print(fileName)
        f = open(fileName,"r")
        delays=process_file_for_nodes(f,[node])
        all_delays=all_delays+delays[0]
        # ls_delays.append(delays[0])
        if len(delays)==0:
            continue
        print("delays:"+str(delays))
        violations=len([1 for i in delays[0] if i > T*UC])
        if len(delays[0]) == 0:
            print("no packet")
        else: DVPs.append(violations/ len(delays[0]))
        # print(f"violations: {violations} len(delays):{len(delays)}" )
        f.close()
    return DVPs, all_delays