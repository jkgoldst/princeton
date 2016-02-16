#!/usr/bin/python3
import sys
import json
import numpy

std_of_diff_between_e1_e2_payoffs = None

def std_of_diff(lst1, lst2):
    n1 = len(lst1)
    n2 = len(lst2)
    sum_of_squares1 = sum(map(lambda x:x*x,lst1))
    sum_of_squares2 = sum(map(lambda x:x*x,lst2))
    square_of_sums1 = sum(map(lambda x:x,lst1)) ** 2
    square_of_sums2 = sum(map(lambda x:x,lst2)) ** 2
    sdsquare1 = sum_of_squares1 - square_of_sums1 / n1
    sdsquare2 = sum_of_squares2 - square_of_sums2 / n2
    ssquare1 = sdsquare1 / (n1 - 1)
    ssquare2 = sdsquare2 / (n2 - 1)
    sigmasquare = ssquare1 / n1 + ssquare2 / n2
    res = numpy.sqrt(sigmasquare)
    res = numpy.around(res, 2)
    res = str(res)
    return res


def variance(l):
    average = sum(l) / len(l)
    result = sum((average - value) ** 2 for value in l) / len(l)
    return result


def generate_arr_of_subjects(subjects_arr):
    skip = True
    res = []
    res_d = {}
    for line in subjects_arr:
        if skip:
            skip = False
            continue
        skip = True
        d = json.loads(line)
        res.append(d)
        res_d[d['chosenDisplayName']] = d
    return res, res_d

def task1(subjects_arr):
    skip = True
    res = {}
    for line in subjects_arr:
        if skip:
            skip = False
            continue
        skip = True
        d = json.loads(line)
        subj = d.get('conditionGroup')
        if res.get(subj):
            res[subj] = res[subj] + 1
        else:
            res[subj] = 1
    output = open('1.csv', 'w')
    l = []
    for key in res:
        l.append(key)
    for i in range(len(l)):
        s = l[i]
        if s == None:
            s = 'None'
        output.write(s)
        if i < (len(l) - 1):
            output.write(',')
    output.write('\n')
    for i in range(len(l)):
        s = l[i]
        a = res.get(s)
        a = str(a)
        output.write(a)
        if i < (len(l) - 1):
            output.write(',')
    output.write('\n')

def generate_list_of_payoffs(responses_arr):
    arr = []
    for line in responses_arr:
        t = line.split(',')
        if len(t) > 4:
            break
        line = line.split(',')
        data = {
            'name': line[1],
            'payoff': line[3]
        }
        arr.append(data)
        


def generate_dict_of_payoffs(responses_arr):
    arr = []
    for line in responses_arr:
        t = line.split(',')
        if len(t) > 4:
            break
        line = line.split(',')
        data = {
            'name': line[1],
            'payoff': line[3]
        }
        arr.append(data)
    d1 = {}
    d = {}
    for item in arr:
        name = item['name']
        payoff = item['payoff']
        val = d.get(name)
        if val:
            d[name] = {
                'payoff_sum': int(val['payoff_sum']) + int(payoff),
                'n': val['n'] + 1
            }
        else:
            d[name] = {
                'payoff_sum': int(payoff),
                'n': 1
            }
        lst = d1.get(name)
        if not lst:
            lst = []
        else:
            lst = lst['payoffs']
        lst.append(float(payoff))
        d1[name] = {
            'payoffs': lst,
            'name': name
        }
    res = {}
    for key in d:
        val = d[key]
        mean = val['payoff_sum'] / val['n']
        res[key] = {
            'mean': mean
        }
    return res, d1


def task2(responses, subjects):
    d_payoffs, l_payoffs = generate_dict_of_payoffs(responses)
    arr_subjs = generate_arr_of_subjects(subjects)[0]
    output = open('2.csv', 'w')
    output.write('name,conditionGroup,mean_payoff\n')

    e1_n_total = 0
    e1_sum_total = 0
    e2_n_total = 0
    e2_sum_total = 0

    e1_list = []
    e2_list = []

    e1_payoffs_list = []
    e2_payoffs_list = []
    for item in arr_subjs:
        name = item['chosenDisplayName']
        cg = item['conditionGroup']
        if cg != 'E1' and cg != 'E2':
            continue
        mean = d_payoffs.get(name)
        if not mean:
            continue
        payoffs = l_payoffs.get(name)['payoffs']
        
        mean = mean['mean']
        output.write(name + ',' + cg + ',' +  str(mean) + '\n')
        if cg == 'E1':
            e1_n_total += 1
            e1_sum_total += mean
            e1_list.append(mean)
            e1_payoffs_list.extend(payoffs)
        if cg == 'E2':
            e2_n_total += 1
            e2_sum_total += mean
            e2_list.append(mean)
            e2_payoffs_list.extend(payoffs)
    e1_avg = e1_sum_total / e1_n_total
    e1_avg = "{:.2f}".format(e1_avg) 
    e2_avg = e2_sum_total / e2_n_total
    e2_avg = "{:.2f}".format(e2_avg) 
    output = open('2_avg_of_mean_payoff_for_e1_and_e2.csv', 'w')
    output.write('e1_avg,e2_avg\n')
    output.write(e1_avg + ',' + e2_avg + '\n')

    e1std = numpy.std(e1_list)
    e2std = numpy.std(e2_list)
    e1std = "{:.2f}".format(e1std) 
    e2std = "{:.2f}".format(e2std)
    output = open('e1_e2_mean_payoff_std.csv', 'w')
    output.write('e1_std,e2_std\n')
    output.write(e1std + ',' + e2std + '\n')

    output = open('2_std_of_all_payoffs.csv', 'w')
    e1std = numpy.std(e1_payoffs_list)
    e2std = numpy.std(e2_payoffs_list)
    e1std = "{:.2f}".format(e1std) 
    e2std = "{:.2f}".format(e2std)
    output.write('e1_std,e2_std\n')
    output.write(e1std + ',' + e2std + '\n')

    global std_of_diff_between_e1_e2_payoffs
    std_of_diff_between_e1_e2_payoffs = std_of_diff(e1_payoffs_list, e2_payoffs_list)
   

def task3(responses, subjects):
    dict_subjs = generate_arr_of_subjects(subjects)[1]
    arr = []
    for line in responses:
        t = line.split(',')
        if len(t) <= 4:
            continue
        obj = json.loads(line)
        if not obj.get('surveyName'):
            print(obj)
            break
        if obj['surveyName'] != 'Group Identity Questions':
            continue
        name = obj['username']
        a = dict_subjs.get(name)
        if not a:
            continue
        cg = a['conditionGroup']        
        if cg != 'C1' and cg != 'E1' and cg != 'E2' and cg != 'C2':
            continue
        arr.append(obj)

    output = open('3.csv', 'w')
    output.write('name,condition_group,mean_score\n')
    c1_sum_total = 0
    c1_n_total = 0
    c2_sum_total = 0
    c2_n_total = 0
    e1_sum_total = 0
    e1_n_total = 0
    e2_sum_total = 0
    e2_n_total = 0

    c1_list = []
    c2_list = []
    e1_list = []
    e2_list = []
    
    c1_q8_list = []
    c2_q8_list = []
    e1_q8_list = []
    e2_q8_list = []
    
    for item in arr:
        answers = item['surveyAnswers']
        total_score = 0
        n = 0
        q8_score = None
        for question in answers:
            if question == 'question8':
                q8_score = int(answers[question])
                continue
            total_score += int(answers[question])
            n += 1
        mean_score = total_score / n
        name = item['username']
        cg = dict_subjs[name]['conditionGroup']
        output.write(name + ',' + cg + ',' + str(mean_score) + '\n')
        if cg == 'E1':
            e1_sum_total += mean_score
            e1_n_total += 1
            e1_list.append(mean_score)
            e1_q8_list.append(q8_score)
        if cg == 'E2':
            e2_sum_total += mean_score
            e2_n_total += 1
            e2_list.append(mean_score)
            e2_q8_list.append(q8_score)            
        if cg == 'C1':
            c1_sum_total += mean_score
            c1_n_total += 1
            c1_list.append(mean_score)
            c1_q8_list.append(q8_score)
        if cg == 'C2':
            c2_sum_total += mean_score
            c2_n_total += 1
            c2_list.append(mean_score)
            c2_q8_list.append(q8_score)
    e1_avg = e1_sum_total / e1_n_total
    e1_avg = "{:.2f}".format(e1_avg) 
    e1_std = numpy.std(e1_list)
    e1_std = "{:.2f}".format(e1_std)

    e2_avg = e2_sum_total / e2_n_total
    e2_avg = "{:.2f}".format(e2_avg) 
    e2_std = numpy.std(e2_list)
    e2_std = "{:.2f}".format(e2_std)

    c1_avg = c1_sum_total / c1_n_total
    c1_avg = "{:.2f}".format(c1_avg) 
    c1_std = numpy.std(c1_list)
    c1_std = "{:.2f}".format(c1_std)

    c2_avg = c2_sum_total / c2_n_total
    c2_avg = "{:.2f}".format(c2_avg)
    c2_std = numpy.std(c2_list)
    c2_std = "{:.2f}".format(c2_std)

    output = open('3_avg_and_std.csv', 'w')
    output.write('e1_avg,e2_avg,c1_avg,c2_avg,e1_std,e2_std,c1_std,c2_std\n')
    output.write(e1_avg + ',' + e2_avg + ',' + c1_avg + ',' + c2_avg + ','
          + c1_std + ',' + e2_std + ',' + c1_std + ',' + c2_std + '\n')

    e1_q8_avg = "{:.2f}".format(numpy.average(e1_q8_list))
    e2_q8_avg = "{:.2f}".format(numpy.average(e2_q8_list))
    c1_q8_avg = "{:.2f}".format(numpy.average(c1_q8_list))
    c2_q8_avg = "{:.2f}".format(numpy.average(c2_q8_list))

    e1_q8_std = "{:.2f}".format(numpy.std(e1_q8_list))
    e2_q8_std = "{:.2f}".format(numpy.std(e2_q8_list))
    c1_q8_std = "{:.2f}".format(numpy.std(c1_q8_list))
    c2_q8_std = "{:.2f}".format(numpy.std(c2_q8_list))

    output = open('3_avg_and_std_for_question_8.csv', 'w')
    output.write('e1_avg,e2_avg,c1_avg,c2_avg,e1_std,e2_std,c1_std,c2_std\n')
    output.write(e1_q8_avg + ',' + e2_q8_avg + ',' + c1_q8_avg + ',' + c2_q8_avg
                 + ','
          + e1_q8_std + ',' + e2_q8_std + ',' + c1_q8_std + ',' + c2_q8_std + '\n')

    e1c1 = std_of_diff(e1_list, c1_list)
    e2c2 = std_of_diff(e2_list, c2_list)
    e1c1q8 = std_of_diff(e1_q8_list, c1_q8_list)
    e2c2q8 = std_of_diff(e2_q8_list, c2_q8_list)
    output = open('std_of_diff_between_means.csv', 'w')
    output.write('payoffs_e1_e2,scores_e1_c1,scores_e2_c2,scores_e1_c1_question8,scores_e2_c2_question8\n')
    output.write(std_of_diff_between_e1_e2_payoffs + ',' + e1c1 + ',' + e2c2 + ',' + e1c1q8 + ',' + e2c2q8 + '\n')

    

def run(responses, subjects):
    subjects = subjects.split('\n')
    subjects = subjects[1:]
    responses = responses.split('\n')
    responses = responses[1:]
    task1(subjects)
    task2(responses, subjects)
    task3(responses, subjects)


if __name__ == '__main__':
    a = std_of_diff([520, 460, 500, 470], [230, 270, 250, 280])
    if len(sys.argv) < 2:
        print("Usage: %s %s %s" % (sys.argv[0],
              'experimentResponses-survey.txt',
              'experimentSubjects-anonymized.txt'))
    responses = open(sys.argv[1]).read()
    subjects = open(sys.argv[2]).read()
    run(responses, subjects)
    print('Done!. results printed in: 1.csv, 2.csv, 3.csv, e1_e2_mean_payoff_std.csv, 3_avg_and_std.csv, 2_avg_of_mean_payoff_for_e1_and_e2.csv, 3_avg_and_std_for_question_8.csv, 2_std_of_all_payoffs.csv, std_of_diff_between_means.csv')
    
