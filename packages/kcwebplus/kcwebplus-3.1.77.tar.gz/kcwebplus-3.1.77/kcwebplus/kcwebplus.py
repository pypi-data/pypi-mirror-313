try:
    from .common import *
except Exception as e:
    if 'unable to open database file' in str(e):
        print('该命令仅支持运行kcwebplus项目')
        exit()
    else:
        print('e',e)
from kcweb import kcweb
def cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr='kcwebplus'):
        "脚本入口"
        cmd_par=kcweb.kcw.get_cmd_par(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr)
        if cmd_par and not cmd_par['project']:
            cmd_par['project']='kcwebplus'
        if cmd_par and cmd_par['server'] and not cmd_par['help']:#启动web服务
            try:
                Queues.delwhere("code in (2,3)")
            except:pass
            #执行kcwebplus自启项
            try:
                startdata=sqlite().connect(model_app_path).where("types='kcwebplus'").table("start").order("id asc").select()
            except:
                print("需要在kcwebplus项目中执行")
                exit()
            for teml in startdata:
                os.system(teml['value'])
            if get_sysinfo()['uname'][0]=='Linux':
                system_start.insert_Boot_up(cmd='cd /kcwebplus && bash server.sh',name='kcwebplus自启',icon='https://img.kwebapp.cn/icon/kcweb.png')
                os.system('nohup kcwebplus index/index/pub/clistartplan --cli > app/runtime/log/server.log 2>&1 &')
        if cmd_par and cmd_par['install'] and not cmd_par['help']:#插入 应用、模块、插件
            if cmd_par['appname']:
                remppath=os.path.split(os.path.realpath(__file__))[0]
                if not os.path.exists(cmd_par['project']+'/'+cmd_par['appname']) and not os.path.exists(cmd_par['appname']):
                    shutil.copytree(remppath+'/tempfile/kcwebplus',cmd_par['project'])
                    if get_sysinfo()['uname'][0]=='Linux':
                        try:
                            os.remove(cmd_par['project']+"/server.bat")
                        except:pass
                    elif get_sysinfo()['uname'][0]=='Windows':
                        try:
                            os.remove(cmd_par['project']+"/server.sh")
                        except:pass
                    print('项目创建成功')
                else:
                    t=kcweb.cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr)
            else:
                t=kcweb.cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr)
        elif cmd_par:
            t=kcweb.cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr)