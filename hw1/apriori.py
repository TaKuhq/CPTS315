s = 500

        
def read_data(filename):
    print('loading data... ', end='')
    browsing_session = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            items = set(line.strip().split())
            browsing_session.append(items)
    print('done')
    return browsing_session


def create_single_item_set(browsing_session):
    print('creating single item set... ', end='')
    single_item_set = set()
    for session in browsing_session:
        for item in session:
            single_item_set.add(item)
    print('done')
    return single_item_set


def create_single_item_support(browsing_session):
    print('creating single item support... ', end='')
    statistics = {}
    single_item_support = {}
    for session in browsing_session:
        for item in session:
            if item not in statistics:
                statistics[item] = 0
            statistics[item] += 1
    for item, count in statistics.items():
        if count >= s:
            score = count / len(browsing_session)
            single_item_support[item] = score
    print('done')
    return single_item_support


def create_pairs_item_set(single_item_support):
    print('creating pairs item set... ', end='')
    pairs_item_set = set()
    single_item_support_list = list(single_item_support)
    for i in range(len(single_item_support_list)):
        for j in range(i, len(single_item_support_list)):
            item1 = single_item_support_list[i]
            item2 = single_item_support_list[j]
            if item1 < item2:
                pairs_item_set.add((item1, item2))
            elif item1 > item2:
                pairs_item_set.add((item2, item1))
    print('done')
    return pairs_item_set


def create_pairs_item_support(browsing_session, pairs_item_set):
    print('creating pairs item support... ', end='')
    statistics = {}
    pairs_item_support = {}
    i = 0
    for session in browsing_session:
        i += 1
        if i % 100 == 0:
            print('{:.2f}%'.format(i / len(browsing_session) * 100))
        for item in pairs_item_set:
            if item[0] in session and item[1] in session:
                if item not in statistics:
                    statistics[item] = 0
                statistics[item] += 1
    for item, count in statistics.items():
        if count >= s:
            pairs_item_support[item] = count / len(browsing_session)
    print('done')
    return pairs_item_support


def compute_confidence_scores_for_pairs_item(single_item_support, pairs_item_support):
    print('computing confidence scores for pairs item... ', end='')
    confidence_scores = {}
    for pair, score in pairs_item_support.items():
        item0 = pair[0]
        item1 = pair[1]
        confidence_score0 = score / single_item_support[item0]
        confidence_score1 = score / single_item_support[item1]
        confidence_scores[item0 + ' ' + item1] = confidence_score0
        confidence_scores[item1 + ' ' + item0] = confidence_score1
    print('done')
    return confidence_scores


def create_triples_item_set(pairs_item_support, top_5_confidence_score):
    print('creating triples item set... ', end='')
    triples_item_set = set()
    pairs_item_support_list = list(pairs_item_support)
    for i in range(len(pairs_item_support_list)):
        for item in top_5_confidence_score:
            item1 = pairs_item_support_list[i]
            item2 = item[0].split()
            triple_item = set()
            triple_item.add(item1[0])
            triple_item.add(item1[1])
            triple_item.add(item2[0])
            triple_item.add(item2[1])
            if len(triple_item) == 3:
                l = list(triple_item)
                l.sort()
                triples_item_set.add('{} {} {}'.format(l[0], l[1], l[2]))
    print('done')
    return triples_item_set


def calculate_top_5_confidence_scores(confidence_scores):
    items = []
    scores = []
    for _, score in confidence_scores.items():
        scores.append(score)
    scores.sort(reverse=True)
    keys = set(confidence_scores.keys())
    for item in keys:
        if confidence_scores[item] >= scores[9]:
            items.append((item, confidence_scores[item]))
    items.sort(key=lambda s:(-s[1], s[0]))
    if len(items) >= 10:
        items = items[0:10]
    return items

def open_top_10_file():



# def create_triples_item_support(browsing_session, triple_item_set):
#     print('creating pairs item support... ', end='')
#     statistics = {}
#     triples_item_support = {}
#     i = 0
#     for session in browsing_session:
#         i += 1
#         if i % 100 == 0:
#             print('{:.2f}%'.format(i / len(browsing_session) * 100))
#         for items in triple_item_set:
#             item = items.split()
#             if item[0] in session and item[1] in session and item[2] in session:
#                 if items not in statistics:
#                     statistics[items] = 0
#                 statistics[items] += 1
#     for item, count in statistics.items():
#         if count >= s:
#             triples_item_support[item] = count / len(browsing_session)
#     return triples_item_support


# def compute_confidence_scores_for_triples_item(pairs_item_support, triples_item_support):
#     print('computing confidence scores for triples item... ', end='')
#     confidence_scores = {}
#     for pair, score in triples_item_support.items():
#         items = pair.split()
#         item0 = items[0]
#         item1 = items[1]
#         item2 = items[2]
#         confidence_score01 = score / pairs_item_support[(item0, item1)]
#         confidence_score02 = score / pairs_item_support[(item0, item2)]
#         confidence_score12 = score / pairs_item_support[(item1, item2)]
#         confidence_scores[item0 + ' ' + item1 + ' ' + item2] = confidence_score01
#         confidence_scores[item0 + ' ' + item2 + ' ' + item1] = confidence_score02
#         confidence_scores[item1 + ' ' + item2 + ' ' + item0] = confidence_score12
#     print('done')
#     return confidence_scores



if __name__ == '__main__':
    file ='./order_p.txt'
    browsing_session = read_data(file)
    
    single_item_set = create_single_item_set(browsing_session)
    single_item_support = create_single_item_support(browsing_session)
    
    pairs_item_set = create_pairs_item_set(single_item_support)
    pairs_item_support = create_pairs_item_support(browsing_session, pairs_item_set)
    
    confidence_score = compute_confidence_scores_for_pairs_item(single_item_support, pairs_item_support)
    top_10_confidence_score = calculate_top_10_confidence_scores(confidence_score)
    out = open('./output.txt', 'w')
    out.write()
    for item in top_10_confidence_score:
        print('{} {:.4f}'.format(item[0], item[1]))
        out.write('{} {:.4f}\n'.format(item[0], item[1]))
    
    # triples_item_set = create_triples_item_set(pairs_item_support, top_5_confidence_score)
    # triples_item_support = create_triples_item_support(browsing_session, triples_item_set)
    
    # confidence_score = compute_confidence_scores_for_triples_item(pairs_item_support, triples_item_support)
    # top_5_confidence_score = calculate_top_5_confidence_scores(confidence_score)
    # out.write('OUTPUT B\n')
    # for item in top_5_confidence_score:
    #     print('{} {:.4f}'.format(item[0], item[1]))
    #     out.write('{} {:.4f}\n'.format(item[0], item[1]))
    out.close()
