import vtracer
import tempfile
from wand.image import Image as WandImage
from PIL import Image as PILImage
import torch
import numpy as np
import os

class AIraster:
    """
    A example node

    Class methods
    -------------
    INPUT_TYPES (dict): 
        Tell the main program input parameters of nodes.
    IS_CHANGED:
        optional method to control when the node is re executed.

    Attributes
    ----------
    RETURN_TYPES (`tuple`): 
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "image": ("IMAGE",),
                "colormode": (["color", "binary"], {
                    "default": "color"
                }),
                "hierarchical": (["stacked", "cutout"], {
                    "default": "stacked"
                }),
                "mode": (["spline", "polygon", "none"], {
                    "default": "spline"
                }),
                "filter_speckle": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 128,
                    "step": 1
                }),
                "color_precision": ("INT", {
                    "default": 6,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "layer_difference": ("INT", {
                    "default": 16,
                    "min": 1,
                    "max": 20,
                    "step": 1
                }),
                "corner_threshold": ("INT", {
                    "default": 60,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "length_threshold": ("FLOAT", {
                    "default": 4.0,
                    "min": 3.5,
                    "max": 10.0,
                    "step": 0.1
                }),
                "max_iterations": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 20,
                    "step": 1
                }),
                "splice_threshold": ("INT", {
                    "default": 45,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "path_precision": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "output_directory": ("STRING", {
                    "default": ""
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("vector_image",)

    FUNCTION = "process_image"

    #OUTPUT_NODE = False

    CATEGORY = "Vectorization"



    def process_image(self, image, output_directory, colormode, hierarchical, mode, filter_speckle, color_precision,
                      layer_difference, corner_threshold, length_threshold, max_iterations, splice_threshold, path_precision):
        try:
            print(f"输入图像形状：{image.shape}")

            # 确保输入 Tensor 是四维，具有 (B, C, H, W) 结构
            if len(image.shape) == 4:
                # 将图像从 (1, H, W, C) 转换为 (H, W, C)
                image = image.squeeze(0)

            print(f"处理后的图像形状：{image.shape}")

            # 将 Tensor 转换为 PIL 图像
            image_array = image.numpy()
            image_array = (image_array * 255).astype(np.uint8)
            pil_image = PILImage.fromarray(image_array)

            print(f"转换后的 PIL 图像：{pil_image}")

            # 将输入图像保存到临时文件
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img_file:
                pil_image.save(temp_img_file, format="PNG")
                temp_img_path = temp_img_file.name

            print(f"临时 PNG 文件路径：{temp_img_path}")
            base_filename = os.path.splitext(os.path.basename(temp_img_path))[0]

            # 检查并创建输出目录
            if not output_directory:
                output_directory = tempfile.gettempdir()
            elif not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # 生成 SVG 文件路径
            svg_filename = os.path.join(output_directory, f"{base_filename}.svg")

            print(f"SVG 文件路径：{svg_filename}")

            # 使用 vtracer 将图像转换为 SVG
            vtracer.convert_image_to_svg_py(temp_img_path,
                                            svg_filename,
                                            colormode=colormode,
                                            hierarchical=hierarchical,
                                            mode=mode,
                                            filter_speckle=filter_speckle,
                                            color_precision=color_precision,
                                            layer_difference=layer_difference,
                                            corner_threshold=corner_threshold,
                                            length_threshold=length_threshold,
                                            max_iterations=max_iterations,
                                            splice_threshold=splice_threshold,
                                            path_precision=path_precision)

            print("SVG 文件已成功生成")

            # 使用 wand 将 SVG 转换为 PNG
            with WandImage(filename=svg_filename) as wand_image:
                wand_image.format = 'png'
                output_png_filename = os.path.join(output_directory, f"{base_filename}.png")
                wand_image.save(filename=output_png_filename)

            # 读取转换后的 PNG 图像
            output_image = PILImage.open(output_png_filename).convert('RGB')
            print(f"转换后的图像信息: 模式={output_image.mode}, 尺寸={output_image.size}")

            # 将 PIL 图像转换为 torch tensor
            tensor_image = torch.from_numpy(np.array(output_image)).permute(2, 0, 1).float() / 255
            print(f"tensor 图像形状: {tensor_image.shape}, 最大值: {tensor_image.max()}, 最小值: {tensor_image.min()}")
            

            return (tensor_image,)

        except Exception as e:
            print(f"错误：{str(e)}")
            return (None,)

NODE_CLASS_MAPPINGS = {
    "AIraster": AIraster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AIraster": "AIraster"
}
