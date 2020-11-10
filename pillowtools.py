from PIL import ImageChops,Image
#比较两个像素点是否相同（差异不大）
def is_pixel_equal(img1,img2,x,y):
  threshold=50
  p1=img1.getpixel((x,y))
  p2=img2.getpixel((x,y))
  if abs(p1[0]-p2[0]) < threshold and abs(p1[1]-p2[1])< threshold and abs(p1[2]-p2[2])< threshold:
    return True
  else:
    return False

def findDiffStart(img1,img2):
  '''
  img1:要比较的第一张图
  img2:要比较的第二张图
  return：图片差异处起点到图片左边缘的距离(px)
  '''
  for row in range(0,img1.size[0]):
    for col in range(0,img1.size[1]):
      if not is_pixel_equal(img1,img2,row,col):
        #如果两个像素点差异（threshold）较大，表示(row,col)到达差异块的左上角
        return row
# print(img1.size)
# left = diff(img1,img2)
# print('different start at ',left)
