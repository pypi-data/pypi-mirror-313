import torch
import clip


class CLIPLoss(torch.nn.Module):

    def __init__(self):
        super(CLIPLoss, self).__init__()
        self.model, self.preprocess = clip.load("ViT-B/32", device="cuda")
        self.upsample = torch.nn.Upsample(scale_factor=7)
        self.avg_pool = torch.nn.AvgPool2d(kernel_size=1024 // 32)
        self.resize_pool = torch.nn.AdaptiveAvgPool2d((224, 224))

    def forward(self, image, text, use_avg_pool=False):
        if use_avg_pool:
            image = self.avg_pool(self.upsample(image))
        similarity = 1 - self.model(image, text)[0] / 100
        return similarity
    
    def compute_distance(self, x, y):
        # Resize images if needed
        if x.shape[2] != 224:
            x = self.resize_pool(x)
        if y.shape[2] != 224:
            y = self.resize_pool(y)
            
        # Get image embeddings using existing model
        clip_feat_x = self.model.encode_image(x)
        clip_feat_y = self.model.encode_image(y)
        
        # Calculate cosine similarity
        sim = torch.nn.functional.cosine_similarity(clip_feat_x, clip_feat_y)
        
        return 1 - sim.mean()
