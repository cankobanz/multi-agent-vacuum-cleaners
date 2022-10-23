# multi-agent-vacuum-cleaners
## Reference: This is a school homework. Below explanation is made by the instructor of CmpE 540 in Bogazici University 2021-2022 Spring  
Minimax algorithm and alpha-beta pruning are applied to solve competing vacuum cleaners that want to clean a room from dirts.  


### RUN CODE
python <main.py> <search-type > <init-file> <n-actions>
where
- for <search-type> :
o min-max (no pruning)  
o alpha-beta (pruning in MAX and MIN nodes)  
- <n-actions> determines the depth of the search tree:  
 Eg. Suppose there are 3 opponent vacuum cleaners which all act optimal:  
o If <n-actions> is 5, the search will be as follows: MAX acts, MIN1, MIN2, MIN3 acts, MAX acts, and
the search stops, and the utility values after the second MAX

Problem Description
The environment is as follows:
- The environment is NxM grid world.
- Each grid in the environment might contain:  
o Vacuum cleaner (our agent)  
o Enemy vacuum cleaners  
o Obstacles that avoid entering to that grid. There is not dirt in the obstacle with grid.  
o One dirt  
- The vacuum cleaners have 6 actions:  
o left, right, up, down moves the cleaner one grid, unless that grid is an obstacle.  
o suck action that sucks one dirt.  
o stop action does nothing.  
§ The environment, agent type, locations of the obstacles, dirt, vacuum cleaners (our agent and other agents) will be provided in a text file.  
§ Tie-breaker:  
o If required, the precedence used as a tie-breaker is as follows: left, right, down, up, stop, suck  
§ Opponent vacuum cleaners, which are numbered with even digits, move randomly  
§ Opponent vacuum cleaners, which are numbered with odd digits, move optimally  
§ Your vacuum cleaner starts first, then other vacuum cleaners (ordered by their digits) move next to each other.  
Utility function:  
The utility value at any node is calculated as follows:  
- If your vacuum cleaner is in the same grid with one of the any other opponent, utility is set to -100 and the episode ends.  
- Otherwise, utility = (the number of dirts cleaned by your cleaner – the number of dirts cleaned by your opponents)  

Example input is like:  
![image](https://user-images.githubusercontent.com/81170575/197393568-80c70c55-30f6-400e-9112-a34ec58579d0.png)  
where  
o x corresponds to obstacles  
o c corresponds to your vacuum cleaner  
o each <digit> corresponds to one of your opponents where  
§ even <digit> opponents move randomly  
§ odd <digit> opponents move optimally  
o . (dot) corresponds to the dirt  
  
Output:  
§ After running the search, you need to print out the following (to standard output):  
Action: <action>  
Value: <value>  
Util calls: <n-util-calls>  
where  
• <action> is the optimal action of your agent in its first move  
• <value> is the (expected) minimax value of the root node  
• <n-util-calls> is the number of calls for utility function  
