__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import Image, ImageEnhance
import urllib2


def GetImageFile(imgurl, suffix="jpg"):
    #FileDownload.DownLoadSingleFile(imgurl, ".\\tmp\\", filename=imgurl.split('/')[-1].split('.')[0] + '.' + suffix)
    #print imgurl
    html = urllib2.urlopen(imgurl).read()
    print "..\\tmp\\" + imgurl.split("/")[-1].split(".")[0] + '.' + suffix
    f = open("..\\tmp\\" + imgurl.split("/")[-1].split(".")[0] + '.' + suffix, "wb")
    f.write(html)
    f.close()


def Min(x, y):
    if x > y: return y
    return x


def Analyse_jwc_codeimg(imgurl, suffix="jpg"):
    image_name = "..\\tmp\\" + imgurl.split('/')[-1].split('.')[0] + '.' + suffix
    #print image_name
    im = Image.open(image_name)
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(10)
    im = im.convert('1')

    #im.save("img_final.jpg") #测试查看

    s = 0      #启始 切割点 x
    t = 0      #启始 切割点 y

    w = 8      #切割 宽 +y
    h = 10      #切割 长 +x

    im_new = []
    for i in range(4): #验证码切割
        im1 = im.crop((s + w * i + i * 2, t, s + w * (i + 1) + i * 2, h))
        im_new.append(im1)
        #im1.save("numer" + str(i) + ".jpg")
        #测试查看
    ret = ""
    for x in range(4):
        xsize, ysize = im_new[x].size
        gd = []
        for i in range(ysize):
            tmp = []
            for j in range(xsize):
                if ( im_new[x].getpixel((j, i)) == 255 ):
                    tmp.append(1)
                else:
                    tmp.append(0)
            gd.append(tmp)
        maxn = -1;
        pos = -1;
        for noi in range(10):
            img = Image.open("..\\var\\jwc_num\\" + str(noi) + ".jpg")
            x_size, y_size = img.size
            gp = []
            for i in range(y_size):
                tmp = []
                for j in range(x_size):
                    if ( img.getpixel((j, i)) == 255 ):
                        tmp.append(1)
                    else:
                        tmp.append(0)
                gp.append(tmp)
            cout = 0
            total = Min(x_size, xsize) * Min(y_size, ysize) * 1.0

            for i in range(ysize):
                for j in range(xsize):
                    if gp[i][j] == gd[i][j]:
                        cout += 1;
            tempmax = cout / total
            if tempmax > maxn:
                maxn = tempmax;
                pos = noi
        if pos == 8 or pos == 3:
            ret = "0"
            break;
        ret = ret + str(pos);
    return ret


def Get_jwc_Code(host, uri="checkcode.asp"):
    while True:
        GetImageFile(host + "/" + uri)
        code = Analyse_jwc_codeimg(host + "/" + uri)
        if len(code) == 4:
            print code
            return code


