


# Intel Realsense D415 python codes
# Install the latest firmware update by "intel-realsense-dfu"
import pyrealsense2 as rs
import cv2
#import logging
import numpy as np
color_map=rs.colorizer()
config = rs.config()
# You need to put your device S/N here
config.enable_device("816312061056")
# If you do not have your device S/N run this code: print(pyrealsense2.device_list)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipe = rs.pipeline()
profile = config.resolve(pipe)  
print(profile.get_device())
pipe.start(config)
window_name = "Display Image"

while True:
    
    data=pipe.wait_for_frames()
    depth = data.get_depth_frame()
    color = data.get_color_frame()
    x_0,y_0 = 200,200
    d = depth.get_distance(x=x_0,y=y_0)

    if not depth or not color:
        continue
    depth_image = np.asanyarray(depth.get_data())
    color_image = np.asanyarray(color.get_data())
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_WINTER)
    images = np.hstack((color_image, depth_colormap))
    cv2.putText(images, str(d) , (int(100),int(100)), cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,255), 1)
    cv2.putText(images, 'o' , (int(x_0),int(y_0)), cv2.FONT_HERSHEY_SIMPLEX,0.4, (0,0,255), 3)
    cv2.imshow(window_name, images)
    key = (cv2.waitKey(1) & 0xFF)
    if key == 27 or key == ord('q'):
        break
        
pipe.stop()
cv2.destroyAllWindows()

