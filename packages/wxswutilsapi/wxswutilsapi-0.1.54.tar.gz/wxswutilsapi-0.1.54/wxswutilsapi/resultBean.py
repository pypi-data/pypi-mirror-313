def okListBean(list=[],total=0):
    try:
        return {"code":0,"list":list,"total":total,"message":'成功',}
    except Exception as e:
        print(f"Unexpected error in okListBean: {e}")

def okDataBean(data):
    try:
        return {"code":0,"data":data,"message":'成功',}
    except Exception as e:
        print(f"Unexpected error in okDataBean: {e}")
            
def errorDataBean(data,code=999,message = ''):
    try:
        return {"code":code,"data":data,"message":message,}
    except Exception as e:
        print(f"Unexpected error in errorDataBean: {e}")