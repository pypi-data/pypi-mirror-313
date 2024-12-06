import torch
from torchstain.base.normalizers.he_normalizer import HENormalizer
from torchstain.torch.utils import cov, percentile
import torch.nn as nn
from huggingface_hub import PyTorchModelHubMixin
import math
from functools import partial
import warnings
import importlib.resources as resources

from PIL import Image
import torchvision.transforms as transforms


class ToTensorCheck(transforms.ToTensor):
    def __call__(self, pic):
        if isinstance(pic, torch.Tensor):
            return pic
        return super().__call__(pic)


class EXAONEPathLoader:
    def __init__(self, model_name="LGAI-EXAONE/EXAONEPath", hf_token=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Initialize the model with proper layers and activation
        self.model = VisionTransformer.from_pretrained(model_name, use_auth_token=hf_token)
        self.model = self.model.to(self.device)
        self.model.eval()

        # Setup the preprocessing transforms
        self.processor = transforms.Compose(
            [
                ToTensorCheck(),
                transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
                transforms.CenterCrop(224),
                #transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ])

    def get_processor_and_model(self):
        return self.processor, self.model


    # Function to get image embedding
    def get_image_embedding(self, image, processor, model, device):
        normalizer = macenko_normalizer()
        norm_img = normalizer(image).to(device)
        image_tensor = processor(norm_img).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(image_tensor).squeeze()

        return output.cpu().numpy().flatten()





"""
Source code ported from: https://github.com/schaugf/HEnorm_python
Original implementation: https://github.com/mitkovetta/staining-normalization
"""
########################################################################################
### macenko.py
########################################################################################

class TorchMacenkoNormalizer(HENormalizer):
    def __init__(self):
        super().__init__()

        self.HERef = torch.tensor([[0.5626, 0.2159],
                                   [0.7201, 0.8012],
                                   [0.4062, 0.5581]])
        self.maxCRef = torch.tensor([1.9705, 1.0308])

        # Avoid using deprecated torch.lstsq (since 1.9.0)
        self.updated_lstsq = hasattr(torch.linalg, 'lstsq')

    def __convert_rgb2od(self, I, Io, beta):
        I = I.permute(1, 2, 0)

        # calculate optical density
        OD = -torch.log((I.reshape((-1, I.shape[-1])).float() + 1) / Io)

        # remove transparent pixels
        ODhat = OD[~torch.any(OD < beta, dim=1)]

        return OD, ODhat

    def __find_HE(self, ODhat, eigvecs, alpha):
        # project on the plane spanned by the eigenvectors corresponding to the two
        # largest eigenvalues
        That = torch.matmul(ODhat, eigvecs)
        phi = torch.atan2(That[:, 1], That[:, 0])
        # print(phi.size())

        minPhi = percentile(phi, alpha)
        maxPhi = percentile(phi, 100 - alpha)

        vMin = torch.matmul(eigvecs, torch.stack((torch.cos(minPhi), torch.sin(minPhi)))).unsqueeze(1)
        vMax = torch.matmul(eigvecs, torch.stack((torch.cos(maxPhi), torch.sin(maxPhi)))).unsqueeze(1)

        # a heuristic to make the vector corresponding to hematoxylin first and the
        # one corresponding to eosin second
        HE = torch.where(vMin[0] > vMax[0], torch.cat((vMin, vMax), dim=1), torch.cat((vMax, vMin), dim=1))

        return HE

    def __find_concentration(self, OD, HE):
        # rows correspond to channels (RGB), columns to OD values
        Y = OD.T

        # determine concentrations of the individual stains
        if not self.updated_lstsq:
            return torch.lstsq(Y, HE)[0][:2]

        return torch.linalg.lstsq(HE, Y)[0]

    def __compute_matrices(self, I, Io, alpha, beta):
        OD, ODhat = self.__convert_rgb2od(I, Io=Io, beta=beta)

        # compute eigenvectors
        _, eigvecs = torch.linalg.eigh(cov(ODhat.T))
        eigvecs = eigvecs[:, [1, 2]]

        HE = self.__find_HE(ODhat, eigvecs, alpha)

        C = self.__find_concentration(OD, HE)
        maxC = torch.stack([percentile(C[0, :], 99), percentile(C[1, :], 99)])

        return HE, C, maxC

    def fit(self, I, Io=240, alpha=1, beta=0.15):
        HE, _, maxC = self.__compute_matrices(I, Io, alpha, beta)

        self.HERef = HE
        self.maxCRef = maxC

    def normalize(self, I, Io=240, alpha=1, beta=0.15, stains=True, form='chw', dtype='int'):
        ''' Normalize staining appearence of H&E stained images

        Example use:
            see test.py

        Input:
            I: RGB input image: tensor of shape [C, H, W] and type uint8
            Io: (optional) transmitted light intensity
            alpha: percentile
            beta: transparency threshold
            stains: if true, return also H & E components

        Output:
            Inorm: normalized image
            H: hematoxylin image
            E: eosin image

        Reference:
            A method for normalizing histology slides for quantitative analysis. M.
            Macenko et al., ISBI 2009
        '''
        c, h, w = I.shape

        HE, C, maxC = self.__compute_matrices(I, Io, alpha, beta)

        # normalize stain concentrations
        C *= (self.maxCRef / maxC).unsqueeze(-1)

        # recreate the image using reference mixing matrix
        Inorm = Io * torch.exp(-torch.matmul(self.HERef, C))
        Inorm[Inorm > 255] = 255
        """
        # Requires Python > 3.10
        match (form, dtype):
            case ('chw', 'int'):
                Inorm = Inorm.reshape(c, h, w).int()
            case ('chw', 'float'):
                Inorm = Inorm.reshape(c, h, w).float() / 255.
            case ('hwc', 'int'):
                Inorm = Inorm.T.reshape(h, w, c).int()
            case ('hwc', 'float'):
                Inorm = Inorm.T.reshape(h, w, c).float() / 255.
            case _:
                raise ValueError('check macenko input form and dtype')"""

        if form == 'chw' and dtype == 'int':
            Inorm = Inorm.reshape(c, h, w).int()
        elif form == 'chw' and dtype == 'float':
            Inorm = Inorm.reshape(c, h, w).float() / 255.
        elif form == 'hwc' and dtype == 'int':
            Inorm = Inorm.T.reshape(h, w, c).int()
        elif form == 'hwc' and dtype == 'float':
            Inorm = Inorm.T.reshape(h, w, c).float() / 255.
        else:
            raise ValueError('check macenko input form and dtype')

        H, E = None, None

        if stains:
            H = torch.mul(Io, torch.exp(torch.matmul(-self.HERef[:, 0].unsqueeze(-1), C[0, :].unsqueeze(0))))
            H[H > 255] = 255
            H = H.T.reshape(h, w, c).int()

            E = torch.mul(Io, torch.exp(torch.matmul(-self.HERef[:, 1].unsqueeze(-1), C[1, :].unsqueeze(0))))
            E[E > 255] = 255
            E = E.T.reshape(h, w, c).int()

        return Inorm, H, E


class macenko_normalizer():
    def __init__(self, target_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load the image from the package's data directory using importlib_resources
        with resources.path('dpfm_model_runners.data', 'macenko_target.png') as target_path:
            self.target = Image.open(target_path)

        self.transform_before_macenko = transforms.Compose([
            ToTensorCheck(),
            transforms.Lambda(lambda x: x * 255)
        ])
        self.normalizer = TorchMacenkoNormalizer()
        self.normalizer.fit(self.transform_before_macenko(self.target))

    def __call__(self, image):
        t_to_transform = self.transform_before_macenko(image)
        try:
            image_macenko, _, _ = self.normalizer.normalize(I=t_to_transform, stains=False, form='chw', dtype='float')
            if torch.any(torch.isnan(image_macenko)):
                Warning("NaN values found in image after Macenko normalization. Returning original image.")
                return transforms.ToTensor()(image).to(self.device)
            else:
                return image_macenko.to(self.device)
        except Exception as e:
            print(str(e))
            return transforms.ToTensor()(image).to(self.device)

########################################################################################
### vision_transformer.py
########################################################################################


def _no_grad_trunc_normal_(tensor, mean, std, a, b):
    # Cut & paste from PyTorch official master until it's in a few official releases - RW
    # Method based on https://people.sc.fsu.edu/~jburkardt/presentations/truncated_normal.pdf
    def norm_cdf(x):
        # Computes standard normal cumulative distribution function
        return (1. + math.erf(x / math.sqrt(2.))) / 2.

    if (mean < a - 2 * std) or (mean > b + 2 * std):
        warnings.warn("mean is more than 2 std from [a, b] in nn.init.trunc_normal_. "
                      "The distribution of values may be incorrect.",
                      stacklevel=2)

    with torch.no_grad():
        # Values are generated by using a truncated uniform distribution and
        # then using the inverse CDF for the normal distribution.
        # Get upper and lower cdf values
        l = norm_cdf((a - mean) / std)
        u = norm_cdf((b - mean) / std)

        # Uniformly fill tensor with values from [l, u], then translate to
        # [2l-1, 2u-1].
        tensor.uniform_(2 * l - 1, 2 * u - 1)

        # Use inverse cdf transform for normal distribution to get truncated
        # standard normal
        tensor.erfinv_()

        # Transform to proper mean, std
        tensor.mul_(std * math.sqrt(2.))
        tensor.add_(mean)

        # Clamp to ensure it's in the proper range
        tensor.clamp_(min=a, max=b)
        return tensor


def trunc_normal_(tensor, mean=0., std=1., a=-2., b=2.):
    # type: (torch.Tensor, float, float, float, float) -> torch.Tensor
    return _no_grad_trunc_normal_(tensor, mean, std, a, b)


def drop_path(x, drop_prob: float = 0., training: bool = False):
    if drop_prob == 0. or not training:
        return x
    keep_prob = 1 - drop_prob
    shape = (x.shape[0],) + (1,) * (x.ndim - 1)  # work with diff dim tensors, not just 2D ConvNets
    random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
    random_tensor.floor_()  # binarize
    output = x.div(keep_prob) * random_tensor
    return output


class DropPath(nn.Module):
    """Drop paths (Stochastic Depth) per sample  (when applied in main path of residual blocks).
    """

    def __init__(self, drop_prob=None):
        super(DropPath, self).__init__()
        self.drop_prob = drop_prob

    def forward(self, x):
        return drop_path(x, self.drop_prob, self.training)


class Mlp(nn.Module):
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = act_layer()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class Attention(nn.Module):
    def __init__(self, dim, num_heads=8, qkv_bias=False, qk_scale=None, attn_drop=0., proj_drop=0.):
        super().__init__()
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = qk_scale or head_dim ** -0.5

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x):
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, C // self.num_heads).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        attn = (q @ k.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x, attn


class Block(nn.Module):
    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm):
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = Attention(
            dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale=qk_scale, attn_drop=attn_drop, proj_drop=drop)
        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

    def forward(self, x, return_attention=False):
        y, attn = self.attn(self.norm1(x))
        if return_attention:
            return attn
        x = x + self.drop_path(y)
        x = x + self.drop_path(self.mlp(self.norm2(x)))
        return x


class PatchEmbed(nn.Module):
    """ Image to Patch Embedding
    """

    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        num_patches = (img_size // patch_size) * (img_size // patch_size)
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        B, C, H, W = x.shape
        x = self.proj(x).flatten(2).transpose(1, 2)
        return x


class VisionTransformer(nn.Module, PyTorchModelHubMixin):
    def __init__(self, img_size=[224], patch_size=16, in_chans=3, num_classes=0, embed_dim=768, depth=12,
                 num_heads=12, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop_rate=0., attn_drop_rate=0.,
                 drop_path_rate=0., norm_layer=nn.LayerNorm, **kwargs):
        super().__init__()
        self.num_features = self.embed_dim = embed_dim

        self.patch_embed = PatchEmbed(
            img_size=img_size[0], patch_size=patch_size, in_chans=in_chans, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches

        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        self.pos_drop = nn.Dropout(p=drop_rate)

        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, depth)]  # stochastic depth decay rule
        self.blocks = nn.ModuleList([
            Block(
                dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, qkv_bias=qkv_bias, qk_scale=qk_scale,
                drop=drop_rate, attn_drop=attn_drop_rate, drop_path=dpr[i], norm_layer=norm_layer)
            for i in range(depth)])
        self.norm = norm_layer(embed_dim)

        # Classifier head
        self.head = nn.Linear(embed_dim, num_classes) if num_classes > 0 else nn.Identity()

        trunc_normal_(self.pos_embed, std=.02)
        trunc_normal_(self.cls_token, std=.02)
        self.apply(self._init_weights)

        # config for PyTorchModelHubMixin
        self.config = {
            "img_size": img_size,
            "patch_size": patch_size,
            "in_chans": in_chans,
            "num_classes": num_classes,
            "embed_dim": embed_dim,
            "depth": depth,
            "num_heads": num_heads,
            "mlp_ratio": mlp_ratio,
            "qkv_bias": qkv_bias,
            "qk_scale": qk_scale,
            "drop_rate": drop_rate,
            "attn_drop_rate": attn_drop_rate,
            "drop_path_rate": drop_path_rate,
        }

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def interpolate_pos_encoding(self, x, w, h):
        npatch = x.shape[1] - 1
        N = self.pos_embed.shape[1] - 1
        if npatch == N and w == h:
            return self.pos_embed
        class_pos_embed = self.pos_embed[:, 0]
        patch_pos_embed = self.pos_embed[:, 1:]
        dim = x.shape[-1]
        w0 = w // self.patch_embed.patch_size
        h0 = h // self.patch_embed.patch_size
        # we add a small number to avoid floating point error in the interpolation
        # see discussion at https://github.com/facebookresearch/dino/issues/8
        w0, h0 = w0 + 0.1, h0 + 0.1
        patch_pos_embed = nn.functional.interpolate(
            patch_pos_embed.reshape(1, int(math.sqrt(N)), int(math.sqrt(N)), dim).permute(0, 3, 1, 2),
            scale_factor=(w0 / math.sqrt(N), h0 / math.sqrt(N)),
            mode='bicubic',
        )
        assert int(w0) == patch_pos_embed.shape[-2] and int(h0) == patch_pos_embed.shape[-1]
        patch_pos_embed = patch_pos_embed.permute(0, 2, 3, 1).view(1, -1, dim)
        return torch.cat((class_pos_embed.unsqueeze(0), patch_pos_embed), dim=1)

    def prepare_tokens(self, x):
        B, nc, w, h = x.shape
        x = self.patch_embed(x)  # patch linear embedding

        # add the [CLS] token to the embed patch tokens
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        # add positional encoding to each token
        x = x + self.interpolate_pos_encoding(x, w, h)

        return self.pos_drop(x)

    def forward(self, x):
        x = self.prepare_tokens(x)
        for blk in self.blocks:
            x = blk(x)
        x = self.norm(x)
        # print(x.type())
        return x[:, 0]

    def get_last_selfattention(self, x):
        x = self.prepare_tokens(x)
        for i, blk in enumerate(self.blocks):
            if i < len(self.blocks) - 1:
                x = blk(x)
            else:
                # return attention of the last block
                return blk(x, return_attention=True)

    def get_intermediate_layers(self, x, n=1):
        x = self.prepare_tokens(x)
        # we return the output tokens from the `n` last blocks
        output = []
        for i, blk in enumerate(self.blocks):
            x = blk(x)
            if len(self.blocks) - i <= n:
                output.append(self.norm(x))
        return output


def vit_base(patch_size=16, **kwargs):
    model = VisionTransformer(
        patch_size=patch_size, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4,
        qkv_bias=True, norm_layer=partial(nn.LayerNorm, eps=1e-6), **kwargs)
    return model