# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:45:17 2017

@author: Bharani Kodirangaiah
•	100 blocks (sectors) numbered from 0-99, each contains 512 bytes of data.
•	Not concerned about placement of the blocks on the disk.
•	All access to the disk should be done through two procedure DREAD and DWRITE.
Note: No need to do actual disk reads and writes; the entire disk can be simulated using a 50K block of memory.
•	Front end program that processes commands: 
    	File create, open, close, delete, read, write, and seek functions
•	When the end of the input data is reached, the following information will be displayed:
	    Directory (illustrating it’s hierarchical structure)
	    Length of each file (in bytes)
	    Number of free directory and user data blocks.
"""
import json

class Disk:
    
    def __init__(self):
        '''
        Initializing
        '''
        self.open=0
        self.seek=0
        self.links=[]
        self.point=0
        self.free=0
        self.create1=0
        self.update=0
        self.output=0
        self.Input=0
        self.big_list=[]
        self.start_point=0
        self.blocks=[]
        self.initialize_block(32,100)                     # (dir content, no of blocks)
        self.free_space_list=[0]*len(self.blocks)
        self.set_freespace()
        self.flag_open_NF=0
        self.flag_delete_NF=0
    
    def initialize_block(self,dir_no,block_size):
        for i in range(block_size):
            dir_1=[['F','xxx',-1,0]]
            for j in range(dir_no):
                dir_1.append(['F','xx',-1,0])
            block=[-1,-1,'xxx']
            block.insert(3,dir_1)
            self.blocks.append(block)

    def print_block(self,block_no=0):
        if block_no:
            print(self.blocks[block_no-1])
            return
        for i in range(len(self.blocks)):
            print("{} : {}".format(i,self.blocks[i]))
        print(self.free_space_list)
    
    def ls(self):
        '''
        Display directory contents
        @param blocks: database structure
        '''
        def iter_row(row, depth = 1):
            '''
            Display the contents of a /path in directory
            @param row: The row in the database corressponding to the path you want to display
            @param depth: The depth of the directory from the give row/path
            '''
            for i in row[-1]:
                #if it is a file
                if i[0] == 'U':
                    print(' |--'*depth + i[1])
                #if it is a Directory
                elif i[0] == 'D':
                    print(' |--'*depth + i[1])
                    iter_row(self.blocks[i[2]], depth+1)
            if row[1]:
                iter_row(self.blocks[row[1]])
        #print current dir
        print(' /')
        iter_row(self.blocks[0])     
        
    def command(self):
        '''
        Test commands: test creating file/directory and wrting to file type seeking, deleting
        '''
        self.create('U','main.txt')
        self.write(10,'hello my first')
        self.create('D','dir1')
        self.create('D','dir2')
        self.create('U','dir2/pig.doc')
        self.write(505,'bugged up I canot atke this')
        self.close()           
        self.create('D','dir2/subdir2')
        self.create('U','dir2/subdir2/dest.docx')
        self.write(12,'destination subdir')
        self.close()
        self.create('D','dir2/subdir2/new')
        self.create('D','dir2/subdir2/new/dir23')
        self.create('U','dir2/goat.jpg')
        self.write(700,'new things adding is fun')
        self.close()
        self.create('U','fist.doc')
        self.write(100,'MEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        self.close()
        self.delete('dir2/goat.jpg')
        self.create('D','dir2/subdir3')
        self.create('D','dir3')
        self.create('D','dir4')
        self.create('D','dir2/subdir4')
        self.create('D','dir2/subdir5')
        
        self.create('U','dir2/subdir.text')
        self.write(505,'testing testing testing testing testing testing testingtesting testing testing')
        self.close()
        self.create('D','dir2/subdir6')
        self.create('D','dir2/subdir6/newtest')
        
        self.create('U','sub')
        self.write(30,'last last i jsfo ngdsgoifd sgosfdg ')
        self.close()
        self.opens('I','dir2/goat.jpg')
        self.close()
        self.opens('U','dir2/pig.doc')
        self.read(600)
        self.close()
        #open update for appending
        self.opens('O','dir2/subdir.text')
        self.write(600,'+addeddCalifornia educational program and current research. It provides connectivity to commercial internet for all CENIC members. CalREN-HPR - CENIC’s high performance Research network serves both private and public research institutes such as the Cal Tech, University of Southern California, UC campuses and NPS. CalREN-HPR is enhanced for big science “power users” with up to 10Gbps backbone bandwidth to poses the advanced network features needed for supporting education applications and researches.')
        self.close()
        self.print_block()
        self.opens('U','dir2/subdir.text')
        self.read(600)
        #self.read(1233)
        self.seeks(1,0)
        self.seeks(0,-20)
        self.seeks(-1,0)
        self.write(510,'hello')        
        self.seeks(-1,0)
        self.read(512)
        self.close()
        self.opens('I','fist.doc')
        self.read(10)
        self.close()
        self.opens('U','fist.doc')
        self.write(700,'There is power in connection, it fuels innovation and moves education and research beyond the boundaries of geography. To deliver advance education and research all over California by providing the world class network important for innovation, collaboration and economic growth connecting California to the world. In 1996, a group of leaders challenged to provide excellent broadband network to consortium of California public research and education institution (CalREN) by Corporation for Education Network Initiative in California (CENIC). CENIC, non-profit corporation for Education networks in California, over 10,000 institutes connect to CENIC which is governed by members of segment. CENIC provides high-data rate, high')
        self.close()

        self.opens('O','fist.doc')
        self.write(100,'California K-12 schools and libraries, California Community Colleges, Caltech, California state University System, Stanford, University of California, USC, California Public libraries, Medical research, and cultural institution all over the state. CENIC has about 3,800 miles optic fiber connecting around 10,000 research centres and education institute in all 58 counties. CENIC provides network design, procures circuits, arranges for state and federal discounts, purchase and install hardware, maintains and monitors network connectivity to all California Public libraries. CENIC has three networks operate parallelly as one independent layer on a single infrastructure, CalREN-Digital California, CalREN-High Performance Research Network and CalREN – experimental/Development.')
        self.close()
        self.ls()        
        #self.print_block()
        return    
     

    def update_support(self,root, dir1):
        """
        argument block number and position which is free and updates with corresponding type and 
        name and saves the link of the file/directory.
        sets link=[block_number, file/directory position in block] which is used in write
        """
        self.blocks[root][3][dir1][0]=self.typ
        self.blocks[root][3][dir1][1]=self.name
        self.blocks[root][3][dir1][2]=self.get_freespace()
        self.link=[root,dir1]
        
    def block_update(self,root):
        for i in range(32):
            if self.blocks[root][3][i][0]=='F':
                self.update_support(root,i)
                self.set_freespace()
                return
        if self.blocks[root][1]!=0:
            root=self.blocks[root][1]
            self.block_update(root)
        else:
            self.blocks[self.get_freespace()][0]=root
            self.blocks[root][1]=self.get_freespace()
            root=self.get_freespace()
            self.set_freespace()
            self.block_update(root)

        
    def write_to_file(self):
        '''
        To store the curent file system state, store the blocks in JSON format to local system
        '''
        dic={"Blocks":self.blocks,
             "FreeSpaceList": self.free_space_list}
        
        with open('JSONData.json', 'w') as f:
            f.write(json.dumps(dic))
        print("Filesystem is saved in JSONData.json")
    
    def get_from_file(self):
        '''
        read from the stored JSON file and resotre the previous session when selected
        '''
        with open('JSONData.json','r') as f:
            data=json.load(f)
        self.free_space_list=data['FreeSpaceList']
        self.blocks=data['Blocks']
        print("Old file system is loaded")
      
    def get_freespace(self):
        '''
        function returns the free block available
        '''
        if 0 not in self.free_space_list:
            print("No free space available")
            return
        a=self.free_space_list.index(0)
        return a
    
    def set_freespace(self):
        '''
        function sets the particular block unavailable once it is assigned to file/directory created
        '''
        if 0 not in self.free_space_list:
            print("No free space available")
            return
        self.free_space_list[self.free_space_list.index(0)]=1
    
    def get_link(self,name,block_no):
        """
        argument name, block return nothing but set the self.file_list
        Takes the name and sets the corresponding files block number, file position in block and link of file
        """
        for i in range(32):
            if self.blocks[block_no][3][i][1]==name:
                file_link=self.blocks[block_no][3][i][2]
                self.file_list=[block_no,file_link,i]
                return
        
        if self.blocks[block_no][1]:
            block_no=self.blocks[block_no][1]
            self.get_link(name,block_no)
        else:
            self.flag_open_NF=1
            return 

    def create(self,typ,name):
        
        self.create1=1
        self.typ=typ.upper()
        self.name=name
        self.blockno_name(name)
        if not self.flag_open_NF:
            print("Directory already has the filename you entered!!")
            self.flag_open_NF=0
            return
        
        if '/' not in name:
            root=0
            self.block_update(root)
        else:
            name=name.split('/')
            self.name=name[-1]
            pr='/'.join(name[:-1])
            self.blockno_name(pr)
            block_no,file_link,file_pos_block=self.file_list
            self.block_update(file_link)
        print(self.name,": is created")            
        return
    
    def write_support(self,file_link,n,data,back=0,fwd=0):
        split_data=[]
        while data:
            split_data.append(data[:504])
            data=data[504:]
        self.blocks[file_link]=[0,0,None]
        self.write_to_filelink(file_link,split_data)
        return
   
    def set_fileblock(self,link):
        self.blocks[link]=[0,0,0]
        d=[]
        for j in range(len(self.blocks[0][3])):
            d.append(['F',0,0,0])
        self.blocks[link].insert(3,d)
        return
    
    def write_output(self,n,data):
        self.big_list=[];split_data=[]
        block_no,file_link,file_pos_block=self.file_list
        self.read_alldata(file_link)
        datas=self.big_list
        datas=datas+''.join(data)
        x=datas
        while datas:
            split_data.append(datas[:504])
            datas=datas[504:]
        self.write_to_filelink(file_link,split_data)
        print("File length",len(x),"Bytes")           
                    
    def find_length_file(self,file_link):
        if self.blocks[file_link][1] == 0:
            s=len(self.blocks[file_link][2])
            return s
        else:
            file_link=self.blocks[file_link][1]
            return self.find_length_file(file_link)+504
    
    def set_link_free(self):
        for i in self.links:
            self.set_fileblock(i)
            self.free_space_list[i]=0
    
    def write_to_filelink(self,file_link,split_data):
        for splits in split_data:
            if self.blocks[file_link][1]==0:
                if split_data[-1] != splits:
                    back=file_link
                    free=self.get_freespace()
                    self.blocks[file_link][1]=free
                    self.blocks[file_link][2]=splits
                    file_link=free
                    self.blocks[free]=[back,0,None]
                    self.set_freespace()
                else:
                    self.blocks[file_link][2]=splits
                
            else:
                self.blocks[file_link][2]=splits
                file_link=self.blocks[file_link][1]
        return
    
    def read_alldata(self,file_link):
        if self.blocks[file_link][1] == 0:
            self.big_list.append(self.blocks[file_link][2])
        else:
            self.big_list.append(self.blocks[file_link][2])
            file_link=self.blocks[file_link][1]
            self.read_alldata(file_link)
        self.big_list=''.join(self.big_list)
    
    def find_link(self,file_link):
        if self.blocks[file_link][1]==0:
            self.links.append(file_link)
        else:
            self.links.append(file_link)
            file_link=self.blocks[file_link][1]
            self.find_link(file_link)

    def write_update(self,data):
        split_data=[];self.big_list=[]
        block_no,file_link,file_pos_block=self.file_list
        self.read_alldata(file_link)
        #print("length of data in file",len(self.big_list),'\nlist::',self.big_list)
        pos=self.start_point; data_list=self.big_list
        data1=data_list[:pos]
        data_list=data1+''.join(data)
        self.big_list=data_list
        list_ele=self.big_list
        x=list_ele
        while list_ele:
            split_data.append(list_ele[:504])
            list_ele=list_ele[504:]
        self.find_link(file_link)
        if len(split_data) <=len(self.links):
            last_block=self.links[(len(split_data)-1)]
            self.blocks[last_block][1]=0
            links_free=self.links[len(split_data):]
            for i in links_free:
                self.set_fileblock(i)
                self.free_space_list[i]=0
        self.write_to_filelink(file_link,split_data)
        size= self.find_length_file(file_link)
        self.blocks[block_no][3][file_pos_block][3]=size
        print("File is",len(x),'bytes')
        return
    
    def write(self,n,data):
        n=int(n);data=str(data)  
        while n>len(data):
            data=data+' '
        if self.Input:
            print("Cannot write to file in OPEN Input mode")
            return
        if not self.create1 and not self.output and not self.update:
            print("No file is open")
            return
        elif self.create1:
            if self.typ == 'D':
                print("Cannot write to Directory")
                return
            block,file=self.link
            file_link=self.blocks[block][3][file][2]    #saves the block of the created file
            self.blocks[block][3][file][3]=len(data)
            self.write_support(file_link,n,data)
            print("File is",len(data),"bytes")
                    
        elif self.output:
            block_no,file_link,file_pos_block=self.file_list
            self.blocks[block_no][3][file_pos_block][3]+=len(data)
            self.write_output(n,data)
            
        elif self.update:
            block_no,file_link,file_pos_block=self.file_list
            self.write_update(data)                  
        
        elif self.Input:
            print("Cannot write to file in INPUT mode")
        return
    
    def delete_support(self,file_link):
        if not self.blocks[file_link][1]:
            if self.blocks[file_link][0]:
                back=self.blocks[file_link][0]
                self.blocks[back][1]=0
            self.free_space_list[file_link]=0
            self.set_fileblock(file_link)
        else:
            file_link=self.blocks[file_link][1]
            self.delete_support(file_link)
            self.set_fileblock(file_link)
            self.free_space_list[file_link]=0
 
    def delete(self,name):
        name=str(name)
        self.blockno_name(name)
        block_no,file_link,file_pos=self.file_list
        if '.' not in name and self.blocks[block_no][3][file_pos][0] == 'D':                             #deleting directory
            a=input('Are you sure you want to delete directory?(y/n)')
            if a.upper()=='Y':
                
                block=self.blocks[block_no][3][file_pos][2]
                for i in range(4):
                    if self.blocks[block][3][i][0]!='F':
                        print("Remove directory contents before deleting.")
                        return
                self.blocks[block_no][3][file_pos][0]='F'
                self.blocks[block_no][3][file_pos][3]=0
                self.free_space_list[block]=0
            else:
                pass
        else:                                               #deleting file
            self.delete_support(file_link)
            self.set_fileblock(file_link)
            self.blocks[block_no][3][file_pos][0]='F'
            self.blocks[block_no][3][file_pos][3]=0
            self.free_space_list[file_link]=0
            self.set_fileblock(file_link)
            #print("delete support",self.free_space_list,'\n',self.blocks[file_link])
        print(name,"Deleted")
   
    def blockno_name(self,name):
        link=0
        if len(name.split('/'))==1:
            self.get_link(name,link)
        else:
            name=name.split('/')
            for name1 in name:
                self.get_link(name1,link)
                link=self.file_list[1]
        return    
        
    def opens(self,mode,name):
        self.big_list=[]
        if '.' not in name:
            print("Please enter filename")
            return
        self.open=1
        self.blockno_name(name)
        block_no,file_link,file_pos_block=self.file_list
        
        if mode.upper()=='I':
            self.Input=1
            
        elif mode.upper()=='U':
            self.update=1
       
        elif mode.upper()=='O':
            self.output=1
            self.link=file_link
            
        if self.flag_open_NF:
            if self.create1:
                print("Close the file")
                return
            print("FILE NOT FOUND!!")
            self.flag_open_NF=0
            return
        
        if self.blocks[block_no][3][file_pos_block][3]==0:
            print("file is empty!!")
        else:
            self.read_alldata(file_link)
            big_list=''.join(self.big_list)
            print("length of file:",name,'is',len(big_list),"bytes")
        return

    
    def read(self,n):
        n=int(n);self.big_list=[]
        if not self.Input and not self.update:
            print("Open file in Input/Update mode to read")
            return
        block_no,file_link,file_pos_block=self.file_list
        self.read_alldata(file_link)
        big_list=self.big_list
        if self.start_point:
            if n>abs(self.start_point-len(big_list)):
                print(big_list[self.start_point:],"<EOF>")
            elif n<=abs(self.start_point-len(big_list)):
                print(big_list[self.start_point:self.start_point+n])
        else:
            if n>len(big_list):
                print(big_list,"<EOF>")
            elif n<=len(big_list):
                print(big_list[:n])
            return
    
    def close(self):
        self.create1=0
        self.open=0
        self.update=0
        self.output=0
        self.Input=0
        self.big_list=[]
        self.flag_delete_NF=0
        self.flag_open_NF=0
        self.start_point=0
        self.links=[]

    def end_of_file(self,file_link):
        if self.blocks[file_link][1] == 0:
            s=len(self.blocks[file_link][2])
            return s
        else:
            file_link=self.blocks[file_link][1]
            return self.end_of_file(file_link)+504
            
    
    def seeks(self,base,offset):
        base=int(base);offset=int(offset)
        """
        base== -1 : begining of the file ; 0 : current position ; +1 :end of the file
        seek -1 0 ; seek +1 0 ; seek 0 -5
        """
        block_no,file_link,file_pos_block=self.file_list
        self.seek=1
        if not self.Input and not self.update:
            print("Open file in Input/Update mode to seek")
            return
        block_no,file_link,file_pos_block=self.file_list
        if base ==-1:
            print("Pointing to begining of file")
            self.start_point=0
            if offset < 0:
                print("Pointing to start of file, Cannot go behind")
                return
            elif offset >=0:
                self.start_point+=offset
        elif base == 1:
            print("Pointer is at end of file")
            if offset>0:
                print("Pointer cannot go behind the file")
                return
            elif offset<=0:
                #x=self.end_of_file1(file_link)
                self.start_point=self.end_of_file(file_link)
                #print("EOF return",self.end_of_file(file_link))
                offset=abs(offset)
                self.start_point-=offset
        elif base == 0:
            print("current position of file is",self.start_point)
            if offset<=0:
                self.start_point-=abs(offset)
            else:
                self.start_point+=offset
            #self.start_point has the position so just pass
            pass
        print("start_point",self.start_point)
        return
    
    def cat(self,name):
        self.big_list=[]
        self.blockno_name(name)
        block_no,file_link,file_pos=self.file_list
        self.read_alldata(file_link)
        print(self.big_list)

d=Disk()
#d.command()

