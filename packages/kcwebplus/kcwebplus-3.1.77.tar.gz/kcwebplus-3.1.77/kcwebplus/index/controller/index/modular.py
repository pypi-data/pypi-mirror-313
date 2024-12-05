from .common import *
kcwebuserinfopath=os.path.split(os.path.realpath(__file__))[0]+"/common/file/"
dqpath=os.path.split(os.path.realpath(__file__))[0]
class modular:
    def index():
        return response.tpl(dqpath+'/tpl/modular/index.html',absolutelypath=True)
    if not os.path.exists(kcwebuserinfopath):
        os.makedirs(kcwebuserinfopath)
    def kcwebsebduser():
        data=request.get_json()
        http=Http()
        http.openurl(config.domain['kcwebapi']+"/pub/sebduser","POST",data)
        res=json_decode(http.get_text)
        return response.json(res)
    def kcwebreg():
        data=request.get_json()
        http=Http()
        http.openurl(config.domain['kcwebapi']+"/pub/reg","POST",data)
        res=json_decode(http.get_text)
        return response.json(res)
    def banduser():
        data=request.get_json()
        http=Http()
        timestamp=times()
        sign=md5(str(data['username'])+str(timestamp)+md5(md5(data['password'])))
        http.set_header['username']=data['username']
        http.set_header['timestamp']=str(timestamp)
        http.set_header['sign']=sign
        http.openurl(config.domain['kcwebapi']+"/user/userinfo")
        res=json_decode(http.get_text)
        if(res['code']==0):
            kcwebuserinfo=res['data']
            kcwebuserinfo['username']=data['username']
            kcwebuserinfo['password']=data['password']
            file_set_content(kcwebuserinfopath+str(G.userinfo['id']),json_encode(kcwebuserinfo))
            return successjson()
        else:
            return errorjson(msg=res['msg'])
        
    def modular_list(kw='',pagenow=1):
        http=Http()
        http.openurl(config.domain['kcwebapi']+"/pub/modular_list","get",params={
            "kw":kw,"pagenow":pagenow
        })
        res=json_decode(http.get_text)
        lists=res['data']['lists']
        for k in lists:
            k['status']=0 #0未安装  1已安装  2安装中 3卸载中 4不可以安装
            if os.path.exists("app/"+str(k['name'])):
                k['status']=1
        if os.path.isfile(kcwebuserinfopath+str(G.userinfo['id'])):
            kcwebuserinfo=file_get_content(kcwebuserinfopath+str(G.userinfo['id']))
        else:
            kcwebuserinfo=''
        if kcwebuserinfo:
            res['kcwebuserinfo']=json_decode(kcwebuserinfo)
        else:
            res['kcwebuserinfo']=''
        return response.json(res)

    def uploadmodular():
        "打包模块上传"
        G.setadminlog="打包模块上传模块"
        kcwebuserinfo=file_get_content(kcwebuserinfopath+str(G.userinfo['id']))
        if kcwebuserinfo:
            kcwebuserinfo=json_decode(kcwebuserinfo)
            data=request.get_json()
            server=create("app",data['name'])
            data=server.packmodular()
            if data[0]:
                data=server.uploadmodular(kcwebuserinfo['username'],kcwebuserinfo['password'])
                if data[0]:
                    return successjson()
                else:
                    return errorjson(msg=data[1])
            return errorjson(msg=data[1])
        else:
            return errorjson("请先配置kcweb账号")
    def installmodular():
        "安装模块"
        G.setadminlog="安装模块"
        arr=request.get_json()
        server=create("app",arr['name'])
        data=server.installmodular(arr['token'])
        time.sleep(1)
        if data[0]:
            # model_intapp_menu.add(title=arr['title'],icon=arr['icon'],url="/"+arr['name'])
            return successjson()
        else:
            return errorjson(msg=data[1])
    def uninstallmodular():
        "卸载模块"
        G.setadminlog="卸载模块"
        arr=request.get_json()
        server=create("app",arr['name'])
        data=server.uninstallmodular()
        time.sleep(1)
        if data[0]:
            model_intapp_menu.delete(title=arr['title'])
            return successjson()
        else:
            return errorjson(msg=data[1])

