#python3
import json
import sys
from random import randrange,randint,choice,shuffle
import pickle
from tqdm import tqdm

def main():
    # scenario = '2_plant_scenario/'
    scenario = '1_airplane_scenario/'
    # with open(scenario + 'classes_plant.json') as file:
    with open(scenario + 'newclass.json') as file:
        data = json.load(file)

    # args = {
    #     'prefix':'plant',
    #     'num_options':4,
    #     'num_iter': 1000,
    #     'data': data
    # }

    focuses = ['age', 'health', 'gender', 'income level', 'education level', 
    'number of dependents', 'survival']

    # makestory_power(data,4)
    # generate_better(args, fn=makestory_power)

    # these guys were here for airplane scenarios

    explanation = {
        'age': 'Age of the person',
        'health': 'Health status of the person',
        'gender': 'Gender of the person',
        'income level': 'Income level of the person',
        'education level': 'Highest level of education the person received',
        'number of dependents': 'Number of people the person supports',
        'survival with jacket': 'Survival chance when given the jacket',
        'survival without jacket': 'Survival chance when not given the jacket',
        'if chosen': 'Survival chance when given the jacket',
        'if not chosen': 'Survival chance when not given the jacket',
    }

    titanic_combo = [
        {'age': '21', 'health': 'in great health', 'gender': 'male', "income level": 'low', "number of dependents":'0', "survival without jacket": '0%', "survival with jacket": '32%'},
        {'age': '32', 'health': 'in great health', 'gender': 'male', "income level": 'low', "number of dependents":'0', "survival without jacket": '0%', "survival with jacket": '32%'},
        {'age': '52', 'health': 'in great health', 'gender': 'female', "income level": 'high', "number of dependents":'1', "survival without jacket": '0%', "survival with jacket": '32%'},
        {'age': '5', 'health': 'in great health', 'gender': 'female', "income level": 'high', "number of dependents":'0', "survival without jacket": '0%', "survival with jacket": '32%'},
    ]

    categories = parse_categories(data)
    badcombo = parse_bad_combo(data,categories)

    args = {        
        'savepath': '1_airplane_scenario/data/dump/',
        'categories': categories,
        'bad_combos': badcombo,
        'num_options': 2,
        'prefix': 'pairs',
        'num_iter': 2000,
        'explanation': explanation,        
    }

    generate_random(args.copy(), fn=makestory)

    args = {        
        'savepath': '1_airplane_scenario/data/dump/',
        'categories': categories,
        'bad_combos': badcombo,
        'num_options': 3,
        'prefix': 'tripset0',
        'num_iter': 1,
        'explanation': explanation,        
    }

    generate_random(args.copy(), fn=makestory)

    args['prefix'] = 'tripset1'
    generate_random(args.copy(), fn=makestory)

    args['prefix'] = 'tripset2'
    generate_random(args.copy(), fn=makestory)

    args['prefix'] = 'tripset3'
    generate_random(args.copy(), fn=makestory)

    args['prefix'] = 'triples'
    args['num_iter'] = 1000
    generate_random(args.copy(), fn=makestory)
    
    generate_titanic(titanic_combo,categories,explanation)

def generate_group(args, fn=None):
    path = args.pop('savepath')
    prefix = args.pop('prefix')
    num_iter = args.pop('num_iter')
    focuses = args.pop('focuses')
    jsfile = open(path+prefix+'_options.js','w')
    # I don't need the text file anymore, but it's easier to view, so I'll keep it
    for f in focuses:
        newargs = args.copy()
        newargs['focus'] = f
        ff = f.replace(' ','_')
        jsfile.write('var '+ff+'_story = [')
        all_attributes = []
        for i in range(num_iter):
            jsfile.write('[')
            m,o = fn(**newargs)
            all_attributes.append(o)            
            for j in range(len(m)):
                jsfile.write("{'table':'" + m[j] +"'}")
                if j < len(m)-1:
                    jsfile.write(',')
            if i < num_iter-1: jsfile.write('],')
            else: jsfile.write(']')
            jsfile.write('\n')
        jsfile.write(']\n')
        # saving pickel of options to make parsing easier
        save_attributes(path+ff+'_pickle',all_attributes)
    jsfile.close()

def generate_better(ags,fn = None):
    args = ags.copy()
    prefix = args.pop('prefix')
    num_iter = args.pop('num_iter')
    all_attributes = []
    jsfile = open(prefix+'_options.js','w')
    jsfile.write('var '+prefix+'_story = [')
    for i in range(num_iter):
        s,o = makestory_power(**args)
        all_attributes.append(o)
        jsfile.write(s)
        if i < num_iter-1: jsfile.write(',')
    jsfile.write(']')
    save_attributes(prefix+'_pickle',all_attributes)
    jsfile.close()

# I hardcoded the javascript generation stuff and now I don't wanna fix it
# so just gonna make a new function
def generate_random(args,fn = None):
    # creates a javascript file containing combos to be chosen from.
    # This file gets copied and pasted to google drive to add to the html file
    path = args.pop('savepath')
    prefix = args.pop('prefix')
    num_iter = args.pop('num_iter')
    categories = args['categories'].copy()
    jsfile = open(path+prefix+'_options.js','w')
    # I don't need the text file anymore, but it's easier to view, so I'll keep it
    jsfile.write('var '+prefix+'_story = [')
    all_attributes = []
    for i in tqdm(range(num_iter)):
        jsfile.write('[')
        m,o = fn(**args)
        all_attributes.append(o)
        
        for j,(table,ops) in enumerate(zip(m,o)):
            # jsfile.write("{'table':'" + table +"'")
            # jsfile.write("'vals':")

            buf = '{'
            for oo,v in ops.items():
                buf += '"'+oo+'"'+':'
                buf += '"'+v+'"'
                # if 'survival' in oo:
                #     buf += v[:-1]
                # elif v == 'N/A':
                #     buf += '0'
                # else:
                #     buf += str(categories[oo].index(v))
                buf += ','
            buf = buf[:-1]
            buf += '}'
            jsfile.write(buf)
            # jsfile.write("}")
            if j < len(m)-1:
                jsfile.write(',')
        if i < num_iter-1: jsfile.write('],')
        else: jsfile.write(']')
        jsfile.write('\n')
    jsfile.write(']')
    # saving pickel of options to make parsing easier
    save_attributes(path+prefix+'_pickle',all_attributes)
    jsfile.close()

def generate_titanic(combos,categories,explanation):
    path = '1_airplane_scenario/data/dump/'
    prefix = 'titanic'
    jsfile = open(path+prefix+'_options.js','w')
    # I don't need the text file anymore, but it's easier to view, so I'll keep it
    jsfile.write('var '+prefix+'_story = [')
    all_attributes = []    
    
    vals = [(form_table(cc,explanation),cc)for cc in combos]

    for j,(table,ops) in enumerate(vals):
        # jsfile.write("{'table':'" + table +"'")
        # jsfile.write("'vals':")

        buf = '{'
        for oo,v in ops.items():
            buf += '"'+oo+'"'+':'
            buf += '"'+v+'"'
            # if 'survival' in oo:
            #     buf += v[:-1]
            # elif v == 'N/A':
            #     buf += '0'
            # else:
            #     buf += str(categories[oo].index(v))
            buf += ','
        buf = buf[:-1]
        buf += '}'
        jsfile.write(buf)
        # jsfile.write("}")
        if j < len(vals)-1:
            jsfile.write(',')
    # jsfile.write('],')
    jsfile.write('\n')
    jsfile.write(']')
    # saving pickel of options to make parsing easier
    save_attributes(path+prefix+'_pickle',all_attributes)
    jsfile.close()

def makestory_power(data, num_options):
    solutions = data['solutions']
    cities = data['cities']
    solus = [{} for i in range(num_options)]

    chosenpop = set()
    # c1 is always large and c2 is always small

    pops = {
        'C1': choice(data['population_size']['large']),
        'C2': choice(data['population_size']['small'])
    }

    chosensol = set()

    justvals = []

    # n_cities = [1,1,1,1]

    # in attempt to even out the cities, shuffle array of two cities 
    a_cities = ['C1','C1','C2','C2']
    shuffle(a_cities)
    
    for l,s in enumerate(solus):
        sset = set(list(solutions.keys()))
        if not sset- chosensol: sol = solutions[choice(list(sset - chosensol))]
        else: sol = solutions[choice(list(sset))]

        # choosing how many cities are affected
        # always just takes out 1
        # num_affected = n_cities[l]

        # affected_cities = set()
        # for i in range(num_affected):
        #     c = choice(list(set(cities)-affected_cities))
        #     affected_cities.add(c)
        affected_cities = [a_cities[l]]

        # now calculating power gain
        gain = make_chance(int(sol['eco_gain'][0]),int(sol['eco_gain'][1]))

        baseset = {
            '👥': '',
            '$$$': '+'+str(gain) + '%',
            '💓': 'No risk'
        }
        s['affected'] = affected_cities
        s['C1'] = baseset.copy()
        s['C2'] = baseset.copy()

        lifeloss = make_chance(int(sol['life_loss'][0]),int(sol['life_loss'][1]))
        losschance = make_chance(int(sol['risk_factor'][0]),int(sol['risk_factor'][1]))

        for c in affected_cities:
            s[c]['💓'] = '-' + str(lifeloss) + ' years\\n(' + str(losschance) + '%' + ' chance)'

        for c in cities:
            s[c]['👥'] = pops[c]

        justvals.append({
            'affected': list(affected_cities),
            'population': pops,
            'eco_gain': gain,
            'life_loss': lifeloss,
            'loss_chance': losschance
        })
    jsvar = turn_js(solus)
    return jsvar, justvals

def turn_js(varis):
    js_var ='['
    for ss in varis:
        js_var += '{'
        for c,v in ss.items():
            js_var += '\'' + c + '\':'
            if not c == 'affected':
                js_var += '\'' + form_table(v) + '\','
            else:
                js_var += str(v) + ','
        js_var = js_var[:-1]
        js_var += '},'
    js_var = js_var[:-1]
    js_var += ']'

    return js_var

# THESE FOLLOWING GUYS WERE FOR AIRPLANE PROBLEM
# generates the random one
def makestory(categories,bad_combos,num_options,surv_factors=None,explanation=None,focus=None):
    # generate an empty option dictionary with empty value for each category
    bareoption = dict([(categ,'') for categ in categories])
    # for this value, I will just randomly generate for now
    # bareoption.update({'with':0})
    # bareoption.update({'without':0})

    invalid = False

    while True:
        options = [bareoption.copy() for i in range(num_options)]
        for categ,classes in categories.items():
            chosen = set()
            invalid = False
            for o in options:
                # if the number of available classes for the option is
                # less than the options we are generating, allow duplicates
                available = set(classes) - check_bad_combos(bad_combos,o,categories)
                if len(available) == 0: 
                    # print(o)
                    invalid = True
                    print('hi')
                    break
                else:
                    attr = choice(list(available))
                    # print("bye")
                    # print(options)
                    # print(categ,attr)
                if invalid:
                    break
                chosen.add(attr)
                o[categ] = attr
            if invalid:
                break
            
            # print(invalid)
        if not invalid: break
        # quit()
        
    # quit()
    # now generating chances
    if not surv_factors:
        for o in options:
            wout = make_chance(1,40)
            wi = make_chance(1,50)
            o['survival without jacket'] = str(wout)+'%'
            o['survival with jacket'] = str(wout + wi) + '%'
    else:
        for o in options:
            wth,wout = calc_surv(surv_factors,o,categories)
            o['survival with jacket'] = wth
            o['survival without jacket'] = wout
    s = []
    for o in options:
        oo = o.copy()        
        s.append(form_table(oo,explanation))
    return s,options

def makestory_focus(categories,bad_combos,num_options,focus,surv_factors=None,explanation=None):    
    goodset = False
    options = [{} for i in range(num_options)]
    
    while not goodset:
        chosen = set()
        for o in options:            
            if 'survival' in focus:
                wout = make_chance(1,40)
                wit = make_chance(wout,90)
                o['survival without jacket'] = str(wout)+'%'
                o['survival with jacket'] = str(wit)+'%'
            else: 
                classes = categories[focus]
                if len(classes) < num_options:
                    val = choice(classes)
                else: val = choice(list(set(classes)-chosen))
                chosen.add(val)
                o[focus] = val    
        
        if not 'survival' in focus:
            wout = make_chance(1,40)
            wit = make_chance(wout,90)
            for o in options:
                o['survival without jacket'] = str(wout)+'%'
                o['survival with jacket'] = str(wit)+'%'
        for categ,classes in categories.items():
            if categ != focus:
                notallowed = set()
                for o in options:
                    notallowed |= check_bad_combos(bad_combos,o,categories)
                avail = list(set(classes)-notallowed)
                if categ in ['income level','education level']:
                    avail.append('N/A')
                if not avail:
                    goodset = False
                    break
                attr = choice(avail)
                for o in options: 
                    print
                    o[categ] = attr
                goodset = True

    s = []
    for o in options:
        s.append(form_table(o,explanation))
    return s,options

def save_attributes(filename, attr_ls):
    pfile = open(filename,'wb')
    pickle.dump(attr_ls,pfile)
    pfile.close()

# this function will return a set of classes the given combo cannot have
def check_bad_combos(bad_combos, combo, data):
    not_allowed = set()

    allowed_feats = ['number of dependents','income level']

    for x,cls in combo.items():
        if x in allowed_feats:
            continue
        if cls in bad_combos:
            if bad_combos[cls]['categories']:
                for c in bad_combos[cls]['categories']:
                    not_allowed |= set(data[c])
            if bad_combos[cls]['classes']:
                not_allowed |= set(bad_combos[cls]['classes'])
    return not_allowed

def parse_categories(data):
    cate = data.pop('categories')
    good_categ = {}
    for c,l in cate.items():
        good_categ[c] = list(l.values())
    return good_categ

def parse_bad_combo(data, categories):
    bc = data.pop('bad combo')
    bad_combos = {}
    for b,c in bc.items():
        bad_combos[b] = {}
        bad_combos[b]['categories'] = c['categories']
        bad_combos[b]['classes'] = []
        if c['classes']:
            for cat,ids in c['classes'].items():
                for i in ids:
                    bad_combos[b]['classes'].append(categories[cat][int(i)])
    return bad_combos

def form_table(option,explanation=None):
    t = '<table>'
    airplane = bool(explanation)
    
    ordered = sorted(option.keys())
    for k in ordered:
        v = option[k]
        if k == '💓' or k == '👥':
            t += '<tr><th style="font-size:large;">' + k + '</th>'
        else:
            if airplane:
                t += '<tr><th style="border-right:0px white">' + k + '</th>'
                t += '<td style="border-left:0px white;width:15px">'
                t += '<span style="cursor:pointer;" title="' + explanation[k] +'"><sup>💡</sup></span>'
                t += '</td>'
            else:
                t += '<tr><th>' + k + '</th>'
        # if type(v) == str: t += '<td>' + v + '</td></tr>'
        # else: t += '<td>' + str(v) + '%</td></tr>'

        t += '<td>' + str(v) + '</td></tr>'
        # names += '<th>' + k + '</th>'
        # if type(v) == str: values += '<td>' + v + '</td>'
        # else: values += '<td>' + str(v) + '%</td>'
    # t = '<table><tr>' + names + '</tr><tr>' + values + '</tr></table>'
    t += '</table>'
    return t

def form_citytable(cities):
    t = '<table style=\"width:250px\">'
    t += '<tr><th>' + 'Region' + '</th><th>' + 'Population size' + '</th></tr>'
    for c,p in cities.items():
        t += '<tr><td style="text-align:center">' + c + '</td><td style="text-align:center">' + str(p) + '</td></tr>'
    t += '</table>'
    return t

def form_sentence_random(option):
    s = 'A '
    s += option['gender'] + ' '
    s += option['age'] + ' '
    if option['career'] != 'N/A': s += option['career'] + ' '
    s += option['health']
    if option['purpose of trip'] != 'N/A': s += ' ' + option['purpose of trip']
    s += '. They would survive with a chance of ' + str(option['with'])
    s += '% with the jacket and with a chance of ' + str(option['without'])
    s += '% without it.'
    return s

def form_sentence_focused(option):
    # print(option)
    s = str(option['age']) + ' year old '
    if 'gender' in option: s += option['gender'] + ' '
    if 'purpose of trip' in option: s += option['purpose of trip']
    if 'career' in option: s += option['career']
    if option['focus'] == 'survival':
        s += 'travelling with ' + option['relationship'] + ' '
        s += option['purpose']
    if 'survival' in option:
        s += ' who would survive with a chance of ' + str(option['survival']['with']) +'%'
        s += ' with the rescue jacket'
        s += ' and with a chance of ' + str(option['survival']['without']) +'%'
        s += ' without the rescue jacket.'
    else: s += ' who would ' + option['survival'] + '.'
    return s

def calc_surv(surv_factors,option,data):
    wi_chance,wo_chance = 0,0
    health = option['health']
    a = str(data['age'].index(option['age']))
    h = str(data['health'].index(option['health']))

    afac = surv_factors['age'][a]
    hfac = surv_factors['health'][h]

    # doing age factor first
    # for without chance first
    wo = afac['without']
    raw_wo = make_chance(int(wo[0]),int(wo[1]))

    # now for with chance. check if dependent on without first
    wi = afac['with']
    if wi[0]=='w/o': raw_wi = make_chance(raw_wo,int(wi[1]))
    else: raw_wi = make_chance(int(wi[0]),int(wi[1]))

    while raw_wi <= raw_wo:
        if wi[0]=='w/o': raw_wi = make_chance(raw_wo,int(wi[1]))
        else: raw_wi = make_chance(int(wi[0]),int(wi[1]))

    # now for health factor
    h_mult = make_chance(float(hfac['mult'][0]) * 1000, float(hfac['mult'][1]) * 1000)/float(1000)

    w_chance = int(h_mult * raw_wi)
    wo_chance = int(h_mult * raw_wo)

    return w_chance,wo_chance

def make_chance(low, high, not_allowed=[],inc=1):
    # making chance in increments of 5
    val = low + randint(0,(high-low)/inc) * inc
    while val in not_allowed:
        val = low + randint(0,(high-low)/inc) * inc
    return val

if __name__ == '__main__':
    main()
