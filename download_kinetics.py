import json
from os import rename
import os
import youtube_dl
import time

def load_json(path):
    with open(path,"r") as f:
        file=json.load(f)
    return file

def show_data_info_list():
    kinetics_400_train_path="E:\\data\\kinetics\\kinetics400\\train.json"
    kinetics_400_test_path ="E:\\data\\kinetics\\kinetics400\\test.json"
    kinetics_400_validate_path="E:\\data\\kinetics\\kinetics400\\validate.json"
    file=load_json(kinetics_400_train_path)
    key_list=[]
    account=0
    for key in file.keys():
        key_list.append(key)
        if len(key_list)==100:
            print(key_list)
            account+=100
            key_list=[]
    account+=len(key_list)

    print("account:",account)

class GetItem(object):
    def __init__(self):
        self.File_Name="test_video_1"
    def rename_hook(self,d):
        # 重命名下载的视频名称的钩子
        if d['status'] == 'finished':
            file_name = '{}.mp4'.format(self.File_Name)
            rename(d['filename'], file_name)
            print('下载完成{}'.format(file_name))

    def download(self,youtube_url):
        # 定义某些下载参数
        ydl_opts = {
            'progress_hooks': [self.rename_hook],
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': '%(id)s%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download([youtube_url])

class Download_Kinetics():
    def __init__(self,data_index=0,check_start_point=False):
        self.data_index=data_index
        self.base_path = "E:\\AI_Project_2020\\YouTube_download\\video\\"
        self.data_info_path={"kinetics_400_train_path":"E:\\data\\kinetics\\kinetics400\\train.json",
                             "kinetics_400_test_path":"E:\\data\\kinetics\\kinetics400\\test.json",
                             "kinetics_400_validate_path":"E:\\data\\kinetics\\kinetics400\\validate.json"}
        self.data_filename_title=["kinetics-400-train","kinetics-400-test","kinetics-400-validate"]
        self.data_info_list=self.get_data_info_list()
        self.data_info=load_json(self.data_info_path[self.data_info_list[self.data_index]])
        self.element_info_list=self.get_element_info_list()

        self.start_index=0
        self.total_num = 10
        # self.total_num=len(self.element_info_list)
        self.check_start_point=check_start_point
        self.check_start_index()

        self.get_item=GetItem()

    def get_data_info_list(self):
        data_info_list=[]
        for key in self.data_info_path.keys():
            data_info_list.append(key)
        return data_info_list
    def get_element_info_list(self):
        element_info_list=[]
        for key in self.data_info.keys():
            element_info_list.append(key)
        return element_info_list

    def check_start_index(self):
        if self.check_start_point:
            file_list = os.listdir(self.base_path)
            for i in range(self.total_num):
                FileName = self.data_filename_title[self.data_index] + "_" + str(i) + "_" + self.element_info_list[
                    i] + ".mp4"
                if FileName in file_list:
                    print(FileName," was alread downloaded !")
                    pass
                else:
                    break

            self.start_index = i
        else:
            pass

    def download_single_video(self,element_index=0):
        annotations=self.data_info[self.element_info_list[element_index]]["annotations"]
        duration=self.data_info[self.element_info_list[element_index]]["duration"]
        subset=self.data_info[self.element_info_list[element_index]]["subset"]
        youtube_url=self.data_info[self.element_info_list[element_index]]["url"]
        File_Name=self.base_path+self.data_filename_title[self.data_index]+"_"+str(element_index)+"_"+self.element_info_list[element_index]
        # File_Name = self.base_path + str(element_index)

        self.get_item.File_Name=File_Name
        self.get_item.download(youtube_url)
        # print(File_Name)

    def start_download(self):
        for element_index in range(self.start_index,self.total_num):
            try:
                self.download_single_video(element_index=element_index)
            except:
                ans=int(input("error occured,please choose what to do next(0:finish,1:skip,2:continue):"))
                if ans==0:
                    break
                elif ans==1:
                    pass
                else:
                    while True:
                        try:
                            self.download_single_video(element_index=element_index)
                        except:
                            ans = int(input("error occured again,please choose what to do next(0:skip,1:continue):"))
                            if ans==0:
                                break
                            else:
                                pass
                    pass

if __name__ == '__main__':
    downloader=Download_Kinetics(check_start_point=True)
    downloader.start_download()