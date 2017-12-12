#-*- coding:utf-8 -*-
from tornado import web, httpserver, ioloop

from create_qr_code import get_code_by_str

SIGN_FILE_HANDELER = open('sign.csv','a',encoding='GBK')

SIGN_FILE_HANDELER.write('姓名,组别,工号,公司\n')
#分机号
class IndexPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

class CodePageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        img_handle=get_code_by_str("http://127.0.0.1:8080/sign")
        self.write(img_handle.getvalue())
#签到系统
class SignHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('sign.html')
    def post(self, *args, **kwargs):
        name =self.get_argument('name')
        group =self.get_argument('group')
        number =self.get_argument('number')
        school = self.get_argument('school')
        if name and group and number and school:
            #写到文件
            SIGN_FILE_HANDELER.write('%s,%s,%s,%s\n' %(name,group,number,school))
            SIGN_FILE_HANDELER.flush()
            self.write('签到成功')
        else:
            self.write('请填写完整信息!')
        print('name',name,'group',group,'number',number,'school',school)

#路由系统
application = web.Application([
            (r"/index", IndexPageHandler),
            (r"/get_code", CodePageHandler),
            (r"/sign", SignHandler),
        ])

if __name__ == '__main__':
        http_server = httpserver.HTTPServer(application)
        http_server.listen(8080)
        ioloop.IOLoop.current().start()