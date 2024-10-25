#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
from scene import Scene
import os
from tqdm import tqdm
from os import makedirs
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from gaussian_renderer import render
import torchvision
from utils.general_utils import safe_state
from argparse import ArgumentParser
from arguments import ModelParams, PipelineParams, get_combined_args
from gaussian_renderer import GaussianModel

def render_set(model_path, name, iteration, views, gaussians, pipeline, background):
    render_path = os.path.join(model_path, name, "ours_{}".format(iteration), "renders")
    gts_path = os.path.join(model_path, name, "ours_{}".format(iteration), "gt")

    makedirs(render_path, exist_ok=True)
    makedirs(gts_path, exist_ok=True)

    for idx, view in enumerate(tqdm(views, desc="Rendering progress")):
        rendering = render(view[1].cuda(), gaussians, pipeline, background)["render"]
        gt = view[0][0:3, :, :]
        torchvision.utils.save_image(rendering, os.path.join(render_path, '{0:05d}'.format(idx) + ".png"))
        torchvision.utils.save_image(gt, os.path.join(gts_path, '{0:05d}'.format(idx) + ".png"))

def render_sets(dataset : ModelParams, pipeline : PipelineParams, skip_train : bool, skip_test : bool, gaussian_dim: int, time_duration: list, rot_4d: bool, force_sh_3d: bool, eval_shfs_4d: bool):
    with torch.no_grad():
        gaussians = GaussianModel(dataset.sh_degree, gaussian_dim=gaussian_dim, time_duration=time_duration, rot_4d=rot_4d, force_sh_3d=force_sh_3d, sh_degree_t=2 if eval_shfs_4d else 0)
        scene = Scene(dataset, gaussians, shuffle=False, time_duration=time_duration)

        bg_color = [1,1,1] if dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        if not skip_train:
             render_set(dataset.model_path, "train", scene.loaded_iter, scene.getTrainCameras(), gaussians, pipeline, background)

        if not skip_test:
             render_set(dataset.model_path, "test", scene.loaded_iter, scene.getTestCameras(), gaussians, pipeline, background)

if __name__ == "__main__":
    # Set up command line argument parser
    parser = ArgumentParser(description="Testing script parameters")
    model = ModelParams(parser, sentinel=True)
    pipeline = PipelineParams(parser)
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--iteration", default=-1, type=int)
    parser.add_argument("--skip_train", action="store_true")
    parser.add_argument("--skip_test", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = get_combined_args(parser)

    # Get config from training
    cfg_path = os.path.join(args.model_path, args.config)
    cfg = OmegaConf.load(cfg_path)
    def recursive_merge(key, host):
        # Skip loaded_pth to preserve CL argument
        if key == 'loaded_pth':
            return
        if isinstance(host[key], DictConfig):
            for key1 in host[key].keys():
                recursive_merge(key1, host[key])
        else:
            #assert hasattr(args, key), key
            setattr(args, key, host[key])
    for k in cfg.keys():
        recursive_merge(k, cfg)

    # Check if data folder exists (e.g if we're rendering at a different host from where the model was trained and the data path is different)
    if not os.path.exists(args.source_path):
        short_path = '/'.join(args.source_path.split('/')[-3:])
        if not os.path.exists(short_path):
            raise FileNotFoundError(f"Could not find path {args.source_path} or {short_path}")
        args.source_path = short_path

    print("Rendering " + args.model_path)
    
    # Initialize system state (RNG)
    safe_state(args.quiet)

    render_sets(model.extract(args), args.iteration, pipeline.extract(args), args.skip_train, args.skip_test, args.gaussian_dim, args.time_duration, args.rot_4d, args.force_sh_3d, args.eval_shfs_4d)