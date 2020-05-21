import falcon, json

class MachinaNav(object):

    def __init__(self, ch):
        self.ch        = ch
    
    def on_post(self, req, resp):
        raw_data = json.load(req.bounded_stream)
        changed_name = list(raw_data.keys())[0]
        print(raw_data)

        if changed_name == 'memoria':
            self.ch.setMemory(int(raw_data.get('memoria')))
        if changed_name == 'kernel':
            self.ch.setKernel(int(raw_data.get('kernel')))
        if changed_name == 'acumulador':
            self.ch.setAcumulador(int(raw_data.get('acumulador')))
        resp.status = falcon.HTTP_200

