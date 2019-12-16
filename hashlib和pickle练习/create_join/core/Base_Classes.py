from core import hash_factory
from conf import setting
import os
import time
import shelve
import time
import glob
from functools import reduce
from core import tools

__all__=["School","Session","Teacher","Classes","Student"]

def cut_file(file_list,abs=False):
	"0.dir，拿到0,拿到一个文件列表的所有文件名"
    file_list=list(map(lambda file: os.path.splitext(file)[0], file_list))

    return file_list

def make_id(path):
    '''创建id'''
	#拿到所有的dir为扩展名的所有id
    other_ids=cut_file(glob.glob1(path, "*.dir"))
    print(other_ids)
    if len(other_ids)==0:
        return "0"
    else:
		#拿到最大的那个数，+1就是我要创建的一条信息的id
		#[1,2,3,4,5,6]
		'''
		1和2比较，拿出2和3比较，拿出3和4比较，拿到最终的6
		'''
        max_num=reduce(lambda x,y:max(int(x),int(y)),other_ids)
        return str(int(max_num)+1)

def list_id(path):
    other_ids = cut_file(glob.glob1(path, "*.dir"))
    for id in other_ids:
        print(id)
    return other_ids


class BaseModel(object):
    '''此类属于基类，存放共通属性的地方'''
    # def __init__(self):
    #     self.datetime = time.strftime("%Y-%m-%d")
    #     self.path = os.path.join(self.path, self.id)
    def save(self):
        '''对象保存到文件'''
        path=os.path.splitext(self.path)[0]
        slv=shelve.open(path)
        slv["obj"]=self
        slv.close()

    @classmethod
    def load(cls):
        path = os.path.join(os.path.splitext(cls.path)[0],"0")
        print(path)
        slv = shelve.open(path)
        obj = slv["obj"]
        print(obj)
        slv.close()
    @classmethod
    def show_item_of_obj(cls):
        '''
        显示所有对象属性
        :param items:
        :return:
        '''

        obj_list=[]
        obj=None
        paths=cut_file(glob.glob1(cls.path,"*.dir"))
        # 补全路径
        for pathi,pathv in enumerate(paths):
            paths[pathi]=os.path.join(cls.path,pathv)


        for path in paths:

            slv=shelve.open(path)
            obj_list.append(slv["obj"])
            slv.close()
        return obj_list




class School(BaseModel):
    '''学校'''
    path = os.path.join(setting.DB_DIR, "school")
    def __init__(self,name,addr):
        self.id=make_id(self.path)
        self.name=name
        self.addr=addr
        self.datetime=time.strftime("%Y-%m-%d")
        self.path = os.path.join(self.path, self.id)

    def __str__(self):
        return self.name

    def __del__(self):
        print(tools.make_color("结束创建"))


class Session(BaseModel):
    path = os.path.join(setting.DB_DIR, "session")
    def __init__(self,name,school_obj):
        # try:
        self.id = make_id(self.path)
        self.name=name
        self.school_obj=school_obj
        self.datetime = time.strftime("%Y-%m-%d")
        self.path = os.path.join(self.path, self.id)
        # except Exception as e:
        #     print(tools.make_color(e))
        #     self.__del__()

    def __str__(self):
        return self.name

    def __del__(self):
        print(tools.make_color("结束创建"))


class Teacher(BaseModel):
    path = os.path.join(setting.DB_DIR, "teacher")
    def __init__(self, name,age, school_obj, session_obj):
        self.id = make_id(self.path)
        self.name=name
        self.age=age
        self.school_obj = school_obj
        self.session_obj=session_obj
        self.datetime = time.strftime("%Y-%m-%d")
        self.path = os.path.join(self.path, self.id)

    def __str__(self):
        return self.name

    def __del__(self):
        print(tools.make_color("结束创建"))
class Classes(BaseModel):
    '''
    班级名，班级对应的学校，班级对应的课程，班级对应对的教师
    '''
    path = os.path.join(setting.DB_DIR, "classes")
    def __init__(self, name,school_obj, session_obj,teacher_obj):
        self.id = make_id(self.path)
        self.name=name
        self.school_obj=school_obj
        self.session_obj=session_obj
        self.teacher_obj=teacher_obj
        self.datetime = time.strftime("%Y-%m-%d")
        self.path = os.path.join(self.path, self.id)

    def __str__(self):
        return self.name

    def __del__(self):
        print(tools.make_color("结束创建"))

class Score_Into(BaseModel):
    '''
	分数类
    打完分数可修改
    '''
    path = os.path.join(setting.DB_DIR, "score")
    def __init__(self,student_obj):
        self.id = make_id(self.path)
        self.student_obj = student_obj
        self.scores={} #"第一课":xxx,
    def inter_score(self,score_name,score):
        '''记录成绩，打完成绩后保存到原来位置'''
        self.scores[score_name]=score
        path=os.path.join(self.path,self.id)
        slv=shelve.open(path)
        slv["obj"] = self
        slv.close()


class Student(BaseModel):
    '''学生类,创建一个学生就创建一个学生成绩系统'''
    path = os.path.join(setting.DB_DIR, "student")
    def __init__(self, name,school_obj, session_obj,class_obj):
        self.id = make_id(self.path)
        self.name = name
        self.school_obj = school_obj
        self.session_obj = session_obj
        self.class_obj = class_obj
        self.datetime = time.strftime("%Y-%m-%d")
        self.path = os.path.join(self.path, self.id)
        st1=Score_Into(self)
        st1.save()
        self.score_obj = st1
    def __str__(self):
        return self.name

    def __del__(self):
        print(tools.make_color("结束创建"))

