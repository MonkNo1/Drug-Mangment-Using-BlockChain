from web3 import Web3
from solcx import compile_source, install_solc
import datetime
install_solc()
con_instance = ""
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
drugcompany = ""
a = ""
tx_recipt = ""


def compile():
    global drugcompany
    global a
    compiled_sol = compile_source(
        '''
    pragma solidity ^0.8.14;
    contract drugcompany
    {
        struct product
        {
            uint avail;
            uint threosold;
            uint rate;
        }
        mapping (uint => product)drugs;
        address producer;
        address drugmanager;
        address hospitalmanager;
        // uint public prodid=0;
        uint orderdid=0;
        struct order
        {
            uint hospid;
            uint time;
            uint drugid;
            uint quantity;
            uint amount;
        }
        mapping (uint => order)orders;
        uint [] hospitals;
        uint public income=0;
        struct patient
    {
        uint hospid;
    }
    struct patient_log
    {
        uint patientid;
        uint docid;
        uint timestamp;
        uint drugid;
        uint amount;
    }
    uint [] patientarr;
    uint [] doctors;
    mapping (uint => patient) patients;
    mapping (uint => patient_log) public logs;
    uint logid=1;
        modifier onlydm(address d)
        {
            require(d==drugmanager);
            _;
        }
        modifier onlyhm(address d)
        {
            require(d==hospitalmanager);
            _;
        }
        function reg_producer(address w) public onlydm(msg.sender)
        {
            producer=w;
        }
        constructor(address hm)
        {
            drugmanager=msg.sender;
            hospitalmanager=hm;
        }
        struct producer_content
        {
            uint amount;
        }
        mapping (uint => producer_content) produced_drug;
        modifier onlyproducer(address j)
        {
            require(j==producer);
            _;
        }
        function add_produced_drug(uint pid,uint a) public onlyproducer(msg.sender)
        {
            produced_drug[pid].amount=a;
        }
        function reg_hos(uint y) public onlyhm(msg.sender)
        {
            hospitals.push(y);
        }
        function reg_patient(uint y,uint hi) public onlyhm(msg.sender)
        {
            patientarr.push(y);
            patients[y].hospid=hi;
        }
            function reg_doctor(uint y) public onlyhm(msg.sender)
        {
            doctors.push(y);
        }
        modifier validam(uint d,uint p)
        {
            require(produced_drug[p].amount==d);
            _;
        }
        function add_drug(uint p,uint a,uint t,uint r) public onlydm(msg.sender) validam(a,p)
        {
        drugs[p].avail=a;
            drugs[p].threosold=t;
            drugs[p].rate=r;
            // prodid+=1;
        }
        function update_avail(uint pi,uint k) public onlydm(msg.sender) validam(k,pi)
        {
            drugs[pi].avail+=k;
        }
        function valid_hos(uint j) public returns(bool)
        {
            uint flag=0;
            for(uint i=0;i<hospitals.length;i++)
            {
                if(hospitals[i]==j)
                {
                    flag=1;
                    return true;
                }
            }
            if (flag==0)
            {
                return false;
            }
        }
            function valid_pait(uint j) public returns(bool)
        {
            uint flag=0;
            for(uint i=0;i<patientarr.length;i++)
            {
                if(patientarr[i]==j)
                {
                    flag=1;
                    return true;
                }
            }
            if (flag==0)
            {
                return false;
            }
        }
            function valid_doctors(uint j) public returns(bool)
        {
            uint flag=0;
            for(uint i=0;i<doctors.length;i++)
            {
                if(doctors[i]==j)
                {
                    flag=1;
                    return true;
                }
            }
            if (flag==0)
            {
                return false;
            }
        }
        modifier validhos(uint tr)
        {
            require(valid_hos(tr)==true);
            _;
        }
        modifier validp(uint tr)
        {
            require(valid_pait(tr)==true);
            _;
        }
        modifier validd(uint tr)
        {
            require(valid_doctors(tr)==true);
            _;
        }
        modifier meetavail(uint hy,uint k)
        {
            require(hy<= drugs[k].avail);
            _;
        }
        modifier meetthros(uint k,uint hy)
        {
            require(hy< drugs[k].threosold);
            _;
        }
        function buy_drug (uint h,uint porid,uint req_amount,uint did,uint patid) public validhos(h) meetavail(req_amount,porid) meetthros(porid,req_amount) validp(patid) validd(did) onlyhm(msg.sender)
        {
            drugs[porid].avail-=req_amount;
            income+=(req_amount*drugs[porid].rate);
            orders[orderdid].hospid=h;
            orders[orderdid].time=block.timestamp;
            orders[orderdid].drugid=porid;
            orders[orderdid].quantity=req_amount;
            orders[orderdid].amount=req_amount*drugs[porid].rate;
            orderdid+=1;
        logs[logid].patientid=patid;
            logs[logid].docid=did;
            logs[logid].timestamp=block.timestamp;
            logs[logid].drugid=porid;
            logs[logid].amount=req_amount;
            logid+=1;
        }
        function drug_av(uint pid) view public returns(uint) 
        {
            return drugs[pid].avail;
        }
    }
    ''', output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()
    a = contract_interface['abi']
    b = contract_interface['bin']
    drugcompany = w3.eth.contract(abi=a, bytecode=b)


def cons():
    global tx_recipt
    tx = drugcompany.constructor('0xedD8b6Ef5c096147c3D8A7B812A1c108626E6a5B').buildTransaction(
        {
            'from': '0x2AfF3a4F93186CbBfAE2a58a73874a08E3882612',
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount('0x2AfF3a4F93186CbBfAE2a58a73874a08E3882612')
        })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=p)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_recipt = w3.eth.wait_for_transaction_receipt(tx_hash)


p = "0x98a37e7864df1b52f073b9f9a2f67b938335b4f881e7933f35d893a3cc141b8f"


def create_inst():
    global tx_recipt
    global con_instance
    con_instance = w3.eth.contract(address=tx_recipt.contractAddress, abi=a)


drud_man_add = "0x2AfF3a4F93186CbBfAE2a58a73874a08E3882612"
drud_pr_key = "0x98a37e7864df1b52f073b9f9a2f67b938335b4f881e7933f35d893a3cc141b8f"
hos_add = "0xedD8b6Ef5c096147c3D8A7B812A1c108626E6a5B"
hos_pkey = "0x8f81dfa66a04e01aaa034923b177e927bde2e3c772cb58704152fce14881011e"


def registerprod():
    tx1 = con_instance.functions.reg_producer('0x1b7ea6b1766a6008630A5f4Ea398e9407ee23BEA').buildTransaction(
        {
            'from': drud_man_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(drud_man_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=p)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def reg_h(hos_id):
    tx1 = con_instance.functions.reg_hos(hos_id).buildTransaction(
        {
            'from': hos_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(hos_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=hos_pkey)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def reg_pat(p_id, h_id):
    tx1 = con_instance.functions.reg_patient(p_id, h_id).buildTransaction(
        {
            'from': hos_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(hos_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=hos_pkey)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def reg_d(doc_id):
    tx1 = con_instance.functions.reg_doctor(doc_id).buildTransaction(
        {
            'from': hos_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(hos_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=hos_pkey)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def produced_data(pid, avail):
    tx1 = con_instance.functions.add_produced_drug(pid, avail).buildTransaction(
        {
            'from': '0x1b7ea6b1766a6008630A5f4Ea398e9407ee23BEA',
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount('0x1b7ea6b1766a6008630A5f4Ea398e9407ee23BEA')
        })
    signed_tx1 = w3.eth.account.sign_transaction(
        tx1, private_key="0x5147e7461ee52b08fea579bcd8825863b8b4269ea1f37e5f1aab43608a657816")
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def up_avail(pid, av):
    tx1 = con_instance.functions.update_avail(pid, av).buildTransaction(
        {
            'from': drud_man_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(drud_man_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=drud_pr_key)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def add_drug_by_dm(p, a, t, r):
    tx1 = con_instance.functions.add_drug(p, a, t, r).buildTransaction(
        {
            'from': drud_man_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(drud_man_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=drud_pr_key)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def buydrug(h, did, rqam, doc, pat):
    tx1 = con_instance.functions.buy_drug(h, did, rqam, doc, pat).buildTransaction(
        {
            'from': hos_add,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.getTransactionCount(hos_add)
        })
    signed_tx1 = w3.eth.account.sign_transaction(tx1, private_key=hos_pkey)
    tx_hash1 = w3.eth.send_raw_transaction(signed_tx1.rawTransaction)


def call_me_first():
    compile()
    cons()
    create_inst()
    registerprod()


def retrive_data(logid):
    res = []
    l = con_instance.functions.logs(logid)
    res.append(l[0])
    res.append(l[1])
    date_time = datetime.datetime.fromtimestamp(l[2])
    d = date_time.strftime("%d/%m/%Y time:  %H:%M:%S")
    res.append(d)
    res.append(l[3])
    res.append(l[4])
    return res
