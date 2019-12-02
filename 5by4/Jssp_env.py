import gym
from gym import spaces
from Function import *

#환경 environment
class JsspEnv(gym.Env):
    metadata = {'render.modes': ['human']}  # what's mean?

    def __init__(self):
        self.action_space = spaces.Discrete(15)
        #self.observation_space = spaces.Box(low=0, high=1, shape=(1, 10))
        self.job = None
        self.map = None
        self.state = None
        #현재 time
        self.t = None
    
    #state 반환
    def reset(self):
        self.job = class_job()
        #job이 3개 time step이 30개
        self.map = np.zeros([5, 30])
        self.t = 0
        self.state = map_to_observation(self.map, self.t, self.job)
        #m_busy_table + j_busy_table + order + tp = state
        return self.state

    def step(self, action):
        #action_job(map, time, class_job, action)
        self.map = action_job(self.map, self.t, self.job, action) #action_job(map, time, class_job, action)
        self.state = map_to_observation(self.map, self.t, self.job)
        self.t += 1
        span = makespan(self.map)

        #일을 다 끝냈고, 제한시간안에 처리 했으면
        #span : 머신들의 job를 처리한 최대 시각 머신1 :3 머신2 : 5 머신3 :1 -> span : 5 
        LIMIT_TIME = 25
        if self.t > span and self.job.j1_order == 3 and self.job.j2_order == 3 and self.job.j3_order == 3 and self.job.j4_order == 2 :
            reward = 150
            done = bool(1)
       
        elif self.t == LIMIT_TIME:#끝남
            reward = 0
            done = bool(1)
            
        else: #아직 안 끝남
            REWARD_WEIGHT = 5
            reward = throughput(self.map, self.t, self.job)*REWARD_WEIGHT
            done = bool(0)

        return self.state, reward, done, {}

    def render(self, mode='human'):
        show_map(self.map)
        
        