import cv2
import numpy as np
import pyrealsense2 as rs


def example_0():

    """
     Example shows how to interuct with the realsense camera by using pyrealsense2 library.
     Also it can be used as camera sight viewer.
    """

    pipeline = rs.pipeline()
    config = rs.config()

    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("Camera not found")
        exit(0)

    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    align_to = rs.stream.color
    align = rs.align(align_to)

    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame: continue

            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.07), cv2.COLORMAP_JET)

            if depth_colormap.shape != color_image.shape: color_image = cv2.resize(color_image, dsize=(depth_colormap.shape[1], depth_colormap.shape[0]), interpolation=cv2.INTER_AREA)

            images = np.hstack((color_image, depth_colormap))

            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense viewer. Press q to exit', images)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    except Exception as e:
        print(e)
        pipeline.stop()

    finally:
        pipeline.stop()

if __name__ == "__main__":
    example_0()