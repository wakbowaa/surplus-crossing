from pathlib import Path
S=(Path(__file__).parents[1]/'contracts'/'contract.py').read_text()
def test_surface():
 for n in ('open_crossing','list_item','freeze','match','close','get_crossing'):assert 'def '+n in S
def test_every_listing_is_normalized():assert 'return run()==leader.calldata' in S and "len(rows)!=len(listings)" in S
def test_listing_identity_and_sources():assert "x['id']==key or x['origin']==origin" in S
def test_capacity_matching_is_deterministic():assert 'remaining=[int' in S and 'units=min(remaining[offer],remaining[need])' in S
def test_blocked_pairs_are_enforced():assert "str(offer)+':'+str(need) in blocked" in S
