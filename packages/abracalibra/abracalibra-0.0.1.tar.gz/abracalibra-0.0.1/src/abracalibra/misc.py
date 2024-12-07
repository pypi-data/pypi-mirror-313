
import torch 
from gpytorch.distributions import MultitaskMultivariateNormal  
from typing import Literal, Optional, Union,List
from functools import wraps
from torch.distributions import Distribution, Normal,Uniform, TransformedDistribution
from torch.distributions.transforms import ComposeTransform,AffineTransform,CumulativeDistributionTransform,Transform

def get_task_covariance(dist:MultitaskMultivariateNormal):
    ntasks = dist.num_tasks
    npoints = dist.event_shape[0] # TODO: Fix this to work with 2D inputs or batching
    covar = dist.covariance_matrix
     
    return covar.view(npoints,ntasks,npoints,ntasks).diagonal(dim1=0,dim2=2).permute(2,0,1)

def make_normal_transform(prior_list:List[Distribution])-> List[Optional[Transform]]:
    normal_cdf_transform = CumulativeDistributionTransform(Normal(0,1))
    transforms = []
    for p in prior_list:
        if isinstance(p,Normal):
            transforms.append(None)
        elif isinstance(p,Uniform):
            affine = AffineTransform(p.low,p.high - p.low)
            transforms.append(ComposeTransform([normal_cdf_transform,affine]))
        elif isinstance(p,TransformedDistribution):
            if not isinstance(p.base_dist,Normal):
                raise ValueError("If using transformed distribution priors, base must be a normal distribution.")
            transforms.append(p.transforms)
        else:
            raise ValueError("Only Normal and Uniform priors are supported currently, need to work out how to map other distributions")
    return transforms