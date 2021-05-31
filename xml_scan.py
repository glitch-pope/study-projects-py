import xml.etree.ElementTree as xml

events=("start", "end")
start_count = end_count = max_depth = 0
for event, element in xml.iterparse('words_pool.xml', events=events):
    if event == 'start':
        start_count += 1
    elif event == 'end':
        end_count += 1
        
    cur_depth = start_count - end_count - 1
    if max_depth <= cur_depth:
        max_depth = cur_depth
    
print(f'XML file tags depth is { max_depth }')