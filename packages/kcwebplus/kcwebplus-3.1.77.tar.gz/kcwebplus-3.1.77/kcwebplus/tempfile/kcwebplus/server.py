#项目运行文件，请务修改
import kcw,sys,app
app=kcw.web(__name__,app)
if __name__ == "__main__":
    try:
        route=sys.argv[1]
        if "eventlog"==route:
            raise Exception("")
    except:
        #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3) 
        app.run(host="0.0.0.0",port="39001",name="python3.8")
    else:
        app.cli(route)
