import os
import itertools
# from matplotlib import pyplot as plt
import math

class experiment:
    def __init__(self, name: str, problems: set, setting: set, mode: set):
        self.name     = name
        self.problems = problems
        self.setting  = setting
        self.mode     = mode
        self.all_exps = set(itertools.product(self.problems, self.setting, self.mode))
        self.data_dict = {}
        
    def setting_name(self, s):
        if s == "-p false -l both":
            return "none"
        elif s == "-p true -l fmutex":
            return "fmutex"
        elif s == "-p true -l reachable":
            return "reach"
        else:
            return "both"
        
    def make_exp_dir(self, dir_name: str):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            
    def run_experiment_miconic(self, timeout: int, dir_name: str):
        timestep = "1:30:1"
        
        for p, s, m in self.all_exps:
            p_num = int(p[7:])
            if p_num > 7:
                timestep = "30:60:5"
            elif p_num > 4 and p_num <= 7:
                timestep = "16:32:2"

            timeout_str = "timeout " + str(timeout) + " "
            py_file_str = "python3 -u planner.py "
            domain_str = "benchmarks/" + self.name + "/domain.pddl "
            problem_str = "benchmarks/" + self.name + "/" + p + ".pddl "
            temp_str   = "temp "
            step_str = timestep + " " # 1:30:1 "
            mode_str = "-x " + m + " "
            setting_str = s + " -r true "
            other_str = "-q ramp | tee "+ dir_name + "/" + self.name + "-" + p[7:] + "-" + m[0] +"-" + self.setting_name(s)
            
            commend = timeout_str + py_file_str + domain_str + problem_str + temp_str + step_str + mode_str + setting_str + other_str
            # print(commend)
            os.system(commend)
    
    def run_experiment_blocks(self, timeout: int, dir_name: str):
        timestep = "1:30:1"
        
        for p, s, m in self.all_exps:
            p_num = int(p[7:])
            if p_num < 7:
                timestep = "1:30:1"
            elif p_num >= 7 and p_num < 10:
                timestep = "15:36:3"
            elif p_num >= 10:
                timestep = "30:60:5"

            timeout_str = "timeout " + str(timeout) + " "
            py_file_str = "python3 -u planner.py "
            domain_str = "benchmarks/" + self.name + "/domain.pddl "
            problem_str = "benchmarks/" + self.name + "/" + p + ".pddl "
            temp_str   = "temp "
            step_str = timestep + " " # 1:30:1 "
            mode_str = "-x " + m + " "
            setting_str = s + " -r true "
            other_str = "-q ramp | tee "+ dir_name + "/" + self.name + "-" + p[7:] + "-" + m[0] +"-" + self.setting_name(s)
            
            commend = timeout_str + py_file_str + domain_str + problem_str + temp_str + step_str + mode_str + setting_str + other_str
            # print(commend)
            os.system(commend)
            
    def run_experiment_rovers(self, timeout: int, dir_name: str):
        timestep = "1:30:1"
        
        for p, s, m in self.all_exps:
            p_num = int(p[7:])
            if p_num > 7:
                timestep = "30:60:5"
            elif p_num > 4 and p_num <= 7:
                timestep = "16:32:2"

            timeout_str = "timeout " + str(timeout) + " "
            py_file_str = "python3 -u planner.py "
            domain_str = "benchmarks/" + self.name + "/domain.pddl "
            problem_str = "benchmarks/" + self.name + "/" + p + ".pddl "
            temp_str   = "temp "
            step_str = timestep + " " # 1:30:1 "
            mode_str = "-x " + m + " "
            setting_str = s + " -r true "
            other_str = "-q ramp | tee "+ dir_name + "/" + self.name + "-" + p[7:] + "-" + m[0] +"-" + self.setting_name(s)
            
            commend = timeout_str + py_file_str + domain_str + problem_str + temp_str + step_str + mode_str + setting_str + other_str
            # print(commend)
            os.system(commend)
            
    def collect_data(self, dir_name: str):
        for p, s, m in self.all_exps:
            file_str = self.name + "-" + p[7:] + "-" + m[0] +"-" + self.setting_name(s)
            p_num = int(p[7:])
            if p_num not in self.data_dict:
                self.data_dict[p_num] = {}
            with open(dir_name + "/" + file_str, 'r') as f:  
                lines = f.readlines() 
                last_line = lines[-2]
                if "Total time:" in last_line:
                    self.data_dict[p_num][m[0] +"-" + self.setting_name(s)] = float(last_line[12: len(last_line) - 2])
                else:
                    self.data_dict[p_num][m[0] +"-" + self.setting_name(s)] = 101
                                
    def create_mode_compare_graph(self):
        x_problems = sorted(list(self.data_dict.keys()))
        
        y_modeP_settingBoth = [math.log2(self.data_dict[x]["p-both"]) + 2 for x in x_problems]
        y_modeS_settingBoth = [math.log2(self.data_dict[x]["s-both"]) + 2 for x in x_problems]
        
        y_modeP_settingFmutex = [math.log2(self.data_dict[x]["p-fmutex"]) + 2 for x in x_problems]
        y_modeS_settingFmutex = [math.log2(self.data_dict[x]["s-fmutex"]) + 2 for x in x_problems]
        
        y_modeP_settingReach = [math.log2(self.data_dict[x]["p-reach"]) + 2 for x in x_problems]
        y_modeS_settingReach = [math.log2(self.data_dict[x]["s-reach"]) + 2 for x in x_problems]
        
        y_modeP_settingNone = [math.log2(self.data_dict[x]["p-none"]) + 2 for x in x_problems]
        y_modeS_settingNone = [math.log2(self.data_dict[x]["s-none"]) + 2 for x in x_problems]
        
        fig      = plt.figure(figsize=(24, 12))
        
        subplot1 = fig.add_subplot(2,2,1) 
        subplot2 = fig.add_subplot(2,2,2) 
        subplot3 = fig.add_subplot(2,2,3) 
        subplot4 = fig.add_subplot(2,2,4)
        
        subplot1.set_title("mode comparison - both")
        subplot1.set_xlabel("problem number")
        subplot1.set_ylabel("log(time)")
        subplot2.set_title("mode comparison - fmutex")
        subplot2.set_xlabel("problem num")
        subplot2.set_ylabel("log(time)")
        subplot3.set_title("mode comparison - reach")
        subplot3.set_xlabel("problem number")
        subplot3.set_ylabel("log(time)")
        subplot4.set_title("mode comparison - none")
        subplot4.set_xlabel("problem num")
        subplot4.set_ylabel("log(time)")
        
        subplot1.plot(x_problems, y_modeP_settingBoth, linestyle='-', marker='o', color = 'g', label = "p-both")
        subplot1.plot(x_problems, y_modeS_settingBoth, linestyle='-', marker='*', color = 'b', label = "s-both")
        
        subplot2.plot(x_problems, y_modeP_settingFmutex, linestyle='-', marker='o', color = 'g', label = "p-fmutex")
        subplot2.plot(x_problems, y_modeS_settingFmutex, linestyle='-', marker='*', color = 'b', label = "s-fmutex")
        
        subplot3.plot(x_problems, y_modeP_settingReach, linestyle='-', marker='o', color = 'g', label = "p-reach")
        subplot3.plot(x_problems, y_modeS_settingReach, linestyle='-', marker='*', color = 'b', label = "s-reach")
        
        subplot4.plot(x_problems, y_modeP_settingNone, linestyle='-', marker='o', color = 'g', label = "p-none")
        subplot4.plot(x_problems, y_modeS_settingNone, linestyle='-', marker='*', color = 'b', label = "s-none")
        
            # width = 0.2
            #
            # subplot1.bar(x_problems, y_modeP_settingBoth, width, alpha = 0.9, label= "p-both")
            # subplot1.bar([x + width for x in x_problems], y_modeS_settingBoth, width, alpha = 0.9, color= 'red', label = "s-both")
            # subplot1.set_xticks([x + width / 2 for x in x_problems])
            # subplot1.set_xticklabels(x_problems)

            # subplot2.bar(x_problems, y_modeP_settingFmutex, width, alpha = 0.9, label= "p-fmutex")
            # subplot2.bar([x + width for x in x_problems], y_modeS_settingFmutex, width, alpha = 0.9, color= 'red', label = "s-fmutex")
            # subplot2.set_xticks([x + width / 2 for x in x_problems])
            # subplot2.set_xticklabels(x_problems)    
            
            # subplot3.bar(x_problems, y_modeP_settingReach, width, alpha = 0.9, label= "p-reach")
            # subplot3.bar([x + width for x in x_problems], y_modeS_settingReach, width, alpha = 0.9, color= 'red', label = "s-reach")
            # subplot3.set_xticks([x + width / 2 for x in x_problems])
            # subplot3.set_xticklabels(x_problems) 
            
            # subplot4.bar(x_problems, y_modeP_settingNone, width, alpha = 0.9, label= "p-none")
            # subplot4.bar([x + width for x in x_problems], y_modeS_settingNone, width, alpha = 0.9, color= 'red', label = "s-none")
            # subplot4.set_xticks([x + width / 2 for x in x_problems])
            # subplot4.set_xticklabels(x_problems)   
            #
        subplot1.legend(loc = 'upper left')
        subplot2.legend(loc = 'upper left')
        subplot3.legend(loc = 'upper left')
        subplot4.legend(loc = 'upper left')
        plt.show()
        
    def create_setting_compare_graph(self):
        x_problems = sorted(list(self.data_dict.keys()))
        
        y_modeP_settingBoth = [math.log2(self.data_dict[x]["p-both"]) + 2 for x in x_problems]
        y_modeP_settingFmutex = [math.log2(self.data_dict[x]["p-fmutex"]) + 2 for x in x_problems]
        y_modeP_settingReach = [math.log2(self.data_dict[x]["p-reach"]) + 2 for x in x_problems]
        y_modeP_settingNone = [math.log2(self.data_dict[x]["p-none"]) + 2 for x in x_problems]
        
        y_modeS_settingBoth = [math.log2(self.data_dict[x]["s-both"]) + 2 for x in x_problems]
        y_modeS_settingFmutex = [math.log2(self.data_dict[x]["s-fmutex"]) + 2 for x in x_problems]
        y_modeS_settingReach = [math.log2(self.data_dict[x]["s-reach"]) + 2 for x in x_problems]
        y_modeS_settingNone = [math.log2(self.data_dict[x]["s-none"]) + 2 for x in x_problems]
        
        fig      = plt.figure(figsize=(24, 12))
        
        subplot1 = fig.add_subplot(1,2,1) 
        subplot2 = fig.add_subplot(1,2,2)
        
        subplot1.set_title("settings comparison - parallel")
        subplot1.set_xlabel("problem number")
        subplot1.set_ylabel("log(time)")
        subplot2.set_title("settings comparison - serial")
        subplot2.set_xlabel("problem num")
        subplot2.set_ylabel("log(time)")
        
        subplot1.plot(x_problems, y_modeP_settingBoth, linestyle='-', marker='o', color = 'g', label = "p-both")
        subplot1.plot(x_problems, y_modeP_settingFmutex, linestyle='-', marker='*', color = 'b', label = "p-fmutex")
        subplot1.plot(x_problems, y_modeP_settingReach, linestyle='-', marker='^', color = 'r', label = "p-reach")
        subplot1.plot(x_problems, y_modeP_settingNone, linestyle='-', marker='s', color = 'y', label = "p-none")
        
        subplot2.plot(x_problems, y_modeS_settingBoth, linestyle='-', marker='o', color = 'g', label = "s-both")
        subplot2.plot(x_problems, y_modeS_settingFmutex, linestyle='-', marker='*', color = 'b', label = "s-fmutex")
        subplot2.plot(x_problems, y_modeS_settingReach, linestyle='-', marker='^', color = 'r', label = "s-reach")
        subplot2.plot(x_problems, y_modeS_settingNone, linestyle='-', marker='s', color = 'y', label = "s-none") 
        
        subplot1.legend(loc = 'upper left')
        subplot2.legend(loc = 'upper left')
        plt.show()
                       
if __name__ == '__main__':
    
    run_which = "rovers"
    settings  = {"-p false -l both", "-p true -l fmutex","-p true -l reachable", "-p true -l both"}
    modes     = {"parallel"} # , "serial"
    
    if run_which == "miconic":
        dir_miconic = "log_miconic"
        miconic_name = "miconic"
        miconic_problem = {"problem01", "problem02","problem03", "problem04","problem05", "problem06","problem07", "problem08","problem09", "problem10"}
        
        exp_miconic = experiment(miconic_name, miconic_problem, settings, modes)
        exp_miconic.make_exp_dir(dir_miconic)
        exp_miconic.run_experiment_miconic(100, dir_miconic)
    #? -------------------------------------------------------------------------------------------
    elif run_which == "blocks":
        dir_blocks = "log_blocks"
        blocks_name = "blocks"
        blocks_problem = {"problem04", "problem05","problem06", "problem07","problem08", "problem09", "problem10", "problem11","problem12", "problem13"} #
        blocks_problem = {"problem06"}
        
        exp_blocks = experiment(blocks_name, blocks_problem, settings, modes)
        exp_blocks.make_exp_dir(dir_blocks)
        exp_blocks.run_experiment_blocks(100, dir_blocks)
    #? -------------------------------------------------------------------------------------------
    elif run_which == "rovers":
        dir_rovers = "log_rovers"
        rovers_name = "rovers"
        rovers_problem = {"problem01", "problem02","problem03", "problem04","problem05", "problem06","problem07", "problem08","problem09", "problem10"}
        
        exp_rovers = experiment(rovers_name, rovers_problem, settings, modes)
        exp_rovers.make_exp_dir(dir_rovers)
        exp_rovers.run_experiment_rovers(100, dir_rovers)
    else:
    # -------------------------------------------------miconic--------------------------------------------------------------------------------------------------------
        # dir_miconic = "log_miconic"
        # miconic_name = "miconic"
        # miconic_problem = {"problem01", "problem02","problem03", "problem04","problem05", "problem06","problem07", "problem08","problem09", "problem10"}
        
        # exp_miconic = experiment(miconic_name, miconic_problem, settings, modes)
        # exp_miconic.collect_data(dir_miconic)
        # exp_miconic.create_mode_compare_graph()
    # -------------------------------------------------blocks--------------------------------------------------------------------------------------------------------
        # dir_blocks = "log_blocks"
        # blocks_name = "blocks"
        # blocks_problem = {"problem04", "problem05","problem06", "problem07","problem08", "problem09", "problem10", "problem11","problem12", "problem13"} #
        
        # exp_blocks = experiment(blocks_name, blocks_problem, settings, modes)
        # exp_blocks.collect_data(dir_blocks)
        # exp_blocks.create_setting_compare_graph()
    # --------------------------------------------------rovers-------------------------------------------------------------------------------------------------------
        dir_rovers = "log_rovers"
        rovers_name = "rovers"
        rovers_problem = {"problem01", "problem02","problem03", "problem04","problem05", "problem06","problem07", "problem08","problem09", "problem10"}
        
        exp_rovers = experiment(rovers_name, rovers_problem, settings, modes)
        exp_rovers.collect_data(dir_rovers)   
        exp_rovers.create_mode_compare_graph()
