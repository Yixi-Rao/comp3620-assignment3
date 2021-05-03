# Benchmarks

## Question 1-8 Benchmarks

Here we report the number of clauses that should be generated for each type of
clause. To check your code, you can simply keep a count every time you add a
new clause, and then print the total out to the terminal (but remember to
delete any print statements before submission). The horizons used below all
give a plan in both serial and parallel settings. Also turn on plangraph when
checking your numbers against ours, e.g.

```sh
python3 planner.py benchmarks/logistics/domain.pddl benchmarks/logistics/problem01.pddl logistics01 30 -p true -x serial # or `parallel` if you want to check Q6
python3 planner.py benchmarks/miconic/domain.pddl benchmarks/miconic/problem01.pddl miconic01 6 -p true -x serial
python3 planner.py benchmarks/blocks/domain.pddl benchmarks/blocks/problem04.pddl blocks04 7 -p true -x serial
python3 planner.py benchmarks/rovers/domain.pddl benchmarks/rovers/problem01.pddl rovers01 8 -p true -x serial
```

|               | logistics01 | miconic01 | blocks04 | rovers01 |
| ------------- | ----------- | --------- | -------- | -------- |
| Fixed Horizon | 30          | 6         | 7        | 8        |
| `start`       | 144         | 4         | 25       | 36       |
| `goal`        | 6           | 1         | 3        | 3        |
| `pre`         | 19,440      | 30        | 532      | 1264     |
| `eff`         | 21,600      | 42        | 1064     | 1576     |
| `frame`       | 8,640       | 48        | 350      | 576      |
| `mutex_q5`    | 1,906,560   | 24        | 1092     | 15272    |
| `mutex_q6`    | 39,240      | 12        | 798      | 5336     |
| `reach`       | 1,524       | 5         | 40       | 132      |
| `fmutex`      | 28,942      | 10        | 690      | 350      |

## Question 10 Benchmarks

All encodings can find a parallel plan within 10 steps, except for logistic09
where the first plan found has 11 steps. For this question we turn plangraph
off. For the basic encoding, we use the command

```sh
python3 planner.py benchmarks/logistics/domain.pddl benchmarks/logistics/problemXX.pddl logisticsXX 10:20:1 -q ramp
```

and for logistic control,

```sh
python3 planner.py benchmarks/logistics/domain.pddl benchmarks/logistics/problemXX.pddl logisticsXX 10:20:1 -q ramp -e logistics
```

where `XX` can be `03`, `04`, `07`, or `09`.

### Solution time for first step with a valid plan

| Problem     | First Step with Plan | Basic Encoding (s) | With Control Knowledge (s) |
| ----------- | -------------------- | ------------------ | -------------------------- |
| logistics03 | 10                   | 6.2                | 0.6                        |
| logistics04 | 10                   | 11                 | 0.8                        |
| logistics07 | 10                   | 3.6                | 0.5                        |
| logistics09 | 11                   | 23                 | 1.9                        |

### Total time

| Problem     | Basic Encoding (s) | With Control Knowledge (s) |
| ----------- | ------------------ | -------------------------- |
| logistics03 | 7.8                | 3.2                        |
| logistics04 | 13                 | 3.5                        |
| logistics07 | 5.0                | 2.3                        |
| logistics09 | 44                 | 16                         |

You should aim for similar times as our basic encoding. For control knowledge,
think of these times as your stretch goal - you don't have to match them to get
full marks (but it should still be somewhat better than the basic encoding).

For Question 10, we will give you up to 5 marks for each control knowledge you
come up with that makes sense and is implemented properly, up to a maximum of
15 marks. You're also free to implement more than three rules, but we will
still allocate a maximum of 15 marks for the rules. To get the full 5 marks,
you need to

- Be able to clearly explain the reasoning behind each rule.
- Find solutions more efficiently (see benchmarks above).
- Not find invalid plans.

The final 5 marks in Question 10 will come from having a good report describing
your reasoning/experiments if any in the report PDF.

For Question 11, we'll give you 5 marks for producing enough experimental
results, 5 marks for your run_experiments script, and 10 marks for the report
PDF. The report should include

- Discussion of the results
- Description of what is there in the tables.
- Interesting trends and why they happens.
- Discussion of strategies used to make it easier/quicker to find plans.
