################################################################################
## GENERATED FILE INFO
##
## Template Source: training/python/split_embedding_codegen_lookup_invoker.template
################################################################################

#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-ignore-all-errors

import torch
from .lookup_args import *
def invoke(
    common_args: CommonArgs,
    optimizer_args: OptimizerArgs,
    momentum1: Momentum,
    iter: int = 0,
    apply_global_weight_decay: bool = False,
    # only pass prev_iter_dev since prev_iter is never created on UVM
    prev_iter_dev: Optional[torch.Tensor] = None,
    gwd_lower_bound: float = 0.0,
) -> torch.Tensor:

    vbe_metadata = common_args.vbe_metadata
    if (common_args.host_weights.numel() > 0):
        T = common_args.D_offsets.numel() - 1
        vbe: bool = vbe_metadata.B_offsets is not None
        if vbe:
            # create offsets with fixed batch size max_B
            # not efficient but for now we just need a functional implementation for CPU
            max_B = vbe_metadata.max_B
            offsets = torch.empty([T * max_B + 1], dtype=common_args.offsets.dtype, device=common_args.offsets.device)
            for t in range(T):
                B_offsets = vbe_metadata.B_offsets
                assert isinstance(B_offsets, torch.Tensor)
                begin = B_offsets[t]
                end = B_offsets[t + 1]
                offsets[t * max_B : t * max_B + end - begin] = common_args.offsets[begin : end]
                offsets[t * max_B + end - begin : (t + 1) * max_B] = common_args.offsets[end]
            offsets[-1] = common_args.offsets[-1]
        else:
            offsets = common_args.offsets
        output = torch.ops.fbgemm.split_embedding_codegen_lookup_adagrad_function_cpu(
            # common_args
            host_weights=common_args.host_weights,
            weights_placements=common_args.weights_placements,
            weights_offsets=common_args.weights_offsets,
            D_offsets=common_args.D_offsets,
            total_D=common_args.total_D,
            max_D=common_args.max_D,
            hash_size_cumsum=common_args.hash_size_cumsum,
            total_hash_size_bits=common_args.total_hash_size_bits,
            indices=common_args.indices,
            offsets=offsets,
            pooling_mode=common_args.pooling_mode,
            indice_weights=common_args.indice_weights,
            feature_requires_grad=common_args.feature_requires_grad,
            # optimizer_args
            gradient_clipping = optimizer_args.gradient_clipping,
            max_gradient=optimizer_args.max_gradient,
            stochastic_rounding=optimizer_args.stochastic_rounding,
            learning_rate=optimizer_args.learning_rate,
            eps=optimizer_args.eps,
            # momentum1
            momentum1_host=momentum1.host,
            momentum1_offsets=momentum1.offsets,
            momentum1_placements=momentum1.placements,
            # momentum2
            # prev_iter
            # row_counter
            # iter
            # max counter
        )
        if vbe:
            output_new = torch.empty([vbe_metadata.output_size], dtype=output.dtype, device=output.device)
            B_offsets_rank_per_feature = vbe_metadata.B_offsets_rank_per_feature
            assert isinstance(B_offsets_rank_per_feature, torch.Tensor)
            output_offsets_feature_rank = vbe_metadata.output_offsets_feature_rank
            assert isinstance(output_offsets_feature_rank, torch.Tensor)
            R = B_offsets_rank_per_feature.size(1) - 1
            for r in range(R):
                D_offset = 0
                for t in range(T):
                    o_begin = output_offsets_feature_rank[r * T + t].item()
                    o_end = output_offsets_feature_rank[r * T + t + 1].item()
                    D = common_args.D_offsets[t + 1].item() - common_args.D_offsets[t].item()
                    b_begin = B_offsets_rank_per_feature[t][r].item()
                    b_end = B_offsets_rank_per_feature[t][r + 1].item()
                    assert o_end - o_begin == (b_end - b_begin) * D
                    output_new[o_begin : o_end] = output[b_begin : b_end, D_offset : D_offset + D].flatten()
                    D_offset += D
            return output_new
        else:
            return output


    return torch.ops.fbgemm.split_embedding_codegen_lookup_adagrad_function(
        # common_args
        placeholder_autograd_tensor=common_args.placeholder_autograd_tensor,
        dev_weights=common_args.dev_weights,
        uvm_weights=common_args.uvm_weights,
        lxu_cache_weights=common_args.lxu_cache_weights,
        weights_placements=common_args.weights_placements,
        weights_offsets=common_args.weights_offsets,
        D_offsets=common_args.D_offsets,
        total_D=common_args.total_D,
        max_D=common_args.max_D,
        hash_size_cumsum=common_args.hash_size_cumsum,
        total_hash_size_bits=common_args.total_hash_size_bits,
        indices=common_args.indices,
        offsets=common_args.offsets,
        pooling_mode=common_args.pooling_mode,
        indice_weights=common_args.indice_weights,
        feature_requires_grad=common_args.feature_requires_grad,
        lxu_cache_locations=common_args.lxu_cache_locations,
        uvm_cache_stats=common_args.uvm_cache_stats,
        # VBE metadata
        B_offsets=vbe_metadata.B_offsets,
        vbe_output_offsets_feature_rank=vbe_metadata.output_offsets_feature_rank,
        vbe_B_offsets_rank_per_feature=vbe_metadata.B_offsets_rank_per_feature,
        max_B=vbe_metadata.max_B,
        max_B_feature_rank=vbe_metadata.max_B_feature_rank,
        vbe_output_size=vbe_metadata.output_size,
        # optimizer_args
        gradient_clipping = optimizer_args.gradient_clipping,
        max_gradient=optimizer_args.max_gradient,
        stochastic_rounding=optimizer_args.stochastic_rounding, # if optimizer == none
        # V1 interface still accepts learning_rate as float
        learning_rate=optimizer_args.learning_rate,
        eps=optimizer_args.eps,
        # momentum1
        momentum1_dev=momentum1.dev,
        momentum1_uvm=momentum1.uvm,
        momentum1_offsets=momentum1.offsets,
        momentum1_placements=momentum1.placements,
        # momentum2
        # prev_iter
        
        prev_iter_dev=prev_iter_dev,
        # row_counter
        # iter
        iter=iter,
        # max counter
        # total_unique_indices
        output_dtype=common_args.output_dtype,
        is_experimental=common_args.is_experimental,
        use_uniq_cache_locations_bwd=common_args.use_uniq_cache_locations_bwd,
        use_homogeneous_placements=common_args.use_homogeneous_placements,
        apply_global_weight_decay=apply_global_weight_decay,
        gwd_lower_bound=gwd_lower_bound,
    )