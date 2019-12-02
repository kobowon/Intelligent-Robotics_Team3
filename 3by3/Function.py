import numpy as np
from math import pow

class class_job:
    def __init__(self):
        self.j1_order = 0
        self.j2_order = 0
        self.j3_order = 0
        self.job_accomplish = 0
        self.job_table = np.array([[[0, 3], [1, 3], [2, 3]], [[0, 2], [2, 3], [1, 4]], [[1, 3], [0, 2], [2, 1]]])

#map[machine_idx, time] = job_idx
        
#time에 machine이 busy한지 [1,1,1]
def machine_busy(map, time): 
    busy_table = np.zeros([1, 3])
    for m_index in range(0, 3):
        if map[m_index, time] != 0:
            busy_table[0, m_index] = 1
    return busy_table

#time에 job이 busy한지 [1,1,1]
def job_busy(map, time):# [1, 1, 1] time에 job
    busy_table = np.zeros([1, 3])
    for m_index in range(0, 3):
        for j_index in range(0, 3):
            #특정 time에 map의 어떤 machine에라도 job이 할당 되어 있으면 해당 job에 대한 busy_table이 1 
            if map[m_index, time] == j_index + 1:
                busy_table[0, j_index] = 1
    return busy_table

#한 종류의 job을 특정 machine에 할당
def occupy1_job(map, time, job, job_type):
    #m_index : 머신
    #t_setp : 할당 기간
    m_index, t_step = job[0], job[1]
    job_busy_table = job_busy(map, time)
    machine_busy_table = machine_busy(map, time)
    #할당하고 싶은 job이 이미 특정 머신에 할당되어 있거나, job을 할당하려는 머신이 busy하면
    if job_busy_table[0, job_type] == 1 or machine_busy_table[0, m_index] == 1:
        return map
    #해당 job_type에 대응하는 job이 어떤 머신에도 할당되지 않았고, 할당하려는 머신도 idle하면
    #머신의 time시점부터 t_step동안 job을 (map에) 할당
    for i in range(time, time + t_step):
        map[m_index, i] = job_type + 1
    return map

#두 종류의 job을 각 머신(job[0])에 t_step(job[1])만큼 할당 
def occupy2_job(map, time, job1, job1_type, job2, job2_type):
    m1_index, t1_step = job1[0], job1[1]
    m2_index, t2_step = job2[0], job2[1]
    job_busy_table = job_busy(map, time)
    machine_busy_table = machine_busy(map, time)
    if job_busy_table[0, job1_type] == 1 or job_busy_table[0, job2_type] == 1 or machine_busy_table[0, m1_index] == 1 \
            or machine_busy_table[0, m2_index] == 1 or m1_index == m2_index:
        return map
    for i in range(time, time + t1_step):
        map[m1_index, i] = job1_type + 1
    for i in range(time, time + t2_step):
        map[m2_index, i] = job2_type + 1
    return map

#세 종류의 job을 각 머신(job[0])에 t_step(job[1])만큼 할당
def occupy3_job(map, time, job1, job1_type, job2, job2_type, job3, job3_type):
    m1_index, t1_step = job1[0], job1[1]
    m2_index, t2_step = job2[0], job2[1]
    m3_index, t3_step = job3[0], job3[1]
    job_busy_table = job_busy(map, time)
    machine_busy_table = machine_busy(map, time)
    if job_busy_table[0, job1_type] == 1 or job_busy_table[0, job2_type] == 1 or machine_busy_table[0, m1_index] == 1 \
            or machine_busy_table[0, m2_index] == 1 or job_busy_table[0, job3_type] == 1 or machine_busy_table[0, m3_index] == 1 \
            or m1_index == m2_index or m1_index == m3_index or m2_index == m3_index:
        return map
    for i in range(time, time + t1_step):
        map[m1_index, i] = job1_type + 1
    for i in range(time, time + t2_step):
        map[m2_index, i] = job2_type + 1
    for i in range(time, time + t3_step):
        map[m3_index, i] = job3_type + 1
    return map

#action이 1인 곳의 첫 번째 index 반환
#one_hot encoding형태의 action 상에서 action_type을 뽑아내는 용도
def action_idx(action):
    for i in range(0, 7):
        if action[0, i] == 1:
            return i

#idx만 1이고 나머지가 0인 사이즈 7벡터 반환
def one_hot(idx):
    hot = np.zeros([1, 7])
    hot[0, idx] = 1
    return hot

#job_table = np.array([[[0/machine, 3/duration], [1, 3], [2, 3]]/job 1, [[0, 2], [2, 3], [1, 4]]/job2, [[1, 3], [0, 2], [2, 1]/job3]])
def action_job(map, time, class_job, action):
    #one hot encoding action 에서 action type을 가져오기
    #action_type = action_idx(action)
    action_type = action
    #왜 하는걸까 -bowonko
    #machine,time = job
    map_o = np.copy(map)

    #action type : 0,1,2,3,4,5,6,7 
    '''
    0 : job 1에 assign
    1 : job 2에 assign
    2 : job 3에 assign
    
    3: job 1,2에 assign
    4: job 1,3에 assign
    5: job 2,3에 assign
    
    6:job1,2,3에 assign
    
    단, job들을 동시에 하나의 machine에 asssgin하는 건 occupy 함수에서 막음
    '''
    
    #action_type에 따라서 머신이 어떤 job을 할당할지 결정된다.
    #class_job.job table 0 or 1 or 2 [job 하나를 한 머신에 할당]
    if action_type == 0 and class_job.j1_order != 3:
        #clss_job.job_table[0,0,:] : [0, 3] => machine_index, duration : 
        
        #from time, class_job.job_table[0, class_job.j1_order, :] == [machine, duration], job_type = 0
        map = occupy1_job(map, time, class_job.job_table[0, class_job.j1_order, :], 0)
        
        #map 전체 원소 비교 - occupy를 했는데 map에 assign된 job이 없다면에 대한 에러처리
        if not np.all(map == map_o):
            #처리 했으니 job1의 다음 대상을 처리
            class_job.j1_order += 1
    elif action_type == 1 and class_job.j2_order != 3:
        map = occupy1_job(map, time, class_job.job_table[1, class_job.j2_order, :], 1)
        if not np.all(map == map_o):
            class_job.j2_order += 1
    elif action_type == 2 and class_job.j3_order != 3:
        map = occupy1_job(map, time, class_job.job_table[2, class_job.j3_order, :], 2)
        if not np.all(map == map_o):
            class_job.j3_order += 1
    
    #class_job.job table 0, 1 or 0,2 or 1,2 [job 2개를 2개의 머신에 할당]        
    elif action_type == 3 and class_job.j1_order != 3 and class_job.j2_order != 3:
        map = occupy2_job(map, time, class_job.job_table[0, class_job.j1_order, :], 0,
                    class_job.job_table[1, class_job.j2_order, :], 1)
        if not np.all(map == map_o):
            class_job.j1_order += 1
            class_job.j2_order += 1
    elif action_type == 4 and class_job.j1_order != 3 and class_job.j3_order != 3:
        map = occupy2_job(map, time, class_job.job_table[0, class_job.j1_order, :], 0,
                    class_job.job_table[2, class_job.j3_order, :], 2)
        if not np.all(map == map_o):
            class_job.j1_order += 1
            class_job.j3_order += 1
    elif action_type == 5 and class_job.j2_order != 3 and class_job.j3_order != 3:
        map = occupy2_job(map, time, class_job.job_table[1, class_job.j2_order, :], 1,
                    class_job.job_table[2, class_job.j3_order, :], 2)
        if not np.all(map == map_o):
            class_job.j2_order += 1
            class_job.j3_order += 1
    
    #class_job.job table 0, 1, 2 [job 3개를 3개의 머신에 할당]
    elif action_type == 6 and class_job.j1_order != 3 and class_job.j2_order != 3 and class_job.j3_order != 3:
        map = occupy3_job(map, time, class_job.job_table[0, class_job.j1_order, :], 0,
                    class_job.job_table[1, class_job.j2_order, :], 1,
                    class_job.job_table[2, class_job.j3_order, :], 2)
        if not np.all(map == map_o):
            class_job.j1_order += 1
            class_job.j2_order += 1
            class_job.j3_order += 1
    return map


def show_map(map):
    for i in range(3):
        for j in range(30):
            print(int(map[i, j]), end =" | ")
        print("\n")


def makespan(map):
    #각 머신이 얼마나 job을 처리했는가 - 각 머신들 중에서 최대로 job을 수행한 기간을 반환
    span = np.zeros([1, 3])
    for i in range(3):
        for j in range(30): 
            #29의 map 상에서 0이 아니라면 어떤 job이 할당되어 있다는 것이고 30의 step을 다 수행했다는 것 
            if not map[i, 29-j] == 0:
                #i : machine
                span[0, i] = 30 - j
                break
    return np.amax(span)


#t >= span(항상 성립)
def throughput(map, t, job):
    #최대 수행 기간
    span = makespan(map)
    if t==0:
        return 0.0
    #job이 다 완료됐고, 최대 수행 길이가 현재 시간보다 짧을 때 즉 일을 현재 시점에서 다 끝냈을 때
    if t > span and job.j1_order == 3 and job.j2_order == 3 and job.j3_order == 3:
        #map에서 전체 머신이 수행한 양/머신들 중 최대 수행량
        return np.count_nonzero(map[:, 0: t])/(span//2)

    else:# t < span(이런 경우는 X)  끝나지 않았으면 
        return np.count_nonzero(map[:, 0: t])/(t)  #pow(t,2)


def map_to_observation(map, t, job):
    span = makespan(map)
    m_busy_table = machine_busy(map, t)
    j_busy_table = job_busy(map, t)
    #정규화
    order = np.array([[job.j1_order/3, job.j2_order/3, job.j3_order/3]])
    #throughput
    tp = throughput(map, t, job)/2
    observation = np.append(m_busy_table, j_busy_table)# 3+3
    observation = np.append(observation, order)# 3
    observation = np.append(observation, tp)# 1
    
    observation = np.reshape(observation, [1, 10])# 3+3+3+1
    
    return observation #machine_busy_table, job_busy_table, job_order, throughput




