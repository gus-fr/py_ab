
==================
AB Test Definition
==================

The experiment can encode a lot of information that needs to be specified. In order to simplify the setup of AB tests, we've designed a small language (heavily inspired from C syntax) that defines valid AB test protocols

-----------------------
Example file definition
-----------------------

Before describing the grammar rules in detail it's useful to look at an example experiment definition

.. code-block:: C

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
                return "123" weighted 3.4,
                        "9.3" weighted 5,
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
