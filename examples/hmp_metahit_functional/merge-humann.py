#!/usr/bin/env python

from sys import argv


if __name__ == "__main__":

    try:
        argv[1]
        argv[2]
        argv[3]
        argv[4]
        argv[5]
        argv[6]
    except:
        print "Usage error!"
        print "$ python merge_humann.py <in_hmp> <skip_rows_hmp> <in_metahit> <skip_rows_metahit> <metahit_map> <out_file>"
        exit(1)

    infile1 = str(argv[1])
    infile2 = str(argv[3])
    metahit_map = str(argv[5])
    outfile = str(argv[6])

    skip1 = int(argv[2])
    skip2 = int(argv[4])

    dataset1 = 'HMP'
    dataset2 = 'MetaHIT'

    file1 = []
    file2 = []
    donel = []
    hmp_bodysites = []
    metahit_ids = []

    # read the first file, save it into a list skipping the given rows
    i = 0
    with open(infile1, 'r') as f:
        for l in f:
            if i < skip1:
                if l.startswith('STSite'):
                    hmp_bodysites = l.strip().split()[1:]

                i += 1
            else:
                file1.append(l.strip().split())

    # filter the HMP dataset at Stool bodysite
    i = 0
    stool_list = []
    hmp = []

    for b in hmp_bodysites:
        if b == 'Stool':
            stool_list.append(i)

        i += 1

    for l in file1:
        lst = []

        for i in stool_list:
            lst.append(l[i])

        hmp.append(lst)

    # read the second file, save it into a list skipping the given rows
    i = 0
    with open(infile2,'r') as f:
        for l in f:
            if i < skip2:
                if l.startswith('ID'):
                    metahit_ids = l.strip().split()[1:]

                i += 1
            else:
                file2.append(l.strip().split())

    # get just the healty MetaHIT samples
    hlist = ['ERS006486', 'ERS006487', 'ERS006488', 'ERS006489', 'ERS006490', 'ERS006491', 'ERS006493', 'ERS006494',
    'ERS006495', 'ERS006496', 'ERS006497', 'ERS006498', 'ERS006499', 'ERS006500', 'ERS006501', 'ERS006503', 'ERS006504',
    'ERS006505', 'ERS006506', 'ERS006507', 'ERS006508', 'ERS006511', 'ERS006513', 'ERS006514', 'ERS006516', 'ERS006517',
    'ERS006519', 'ERS006525', 'ERS006527', 'ERS006528', 'ERS006529', 'ERS006530', 'ERS006531', 'ERS006532', 'ERS006533',
    'ERS006534', 'ERS006535', 'ERS006536', 'ERS006537', 'ERS006538', 'ERS006540', 'ERS006541', 'ERS006542', 'ERS006544',
    'ERS006547', 'ERS006548', 'ERS006549', 'ERS006550', 'ERS006551', 'ERS006552', 'ERS006553', 'ERS006554', 'ERS006555',
    'ERS006556', 'ERS006557', 'ERS006558', 'ERS006560', 'ERS006561', 'ERS006562', 'ERS006564', 'ERS006565', 'ERS006568',
    'ERS006569', 'ERS006570', 'ERS006571', 'ERS006573', 'ERS006578', 'ERS006579', 'ERS006580', 'ERS006581', 'ERS006584',
    'ERS006585', 'ERS006586', 'ERS006588', 'ERS006589', 'ERS006590', 'ERS006592', 'ERS006593', 'ERS006596', 'ERS006597',
    'ERS006600', 'ERS006601', 'ERS006604', 'ERS006607', 'ERS006608', 'ERS006566', 'ERS006559', 'ERS006574', 'ERS006526',
    'ERS006539', 'ERS006599', 'ERS006602', 'ERS006524', 'ERS006587', 'ERS006545', 'ERS006575', 'ERS006510', 'ERS006594',
    'ERS006492']
    healthy = []

    # read mapping metahit input file
    with open(metahit_map, 'r') as f:
        for row in f:
            ers_id, real = row.strip().split()

            # keep only healthy
            if ers_id in hlist:
                healthy.append(real)

    # remove from the MetaHIT samples the non-healthy ones
    i = 0
    filter_list = []
    metahit = []

    for j in metahit_ids:
        for h in healthy:
            if h in j:
                filter_list.append(i)

        i += 1

    for l in file2:
        lst = [l[0]]

        for i in filter_list:
            lst.append(l[i])

        metahit.append(lst)

    # write the output file
    with open(outfile, 'w') as f:
        # write the dataset information
        f.write(''.join(['\t'.join(['dataset', '\t'.join([dataset1 for i in range(len(hmp[0]) - 1)]),
                         '\t'.join([dataset2 for i in range(len(metahit[0]) - 1)])]),
                         '\n']))

        # at the end of this for the output file will contains all the hmp, together with the ones shared with metahit
        for l1 in hmp:
            m1 = l1[0].replace('.', '|')
            done = False

            for l2 in metahit:
                m2 = l2[0].replace('.', '|')

                if m1 == m2: # both dataset has the same row
                    taxa = m1[:m1.rfind('_')]
                    f.write(''.join(['\t'.join([taxa, '\t'.join([i for i in l1[1:]]),
                                     '\t'.join([i for i in l2[1:]])]),
                                     '\n']))
                    donel.append(m1)
                    done = True
                    break

            if not done: # the second dataset misses the row
                taxa = m1[:m1.rfind('_')]
                f.write(''.join(['\t'.join([taxa, '\t'.join([str(i) for i in l1[1:]]),
                                 '\t'.join(['0.0' for i in range(len(metahit[0]) - 1)])]),
                                 '\n']))
                donel.append(m1)

        # look for the ignored rows in metahit
        for l2 in metahit:
            m2 = l2[0].replace('.', '|')

            if m2 not in donel: # the first dataset misses the row
                taxa = m2[:m2.rfind('_')]
                f.write(''.join(['\t'.join([taxa, '\t'.join(['0.0' for i in range(len(hmp[0]) - 1)]),
                                 '\t'.join([str(i) for i in l2[1:]])]),
                                 '\n']))
