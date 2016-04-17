from .models import Asset, HighVolume, LowVolume

##### Fuzzy String Matching ######
def fuzzy(pattern, db_item, adj_bonus=5, sep_bonus=10, camel_bonus=10,
                lead_penalty=-3, max_lead_penalty=-9, unmatched_penalty=-1):
    """Return match boolean and match score.
    :param pattern: the pattern to be matched
    :type pattern: ``str``
    :param instring: the containing string to search against
    :type instring: ``str``
    :param int adj_bonus: bonus for adjacent matches
    :param int sep_bonus: bonus if match occurs after a separator
    :param int camel_bonus: bonus if match is uppercase
    :param int lead_penalty: penalty applied for each letter before 1st match
    :param int max_lead_penalty: maximum total ``lead_penalty``
    :param int unmatched_penalty: penalty for each unmatched letter
    :return: 2-tuple with match truthiness at idx 0 and score at idx 1
    :rtype: ``tuple``
    """
    instring = db_item.name

    score, p_idx, s_idx, p_len, s_len = 0, 0, 0, len(pattern), len(instring)
    prev_match, prev_lower = False, False
    prev_sep = True  # so that matching first letter gets sep_bonus
    best_letter, best_lower, best_letter_idx = None, None, None
    best_letter_score = 0
    matched_indices = []

    while s_idx != s_len:
        p_char = pattern[p_idx] if (p_idx != p_len) else None
        s_char = instring[s_idx]
        p_lower = p_char.lower() if p_char else None
        s_lower, s_upper = s_char.lower(), s_char.upper()

        next_match = p_char and p_lower == s_lower
        rematch = best_letter and best_lower == s_lower

        advanced = next_match and best_letter
        p_repeat = best_letter and p_char and best_lower == p_lower

        if advanced or p_repeat:
            score += best_letter_score
            matched_indices.append(best_letter_idx)
            best_letter, best_lower, best_letter_idx = None, None, None
            best_letter_score = 0

        if next_match or rematch:
            new_score = 0

            # apply penalty for each letter before the first match
            # using max because penalties are negative (so max = smallest)
            if p_idx == 0:
                score += max(s_idx * lead_penalty, max_lead_penalty)

            # apply bonus for consecutive matches
            if prev_match:
                new_score += adj_bonus

            # apply bonus for matches after a separator
            if prev_sep:
                new_score += sep_bonus

            # apply bonus across camelCase boundaries
            if prev_lower and s_char == s_upper and s_lower != s_upper:
                new_score += camel_bonus

            # update pattern index iff the next pattern letter was matched
            if next_match:
                p_idx += 1

            # update best letter match (may be next or rematch)
            if new_score >= best_letter_score:
                # apply penalty for now-skipped letter
                if best_letter is not None:
                    score += unmatched_penalty
                best_letter = s_char
                best_lower = best_letter.lower()
                best_letter_idx = s_idx
                best_letter_score = new_score

            prev_match = True

        else:
            score += unmatched_penalty
            prev_match = False

        prev_lower = s_char == s_lower and s_lower != s_upper
        prev_sep = s_char in '_ '

        s_idx += 1

    if best_letter:
        score += best_letter_score
        matched_indices.append(best_letter_idx)

    return [instring, score, db_item]

def fuzzy_pal(search_term, search_list):
    matches = []

    for word in search_list:
        matches.append(
            fuzzy(search_term, word))

    for i in range(1, len(matches)):
        j = i
        while j > 0 and matches[j][1] < matches[j-1][1]:
            matches[j], matches[j-1] = matches[j-1], matches[j]
            j -= 1
    cleaned_up = []
    
    for match in matches:
        cleaned_up.append(match[2])

    return cleaned_up[::-1][:20]

##### Various Form Functions #####
def get_new_item_form_data(request):
    item_type = request.POST.get('item_type')
    item_name = request.POST.get('item_name')
    item_quantity = request.POST.get('quantity')
    item_storage = request.POST.get('storage_location')

    if not request.POST.get('consumable_location') == '':
        item_consume = request.POST.get('consumable_location')
    else:
        item_consume = None

    item_reorder = request.POST.get('reorder_point')

    return (item_type, item_name, item_quantity,
            item_storage, item_consume, item_reorder)


##### Database CRUD Functions #####
def add_item_via_form_data(form_data):
    db_models = {
            'low':LowVolume(),
            'high':HighVolume(),
            'asset':Asset()}

    model = db_models[form_data[0]]

    model.name = form_data[1]
    model.quantity = form_data[2]
    model.storage_location = form_data[3]
    model.reorder_point = form_data[5]
    model.last_reorder_date = None

    if form_data[0] == 'high':
        model.consumable_location = form_data[4]

    model.save()
