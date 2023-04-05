from solcx import compile_source,install_solc
install_solc()
compiled_sol=compile_source(
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
   mapping (uint => patient_log) logs;
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
'''
    ,output_values=['abi','bin']
)

contract_id,contract_interface=compiled_sol.popitem()
a=contract_interface['abi']
b=contract_interface['bin']
a

from web3 import Web3
w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

drugcompany=w3.eth.contract(abi=a,bytecode=b)

tx=drugcompany.constructor('0xf694b75C6DD0770cC783687618819B5580D92BA6').buildTransaction(
{
    'from':'0xaC33Ec0a87ab95EeDD668dF6BDE58edA2a4073B4',
    'gasPrice':w3.eth.gas_price,
    'nonce':w3.eth.getTransactionCount('0xaC33Ec0a87ab95EeDD668dF6BDE58edA2a4073B4')
})

p="0xf8afc9e6c1328a53b4b168e5a51815389ca73e555fb1ced8d733558f8317d79b"
signed_tx=w3.eth.account.sign_transaction(tx,private_key=p)

tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)

tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)

con_instance=w3.eth.contract(address=tx_recipt.contractAddress,abi=a)

drud_man_add="0xaC33Ec0a87ab95EeDD668dF6BDE58edA2a4073B4"
drud_pr_key="0xf8afc9e6c1328a53b4b168e5a51815389ca73e555fb1ced8d733558f8317d79b"
hos_add="0xf694b75C6DD0770cC783687618819B5580D92BA6"
hos_pkey="0xd3b2d88d9d23d4d1c4bc5f6bc4b681210d9c106b70ed9c4eabd6d00d4e4dddeb"

tx1=con_instance.functions.reg_producer('0x2381a8c33c711003e2DDDf34A4E05f17662dF2d8').buildTransaction(
{
    'from':drud_man_add,
    'gasPrice':w3.eth.gas_price,
    'nonce':w3.eth.getTransactionCount(drud_man_add)
})
signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=p)
tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)

def reg_h(hos_id):
    tx1=con_instance.functions.reg_hos(hos_id).buildTransaction(
    {
        'from':hos_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(hos_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=hos_pkey)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def reg_pat(p_id,h_id):
    tx1=con_instance.functions.reg_patient(p_id,h_id).buildTransaction(
    {
        'from':hos_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(hos_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=hos_pkey)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def reg_d(doc_id):
    tx1=con_instance.functions.reg_doctor(doc_id).buildTransaction(
    {
        'from':hos_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(hos_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=hos_pkey)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def produced_data(pid,avail):
    tx1=con_instance.functions.add_produced_drug(pid,avail).buildTransaction(
    {
        'from':'0x2381a8c33c711003e2DDDf34A4E05f17662dF2d8',
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount('0x5E5Df54E1FDE965266dB50cC2001fA5bDd5511ac')
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key="0xfa8ef15a3923121d746cc46cb245ea9e9e9a0285d10a6c0098b9691dd830d414")
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def up_avail(pid,av):
    tx1=con_instance.functions.update_avail(pid,av).buildTransaction(
    {
        'from':drud_man_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(drud_man_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=drud_pr_key)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def add_drug_by_dm(p,a,t,r):
    tx1=con_instance.functions.add_drug(p,a,t,r).buildTransaction(
    {
        'from':drud_man_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(drud_man_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=drud_pr_key)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)
def buydrug(h,did,rqam,doc,pat):
    tx1=con_instance.functions.buy_drug(h,did,rqam,doc,pat).buildTransaction(
    {
        'from':hos_add,
        'gasPrice':w3.eth.gas_price,
        'nonce':w3.eth.getTransactionCount(hos_add)
    })
    signed_tx1=w3.eth.account.sign_transaction(tx1,private_key=hos_pkey)
    tx_hash1=w3.eth.send_raw_transaction(signed_tx1.rawTransaction)

reg_pat(164,82)

reg_d(764)

produced_data(456,120)

add_drug_by_dm(456,120,55,45)

buydrug(82,456,35,764,164)

reg_h(82)

con_instance.functions.income().call()
