from pathlib import Path
import json,re,time
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as ca
R=Path(__file__).parents[1];ROOT=R.parents[3]
def env(name):
 text=(ROOT/'accounts.env').read_text(encoding='utf-8');return re.search(r'^'+re.escape(name)+r'\s*=\s*"?([^"\r\n]+)',text,re.M).group(1).strip()
def calldata(method=None,args=None,kwargs=None):
 out={}
 if method is not None:out['method']=method
 if args:out['args']=args
 if kwargs:out['kwargs']=kwargs
 return out
ca.make_calldata_object=calldata
client=create_client(chain=studionet,account=create_account(account_private_key=env('ACCOUNT_6_GENLAYER_PRIVATE_KEY')));deployment=json.loads((R/'deployment.json').read_text(encoding='utf-8'));address=deployment['contractAddress'];record_id='SURPLUS_CROSSING-'+str(int(time.time()));args=[record_id, "https://www.fao.org/platform-food-loss-waste/en/"];tx=client.write_contract(address=address,function_name='open_crossing',args=args);receipt=client.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);full=client.get_transaction(transaction_hash=tx);leaders=full.get('consensus_data',{}).get('leader_receipt') or [];leaders=[leaders] if isinstance(leaders,dict) else leaders;assert full.get('result_name')=='MAJORITY_AGREE' and any(x.get('execution_result')=='SUCCESS' for x in leaders),full;record=client.read_contract(address=address,function_name='get_crossing',args=[record_id]);out={'recordType':'operator-created lifecycle fixture; not independent third-party evidence','recordId':record_id,'contractAddress':address,'transaction':str(tx),'readback':record};(R/'network-run.json').write_text(json.dumps(out,indent=2,default=str)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,default=str),flush=True)
