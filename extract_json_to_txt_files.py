# Parse black metal JSON data to txt files
# https://github.com/niittymaa/Black-Metal-Lyric-Database

import os
import json

class Extract_JSON():
    def __init__(self):
        self.json_filename = 'black_metal.json'
        self.convert_to_txt()
        
    def convert_to_txt(self):
 
        # Check if json file exist
        if os.path.exists(self.json_filename):
 
            json_data = {}
            extracted_data = []
            
            def save_text_file(data):
                                              
                filename = self.clean_name(data['song']) + ' - ' + self.clean_name(data['artist']) + '.txt'
                file_path = os.path.join(os.getcwd(), 'Lyrics', data['artist'])
                
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                
                file_path = os.path.join(file_path, filename)
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        reformatted_data = ''
                        for lyric in data['lyrics']:
                            reformatted_data += lyric
                        # Try to split string from target word like "Lyrics"
                        if len(reformatted_data.split('Lyrics', 1)) > 1:
                            reformatted_data = reformatted_data.split('Lyrics', 1)[1]
                        f.write(str(reformatted_data))     
                                   
                except OSError as exc:
                    print(exc)
                    
            with open(self.json_filename) as json_file:
                json_data = json.load(json_file)
                print('File Found:', self.json_filename)
            
            for artist in json_data:
                artist_data = {'artist': self.clean_name(self.remove_words_within(artist['name'].replace('_', ' ').strip()))}
                for releases in artist['releases']:
                    for song in releases['songs']:
                        artist_data['song'] = self.clean_name(self.remove_words_within(song['name'][0].replace('_', ' ').strip()))
                        artist_data['lyrics'] = song['lyrics']                        
                        save_text_file(artist_data)
        
    def clean_name(self, name):        
        return_name = name
        remove_symbols = [*'<>:"/\|?*()']
        for i in remove_symbols:
            return_name = return_name.replace(i, '')
        return return_name
    
    def remove_words_within(self, text):
        words = text.split()
        result = ''
        in_brackets = False
        for word in words:
            if '(' in word:
                in_brackets = True
                word = ''
            if ')' in word:
                in_brackets = False
                word = ''
            if not in_brackets:
                result += word + ' '        
        return result.strip()
    
    
def main():
    Extract_JSON()
    
if __name__ == '__main__':
    main()