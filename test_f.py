import itertools
from DBControll.ConnectDatabase import ConnectDatabase
from DBControll.LinkTable import LinkTable
from path_calculate.get_path import GetPath

ConnectDatabase()
original_link = LinkTable().pop_all_link()

sque = ['Mission', 'Mobile', 'Massive', 'normal']
all_Q_sequence = list(itertools.permutations(sque))
ett_list = list()

for Q in all_Q_sequence:
    ett = GetPath().excute_ETT_all_sequency(Q)
    print('{}: {}'.format(Q, ett))
    LinkTable().delete_all()
    for link in original_link:
        LinkTable().insert_link(start_node=link[0], end_node=link[1],
                                bandwidth=link[2], ETX=link[3])
    if ett < 10:
        ett_list.append(ett)
nsdar_sdn = ett_list[0]
sorted_ett_list = sorted(ett_list)
print('available path count: {}'.format(len(ett_list)))
print('NSDAR-SDN rank: {}'.format(sorted_ett_list.index(nsdar_sdn)))

ett = GetPath().excute_ETT_NSR_SDN()
print('{}: {}'.format('NSRSDN', ett))
LinkTable().delete_all()
for link in original_link:
    LinkTable().insert_link(start_node=link[0], end_node=link[1],
                            bandwidth=link[2], ETX=link[3])
