
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
