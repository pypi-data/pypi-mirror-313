import torch
import torch.nn.functional as F
import PIL
import os
import numpy as np
import torchvision.models as models
from torchvision.utils import make_grid, save_image

from .utils import find_alexnet_layer, find_vgg_layer, find_resnet_layer, find_densenet_layer, find_squeezenet_layer, visualize_cam, Normalize


class GradCAM(object):
    """Calculate GradCAM salinecy map.

    A simple example:

        # initialize a model, model_dict and gradcam
        resnet = torchvision.models.resnet101(pretrained=True)
        resnet.eval()
        model_dict = dict(model_type='resnet', arch=resnet, layer_name='layer4', input_size=(224, 224))
        gradcam = GradCAM(model_dict)

        # get an image and normalize with mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
        img = load_img()
        normed_img = normalizer(img)

        # get a GradCAM saliency map on the class index 10.
        mask, logit = gradcam(normed_img, class_idx=10)

        # make heatmap from mask and synthesize saliency map using heatmap and img
        heatmap, cam_result = visualize_cam(mask, img)


    Args:
        model_dict (dict): a dictionary that contains 'model_type', 'arch', layer_name', 'input_size'(optional) as keys.
        verbose (bool): whether to print output size of the saliency map givien 'layer_name' and 'input_size' in model_dict.
    """

    def __init__(self, model_dict, verbose=False):
        model_type = model_dict['type']
        layer_name = model_dict['layer_name']
        self.model_arch = model_dict['arch']

        self.gradients = dict()
        self.activations = dict()

        def backward_hook(module, grad_input, grad_output):
            self.gradients['value'] = grad_output[0]
            return None

        def forward_hook(module, input, output):
            self.activations['value'] = output
            return None

        if 'vgg' in model_type.lower():
            target_layer = find_vgg_layer(self.model_arch, layer_name)
        elif 'resnet' in model_type.lower():
            target_layer = find_resnet_layer(self.model_arch, layer_name)
        elif 'densenet' in model_type.lower():
            target_layer = find_densenet_layer(self.model_arch, layer_name)
        elif 'alexnet' in model_type.lower():
            target_layer = find_alexnet_layer(self.model_arch, layer_name)
        elif 'squeezenet' in model_type.lower():
            target_layer = find_squeezenet_layer(self.model_arch, layer_name)

        target_layer.register_forward_hook(forward_hook)
        target_layer.register_full_backward_hook(backward_hook)

        if verbose:
            try:
                input_size = model_dict['input_size']
            except KeyError:
                print("please specify size of input image in model_dict. e.g. {'input_size':(224, 224)}")
                pass
            else:
                device = 'cuda' if next(self.model_arch.parameters()).is_cuda else 'cpu'
                self.model_arch(torch.zeros(1, 3, *(input_size), device=device))
                print('saliency_map size :', self.activations['value'].shape[2:])

    def forward(self, input, class_idx=None, retain_graph=False):
        """
        Args:
            input: input image with shape of (1, 3, H, W)
            class_idx (int): class index for calculating GradCAM.
                    If not specified, the class index that makes the highest model prediction score will be used.
        Return:
            mask: saliency map of the same spatial dimension with input
            logit: model output
        """
        b, c, h, w = input.size()

        logit = self.model_arch(input)
        if class_idx is None:
            score = logit[:, logit.max(1)[-1]].squeeze()
        else:
            score = logit[:, class_idx].squeeze()

        self.model_arch.zero_grad()
        score.backward(retain_graph=retain_graph)
        gradients = self.gradients['value']
        activations = self.activations['value']
        b, k, u, v = gradients.size()

        alpha = gradients.view(b, k, -1).mean(2)
        # alpha = F.relu(gradients.view(b, k, -1)).mean(2)
        weights = alpha.view(b, k, 1, 1)

        saliency_map = (weights * activations).sum(1, keepdim=True)
        saliency_map = F.relu(saliency_map)
        saliency_map = F.interpolate(saliency_map, size=(h, w), mode='bilinear', align_corners=False)
        saliency_map_min, saliency_map_max = saliency_map.min(), saliency_map.max()
        saliency_map = (saliency_map - saliency_map_min).div(saliency_map_max - saliency_map_min).data

        return saliency_map, logit

    def __call__(self, input, class_idx=None, retain_graph=False):
        return self.forward(input, class_idx, retain_graph)


class GradCAMpp(GradCAM):
    """Calculate GradCAM++ salinecy map.

    A simple example:

        # initialize a model, model_dict and gradcampp
        resnet = torchvision.models.resnet101(pretrained=True)
        resnet.eval()
        model_dict = dict(model_type='resnet', arch=resnet, layer_name='layer4', input_size=(224, 224))
        gradcampp = GradCAMpp(model_dict)

        # get an image and normalize with mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
        img = load_img()
        normed_img = normalizer(img)

        # get a GradCAM saliency map on the class index 10.
        mask, logit = gradcampp(normed_img, class_idx=10)

        # make heatmap from mask and synthesize saliency map using heatmap and img
        heatmap, cam_result = visualize_cam(mask, img)


    Args:
        model_dict (dict): a dictionary that contains 'model_type', 'arch', layer_name', 'input_size'(optional) as keys.
        verbose (bool): whether to print output size of the saliency map givien 'layer_name' and 'input_size' in model_dict.
    """

    def __init__(self, model_dict, verbose=False):
        super(GradCAMpp, self).__init__(model_dict, verbose)

    def forward(self, input, class_idx=None, retain_graph=False):
        """
        Args:
            input: input image with shape of (1, 3, H, W)
            class_idx (int): class index for calculating GradCAM.
                    If not specified, the class index that makes the highest model prediction score will be used.
        Return:
            mask: saliency map of the same spatial dimension with input
            logit: model output
        """
        b, c, h, w = input.size()

        logit = self.model_arch(input)
        if class_idx is None:
            score = logit[:, logit.max(1)[-1]].squeeze()
        else:
            score = logit[:, class_idx].squeeze()

        self.model_arch.zero_grad()
        score.backward(retain_graph=retain_graph)
        gradients = self.gradients['value']  # dS/dA
        activations = self.activations['value']  # A
        b, k, u, v = gradients.size()

        alpha_num = gradients.pow(2)
        alpha_denom = gradients.pow(2).mul(2) + \
                      activations.mul(gradients.pow(3)).view(b, k, u * v).sum(-1, keepdim=True).view(b, k, 1, 1)
        alpha_denom = torch.where(alpha_denom != 0.0, alpha_denom, torch.ones_like(alpha_denom))

        alpha = alpha_num.div(alpha_denom + 1e-7)
        positive_gradients = F.relu(score.exp() * gradients)  # ReLU(dY/dA) == ReLU(exp(S)*dS/dA))
        weights = (alpha * positive_gradients).view(b, k, u * v).sum(-1).view(b, k, 1, 1)

        saliency_map = (weights * activations).sum(1, keepdim=True)
        saliency_map = F.relu(saliency_map)
        saliency_map = F.interpolate(saliency_map, size=(224, 224), mode='bilinear', align_corners=False)
        saliency_map_min, saliency_map_max = saliency_map.min(), saliency_map.max()
        saliency_map = (saliency_map - saliency_map_min).div(saliency_map_max - saliency_map_min).data

        return saliency_map, logit


def GradCAMPP(img_path, model_name, layer_name=None, input_size=(224, 224)):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    pil_img = PIL.Image.open(img_path)  # PIL image

    normalizer = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    torch_img = torch.from_numpy(np.array(pil_img)).permute(2, 0, 1).unsqueeze(0).float().div(255).to(device)
    torch_img = F.interpolate(torch_img, size=(224, 224), mode='bilinear', align_corners=False)
    normed_torch_img = normalizer(torch_img)

    cam_dict = dict()

    if model_name == 'resnet':
        resnet = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
        resnet.eval(), resnet.to(device)

        resnet_model_dict = dict(type='resnet', arch=resnet, layer_name='layer4' if layer_name is None else layer_name, input_size=input_size)
        resnet_gradcam = GradCAM(resnet_model_dict, True)
        resnet_gradcampp = GradCAMpp(resnet_model_dict, True)
        cam_dict['resnet'] = [resnet_gradcam, resnet_gradcampp]

    elif model_name == 'vgg':
        vgg = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        vgg.eval(), vgg.to(device)

        vgg_model_dict = dict(type='vgg', arch=vgg, layer_name='features_29' if layer_name is None else layer_name, input_size=input_size)
        vgg_gradcam = GradCAM(vgg_model_dict, True)
        vgg_gradcampp = GradCAMpp(vgg_model_dict, True)
        cam_dict['vgg'] = [vgg_gradcam, vgg_gradcampp]

    elif model_name == 'densenet':
        densenet = models.densenet161(weights=models.DenseNet161_Weights.DEFAULT)
        densenet.eval(), densenet.to(device)

        densenet_model_dict = dict(type='densenet', arch=densenet, layer_name='features_norm5' if layer_name is None else layer_name, input_size=input_size)
        densenet_gradcam = GradCAM(densenet_model_dict, True)
        densenet_gradcampp = GradCAMpp(densenet_model_dict, True)
        cam_dict['densenet'] = [densenet_gradcam, densenet_gradcampp]

    elif model_name == 'squeezenet':
        squeezenet = models.squeezenet1_1(weights=models.SqueezeNet1_1_Weights.DEFAULT)
        squeezenet.eval(), squeezenet.to(device)

        squeezenet_model_dict = dict(type='squeezenet', arch=squeezenet, layer_name='features_12_expand3x3_activation' if layer_name is None else layer_name, input_size=input_size)
        squeezenet_gradcam = GradCAM(squeezenet_model_dict, True)
        squeezenet_gradcampp = GradCAMpp(squeezenet_model_dict, True)
        cam_dict['squeezenet'] = [squeezenet_gradcam, squeezenet_gradcampp]

    elif model_name == 'all':
        resnet = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
        resnet.eval(), resnet.to(device)

        resnet_model_dict = dict(type='resnet', arch=resnet, layer_name='layer4' if layer_name is None else layer_name, input_size=input_size)
        resnet_gradcam = GradCAM(resnet_model_dict, True)
        resnet_gradcampp = GradCAMpp(resnet_model_dict, True)
        cam_dict['resnet'] = [resnet_gradcam, resnet_gradcampp]

        vgg = models.vgg16(weights=models.VGG16_Weights.DEFAULT)
        vgg.eval(), vgg.to(device)

        vgg_model_dict = dict(type='vgg', arch=vgg, layer_name='features_29' if layer_name is None else layer_name, input_size=input_size)
        vgg_gradcam = GradCAM(vgg_model_dict, True)
        vgg_gradcampp = GradCAMpp(vgg_model_dict, True)
        cam_dict['vgg'] = [vgg_gradcam, vgg_gradcampp]

        densenet = models.densenet161(weights=models.DenseNet161_Weights.DEFAULT)
        densenet.eval(), densenet.to(device)

        densenet_model_dict = dict(type='densenet', arch=densenet, layer_name='features_norm5' if layer_name is None else layer_name, input_size=input_size)
        densenet_gradcam = GradCAM(densenet_model_dict, True)
        densenet_gradcampp = GradCAMpp(densenet_model_dict, True)
        cam_dict['densenet'] = [densenet_gradcam, densenet_gradcampp]

        squeezenet = models.squeezenet1_1(weights=models.SqueezeNet1_1_Weights.DEFAULT)
        squeezenet.eval(), squeezenet.to(device)

        squeezenet_model_dict = dict(type='squeezenet', arch=squeezenet, layer_name='features_12_expand3x3_activation' if layer_name is None else layer_name, input_size=input_size)
        squeezenet_gradcam = GradCAM(squeezenet_model_dict, True)
        squeezenet_gradcampp = GradCAMpp(squeezenet_model_dict, True)
        cam_dict['squeezenet'] = [squeezenet_gradcam, squeezenet_gradcampp]

    images = []
    for gradcam, gradcam_pp in cam_dict.values():
        mask, _ = gradcam(normed_torch_img)
        heatmap, result = visualize_cam(mask, torch_img)

        mask_pp, _ = gradcam_pp(normed_torch_img)
        heatmap_pp, result_pp = visualize_cam(mask_pp, torch_img)

        images.append(torch.stack([torch_img.squeeze().cpu(), heatmap, heatmap_pp, result, result_pp], 0))

    images = make_grid(torch.cat(images, 0), nrow=5)

    # 分割路径
    parts = img_path.split(os.sep)
    # 获取到VOC2012目录
    base_dir = os.sep.join(parts[:-2])

    # 创建outputs目录
    output_dir = os.path.join(base_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    # 获取原始文件名并构建新文件名
    original_name = os.path.basename(img_path)
    output_name = os.path.splitext(original_name)[0] + '_gradcam.jpg'

    # 构建完整的输出路径
    output_path = os.path.join(output_dir, output_name)

    # 保存图片
    save_image(images, output_path)
    print(f'Grad cam results are saved at {output_path}')

    return heatmap, heatmap_pp, result, result_pp
