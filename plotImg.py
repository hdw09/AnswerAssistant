from aip import AipOcr
import io

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def markRect(box, scaleSize, lable, colorDef, axis, plt):
	axis.add_patch(plt.Rectangle((box[0] * scaleSize, box[1] * scaleSize), box[2] * scaleSize, box[3] * scaleSize, color=colorDef, fill=False, linewidth=2))
	axis.text(box[0] * scaleSize + box[2] * scaleSize + 10, box[1] * scaleSize + box[3] * scaleSize / 2, lable, size='x-large', color='white', bbox={'facecolor':colorDef, 'alpha':1.0})

def Box2Rect(box, scaleSize):
	return [box[0] * scaleSize, box[1] * scaleSize, (box[0] + box[2]) * scaleSize, (box[1] + box[3]) * scaleSize]

def baidu_OCR(img):
	imgByteArr = io.BytesIO()
	img.save(imgByteArr, format='PNG')
	result = client.basicGeneral(imgByteArr.getvalue())
	text = ""
	if result.has_key("words_result_num") :
		index = 0
		while index < result["words_result_num"]:
			 text = text + result["words_result"][index]['words']
			 index = index + 1
	return text
