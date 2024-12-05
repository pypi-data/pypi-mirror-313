from .common import *
dqpath=os.path.split(os.path.realpath(__file__))[0]
def before_request():
    pass
class pub:
    def outlogin():
        account_token=request.args.get("account_token")
        if account_token:
            del_cache(account_token)
        else:
            del_session('userinfo')
        return successjson()
    def get_account_token(username,sign,timestamp,random,types="get_account_token"):
        "获取用户token"
        status,code,msg,account_token=serlogin(username,sign,timestamp,random,types)
        if status:
            return successjson(data={"account_token":account_token},msg=msg)
        else:
            return errorjson(code=-1,msg=msg)
    def login(username,sign,timestamp,random,types="session"):
        "登录"
        G.setadminlog=username+",登录系统"
        status,code,msg,account_token=serlogin(username,sign,timestamp,random,types)
        if status:
            return successjson(data=account_token,msg=msg)
        else:
            return errorjson(code=code,msg=msg)
    def addr():
        return successjson(request.HEADER.Physical_IP())

    def getkcweb():
        config.kcweb['path']=get_kcweb_folder()
        return successjson(config.kcweb)
    
    def checkserver():
        return successjson()
    # def script(assembly='core',t=''):
    #     ETag=md5('567890'+assembly+t+globals.HEADER.URL)
    #     response.r=ETag
    #     response.h5url=json_encode({
    #         'describe':'', #这里是前端的域名
    #         'h5':'',
    #     })
    #     response.lang=json_encode({
    #         'function':{},
    #         'lang':{}
    #     })
    #     pixelunit='rem'
    #     HTTP_USER_AGENT=request.HEADER.HTTP_USER_AGENT()
    #     if 'Android' in HTTP_USER_AGENT:
    #         if 'MQQBrowser' in HTTP_USER_AGENT or 'AlipayClient' in HTTP_USER_AGENT:
    #             pixelunit='px'
    #         elif 'Android 10' in HTTP_USER_AGENT or 'Android 9' in HTTP_USER_AGENT or 'Android 8' in HTTP_USER_AGENT or 'Android 7' in HTTP_USER_AGENT or 'Android 6' in HTTP_USER_AGENT or 'Android 5' in HTTP_USER_AGENT:
    #             pixelunit='px'
    #     response.pixelunit=pixelunit
    #     response.otherconfig=json_encode({
    #         'adminphone':375, #后台设计模板时手机屏幕宽 (注：该值不可以修改，否则将对bcni的项目rem布局造成重大影响)
    #         'pixelunit':pixelunit,#像素单位
    #         'rem':1,
    #         'HTTP_USER_AGENT':HTTP_USER_AGENT
    #     })
    #     response.interurl=json_encode({ #后端接口域名
    #         'inter':''
    #     })
    #     response.staticurl=config.domain['kcwebstatic']+'/'
    #     if assembly:
    #         try:
    #             assemblys=assembly.split(',')
    #         except:
    #             assemblys=[]
    #         assemblyss=[]
    #         jsarr=[]
    #         cssarr=[]
    #         for k in assemblys:
    #             if 'layer'==k:
    #                 jsarr.append(config.domain['kcwebstatic']+'/'+'layer/3.1.1/layer.js')
    #             elif 'jquery'==k:
    #                 jsarr.append(config.domain['kcwebstatic']+'/'+'jquery/2.2.4/jquery.min.js')
    #             elif 'echarts'==k:
    #                 jsarr.append(config.domain['kcwebstatic']+'/'+'echarts/5.5.0/echarts.min.js')
    #             elif 'wangeditor'==k:
    #                 jsarr.append(config.domain['kcwebstatic']+'/'+'wangeditor/index.js')
    #                 cssarr.append(config.domain['kcwebstatic']+'/'+'wangeditor/css/style.css')
    #             else:
    #                 assemblyss.append(k)
    #         response.assembly=assemblyss
    #         response.jsarr=jsarr
    #         response.cssarr=cssarr
    #     return response.tpl(dqpath+'/tpl/static/script.html',response_cache=True,ETag=ETag,header={"Content-type":"application/javascript; charset=utf-8","Access-Control-Allow-Origin":"*","Access-Control-Allow-Credentials":"true"})
    def clistartplan():
        #这里是初始化计划任务 （cli方式运行）
        try:
            serverserverintervals=sqlite("interval",model_intapp_index_path).select()
            if serverserverintervals and (times()-int(serverserverintervals[0]['updtime'])) > 5:
                for serverserverinterval in serverserverintervals:
                        serverserverinterval['updtime']=times()
                        sqlite("interval",model_intapp_index_path).where("id",serverserverinterval['id']).update(serverserverinterval)
                        PLANTASK.plantask(serverserverinterval) #添加计划任务
                while True:
                    time.sleep(100)
        except:
            pass
    def webclosemsg(a1='',a2='',a3='',a4='',a5='',a6='',a7='',a8='',a9='',a10=''):
        format='json'
        if format=='html':
            return '您访问的站点正在维护中，暂时无法访问，请稍后在试'
        elif format=='json':
            return errorjson(code=-1,msg='您访问的站点正在维护中，暂时无法访问，请稍后在试')
    def gitpull():
        "执行git"
        path=request.args.get('path')
        branch=request.args.get('branch') #强制更新指定分支
        title=request.args.get('title')
        taskid=md5(randoms()+str(times()))
        if not title:
            title="git pull，"+path
        if 'Linux' in get_sysinfo()['platform']:
            shell='cd '+path+' && git reset --hard'
            if branch:
                shell+=' origin/'+branch
            shell+=' && git clean -f && git pull'
            Queues.insert(target=PUBLICOther.gitpull,args=(taskid,path,shell),title=title,describes="执行命令："+shell,taskid=taskid,start=10,updtime=times()+1)
        elif 'Window' in get_sysinfo()['platform']:
            shell="git reset --hard"
            if branch:
                shell+=' origin/'+branch
            Queues.insert(target=PUBLICOther.gitpull,args=(taskid,path,shell),title=title,describes="执行命令："+shell,taskid=taskid)
            shell='git clean -f'
            Queues.insert(target=PUBLICOther.gitpull,args=(taskid,path,shell),title=title,describes="执行命令："+shell,taskid=taskid)
            shell='git pull'
            Queues.insert(target=PUBLICOther.gitpull,args=(taskid,path,shell),title=title,describes="执行命令："+shell,taskid=taskid)
        G.setadminlog="执行命令："+shell
        return successjson("命令已添加到任务队列中")
    
class PUBLICOther():
    def gitpull(taskid,path,shell):
        pi=subprocess.Popen(shell,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        strs=pi.stdout.read().decode()
        if path=='/kcwebplus/pythoninvdatap':
            try:
                os.remove("app/zcg.zip")
            except:pass
            # time.sleep(1)
            kcwebzip.packzip("pythoninvdatap/app/zcg","app/zcg.zip")
            kcwebzip.unzip_file("app/zcg.zip","app/zcg")
            try:
                os.remove("app/zcg.zip")
            except:pass
            strs="文件已更新："+strs
        Queues.setfield(taskid,'msg',"执行结果："+str(strs))
        # f=open(path+"/gitpull.log","w",encoding='utf-8')
        # f.write("\n时间:%s\n%s\n%s\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),shell,strs))
        # f.close()


    