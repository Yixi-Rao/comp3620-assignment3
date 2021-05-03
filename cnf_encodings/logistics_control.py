# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2021
# Authors: COMP3620 team

""" Student Details

    Student Name:
    Student ID:
    Email:
    Date:
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


class LogisticsEncoding(BasicEncoding):
    """ An encoding which extends BasicEncoding but adds control knowledge
        specific for the Logistics domain.
    """

################################################################################
#                You need to implement the following methods                   #
################################################################################

    def make_control_knowledge_variables(self, horizon: int) -> None:
        """ Make the variable for the problem.

            Use the function self.new_cnf_code(step, name, object) to make
            whatever codes for CNF variables you need to make your control
            knowledge for the Logistics problem.

            You can make variables which mean anything if you can think of
            constraints to make that enforce that meaning. As an example, if
            you were making control logic for the miconics domain, you might
            make variables which keep track if each passenger has ever
            been in an elevator and is now not.

            For a passenger p, and t > 0:
                was_boarded(p)@t <->
                    (-boarded(p)@t ^ (boarded(p)@t-1 v was_boarded(p)@t-1))

            For example, you might make a dictionary called
            self.was_boarded_at_t indexed by passenger names, where the values
            are lists where the ith index contains the cnf code for
            was_boarded(p)@i, which you got by calling self.new_cnf_code(i,
            f"was_boarded({was_boarded.passenger})", was_boarded).

            You can see here that this is using an object called was_boarded
            which has an attribute "passenger" as the object. This might not be
            the simplest way, you might wish to just use a string instead of a
            more complicated object. For example, self.new_cnf_code(i,
            f"was_boarded({passenger})", f"was_boarded({passenger})").

            You can then use these variables, along with the fluent and action
            variables to make your control knowledge.

            Note that the use of `make_control_knowledge_variables` is
            completely optional. You don't have to implement any code
            in this method. At the end of the day, the most important thing
            is to add new clauses in `make_control_knowledge`.
        """
        """ *** YOUR CODE HERE *** """

    def make_control_knowledge(self, horizon: int) -> None:
        """ This is where you should make your control knowledge clauses.

            These clauses should have the type "control".
        """

        """ *** YOUR CODE HERE *** """


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
