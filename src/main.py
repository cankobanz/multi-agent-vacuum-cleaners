from sys import maxsize
import sys

search_type = sys.argv[1]
initial_state_path = sys.argv[2]
depth = int(sys.argv[3])
file = open(initial_state_path)

input_file = file.readlines()

#search_type = 'alpha-beta'
#depth = 3
#input_file = [list('xxxxxxxxxx\n'),list('x        x\n'),list('x 2 x  . x\n'),list('xx.xx    x\n'),list('xxcxx  . x\n'),list('xxxxxxxxxx')]

def create_maze(raw):
    num_agent = 0
    agent_positions = {} 
    grid_world = []
    goal = []
    for r in range(len(raw)):
        line = []
        line_goal = []
        if raw[r][-1] == '\n':
            raw[r] = raw[r][:-1]

        grid_world.append(line)
        goal.append(line_goal)
        for c in range(len(raw[r])):
            line.append(raw[r][c])
            line_goal.append(raw[r][c])
            if raw[r][c] == 'c':
                grid_world[r][c] = ' '
                goal[r][c] = ' '
                agent_positions[raw[r][c]] = (r, c)
                num_agent +=1
            if raw[r][c].isdigit():
                agent_positions[raw[r][c]] = (r, c)
                grid_world[r][c] = ' '
                goal[r][c] = ' '
                num_agent +=1
            if raw[r][c] == '.':
                goal[r][c] = ' '
    return agent_positions, grid_world, goal, num_agent


def create_copy_map(data):
    copy_map = []
    for r in range(0, len(data)):
        line = []
        copy_map.append(line)
        for c in range(0, len(data[r])):
            line.append(data[r][c])
    return copy_map


def find_next_active_agent(agents, current_agent):
    agents.remove('c')
    agents.sort()
    agents.insert(0, 'c')

    current_agent = agents[(agents.index(current_agent) + 1) % len(agents)]

    return current_agent


class Node:
    def __init__(self, agent_positions, data, active_agent):
        self.data = create_copy_map(data)
        self.agent_positions = agent_positions
        self.action = None

        self.active_agent = active_agent
        self.active_location = self.agent_positions[self.active_agent]

        self.cleaned_dirts = self.create_cleaned_dirts()
        self.utility = None

        self.depth = None

        self.state = (self.agent_positions, self.data)

        self.parent = None
        self.children = None

    def isDirt(self):
        if self.data[self.active_location[0]][self.active_location[1]] == '.':
            return True
        else:
            return False

    def remove_dirt(self):
        position = self.parent.active_location
        self.data[position[0]][position[1]] = ' '

    def create_cleaned_dirts(self):
        cleaned_dirts = {}
        for agent in self.agent_positions.keys():
            cleaned_dirts.update({agent: 0})
        return cleaned_dirts

    def calculate_utility(self):
        #agent_position_list = self.agent_positions.values()
        #if len(agent_position_list) != len(set(agent_position_list)):
            #self.data = goal_state
            #return -100

        return self.cleaned_dirts['c'] - (sum(list(self.cleaned_dirts.values())) - self.cleaned_dirts['c'])


def find_children(current_node):
    current_r, current_c = current_node.active_location

    children = []

    dr = [0, 0, 1, -1, 0, 0]
    dc = [-1, 1, 0, 0, 0, 0]

    for i in range(0, 6):

        possible_r = current_r + dr[i]
        possible_c = current_c + dc[i]

        if possible_r < 0 or possible_c < 0:
            continue
        if possible_r >= len(current_node.data) or possible_c >= len(current_node.data[0]):
            continue
        if current_node.data[possible_r][possible_c] == 'x':
            continue

        child_agent_positions = {}
        for element in current_node.agent_positions.items():
            child_agent_positions.update({element[0]: element[1]})

        child_agent_positions[current_node.active_agent] = (possible_r, possible_c)
        child_data = create_copy_map(current_node.data)

        next_agent = find_next_active_agent(list(child_agent_positions.keys()), current_node.active_agent)

        child = Node(child_agent_positions, child_data, next_agent)

        for key, value in current_node.cleaned_dirts.items():
            child.cleaned_dirts.update({key: value})

        child.parent = current_node
        if i == 0:
            child.action = "left"
            children.append(child)
        elif i == 1:
            child.action = "right"
            children.append(child)
        elif i == 2:
            child.action = "down"
            children.append(child)
        elif i == 3:
            child.action = "up"
            children.append(child)
        elif i == 4:
            child.action = "stop"
            children.append(child)
        elif i == 5:
            child.action = "suck"
            if current_node.isDirt():
                child.cleaned_dirts[current_node.active_agent] += 1
                child.remove_dirt()
            children.append(child)

    return children


def minimax(state, depth, count_utility):
    
    agent_position_dict = state.agent_positions
    c_position = agent_position_dict['c']
    agent_position_dict.pop('c')
    agent_position_values = agent_position_dict.values()
    if c_position in agent_position_values:
        agent_position_dict['c'] = c_position
        state.utility = -100
        return state.utility, count_utility, state.action
    agent_position_dict['c'] = c_position
        
    if depth == 0 or state.state[1] == goal_state:
        count_utility += 1
        state.utility = state.calculate_utility()
        return state.utility, count_utility, state.action

    children = find_children(state)
    # MAX AGENT
    if state.active_agent == 'c':
        maxEval = -maxsize
        for child in children:
            evaluation, count_utility, _ = minimax(child, depth - 1, count_utility)
            if evaluation > maxEval:
                golden_child = child
            maxEval = max(maxEval, evaluation)
        return maxEval, count_utility, golden_child.action
    else:
        # MIN AGENT
        if int(state.active_agent) % 2 != 0:
            minEval = +maxsize
            for child in children:
                evaluation, count_utility, _ = minimax(child, depth - 1, count_utility)
                minEval = min(minEval, evaluation)
            return minEval, count_utility, state.action
        # RANDOM AGENT
        else:
            tot_utility = 0
            for child in children:
                evaluation, count_utility, _ = minimax(child, depth - 1, count_utility)
                tot_utility += evaluation
            tot_utility /= len(children)
            return tot_utility, count_utility, state.action


def alpha_beta_pruning(state, depth, alpha, beta, count_utility):
    agent_position_dict = state.agent_positions
    c_position = agent_position_dict['c']
    agent_position_dict.pop('c')
    agent_position_values = agent_position_dict.values()
    if c_position in agent_position_values:
        agent_position_dict['c'] = c_position
        state.utility = -100
        return state.utility, count_utility, state.action
        
    agent_position_dict['c'] = c_position
    
    if depth == 0 or state.state[1] == goal_state:
        count_utility += 1
        state.utility = state.calculate_utility()
        return state.utility, count_utility, state.action
    
    children = find_children(state)
    # MAX AGENT
    if state.active_agent == 'c':
        maxEval = -maxsize
        for child in children:
            evaluation, count_utility, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, count_utility)
            if evaluation > maxEval:
                golden_child = child
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, count_utility, golden_child.action
    else:
        # MIN AGENT
        if int(state.active_agent) % 2 != 0:
            minEval = +maxsize
            for child in children:
                evaluation, count_utility, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, count_utility)
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval, count_utility, state.action
        # RANDOM AGENT
        else:
            tot_utility = 0
            for child in children:
                evaluation, count_utility, _ = minimax(child, depth - 1, count_utility)
                tot_utility += evaluation
            tot_utility /= len(children)
            return tot_utility, count_utility, state.action


pos, maze, goal_state, num_agent = create_maze(input_file)
initial_node = Node(pos, maze, 'c')

if search_type == "min-max":
    value, n_util_calls, action = minimax(initial_node, depth*num_agent, 0)
    value = "{:.2f}".format(value)
    print("{} {} {}".format(action, value, n_util_calls))

if search_type == "alpha-beta":
    value, n_util_calls, action = alpha_beta_pruning(initial_node, depth*num_agent, -maxsize, +maxsize, 0)
    value = "{:.2f}".format(value)    
    print("{} {} {}".format(action, value ,n_util_calls))
