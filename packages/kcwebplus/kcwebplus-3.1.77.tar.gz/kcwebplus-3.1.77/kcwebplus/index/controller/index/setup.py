from .common import *
import oss2
dqpath=os.path.split(os.path.realpath(__file__))[0]
def customizeProcess(data):
    pid=os.getpid()
    set_cache(md5(data['paths']+data['other']),pid,0)
    os.system("cd "+data['paths']+" && "+data['other'])
def getinterpreter(paths,types,filename,other):
    interpreter=md5(paths+types+filename+other) #解释器
    if types=='python3.6':
        if os.path.isfile('/usr/local/python/python3.6/bin/python3'):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/python/python3.6/bin/python3 /usr/bin/"+interpreter)
        else:
            return False,'未安装python3.6'
    elif types=='python3.8':
        if os.path.isfile('/usr/local/python/python3.8/bin/python3'):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/python/python3.8/bin/python3 /usr/bin/"+interpreter)
        else:
            return False,'未安装python3.8'
    elif types=='python3.9':
        if os.path.isfile('/usr/local/python/python3.9/bin/python3'):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/python/python3.9/bin/python3 /usr/bin/"+interpreter)
        else:
            return False,'未安装python3.9'
    elif types=='npm':
        if os.path.isfile('/usr/local/nodejs/nodejs14.16/bin/npm'):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/nodejs/nodejs14.16/bin/npm /usr/bin/"+interpreter)
        else:
            return False,'未安装npm'
    elif types=='php7.2':
        if os.path.isfile("/usr/local/php/php7.2/bin/php"):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/php/php7.2/bin/php /usr/bin/"+interpreter)
        else:
            return False,'您必须使用本系统的软件插件安装php7.2后才能使用该功能'
    elif types=='php7.3':
        if os.path.isfile("/usr/local/php/php7.3/bin/php"):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/php/php7.3/bin/php /usr/bin/"+interpreter)
        else:
            return False,'您必须使用本系统的软件插件安装php7.3后才能使用该功能'
    elif types=='php7.4':
        if os.path.isfile("/usr/local/php/php7.4/bin/php"):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/php/php7.4/bin/php /usr/bin/"+interpreter)
        else:
            return False,'您必须使用本系统的软件插件安装php7.4后才能使用该功能'
    elif types=='php8.2':
        if os.path.isfile("/usr/local/php/php8.2/bin/php"):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/php/php8.2/bin/php /usr/bin/"+interpreter)
        else:
            return False,'您必须使用本系统的软件插件安装php8.2后才能使用该功能'
    elif types=='php8.3':
        if os.path.isfile("/usr/local/php/php8.3/bin/php"):
            if not os.path.isfile("/usr/bin/"+interpreter):
                os.system("ln -s /usr/local/php/php8.3/bin/php /usr/bin/"+interpreter)
        else:
            return False,'您必须使用本系统的软件插件安装php8.3后才能使用该功能'
    return True,interpreter
class setup:
    def index():
        return response.tpl(dqpath+'/tpl/setup/index.html',absolutelypath=True)
    def basepage():
        "基本配置"
        return response.tpl(dqpath+'/tpl/setup/basepage.html',absolutelypath=True)
    def startpage():
        "开机启动项"
        return response.tpl(dqpath+'/tpl/setup/startpage.html',absolutelypath=True)
    def bacrecpage():
        "备份恢复页面"
        return response.tpl(dqpath+'/tpl/setup/bacrecpage.html',absolutelypath=True)
    def pythonrun():
        "项目管理器"
        response.yunpath=os.getcwd()
        return response.tpl(dqpath+'/tpl/setup/pythonrun.html',absolutelypath=True)
    def getbanddomain():
        G.setadminlog="获取绑定域名"
        status,webitem=kcwebplusdomain.getbanddomain()
        if status:
            return successjson(webitem)
        else:
            return errorjson(msg=webitem)
    def banddomainall():
        G.setadminlog="绑定域名"
        domain=request.get_json()['domain']
        proxy_pass=request.get_json()['proxy_pass']
        status,msg=kcwebplusdomain.banddomainall(domain=domain,proxy_pass=proxy_pass)
        if status:
            return successjson()
        else:
            return errorjson(msg=msg)
    def delbanddomain():
        G.setadminlog="删除绑定域名"
        status,msg=kcwebplusdomain.delbnddomain()
        if status:
            return successjson()
        else:
            return errorjson(msg=msg)
    def restart(types='stop'):
        "启动/停止项目管理"
        G.setadminlog="启动/停止项目管理"
        data=request.get_json()
        if data['types']=='kcwebplus':
            paths=os.getcwd().replace('\\','/')
            if types=='start':
                if 'Linux' in get_sysinfo()['platform']:
                    yunpath=paths+"/app/runtime/log/"+md5(data['other'])+'.log'
                    cmd="cd "+paths+" && nohup kcwebplus "+data['other']+" --cli"+"  > "+yunpath+" 2>&1 &"
                elif 'Windows' in get_sysinfo()['platform']:
                    yunpath=paths+"/app/runtime/log/"+md5(data['other'])+'.log'
                    cmd="start /b kcwebplus "+data['other']+" --cli"#+"  > "+yunpath
                else:
                    return errorjson(msg="不支持该系统")
                kill_route_cli(data['other'])
                time.sleep(0.1)
                os.system(cmd)
                # print(yunpath)
                time.sleep(3)
                if not get_kcweb_cli_info(data['other'],'pid'):
                    return errorjson(msg="启动失败"+cmd)
                else:
                    return successjson()
            elif types=='stop':
                kill_route_cli(data['other'])
                return successjson()
        elif data['types']=='customize':
            if types=='start':
                t=multiprocessing.Process(target=customizeProcess,args=(data,))
                t.daemon=True
                t.start()
            elif types=='stop':
                pid=get_cache(md5(data['paths']+data['other']))
                if pid:
                    kill_pid(pid)
            return successjson()
        else:
            ttt,interpreter=getinterpreter(data['paths'],data['types'],data['filename'],data['other']) #md5(data['paths']+data['types']+data['filename']+data['other']) #解释器
            
            if types=='start':
                if data['paths']=='/kcwebplus':
                    logpath=data['paths']+"/app/runtime/log/"
                else:
                    logpath=data['paths']+"/kcwebplus_log/"
                if not os.path.exists(logpath):
                    os.makedirs(logpath, exist_ok=True)
                yunpath=logpath+interpreter+'.log'
                if data['other']: #带运行参数
                    cmd="cd "+data['paths']+"&& nohup "+interpreter+" "+data['filename']+" "+data['other']+"  > "+yunpath+" 2>&1 &"
                    os.system(cmd)
                else:
                    cmd="cd "+data['paths']+"&& nohup "+interpreter+" "+data['filename']+"  > "+yunpath+" 2>&1 &"
                    os.system(cmd)
                time.sleep(3)
                if get_process_id(interpreter):
                    return successjson()
                else:
                    return errorjson(data=cmd,msg="启动失败")
            elif types=='stop':
                if data['types']=='npm':
                    os.system("pkill -9 node")
                else:
                    os.system("pkill -9 "+interpreter[:12])
                return successjson()
    def setpythonrun():
        "设置/添加项目管理"
        G.setadminlog="设置/添加项目管理"
        data=request.get_json()
        if data['types']=='kcwebplus':
            if 'Linux' in get_sysinfo()['platform'] or 'Windows' in get_sysinfo()['platform']:
                pass
            else:
                return errorjson(msg="不支持该系统")
            paths=os.getcwd().replace('\\','/')
            if not data['other']:
                return errorjson(msg='kcwebplus项目路由地址不能为空')
            data['other']=data['other'].replace(' ','')
            if data['other'][0:6]=='server':
                return errorjson(msg='不支持该路由参数')
            if data['id']:
                if sqlite("pythonrun").where("id!='"+str(data['id'])+"' and types='"+data['types']+"' and other='"+data['other']+"'").count():
                    return errorjson(msg='该路由地址已存在')
            else:
                if sqlite("pythonrun").where("types='"+data['types']+"' and other='"+data['other']+"'").count():
                    return errorjson(msg='该路由地址已存在')
            if not  os.path.exists(paths+"/app/runtime/log/"):
                os.makedirs(paths+"/app/runtime/log/", exist_ok=True)
            if data['id']:
                data.update(updtime=times(),addtime=times())
                del data['status']
                try:
                    del data['interpreter']
                except:pass
                try:
                    data['process']
                except:pass
                sqlite("pythonrun").where("id",data['id']).update(data)
            else:
                del data['id']
                data.update(updtime=times(),addtime=times())
                sqlite("pythonrun").insert(data)
            return successjson()
        elif data['types']=='customize':
            if not data['paths']:
                return errorjson(msg='请选择运行目录')
            if not data['other']:
                return errorjson(msg='请输入命令')
            if not os.path.exists(data['paths']+"/kcwebplus_log"):
                os.makedirs(data['paths']+"/kcwebplus_log", exist_ok=True)
            if data['id']:
                data.update(updtime=times(),addtime=times())
                del data['status']
                try:
                    data['process']
                except:pass
                sqlite("pythonrun").where("id",data['id']).update(data)
            else:
                del data['id']
                data.update(updtime=times(),addtime=times())
                sqlite("pythonrun").insert(data)
            return successjson()
        elif 'Linux' in get_sysinfo()['platform']:
            ttt,interpreter=getinterpreter(data['paths'],data['types'],data['filename'],data['other']) #解释器
            if not ttt:
                return errorjson(msg=interpreter)
            if data['paths']=='/kcwebplus':
                if not os.path.exists(data['paths']+"/app/runtime/log"):
                    os.makedirs(data['paths']+"/app/runtime/log", exist_ok=True)
            else:
                if not os.path.exists(data['paths']+"/kcwebplus_log"):
                    os.makedirs(data['paths']+"/kcwebplus_log", exist_ok=True)
            if data['id']:
                arr=sqlite("pythonrun").where("id",data['id']).find()
                ttt,interpreterj=getinterpreter(arr['paths'],arr['types'],arr['filename'],arr['other']) #解释器
                if interpreterj!=interpreter:#删除之前的
                    os.system("pkill -9 "+interpreterj[:12])
                    try:
                        os.remove("/usr/bin/"+interpreterj)
                    except:pass
                data.update(updtime=times(),addtime=times())
                del data['status']
                del data['interpreter']
                try:
                    data['process']
                except:pass
                sqlite("pythonrun").where("id",data['id']).update(data)
                return successjson()
            else:
                del data['id']
                data.update(updtime=times(),addtime=times())
                sqlite("pythonrun").insert(data)
                return successjson()
        else:
            return errorjson(msg="不支持该系统，当前只支持linux")
    def logpythonrun(id):
        "项目管理日志"
        G.setadminlog="项目管理日志"
        arr=sqlite("pythonrun").where('id',id).find()
        if arr['types']=='kcwebplus':
            if 'Windows' in get_sysinfo()['platform']:
                return errorjson(msg='暂不支持Windows')
            paths=os.getcwd().replace('\\','/')
            yunpath=paths+"/app/runtime/log/"+md5(arr['other'])+'.log'
            f=open(yunpath)
            data=f.read()
            f.close()
            return successjson(data)
        elif arr['types']=='customize':
            return errorjson(msg='暂不支持自定义命令日志')
        else:
            ttt,interpreter=getinterpreter(arr['paths'],arr['types'],arr['filename'],arr['other']) #解释器
            # data=file_get_content(arr['paths']+"/"+interpreter+".log")
            
            if arr['paths']=='/kcwebplus':
                logpath=arr['paths']+"/app/runtime/log/"
                yunpath=logpath+interpreter+'.log'
            else:
                logpath=arr['paths']+"/kcwebplus_log/"
            if not os.path.exists(logpath):
                os.makedirs(logpath, exist_ok=True)
            yunpath=logpath+interpreter+'.log'
            f=open(yunpath)
            data=f.read()
            f.close()
            return successjson(data)
    def delpythonrun(id=''):
        "删除项目管理"
        G.setadminlog="删除项目管理"
        try:
            if id:
                id=[id]
            else:
                id=request.get_json()
            arr=sqlite("pythonrun").where('id','in',id).field("paths,types,filename,other").select()
            for k in arr:
                if k['types']=='kcwebplus':
                    kill_route_cli(k['other'])
                elif k['types']=='customize':
                    pid=get_cache(md5(k['paths']+k['other']))
                    if pid:
                        kill_pid(pid)
                else:
                    ttt,interpreter=getinterpreter(k['paths'],k['types'],k['filename'],k['other']) #解释器
                    os.system("pkill -9 "+interpreter[:12])
                    if os.path.isfile("/usr/bin/"+interpreter):
                        os.remove("/usr/bin/"+interpreter)
            sqlite("pythonrun").where('id','in',id).delete()
        except:
            return errorjson(msg="失败")
        else:
            return successjson()
    def pythonrulists(id=''):
        "项目管理列表"
        if id:
            return successjson(sqlite("pythonrun").find(id))
        where=None
        kw=request.args.get('kw')
        pagenow=request.args.get('pagenow')
        pagesize=request.args.get('pagesize')
        if kw:
            where=[("title","like","%"+str(kw)+"%"),'or',("descs","like","%"+str(kw)+"%")]
        if not pagenow:
            pagenow=1
        else:
            pagenow=int(pagenow)
        if not pagesize:
            pagesize=10
        else:
            pagesize=int(pagesize)
        lists=sqlite("pythonrun").where(where).page(pagenow,pagesize).select()
        for k in lists:
            if k['types']=='kcwebplus':
                k['interpreter']='kcwebplus'
                if get_kcweb_cli_info(k['other'],'pid'):
                    k['status']=1 #运行中
                else:
                    k['status']=0 #已停止
            elif k['types']=='customize':
                k['interpreter']=''
                pid=get_cache(md5(k['paths']+k['other']))
                if get_pid_info(pid):
                    k['status']=1 #运行中
                else:
                    k['status']=0 #已停止
            else:
                ttt,interpreter=getinterpreter(k['paths'],k['types'],k['filename'],k['other']) #解释器
                k['interpreter']=interpreter
                if get_process_id(interpreter):
                    k['status']=1 #运行中
                else:
                    k['status']=0 #已停止
        count=sqlite("pythonrun").where(where).count()
        data=return_list(lists,count,pagenow,pagesize)
        return successjson(data)
    def setbaseconfig(types='get'):
        "保存配置信息"
        if types=='get':
            return successjson(getbaseconfig())
        else:
            G.setadminlog="保存配置信息"
            getbaseconfig(types=types,config=request.get_json())
            return successjson(msg="保存成功")

    def addstart():
        "添加启动项"
        G.setadminlog="添加启动项"
        data=request.get_json()
        if sqlite("start").connect(model_app_path).where("value",data['value']).count():
            return errorjson(msg="禁止重复添加")
        try:
            icon=data['icon']
        except:
            icon=''
        if system_start.insert_Boot_up(cmd=data['value'],name=data['name'],types=data['types'],admin_id=G.userinfo['id'],icon=icon):
            return successjson()
        else:
            return errorjson(msg="添加失败，该系统支不支持")
    def delstart():
        G.setadminlog="删除启动项"
        data=request.get_json()
        if system_start.del_Boot_up(cmd=data['value'],id=data['id']):
            return successjson()
        else:
            return errorjson()
    def startlist():
        "启动项列表"
        pagenow=request.args.get('pagenow')
        pagesize=request.args.get('pagesize')
        if not pagenow:
            pagenow=1
        else:
            pagenow=int(pagenow)
        if not pagesize:
            pagesize=100
        else:
            pagesize=int(pagesize)
        yz=system_start.lists(pagenow,pagesize)
        lists=yz[0]
        count=yz[1]
        data=return_list(lists,count,pagenow,pagesize)
        
        return successjson(data)

    def aliyunosslist(types='app'):
        if not os.path.isfile("app/common/file/config.conf"):
            return errorjson(msg="请先配置阿里云oss配置信息")
        data=json_decode(file_get_content("app/common/file/config.conf"))
        prefix=request.args.get("prefix")
        if not prefix:
            if types=='app':
                prefix="backups/"+data['aliyun']['backpath']+"/app/"
            else:
                prefix="backups/"+data['aliyun']['backpath']+"/backup/mysql/"
        data=[]
        try:
            fileconfig=json_decode(file_get_content("app/common/file/config.conf"))
            auth = oss2.Auth(fileconfig['aliyun']['access_key'],fileconfig['aliyun']['access_key_secret'])
            bucket = oss2.Bucket(auth,fileconfig['aliyun']['address'],fileconfig['aliyun']['bucket'])
            # 列举fun文件夹下的文件与子文件夹名称，不列举子文件夹下的文件。
            
            for obj in oss2.ObjectIterator(bucket, prefix = prefix, delimiter = '/'):
                # 通过is_prefix方法判断obj是否为文件夹。
                if obj.is_prefix():  # 文件夹
                    data.insert(0,{"name":obj.key.split("/")[-2],"path":obj.key,"type":"folder"})
                else:                # 文件
                    data.insert(0,{"name":obj.key.split("/")[-1],"path":obj.key,"type":"file"})
        except:pass
        # data1=[]
        # i=len(data)
        # while True:
        #     i+=1
        #     if i<0:
        #         break
        #     else:
        #         data1.append(data[i])
        return successjson(data)
    def aliyunossdownload(types=""):
        "从阿里云备份点恢复"
        if not os.path.isfile("app/common/file/config.conf"):
            return errorjson(msg="请先配置阿里云oss配置信息")
        fileconfig=json_decode(file_get_content("app/common/file/config.conf"))
        auth = oss2.Auth(fileconfig['aliyun']['access_key'],fileconfig['aliyun']['access_key_secret'])
        bucket = oss2.Bucket(auth,fileconfig['aliyun']['address'],fileconfig['aliyun']['bucket'])
        filepath=request.args.get("filepath")
        if types=='mysql': #恢复mysql
            pass
        else: #恢复文稿
            bucket.get_object_to_file(filepath, "backup.zip")
            kcwebzip.unzip_file("backup.zip","backup/app")
            os.remove("backup.zip")
            if os.path.exists("backup/app"):
                filelist=get_file("backup/app")
                for k in filelist:
                    if k['type']=='folder' and '__pycache__' not in k['path']:
                        if 'common/file' == k['path'][-11:]:
                            path=re.sub("backup/","",k['path'])
                            if os.path.exists(path):
                                shutil.rmtree(path)
                            shutil.copytree(k['path'],path)
        return successjson()
    def backup(types=''):
        "备份全部"
        G.setadminlog="备份全部"
        paths=request.args.get("paths")
        if paths: #备份目录  app/common/file
            shutil.copytree(paths,"backup/"+paths)
        else: #备份全部
            filelist=get_file("app")
            if os.path.exists("backup"):
                shutil.rmtree("backup")
            for k in filelist:
                if k['type']=='folder' and '__pycache__' not in k['path']:
                    if 'common/file' == k['path'][-11:]:
                        shutil.copytree(k['path'],"backup/"+k['path'])
                        # print(k['path'],"backup/"+k['path'])
        if types=='aliyun':#备份文件上传到阿里云oss
            if not os.path.isfile("app/common/file/config.conf"):
                print("您没有保存阿里云oss修改配置信息而无法上传")
            else:
                fileconfig=json_decode(file_get_content("app/common/file/config.conf"))
                backpath=fileconfig['aliyun']['backpath']
                if backpath:
                    if backpath[:1]=='/':
                        backpath=backpath[1:]
                    if backpath[-1]=='/':
                        backpath=backpath[:-1]
                else:
                    backpath="kcweb"
                auth = oss2.Auth(fileconfig['aliyun']['access_key'],fileconfig['aliyun']['access_key_secret'])
                bucket = oss2.Bucket(auth,fileconfig['aliyun']['address'],fileconfig['aliyun']['bucket'])
                kcwebzip.packzip("backup/app","backup/app.zip")
                oss2.resumable_upload(bucket,"backups/"+backpath+"/app/"+time.strftime("%Y%m%d-%H:%M:%S",time.localtime(times()))+".zip","backup/app.zip")
                filelist=[]
                for obj in oss2.ObjectIterator(bucket, prefix="backups/"+backpath+"/app/"):
                    filelist.append(obj.key)
                i=0
                while True:
                    if len(filelist)-i <= 30: #在阿里云保留30个备份文件
                        break
                    bucket.delete_object(filelist[i])
                    i+=1
                os.remove("backup/app.zip")
                print("上传到阿里云oss成功")
        if not config.app['cli']:
            return successjson(msg="所有文稿备份成功")
    def recovery():
        "恢复文稿"
        G.setadminlog="恢复文稿"
        paths=request.args.get("paths")
        if paths: #恢复指定目录 app/common/file
            shutil.copytree("backup/"+paths,paths)
        elif os.path.exists("backup/app"): #恢复全部文稿
            filelist=get_file("backup/app")
            for k in filelist:
                if k['type']=='folder' and '__pycache__' not in k['path']:
                    if 'common/file' == k['path'][-11:]:
                        path=re.sub("backup/","",k['path'])
                        if os.path.exists(path):
                            shutil.rmtree(path)
                        shutil.copytree(k['path'],path)
                        print(k['path'],path)
            return successjson(msg="所有文稿恢复成功")
        else:
            return errorjson(msg="备份目录不存在")
    def download(name=""):
        "下载备份文件"
        G.setadminlog="下载备份文件"
        if os.path.exists("backup"):
            kcwebzip.packzip("backup","backup.zip")
            f=open("backup.zip","rb")
            body=f.read()
            f.close()
            os.remove("backup.zip")
            return body,"200 ok",{"Content-Type":"application/zip","Accept-Ranges":"bytes"}
        else:
            return "没有备份文件，请备份文件后再下载"
    def postsup():
        "上传备份文件"
        G.setadminlog="上传备份文件"
        if request.binary.save('file',"backup."+request.binary.filesuffix('file')):
            kcwebzip.unzip_file("backup.zip","backup")
            os.remove("backup.zip")
            return successjson()
        else:
            return errorjson(msg="上传失败")
    def dowfile(name=''):
        "下载指定文件"
        G.setadminlog="下载指定文件"
        pathname=request.args.get("pathname")
        return response.download(pathname)
    def uploadfile():
        "上传文件导指定目录"
        G.setadminlog="上传文件导指定目录"
        pathname=request.args.get("pathname")
        if request.binary.save('file',pathname):
            return successjson()
        else:
            return errorjson(msg="上传失败")
    def backxz(name=''):
        "压缩指定文件夹并下载"
        G.setadminlog="压缩指定文件夹并下载"
        paths=request.args.get("paths")
        kcwebzip.packzip(paths,"backxz.zip")
        f=open("backxz.zip","rb")
        body=f.read()
        f.close()
        os.remove("backxz.zip")
        return body,"200 ok",{"Content-Type":"application/zip","Accept-Ranges":"bytes"}
    def upunback():
        "上传zip压缩包并解压指定文件夹"
        G.setadminlog="上传zip压缩包并解压指定文件夹"
        paths=request.args.get("paths")
        if request.binary.save('file',"backxz."+request.binary.filesuffix('file')):
            try:
                kcwebzip.unzip_file("backxz.zip",paths)
                os.remove("backxz.zip")
            except:
                return errorjson(msg="文件格式错误")
            return successjson()
        else:
            return errorjson(msg="上传失败")
        return successjson()
