# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2021
# Authors: COMP3620 team

""" Student Details

    Student Name: Yixi Rao
    Student ID: u6826541
    Email: u6826541@anu.edu.au
    Date: 2021/05/18
"""

"""
    In this file you will implement some constraints which represent
    domain-specific control knowledge for the Logistics domain
    (benchmarks/logistics).

    These constraints will be used in addition to a standard flat encoding of
    the Logistics problem instances, without plan graph mutexes (which you are
    assumed to have completed while going through Exercises 1-6).

    Those constraints should make solving the problem easier. This may be at
    the cost of optimality. That is, your additional constraints may rule out
    some solutions to make planning easier -- for example, by restricting the
    way trucks and planes can move -- but they should preserve SOME solution
    (the problems might be very easy to solve if you added a contradiction, but
    wholly uninteresting!).

    Often control knowledge for planning problems is based on LTL (Linear
    Temporal Logic - https://en.wikipedia.org/wiki/Linear_temporal_logic) and
    you might get inspired by studying this.

    We do not expect you to implement an automatic compilation of arbitrary LTL
    into SAT, just some control knowledge rules for problems from the Logistics
    domain.

    As an example rule to get you started, you could assert that if a package
    was at its destination, then it cannot leave.

    That is you could iterate over the goal of the problem to find the
    propositions which talk about where the packages should end up and make
    some constraints asserting that if one of the corresponding fluents is true
    at step t then it must still be true at step t + 1

    You will be marked based on the correctness, inventiveness, and
    effectiveness of the control knowledge you devise.

    You should aim to make at least three different control rules. Feel free to
    leave (but comment out) rules which you abandon if you think they are
    interesting and want us to look at them.

    Use the flag "-e logistics" to select this encoding and the flag "-p false"
    to disable the plangraph mutexes.
"""


from strips_problem import Action, Proposition
from .basic import BasicEncoding
encoding_class = 'LogisticsEncoding'
import itertools


class LogisticsEncoding(BasicEncoding):
    """ An encoding which extends BasicEncoding but adds control knowledge
        specific for the Logistics domain.
    """

################################################################################
#                You need to implement the following methods                   #
################################################################################

    def make_control_knowledge_variables(self, horizon: int) -> None:
        """ Make the variable for the problem.

            NOTE#! Use the function self.new_cnf_code(step, name, object) to make
            whatever codes for CNF variables you need to make your control
            knowledge for the Logistics problem.

            You can make variables which mean anything if you can think of
            constraints to make that enforce that meaning. As an example, if
            you were making control logic for the miconics domain, you might
            make variables 
            which keep track if each passenger has ever been in an elevator and is now not.

            For a passenger p, and t > 0:
                was_boarded(p)@t <-> (-boarded(p)@t ^ (boarded(p)@t-1 v was_boarded(p)@t-1))

            For example, you might make a dictionary called
            self.was_boarded_at_t indexed by passenger names, where the values
            are lists where the ith index contains the cnf code for
            was_boarded(p)@i, which you got by calling 
            #! self.new_cnf_code(i, f"was_boarded({was_boarded.passenger})", was_boarded).

            You can see here that this is using an object called was_boarded
            which has an attribute "passenger" as the object. This might not be
            the simplest way, you might wish to just use a string instead of a
            more complicated object. For example, 
            #! self.new_cnf_code(i, f"was_boarded({passenger})", f"was_boarded({passenger})").

            You can then use these variables, along with the fluent and action
            variables to make your control knowledge.

            Note that the use of `make_control_knowledge_variables` is
            completely optional. You don't have to implement any code
            in this method. At the end of the day, the most important thing
            is to add new clauses in `make_control_knowledge`.
        """
        # self.new_cnf_code(0, f"was_boarded({2})", f"was_boarded({9})")
        pass

    def make_control_knowledge(self, horizon: int) -> None:
        """ This is where you should make your control knowledge clauses.
        
            If you are using the vscode, I highly recommend you to install the Better Comments extension(optional) because I use some 
            notations to categorise different types of definition, for example:
            #? this notation represents rule number e.g. Rule 3
            #* this notation represents control knowledge plain text definition
            #! this notaion represents the first order logic of control knowledge
            
            These clauses should have the type "control".
        """        
        # unload_act_dict = {}
        # fly_act_dict    = {}
        at_plane_objs         = {} # proposition "at plane pac" dictionnary indexed by its name
        at_truck_objs         = {} # proposition "at truck pac" dictionnary indexed by its name
        in_package_plane_objs = {} # proposition "in plane pac" dictionnary indexed by its name
        pac_Gloc              = {} # the package goal location dictionary indexed by the package
        
        airport_locs = set() # set of all airport locations
        all_locs     = set() # set of all locations
        all_pacs     = set() # set of all packages
        all_planes   = set() # set of all planes
        all_trunks   = set() # set of all trucks
        # initialization    
        for p in self.problem.propositions:
            if "at plane" in str(p):
                at_plane_objs[str(p)] = p
                all_planes.add(p.variables[0])
                airport_locs.add(p.variables[1])
                
            elif "in package" in str(p):
                all_pacs.add(p.variables[0])
                if "plane" in str(p):
                    in_package_plane_objs[str(p)] = p
                    
            elif "at truck" in str(p):
                at_truck_objs[str(p)] = p
                all_trunks.add(p.variables[0])
                all_locs.add(p.variables[1])
                
        #? Rule 1
        #* if a package was at its destination, then it cannot leave.
        #! any g: g in goal ^ g@t -> g@t+1
        
        for g in self.problem.goal:
            pac_Gloc[g.variables[0]] = g.variables[1]
            for s in range(0, horizon):
                g_int = self.proposition_fluent_codes[(g, s)]
                n_int = self.proposition_fluent_codes[(g, s + 1)]
                self.add_clause([-1 * g_int, n_int], "control")

        #? Rule 2 
        #* in a city, a truck(or an airplane) appears at one and only one location(or airport) in a time step
        #! at(truck, loc_x)@t -> (any loc_y: loc_x != loc_y) -at(truck, loc_y)@t 
        #! at(plane, loc_x)@t -> (any loc_y: loc_x != loc_y) -at(plane, loc_y)@t 
        # truck clauses
        for p_s, p_int in self.proposition_fluent_codes.items():
            if "at truck" in str(p_s):
                p_obj, step = p_s
                truck1 = p_obj.variables[0]
                t1_loc = p_obj.variables[1]
                for loc in all_locs:
                    if loc != t1_loc and "at " + truck1 + " " + loc in at_truck_objs:
                        t1_loc2_obj = at_truck_objs["at " + truck1 + " " + loc]
                        t1_loc2_int = self.proposition_fluent_codes[(t1_loc2_obj, step)]
                        # print(str(p_obj) + " | " + str(t1_loc2_obj))
                        self.add_clause([-1 * p_int, -1 * t1_loc2_int], "control")
        # airplane clauses
        for p_s, p_int in self.proposition_fluent_codes.items():
            if "at plane" in str(p_s):
                p_obj, step = p_s
                plane1 = p_obj.variables[0]
                p1_loc = p_obj.variables[1]
                for loc in airport_locs:
                    if loc != p1_loc and "at " + plane1 + " " + loc in at_plane_objs:
                        p1_loc2_obj = at_plane_objs["at " + plane1 + " " + loc]
                        p1_loc2_int = self.proposition_fluent_codes[(p1_loc2_obj, step)]
                        # print(str(p_obj) + " | " + str(p1_loc2_obj))
                        self.add_clause([-1 * p_int, -1 * p1_loc2_int], "control")
        
        #? Rule 3 
        #* Do not unload a package from an airplane if the airplane is not in the package goal city
        #! any plane, any loc, any pac: -correct_city(pac, loc)@t ^ at(plane, loc)@t ^ in(pac, plane)@t -> in(pac, plane)@t+1
        
        for pln, loc, pac in itertools.product(all_planes, airport_locs, all_pacs):
            if pac not in pac_Gloc:
                continue
            if pac_Gloc[pac][4] != loc[4]: # whether the package's goal city is the current plane's city
                for s in range(0, horizon - 1):
                    atPlane_int    = self.proposition_fluent_codes[(at_plane_objs["at " + pln + " " + loc], s)]
                    inPac_int      = self.proposition_fluent_codes[(in_package_plane_objs["in " + pac + " " + pln], s)]
                    inPac_next_int = self.proposition_fluent_codes[(in_package_plane_objs["in " + pac + " " + pln], s + 1)]
                    self.add_clause([-1 * atPlane_int, -1 * inPac_int, inPac_next_int], "control")
        
        #? Rule 4 (abandon)
        #* if the package is in the airplane, and the package is in the correct city, then the aeroplne will stay at that airport in next step for unloading 
        #! any plane, any loc, any pac: correct_city(pac, loc)@t ^ at(plane, loc)@t ^ in(pac, plane)@t -> at(plane, loc)@t+1
        
        # for pln, loc, pac in itertools.product(all_planes, airport_locs, all_pacs):
        #     if pac not in pac_Gloc:
        #         continue
        #     if pac_Gloc[pac][4] == loc[4]:
        #         for s in range(0, horizon - 1):
        #             atPlane_int = self.proposition_fluent_codes[(at_plane_objs["at " + pln + " " + loc], s)]
        #             inPac_int   = self.proposition_fluent_codes[(in_package_plane_objs["in " + pac + " " + pln], s)]
        #             atPlane_next_int = self.proposition_fluent_codes[(at_plane_objs["at " + pln + " " + loc], s + 1)]
        #             self.add_clause([-1 * atPlane_int, -1 * inPac_int, atPlane_next_int], "control")  
                    
                    
        
        #? Rule 5 (abandon):
        #* Do not move an airplane (FLY-AIRPLANE)
        #* if there is an object in the airplane (in ?obj ?airplane)
        #* that needs to be unloaded at that location. (UNLOAD-AIRPLANE)
        #! UNLOAD-AIRPLANE@t -> not FLY-AIRPLANE@t
        #! unload-airplane _ plane2 city4-2 -> not fly-airplane plane2 city4-2 _ 
                        
        #    
        # for act in self.problem.actions:
        #     act_name = act.name
        #     act_para = tuple(act.parameters)

        #     if act_name == "unload-airplane":
        #         pac, plane, loc = tuple(act.parameters)
                
        #         airport_locs.add(loc)
        #         all_pacs    .add(pac)
        #         all_planes  .add(plane)
                
        #         unload_act_dict[(pac, plane, loc)] = act
                
        #     elif act_name == "fly-airplane":
        #         fly_act_dict[act_para] = act
                
        # for unload_para, unload_obj in unload_act_dict.items():
        #     _, plane, loc1 = unload_para
            
        #     for pac, loc2 in itertools.product(all_pacs, airport_locs):
        #         if loc1 == loc2:
        #             continue
        #         else:
        #             for s in range(0, horizon):
        #                 unload_int = self.action_fluent_codes[(unload_obj, s)]
        #                 fly_int    = self.action_fluent_codes[(fly_act_dict[(plane, loc1, loc2)], s)]
        #                 self.add_clause([-1 * unload_int, -1 * fly_int], "control")
        #            

################################################################################
#                    Do not change the following method                        #
################################################################################

    def encode(self, horizon, exec_semantics, plangraph_constraints):
        """ Make an encoding of self.problem for the given horizon.

            For this encoding, we have broken this method up into a number
            of sub-methods that you need to implement.

           (LogisticsEncoding, int, str, str) -> None
        """
        super().encode(horizon, exec_semantics, plangraph_constraints)
        self.make_control_knowledge_variables(horizon)
        self.make_control_knowledge(horizon)
