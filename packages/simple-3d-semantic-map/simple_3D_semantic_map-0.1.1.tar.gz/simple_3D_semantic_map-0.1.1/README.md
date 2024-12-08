# Simple 3D Semantic Map

The library that containt all requirement elements to create 3D semantic map.

## How to build 3D semantic map
1. Choose image. You can use webcam, Intel RealSense camera or just load it from any pointed source.
2. Get image depth. Use any function with depth estimation model or capture it using Intel Realsesne camera.
3. Segment image - this package containt few model that will do it.
4. Create 3D semantic map - combine labeled image with its depth into map. Use create_semantic_3D_map funtion for it.
Note: Intel RealSense camera is not required to use this package properly.