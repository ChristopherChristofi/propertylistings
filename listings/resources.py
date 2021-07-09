regions = {
    "Cardiff": "93482",
    "Devon": "61297",
    "Edinburgh": "95760",
    "Essex": "61299",
    "Glasgow": "95748",
    "Greater-Manchester": "79192",
    "Isle-Of-Wight": "61521",
    "Leicestershire": "61309",
    "London": "93917",
    "Oxfordshire": "61317",
    "Somerset": "61322"
}

region_options = [k for k in regions.keys()]

do_not_show_options = {
            1 : "&dontShow={option_1}",
            2 : "&dontShow={option_1}%2C{option_2}",
            3 : "&dontShow={option_1}%2C{option_2}%2C{option_3}",
            "empty" : "&dontShow="
            }

not_options = {
        1 : '',
        2 : '',
        3 : ''
        }

must_have_options = {
        1 : "&mustHave={option_1}",
        2 : "&mustHave={option_1}%2C{option_2}",
        3 : "&mustHave={option_1}%2C{option_2}%2C{option_3}",
        4 : "&mustHave={option_1}%2C{option_2}%2C{option_3}%2C{option_2}",
        5 : "&mustHave={option_1}%2C{option_2}%2C{option_3}%2C{option_2}%2C{option_3}",
        6 : "&mustHave={option_1}%2C{option_2}%2C{option_3}%2C{option_2}%2C{option_3}%2C{option_2}"
        }

must_options = {
        1 : '',
        2 : '',
        3 : '',
        4 : '',
        5 : '',
        6 : ''
        }