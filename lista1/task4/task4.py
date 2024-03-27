def get_data(filename):
    with open(filename) as f:
        lines = f.readlines()
        data = []
        for line in lines:
            line = line.split(' ')
            data.append({'fields': [int(c) for c in list(line[0])], 'length': int(line[1])})
        return data


def opt_dist(data) -> int:
    pref = [0]
    [pref.append(pref[-1] + num) for num in data['fields']]
    count = sum(data['fields'])
    longest = len(data['fields']) + 1
    for i in range(data['length'], longest):
        inside = pref[i] - pref[i - data['length']]
        outside = count - inside
        changed = (data['length'] - inside) + outside
        longest = min(longest, changed)
    return longest


data = get_data('zad4_input.txt')
res = [str(opt_dist(d)) for d in data]
with open('zad4_output.txt', 'w', encoding='utf-8') as f:
    f.writelines(res)

