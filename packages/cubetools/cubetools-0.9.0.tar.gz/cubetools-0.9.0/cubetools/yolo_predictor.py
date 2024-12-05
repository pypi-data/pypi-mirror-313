import torch
try:
    import torch_npu
except:
    pass
from ultralytics.nn.autobackend import AutoBackend


def set_predictor(model, device='auto'):
    if device == 'auto':
        device = 'cpu'
        if hasattr(torch, 'npu') and torch.npu.is_available():
            device = 'npu'
        if torch.cuda.is_available():
            device = 'cuda'

    custom = {"conf": 0.25, "batch": 1, "save": False, "mode": "predict"}  # method defaults
    args = {**model.overrides, **custom}
    model.predictor = model._smart_load('predictor')(overrides=args, _callbacks=model.callbacks)
    model.predictor.setup_model(model=model.model, verbose=False)

    """Initialize YOLO model with given parameters and set it to evaluation mode."""
    model.predictor.model = AutoBackend(
        weights=model.model or model.predictor.args.model,
        device=torch.device(device),
        dnn=model.predictor.args.dnn,
        data=model.predictor.args.data,
        fp16=model.predictor.args.half,
        batch=model.predictor.args.batch,
        fuse=True,
        verbose=False,
    )

    model.predictor.device = model.predictor.model.device  # update device
    model.predictor.args.half = model.predictor.model.fp16  # update half
    model.predictor.model.eval()
