# Image-vector-for-ComfyUI
一个打包了vtracer的comfyui节点，用于把像素转矢量  a wrap-up comfyui nodes for concerting pix to raster
shot out to Vtracer!
https://github.com/visioncortex/vtracer


install guide安装指南:

1. cd comfyui/custom_nodes(导航至自定义节点文件夹)
2. git clone(把代码复制到本地)
3. pip install -r requirements.txt(安装依赖)
   (if you are using comfyui-portable, first cd to the folder called"python_embeded",then run "python.exe -m pip install"+"requirements" 如果你用的是comfyui便携版，先导航到python_embeded 这个文件夹，然后用python.exe -m pip install+你要安装的依赖)
4. install another requirement(https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-33-Q16-HDRI-x64-dll.exe), details on: https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows
5. restart comfyui(重启comfyUI)

user guide使用说明：

![image](https://github.com/archifancy/Image-vector-for-ComfyUI/assets/125116261/36c8bd0d-1621-4ba3-966d-2ae54c203bb8)
SVG file 转换后效果：
![image](https://github.com/archifancy/Image-vector-for-ComfyUI/assets/125116261/cd49ccec-f76b-418a-ae3e-a41954d90877)

具体参数调整参考：https://github.com/visioncortex/vtracer
just copy your dir to the output_dir,and click queue prompt, you will get your svg file in the folder
你进需要把文件保存路径拷贝到output_dir，点击生成就可以获得文件
