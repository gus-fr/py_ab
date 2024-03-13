# PYthonABTesting
Library that defines a simplified language to set up and generate AB test functions within a python ecosystempy

# Getting Started
First 'pip install py-ab-experiment' to install the library

To get started you can use one of the sample files provided in `src/tests/unit/test_programs`
These are sample AB test definitions that both serve as unit tests, and provide sample file definitons.
using the `splitter_test.pyab` definition, which is defined as
```
def basic_experiment_1{
        //some splitter fields
        splitters: my_id
        if field_1 == 'a'{
                return "Setting 1" weighted 4, "Setting 2" weighted 1
        }
        else{
                return "Setting 1" weighted 1, "Setting 2" weighted 1
        }
}
```


You can then load an experiment in python by
```
from pyab_experiment.experiment_evaluator import ExperimentEvaluator
with open(file_name, "r") as fp:
    experiment = ExperimentEvaluator(fp.read()) # load and compile the experiment code
```

and then run experiments by calling the experiment object with the fields needed
```
    experiment_group = experiment(my_id=123,field1='a')
```

you can call the experiment class many times, and as long as the my_id field is different you should get
on average 'Setting 1' about 80% of the times (as long as field1='a'). If field1 is anything other than 'a'
you will get a 50/50 split between 'Setting 1' and 'Setting 2'


# AB Testing
A/B testing frameworks are essential for businesses as they provide a structured approach to comparing different versions of variables like websites, advertisements, or products. This methodology involves presenting variations to users randomly and analyzing how these changes impact user behavior and key metrics. A/B testing is valuable for optimizing digital marketing strategies, refining product concepts, enhancing pricing strategies, and improving user experience. By using A/B testing, businesses can make informed decisions based on real-time user behavior data, leading to better conversion rates and return on investmen

## AB testing technicalities
So the idea is to have a standard way to split a set of variables into two (or more) groups (A/B/...)
based on some rules.
The simplest case to handle is when we have one numeric variable (for example `my_id`) that we want to split into 2 separate buckets A and B. Assuming that the distribution is uniform (more or less) if we run `my_id %2` over the incoming data, we'll have even ids fall in one bucker, and odd id's in another bucket. we can generalize to n groups by modding over n.

This raises a number of technical problems, that are well described in this insightful [post](http://blog.richardweiss.org/2016/12/25/hash-splits.html). One solution to the problems raised is to use a hashing technique rather than using the id directly.
In summary Hashing helps in assigning users to test groups by ensuring consistent and deterministic allocation based on their unique identifiers, such as user IDs or session IDs. This deterministic assignment is crucial for meaningful test results, as it guarantees that the same user will always be assigned to the same bucket given the same input criteria. Hashing allows for scalability, efficiently handling a large number of users and providing a consistent way to distribute users across buckets regardless of the test size. Additionally, hashing offers flexibility by enabling easy allocation of different proportions of users to various buckets, allowing control over allocation percentages by adjusting the hash range

The code implementation in this repository follows the hashing approach.

## Choosing A/B tests
Another important criteria considered is the ability to run different experiments simultaneously given certain conditions.

For instance in addition to the `my_id` field, our data may contain other descriptive attributes like locations, colors, weights, etc (depending on the domain).

Based on these attributes, we may want to set different buckets based on the descriptive fields. As a concrete example suppose we have a field `cost` that describes the cost of a product. We may want to run a different test based on wether something is expensive or not. A potential setup would look like 'if price <100: run one test variant, else run a different variant'.

The ability to choose test based on variable conditionals has been incorporated in the AB test definition

## weights
Of curse we may also want to run AB tests with weights other than 50/50 for 2 tests, or uniformly distributed weights in the general case.

We've added a mechanism to specify how much weight to give to an individual group in each of the AB tests specified.

# AB Test Definition
The requirements above encode a lot of information that needs to be coded as a specification. In order to simplify the setup of AB tests, we've designed a small language (heavily inspired from C syntax) that defines valid AB test protocols

## Example file definition
Before describing the grammar rules in detail it's useful to look at an example experiment definition

```
/*************************************************************
Sample experiment definition with all language features
the language syntax is quite basic. The definition is inspired
by (a heavyly reduced subset of) C syntax. Unlike python indentation has no meaning
However for readability it's still highly recommended.
Also C-like comment blocks are allowed!!!
**************************************************************/

def complex_experiment_defn{
    // an optional salt (must come before splitting fields)
    salt: "csdvs887"

    // define splitting fields here, these define how a group is chosen
    splitters: my_fld, my_fld_1

    // The last part is a conditional expression.
    // here we define the conditions for choosing a group.

    // boolean operator precedence follows standard practice
    // i.e. 'not' has highest precedence, followed by 'and',
    //to finish with 'or' as the lowest precedence operator
    if field1=='a' and not field2 >4 or field3<9{
        if field4 == 'xyz'{

            // Return statements are probabilistic by nature
            // the weight defines the relative frequency of seeing one setting vs others
            return 123 weighted 3.4,
                    9.3 weighted 5,
                    "abc" weighted 3 /* like in C, embedded, multiline
                    block comment also works */
        }
        else if field5 != 'x'{
            return "Setting 1.1.1" weighted 1,
                    "Setting 1.1.2" weighted 0

        }
        else if field6 in (1,2,3) and field7 not in (8,9,10){
            return "Setting 1.2.1" weighted 0.5,
                    "Setting 1.2.2" weighted 0.5

        }
        else{
            return "Setting 1.3.1" weighted 0.5,
                    "Setting 1.3.2" weighted 0.5

        }
    }
    else{
        return "default" weighted 1 // comments inline after code are also ignored
    }
}
```

TBC
