import xml.etree.ElementTree as xml

def scan_file(filename=''):
    if not filename:
        print('Empty filename')
        return
    
    def scan(filename):
        start_count = end_count = max_depth = 0
        events=("start", "end")
        try:
            context = xml.iterparse(filename, events=events)
        
            for event, element in context:
                if event == 'start':
                    start_count += 1
                elif event == 'end':
                    end_count += 1
                    
                cur_depth = start_count - end_count - 1
                if max_depth <= cur_depth:
                    max_depth = cur_depth
                
            print(f'XML file tags depth is { max_depth }')
            
        except (FileNotFoundError, IOError):
            print('File not found')
    
    extension = '.xml'
    if '.' in filename:
        if filename[-4:] == extension:
            scan(filename)
        else:
            print('Invalid file extension')
    else:
        scan(filename + extension)

print('Enter the filename w/ or w/o expression:')
scan_file(input())
