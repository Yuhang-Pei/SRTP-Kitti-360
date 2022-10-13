import os
import sre_constants

def main():
    with open('taxonomy.json', 'r') as taxonomy:
        with open('data_select.bat', 'w') as batch:
            for line in taxonomy:
                if (line.find('sedan') > -1):
                    model_index = line[4:line.find(',')]
                    src_model_dir = 'F:\\Research\\SRTP\\Data\\car\\' + model_index
                    dst_model_dir = 'F:\\Research\\SRTP\\Data\\selected\\' + model_index
                    cmd = 'xcopy ' + src_model_dir + ' ' + dst_model_dir + ' /i /e\n'
                    batch.write(cmd)
                    

    
    


if __name__ == '__main__':
    main()