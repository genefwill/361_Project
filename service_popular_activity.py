from time import sleep
import json
import random

def listen_request():
    with open('request_most_popular.txt', 'r+') as f:
        txt_command = f.read()
        
        if txt_command == 'WHAT_IS_THE_MOST_POPULAR_ACTIVITY':            
            find_popular_activity()
            
            # Clear the file content and move to the beinning of the file             
            f.truncate(0)
            f.seek(0)            
            f.write('')
            f.close
            
            
def find_popular_activity():
    with open('content_rated.json') as f:
        pop_act = ''
        pop_score = random.randint(1,7)
        
        data = json.load(f)
        print (data)
        
        for act_object in data:
            if act_object['score'] == pop_score:
                pop_object= act_object
       
        with open('activity.txt', 'w') as outfile:
            json.dump(pop_object, outfile)
        return pop_act   
    
if __name__ == "__main__":
    while True:
        #sleep(1)
        listen_request()