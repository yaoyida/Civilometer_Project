import json

infile = '/home/agong/Desktop/desktop-files-2012-08-04/fixtures-8/tb_app_codebook.json'
outfile = '/home/agong/Desktop/cvm_codebook.json'

#This list was created by hand on 2012/08/06, after the codebook creation blitz with Aleks and Michael, but before final coding was completed.
ids = ['501c0e2333679d12678d8410', '50199d1a33679d12678d8406', '5019a06633679d12678d8408', '50199ad233679d12678d8405', '501c172e33679d12678d8414', '500ee12233679d206395fbe0', '500edd2833679d206395fbdd', '50199e2c33679d12678d8407', '501995d033679d12678d8402', '501c17bc33679d12678d8415']

J = json.load( file(infile, 'r') )
print len(J)

K = []
for j in J:
    #Keep only the codebooks we want to keep
    if j["_id"]["$oid"] in ids:
        print j["_id"]["$oid"], j["profile"]["name"]
        K.append( j )

print len(K)
file(outfile, 'w').write(json.dumps(K, indent=2))



