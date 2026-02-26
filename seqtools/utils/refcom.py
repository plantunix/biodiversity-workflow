## reference search function ##
def rsearch(record, key):                                                      # Reference annotations can be "authors", "title" and
    references = record.annotations.get('references')                          # "journal". these annotations are stored inside reference
    if key in ["authors", "title", "journal"]:                                 # instances(dict()). This function will search all instances
        ref_payload = []                                                       # and output various variables for each annotation.
        for ref in references:
            reference = getattr(ref, f'{key}', 'Not Available')
            ref_payload.append(reference)
        ref1, ref2, ref3, ref4, ref5 = (ref_payload + ["Not Available"] * 5)[:5]
        return ref_payload, ref1, ref2, ref3, ref4, ref5
    else:
        error = "Invalid annotation parameter. Reference search function accepts only authors, title or journal as parameters."
        print(error)
        return

## comment search function ##
def csearch(record, key):                                                       # Structured comment annotations can have different
    comment = record.annotations.get('structured_comment')                      # data points, mostly related to assembly. This
    try:                                                                        # function will search a given DP and extract it.
        assembly = comment["Assembly-Data"]
        if key in ["Sequencing Technology", "Assembly Method", "Assembly Name"]:
            value = assembly.get(f'{key}', 'Not Available')
            return value
        else:
            error = f"Invalid function parameter '{key}'. Comment search function accepts only assembly_name, sequencing_technology or\
                assembly_method as parameters."
            print(error)
            return
    except TypeError:
        value = 'Not Available'
        return value
