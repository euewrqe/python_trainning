from core import tools
from core.Base_Classes import School,Session,Teacher,Classes,Student
def action_to_school():
    '''管理学校'''
    def create():
        name=input("请输入学校名")
        addr=input("请输入学校地址")
        obj=School(name,addr)
        obj.save()
        print(tools.make_color("学校名[%s],学校地址[%s],创建时间[%s],创建完毕"%(obj.name,obj.addr,obj.datetime),"yellow"))
    def select():
        msg_list=School.show_item_of_obj()
        for obj in msg_list:
             print(tools.make_color("学校名[%s],学校地址[%s],创建时间[%s]" % (obj.name, obj.addr,obj.datetime), "yellow"))
    def delete():
        pass

    action_dict={
        1:create,
        2:select,
        3:delete
    }
    while True:
        func=tools.input_mod(action_dict,title="管理学校")
        if func == "exit":
            break
        else:
            func()

def action_to_session():
    '''管理课程'''
    def create():
        name=input("请输入课程名")
        msg_list = School.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,学校名[%s],学校地址[%s]" % (i,obj.name, obj.addr), "yellow"))
        school_num=int(input("请选择课程所在的学校的编号"))
        school_obj=msg_list[school_num]
        obj = Session(name, school_obj)
        obj.save()
        print(tools.make_color("课程名[%s],课程所在学校[%s],创建时间[%s],创建完毕"%(obj.name,obj.school_obj.name,obj.datetime),"yellow"))

    def select():
        msg_list = Session.show_item_of_obj()
        for obj in msg_list:
            print(tools.make_color("课程名[%s],课程所在学校[%s],创建时间[%s]" % (obj.name,obj.school_obj.name,obj.datetime), "yellow"))


    def delete():
        pass
    action_dict = {
        1: create,
        2: select,
        3: delete
    }
    while True:
        func = tools.input_mod(action_dict, title="管理课程")
        if func == "exit":
            break
        else:
            func()
def action_to_teacher():
    '''管理教师'''
    def create():
        name = input("请输入教师名")
        age = input("教师年龄")
        msg_list = School.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,学校名[%s],学校地址[%s]" % (i,obj.name, obj.addr), "yellow"))
        school_num=int(input("请选择课程所在的学校的编号"))
        school_obj=msg_list[school_num]
        msg_list = Session.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,课程名[%s],学校名[%s]" % (i,obj.name, obj.school_obj.name), "yellow"))
        session_num=int(input("请选择课程的编号"))
        session_obj=msg_list[session_num]
        obj = Teacher(name,age, school_obj,session_obj)
        obj.save()
        print(tools.make_color("老师名字[%s],年龄[%s],学校名[%s],课程名[%s],创建时间[%s],创建完毕"%
                               (obj.name,obj.age,obj.school_obj.name,obj.session_obj.name,obj.datetime),"yellow"))

    def select():
        msg_list = Teacher.show_item_of_obj()
        for obj in msg_list:
            print(tools.make_color("老师名字[%s],年龄[%s],学校名[%s],课程名[%s]" %
                                   (obj.name,obj.age,obj.school_obj.name,obj.session_obj.name), "yellow"))
    def delete():
        pass

    action_dict = {
        1: create,
        2: select,
        3: delete
    }
    while True:
        func = tools.input_mod(action_dict, title="管理教师")
        if func == "exit":
            break
        else:
            func()
    pass
def action_to_class():
    '''管理班级'''
    def create():
        name = input("请输入班级名")
        #关联学校
        msg_list = School.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,学校名[%s],学校地址[%s]" % (i,obj.name, obj.addr), "yellow"))
        school_num=int(input("请选择课程所在的学校的编号"))
        school_obj=msg_list[school_num]
        #关联课程
        msg_list = Session.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,课程名[%s],学校名[%s]" % (i,obj.name, obj.school_obj.name), "yellow"))
        session_num=int(input("请选择课程的编号"))
        session_obj=msg_list[session_num]
        #关联老师
        msg_list = Teacher.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,老师名字[%s],课程名[%s]" % (i,obj.name, obj.session_obj.name), "yellow"))
        teacher_num=int(input("请选择老师的编号"))
        teacher_obj=msg_list[teacher_num]
        obj = Classes(name, school_obj, session_obj,teacher_obj)
        obj.save()

        print(tools.make_color("班级名[%s],学校名[%s],课程名[%s],关联老师[%s],创建时间[%s],创建完毕" %
                           (obj.name, obj.school_obj.name, obj.session_obj.name, obj.teacher_obj.name, obj.datetime), "yellow"))

    def select():
        msg_list = Classes.show_item_of_obj()
        for obj in msg_list:
            print(tools.make_color("班级名[%s],学校名[%s],课程名[%s],关联老师[%s],创建时间[%s]" %
                                   (obj.name,obj.school_obj.name,obj.session_obj.name,obj.teacher_obj.name,obj.datetime), "yellow"))
    def delete():
        pass

    action_dict = {
        1: create,
        2: select,
        3: delete
    }
    while True:
        func = tools.input_mod(action_dict, title="管理班级")
        if func == "exit":
            break
        else:
            func()
def action_to_student():
    '''管理学生'''
    def create():
        name = input("请输入学生名")
        # 关联学校
        msg_list = School.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,学校名[%s],学校地址[%s]" % (i,obj.name, obj.addr), "yellow"))
        school_num=int(input("请选择课程所在的学校的编号"))
        school_obj=msg_list[school_num]

        # 关联课程
        msg_list = Session.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,课程名[%s],学校名[%s]" % (i,obj.name, obj.school_obj.name), "yellow"))
        session_num=int(input("请选择课程的编号"))
        session_obj=msg_list[session_num]

        #关联班级
        msg_list = Classes.show_item_of_obj()
        for i,obj in enumerate(msg_list):
            print(tools.make_color("%s,班级名[%s],学校名[%s],课程名[%s],关联老师[%s]" %
                                   (i,obj.name, obj.school_obj.name,obj.session_obj.name,obj.teacher_obj.name), "yellow"))
        class_num=int(input("请选择班级的编号"))
        class_obj=msg_list[class_num]
        obj = Student(name, school_obj, session_obj,class_obj)
        obj.save()

        print(tools.make_color("学生名[%s],学校名[%s],课程名[%s],关联班级[%s],创建时间[%s],创建完毕" %
                           (obj.name, obj.school_obj.name, obj.session_obj.name, obj.class_obj.name, obj.datetime),
                           "yellow"))

    def select():
        msg_list = Teacher.show_item_of_obj()
        for obj in msg_list:
            print(tools.make_color("学生名[%s],学校名[%s],课程名[%s],关联班级[%s],创建时间[%s]" %
                                   (obj.name, obj.school_obj.name, obj.session_obj.name, obj.class_obj.name, obj.datetime), "yellow"))
    def delete():
        pass

    action_dict = {
        1: create,
        2: select,
        3: delete
    }
    while True:
        func = tools.input_mod(action_dict, title="管理学生")
        if func == "exit":
            break
        else:
            func()
    pass
def main():
    manager_menu_dict={
        1:action_to_school,
        2:action_to_session,
        3:action_to_teacher,
        4:action_to_class,
        5:action_to_student,
    }
    while True:
        func=tools.input_mod(manager_menu_dict,"管理员入口")
        if func == "exit":
            break
        else:
            func()

