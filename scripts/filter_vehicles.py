cars = dict()
mm = open('cars', 'r')
allmm = mm.readlines()
mm.close()
for item in allmm:
    me, ml = item.split(',', 1)
    make = me.strip()
    model = ml.strip()

    if make not in cars:
        cars[make] = set()

    cars[make].add(model)

vehicle_type = 'mpv'

cl = open('initial-'+vehicle_type+'s-list' ,'r')
er = open('err-first-'+vehicle_type+'s-list', 'w')
rl = open('real-first-'+vehicle_type+'s-list', 'w')
allcl = cl.readlines()
cl.close()

for item in allcl:
    me, mlyr = item.split('","', 1)
    make = me.strip()[1:].lower()

    if make in cars:
        rl.write(item)
    else:
        er.write(item)

rl.close()
er.close()